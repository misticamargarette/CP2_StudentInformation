import json
from pathlib import Path


class StudentModel:
    def __init__(self, file_name="students.json"):
        self.file_path = Path(file_name)
        self.students = self.load_students()

    def load_students(self):
        try:
            with self.file_path.open("r") as file:
                return json.load(file)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def save_students(self):
        with self.file_path.open("w") as file:
            json.dump(self.students, file, indent=4)

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
