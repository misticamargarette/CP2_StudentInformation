class StudentView:
    def display_menu(self):
        print("\nStudent Management System")
        print("1. Add student")
        print("2. View students")
        print("3. Search student")
        print("4. Update student")
        print("5. Delete student")
        print("6. Exit")

    def get_menu_choice(self):
        while True:
            choice = input("Enter your choice (1-6): ").strip()
            if choice in ["1", "2", "3", "4", "5", "6"]:
                return choice
            print("Invalid choice. Please enter 1 to 6.")

    def get_non_empty_input(self, prompt):
        while True:
            value = input(prompt).strip()
            if value:
                return value
            print("Input cannot be empty.")

    def get_student_id(self):
        while True:
            student_id = input("Enter student ID: ").strip()
            if student_id.isdigit():
                return student_id
            print("Student ID must be numeric only.")

    def get_contact_number(self, allow_empty=False):
        while True:
            contact_number = input("Enter contact number: ").strip()
            if allow_empty and not contact_number:
                return ""
            if contact_number.isdigit() and len(contact_number) >= 7:
                return contact_number
            print("Contact number must be numeric and at least 7 digits.")

    def get_student_details(self):
        return {
            "student_id": self.get_student_id(),
            "name": self.get_non_empty_input("Enter student name: "),
            "course": self.get_non_empty_input("Enter course: "),
            "year_level": self.get_non_empty_input("Enter year level: "),
            "contact_number": self.get_contact_number(),
        }

    def get_student_updates(self, student):
        print("Press Enter to keep current value.")

        updates = {
            "name": input(f"Name ({student['name']}): ").strip(),
            "course": input(f"Course ({student['course']}): ").strip(),
            "year_level": input(f"Year Level ({student['year_level']}): ").strip(),
        }

        while True:
            contact = input(f"Contact ({student['contact_number']}): ").strip()
            if not contact or (contact.isdigit() and len(contact) >= 7):
                updates["contact_number"] = contact
                return updates
            print("Contact number must be numeric and at least 7 digits.")

    def show_message(self, message):
        print(message)

    def show_add_student_header(self):
        print("\nAdd Student")

    def show_student_list_header(self):
        print("\nStudent List")

    def show_search_student_header(self):
        print("\nSearch Student")

    def show_update_student_header(self):
        print("\nUpdate Student")

    def show_delete_student_header(self):
        print("\nDelete Student")

    def display_students(self, students):
        self.show_student_list_header()

        if not students:
            print("No student records found.")
            return

        for index, student in enumerate(students, start=1):
            self.display_student(student, index)

    def display_student(self, student, index=None):
        if index:
            print(f"\nStudent #{index}")
        else:
            print("\nStudent Found")

        print(f"ID: {student['student_id']}")
        print(f"Name: {student['name']}")
        print(f"Course: {student['course']}")
        print(f"Year Level: {student['year_level']}")
        print(f"Contact: {student['contact_number']}")
