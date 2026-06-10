from models.student_model import StudentModel
from views.student_view import StudentView


class StudentController:
    def __init__(self):
        self.model = StudentModel()
        self.view = StudentView()

    def run(self):
        while True:
            self.view.display_menu()
            choice = self.view.get_menu_choice()

            if choice == "1":
                self.add_student()
            elif choice == "2":
                self.view_students()
            elif choice == "3":
                self.search_student()
            elif choice == "4":
                self.update_student()
            elif choice == "5":
                self.delete_student()
            else:
                self.view.show_message("Exiting program...")
                self.model.save_students()
                break

    def add_student(self):
        self.view.show_add_student_header()
        student = self.view.get_student_details()

        if self.model.add_student(student):
            self.view.show_message("Student added successfully.")
        else:
            self.view.show_message("Student ID already exists.")

    def view_students(self):
        self.view.display_students(self.model.get_all_students())

    def search_student(self):
        self.view.show_search_student_header()

        if not self.model.get_all_students():
            self.view.show_message("No records found.")
            return

        student_id = self.view.get_student_id()
        student = self.model.find_student(student_id)

        if student:
            self.view.display_student(student)
        else:
            self.view.show_message("Student not found.")

    def update_student(self):
        self.view.show_update_student_header()

        student_id = self.view.get_student_id()
        student = self.model.find_student(student_id)

        if not student:
            self.view.show_message("Student not found.")
            return

        updates = self.view.get_student_updates(student)
        self.model.update_student(student_id, updates)
        self.view.show_message("Student updated successfully.")

    def delete_student(self):
        self.view.show_delete_student_header()

        student_id = self.view.get_student_id()

        if self.model.delete_student(student_id):
            self.view.show_message("Student deleted successfully.")
        else:
            self.view.show_message("Student not found.")
