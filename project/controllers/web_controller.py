from functools import wraps

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.student_model import StudentModel


def create_web_controller():
    controller = Blueprint("student_web", __name__)
    model = StudentModel()

    def login_required(view):
        @wraps(view)
        def wrapped_view(*args, **kwargs):
            if not session.get("is_logged_in"):
                return redirect(url_for("student_web.login"))
            return view(*args, **kwargs)

        return wrapped_view

    @controller.route("/", methods=["GET", "POST"])
    def login():
        if session.get("is_logged_in"):
            return redirect(url_for("student_web.dashboard"))

        if request.method == "POST":
            username = request.form.get("username", "").strip()
            password = request.form.get("password", "").strip()

            if username == "admin" and password == "admin":
                session["is_logged_in"] = True
                return redirect(url_for("student_web.login_loader"))

            flash("Invalid username or password.", "error")

        return render_template("login.html")

    @controller.route("/login-loader")
    @login_required
    def login_loader():
        return render_template("login_loader.html")

    @controller.route("/logout")
    @login_required
    def logout():
        session.clear()
        flash("You have been logged out.", "success")
        return redirect(url_for("student_web.login"))

    @controller.route("/students")
    @login_required
    def dashboard():
        query = request.args.get("q", "")
        students = model.search_students(query)
        all_students = model.get_all_students()
        courses = {student["course"] for student in all_students if student.get("course")}
        year_levels = {student["year_level"] for student in all_students if student.get("year_level")}
        student_rows = [format_student_row(student, index) for index, student in enumerate(students)]

        return render_template(
            "dashboard.html",
            students=student_rows,
            query=query,
            total_students=len(all_students),
            course_count=len(courses),
            year_level_count=len(year_levels),
        )

    @controller.route("/students/add", methods=["GET", "POST"])
    @login_required
    def add_student():
        if request.method == "POST":
            student = get_student_from_form()
            error = validate_student(student)

            if error:
                flash(error, "error")
                return render_template("student_form.html", student=student, mode="add")

            if model.add_student(student):
                flash("Student added successfully.", "success")
                return redirect(url_for("student_web.dashboard"))

            flash("Student ID already exists.", "error")

        return render_template("student_form.html", student=None, mode="add")

    @controller.route("/students/<student_id>/edit", methods=["GET", "POST"])
    @login_required
    def edit_student(student_id):
        student = model.find_student(student_id)
        if not student:
            flash("Student not found.", "error")
            return redirect(url_for("student_web.dashboard"))

        if request.method == "POST":
            updates = get_student_from_form(include_id=False)
            error = validate_student(updates, include_id=False)

            if error:
                flash(error, "error")
                form_student = {**student, **updates}
                return render_template("student_form.html", student=form_student, mode="edit")

            model.update_student(student_id, updates)
            flash("Student updated successfully.", "success")
            return redirect(url_for("student_web.dashboard"))

        return render_template("student_form.html", student=student, mode="edit")

    @controller.route("/students/<student_id>/delete", methods=["POST"])
    @login_required
    def delete_student(student_id):
        if model.delete_student(student_id):
            flash("Student deleted successfully.", "success")
        else:
            flash("Student not found.", "error")

        return redirect(url_for("student_web.dashboard"))

    return controller


def get_student_from_form(include_id=True):
    student = {
        "name": request.form.get("name", "").strip(),
        "course": request.form.get("course", "").strip(),
        "year_level": request.form.get("year_level", "").strip(),
        "contact_number": request.form.get("contact_number", "").strip(),
        "status": request.form.get("status", "Active").strip() or "Active",
    }

    if include_id:
        student["student_id"] = request.form.get("student_id", "").strip()

    return student


def validate_student(student, include_id=True):
    if include_id and not student.get("student_id", "").isdigit():
        return "Student ID must be numeric only."

    required_fields = ["name", "course", "year_level", "contact_number"]
    for field in required_fields:
        if not student.get(field):
            return "Please complete all fields."

    contact_number = student.get("contact_number", "")
    if not contact_number.isdigit() or len(contact_number) < 7:
        return "Contact number must be numeric and at least 7 digits."

    if student.get("status") not in ["Active", "Inactive"]:
        return "Please select a valid status."

    return None


def format_student_row(student, index):
    return {
        **student,
        "status": student.get("status", "Active"),
        "initials": get_initials(student.get("name", "")),
        "avatar_class": ["av-teal", "av-blue", "av-purple", "av-amber"][index % 4],
    }


def get_initials(name):
    parts = [part for part in name.split() if part]
    if not parts:
        return "ST"

    return "".join(part[0] for part in parts[:2]).upper()
