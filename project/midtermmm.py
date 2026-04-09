import json

FILE_NAME = "students.json"


def load_students():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


def save_students(students):
    with open(FILE_NAME, "w") as file:
        json.dump(students, file, indent=4)


def display_menu():
    print("\nStudent Management System")
    print("1. Add student")
    print("2. View students")
    print("3. Search student")
    print("4. Update student")
    print("5. Delete student")
    print("6. Exits")

    print("4. Exit")


def get_menu_choice():
    while True:
        choice = input("Enter your choice (1-6): ").strip()
        if choice in ["1", "2", "3", "4", "5", "6"]:
            return choice
        print("Invalid choice. Please enter 1 to 6.")
        choice = input("Enter your choice (1-4): ").strip()
        if choice in ["1", "2", "3", "4"]:
            return choice
        print("Invalid choice. Please enter a number from 1 to 4.")


def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty.")


def get_student_id():
    while True:
        student_id = input("Enter student ID: ").strip()
        if student_id.isdigit():
            return student_id
        print("Student ID must be numeric only.")
        print("Student ID must contain numbers only.")


def get_contact_number():
    while True:
        contact_number = input("Enter contact number: ").strip()
        if contact_number.isdigit() and len(contact_number) >= 7:
            return contact_number
        print("Contact number must be numeric and at least 7 digits.")


def student_exists(students, student_id):
    for student in students:
        if student["student_id"] == student_id:
            return True
    return False


def find_student(students, student_id):
    for student in students:
        if student["student_id"] == student_id:
            return student
    return None


def add_student(students):
    print("\nAdd Student")

    student_id = get_student_id()

    if find_student(students, student_id):
        print("Student ID already exists.")
        return

    name = get_non_empty_input("Enter name: ")
    student_id = get_student_id()

    if student_exists(students, student_id):
        print("Student ID already exists.")
        return

    name = get_non_empty_input("Enter student name: ")
    course = get_non_empty_input("Enter course: ")
    year_level = get_non_empty_input("Enter year level: ")
    contact_number = get_contact_number()

    student = {
        "student_id": student_id,
        "name": name,
        "course": course,
        "year_level": year_level,
        "contact_number": contact_number
    }
    students.append(student)
    print("Student added successfully.")


def view_students(students):
    print("\nStudent List")

    if not students:
        print("No student records found.")
        return

    for i, s in enumerate(students, start=1):
        print(f"\nStudent #{i}")
        print(f"ID: {s['student_id']}")
        print(f"Name: {s['name']}")
        print(f"Course: {s['course']}")
        print(f"Year Level: {s['year_level']}")
        print(f"Contact: {s['contact_number']}")


def search_student(students):
    print("\nSearch Student")

    if not students:
        print("No records found.")
        return

    student_id = get_student_id()
    student = find_student(students, student_id)

    if student:
        print("\nStudent Found")
        print(student)
    else:
        print("Student not found.")


def update_student(students):
    print("\nUpdate Student")

    student_id = get_student_id()
    student = find_student(students, student_id)

    if not student:
        print("Student not found.")
        return

    print("Press Enter to keep current value.")

    new_name = input(f"Name ({student['name']}): ").strip()
    new_course = input(f"Course ({student['course']}): ").strip()
    new_year = input(f"Year Level ({student['year_level']}): ").strip()
    new_contact = input(f"Contact ({student['contact_number']}): ").strip()

    if new_name:
        student["name"] = new_name
    if new_course:
        student["course"] = new_course
    if new_year:
        student["year_level"] = new_year
    if new_contact.isdigit():
        student["contact_number"] = new_contact

    print("Student updated successfully.")


def delete_student(students):
    print("\nDelete Student")

    student_id = get_student_id()
    student = find_student(students, student_id)

    if not student:
        print("Student not found.")
        return

    students.remove(student)
    print("Student deleted successfully.")


def main():
    students = load_students()
    if len(students) == 0:
        print("No student records available.")
        return

    for index, student in enumerate(students, start=1):
        print(f"\nStudent #{index}")
        print(f"ID: {student['student_id']}")
        print(f"Name: {student['name']}")
        print(f"Course: {student['course']}")
        print(f"Year Level: {student['year_level']}")
        print(f"Contact Number: {student['contact_number']}")
def search_student(students):
    print("\nSearch Student")
    if len(students) == 0:
        print("No student records available.")
        return

    student_id = get_student_id()
    student = find_student(students, student_id)

    if student is None:
        print("Student not found.")
        return

    print("\nStudent Found")
    print(f"ID: {student['student_id']}")
    print(f"Name: {student['name']}")
    print(f"Course: {student['course']}")
    print(f"Year Level: {student['year_level']}")
    print(f"Contact Number: {student['contact_number']}")
def main():
    students = []

    while True:
        display_menu()
        choice = get_menu_choice()

        if choice == "1":
            add_student(students)
            save_students(students)

        elif choice == "2":
            view_students(students)

        elif choice == "3":
            search_student(students)

        elif choice == "4":
            update_student(students)

        elif choice == "5":
            delete_student(students)
            save_students(students)

        else:
            print("Exiting program...")
            save_students(students)
            break


if __name__ == "__main__":
    main()
