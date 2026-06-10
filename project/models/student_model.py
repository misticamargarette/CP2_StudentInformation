from pathlib import Path

from openpyxl import Workbook, load_workbook


FIELDS = ["student_id", "name", "course", "year_level", "contact_number", "status"]
HEADERS = ["Student ID", "Name", "Course", "Year", "Contact Number", "Status"]


class StudentModel:
    def __init__(self, file_name="students.xlsx"):
        self.file_path = Path(file_name)
        self.legacy_json_path = Path("students.json")
        self.ensure_workbook()
        self.students = self.load_students()

    def ensure_workbook(self):
        if self.file_path.exists():
            return

        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Students"
        sheet.append(HEADERS)

        legacy_students = self.load_legacy_json()
        for student in legacy_students:
            sheet.append([student.get(field, "") for field in FIELDS])

        workbook.save(self.file_path)

    def load_legacy_json(self):
        if not self.legacy_json_path.exists():
            return []

        try:
            import json

            with self.legacy_json_path.open("r") as file:
                data = json.load(file)
        except (OSError, json.JSONDecodeError):
            return []

        if not isinstance(data, list):
            return []

        return [student for student in data if isinstance(student, dict)]

    def load_students(self):
        workbook = load_workbook(self.file_path)
        sheet = workbook.active
        students = []

        for row in sheet.iter_rows(min_row=2, values_only=True):
            if not any(row):
                continue

            student = {}
            for field, value in zip(FIELDS, row):
                student[field] = "" if value is None else str(value)

            student.setdefault("status", "Active")
            students.append(student)

        return students

    def save_students(self):
        workbook = Workbook()
        sheet = workbook.active
        sheet.title = "Students"
        sheet.append(HEADERS)

        for student in self.students:
            sheet.append([student.get(field, "") for field in FIELDS])

        workbook.save(self.file_path)

    def get_all_students(self):
        return self.students

    def find_student(self, student_id):
        for student in self.students:
            if student["student_id"] == student_id:
                return student
        return None

    def add_student(self, student):
        if self.find_student(student["student_id"]):
            return False

        self.students.append(student)
        self.save_students()
        return True

    def search_students(self, query):
        query = query.strip().lower()
        if not query:
            return self.students

        return [
            student
            for student in self.students
            if query in student["student_id"].lower()
            or query in student["name"].lower()
            or query in student["course"].lower()
            or query in student["year_level"].lower()
            or query in student["contact_number"].lower()
            or query in student.get("status", "").lower()
        ]

    def update_student(self, student_id, updates):
        student = self.find_student(student_id)
        if not student:
            return False

        for field, value in updates.items():
            if value:
                student[field] = value

        self.save_students()
        return True

    def delete_student(self, student_id):
        student = self.find_student(student_id)
        if not student:
            return False

        self.students.remove(student)
        self.save_students()
        return True
