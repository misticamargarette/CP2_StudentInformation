from functools import wraps
import re

from flask import Blueprint, flash, redirect, render_template, request, session, url_for

from models.student_model import StudentModel

STUDENT_ID_PATTERN = re.compile(r"^\d{4}-\d{5}-[A-Z]{2}-\d$")
COURSE_ABBREVIATIONS = {
    "Bachelor of Science in Psychology": "BS Psych",
    "Bachelor of Secondary Education Major in English": "BSEd Eng",
    "Bachelor of Secondary Education Major in Social Studies": "BSEd SocSci",
    "Bachelor of Elementary Education": "BEEd",
    "Bachelor of Science in Information Technology": "BSIT",
    "Bachelor of Science in Computer Engineering": "BSCpE",
    "Bachelor of Science in Industrial Engineering": "BSIE",
    "Bachelor of Science in Business Administration Major in Human Resource Management": "BSBA-HRM",
    "Diploma in Computer Engineering Technology": "DCET",
    "Diploma in Information Technology": "DIT",
}


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
            student = get_student_from_form(form_mode="add")
            error = validate_student(student, form_mode="add")

            if error:
                flash(error, "error")
                return render_template("student_form.html", student=student, mode="add")

            add_result = model.add_student(student)
            if add_result is True:
                flash("Student added successfully.", "success")
                return redirect(url_for("student_web.dashboard"))

            if add_result == "locked":
                flash("Close students.xlsx, then try saving again.", "error")
                return render_template("student_form.html", student=student, mode="add")

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
            updates = get_student_from_form(include_id=False, form_mode="edit")
            error = validate_student(updates, include_id=False, form_mode="edit")

            if error:
                flash(error, "error")
                form_student = {**student, **updates}
                return render_template("student_form.html", student=form_student, mode="edit")

            update_result = model.update_student(student_id, updates)
            if update_result == "locked":
                flash("Close students.xlsx, then try updating again.", "error")
                form_student = {**student, **updates}
                return render_template("student_form.html", student=form_student, mode="edit")

            flash(f"{updates['name']} has been updated successfully.", "success")
            return redirect(url_for("student_web.dashboard"))

        return render_template("student_form.html", student=student, mode="edit")

    @controller.route("/students/<student_id>/delete", methods=["POST"])
    @login_required
    def delete_student(student_id):
        delete_result = model.delete_student(student_id)
        if delete_result is True:
            flash("Student deleted successfully.", "success")
        elif delete_result == "locked":
            flash("Close students.xlsx, then try deleting again.", "error")
        else:
            flash("Student not found.", "error")

        return redirect(url_for("student_web.dashboard"))

    return controller


def get_student_from_form(include_id=True, form_mode="add"):
    student = {
        "name": request.form.get("name", "").strip(),
        "course": request.form.get("course", "").strip(),
        "year_level": request.form.get("year_level", "").strip(),
        "age": request.form.get("age", "").strip(),
        "contact_number": request.form.get("contact_number", "").strip(),
        "address": request.form.get("address", "").strip(),
        "emergency_name": request.form.get("emergency_name", "").strip(),
        "emergency_relationship": request.form.get("emergency_relationship", "").strip(),
        "emergency_contact_number": request.form.get("emergency_contact_number", "").strip(),
    }

    if form_mode == "edit":
        student["status"] = request.form.get("status", "Active").strip() or "Active"
    else:
        student["status"] = "Active"

    if include_id:
        student["student_id"] = request.form.get("student_id", "").strip()

    return student


def validate_student(student, include_id=True, form_mode="add"):
    if include_id:
        student_id = student.get("student_id", "")
        if not STUDENT_ID_PATTERN.fullmatch(student_id):
            return "Student ID must use this format: 2025-00540-BN-0."

    required_fields = [
        "name",
        "course",
        "year_level",
        "age",
        "contact_number",
        "address",
        "emergency_name",
        "emergency_relationship",
        "emergency_contact_number",
    ]
    for field in required_fields:
        if not student.get(field):
            return "Please complete all fields."

    contact_number = student.get("contact_number", "")
    if not contact_number.isdigit() or len(contact_number) != 11:
        return "Contact number must be exactly 11 numbers."

    emergency_contact_number = student.get("emergency_contact_number", "")
    if not emergency_contact_number.isdigit() or len(emergency_contact_number) != 11:
        return "Emergency contact number must be exactly 11 numbers."

    if student.get("emergency_relationship") not in ["Guardian", "Mother", "Father"]:
        return "Please select a valid emergency contact relationship."

    age = student.get("age", "")
    if not age.isdigit() or not 1 <= int(age) <= 120:
        return "Age must be a number from 1 to 120."

    if form_mode == "edit" and student.get("status") not in ["Active", "Inactive"]:
        return "Please select a valid status."

    return None


def format_student_row(student, index):
    return {
        **student,
        "age": student.get("age", ""),
        "address": student.get("address", ""),
        "emergency_name": student.get("emergency_name", ""),
        "emergency_relationship": student.get("emergency_relationship", ""),
        "emergency_contact_number": student.get("emergency_contact_number", ""),
        "course_short": COURSE_ABBREVIATIONS.get(student.get("course", ""), student.get("course", "")),
        "status": student.get("status", "Active"),
        "initials": get_initials(student.get("name", "")),
        "avatar_class": ["av-teal", "av-blue", "av-purple", "av-amber"][index % 4],
    }


def get_initials(name):
    parts = [part for part in name.split() if part]
    if not parts:
        return "ST"

    return "".join(part[0] for part in parts[:2]).upper()
