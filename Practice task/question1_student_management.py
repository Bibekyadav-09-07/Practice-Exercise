SUBJECT_COUNT = 5


def read_integer(prompt, minimum=None, maximum=None):
    while True:
        try:
            value = int(input(prompt))
            if minimum is not None and value < minimum:
                print("Value must be at least {}.".format(minimum))
            elif maximum is not None and value > maximum:
                print("Value must be no more than {}.".format(maximum))
            else:
                return value
        except ValueError:
            print("Please enter a whole number.")


def read_marks():
    marks = []
    for subject_number in range(1, SUBJECT_COUNT + 1):
        marks.append(read_integer(
            "Enter marks for subject {} (0-100): ".format(subject_number),
            0, 100
        ))
    return tuple(marks)


def register_student(students):
    student_id = input("Student ID: ").strip()
    if not student_id:
        print("Student ID cannot be empty.")
        return
    if student_id in students:
        print("That student ID is already registered.")
        return
    name = input("Student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    age = read_integer("Age: ", 1)
    marks = read_marks()
    students[student_id] = {"name": name, "age": age, "marks": marks}
    print("Student registered successfully.")


def display_students(students):
    if not students:
        print("No students are registered.")
        return
    for student_id, student in students.items():
        print("ID: {} | Name: {} | Age: {} | Marks: {}".format(
            student_id, student["name"], student["age"], student["marks"]
        ))


def search_student(students):
    student_id = input("Enter student ID to search: ").strip()
    student = students.get(student_id)
    if student is None:
        print("Student not found.")
    else:
        print("ID: {} | Name: {} | Age: {} | Marks: {}".format(
            student_id, student["name"], student["age"], student["marks"]
        ))


def update_marks(students):
    student_id = input("Enter student ID: ").strip()
    student = students.get(student_id)
    if student is None:
        print("Student not found.")
        return
    student["marks"] = read_marks()
    print("Marks updated successfully.")


def remove_student(students):
    student_id = input("Enter student ID to remove: ").strip()
    if student_id not in students:
        print("Student not found.")
        return
    del students[student_id]
    print("Student removed successfully.")


def display_students_by_age(students):
    lower_age = read_integer("Minimum age: ", 1)
    upper_age = read_integer("Maximum age: ", lower_age)
    matches = []
    for student_id, student in students.items():
        if lower_age <= student["age"] <= upper_age:
            matches.append((student_id, student))
    if not matches:
        print("No students were found in that age range.")
        return
    for student_id, student in matches:
        print("ID: {} | Name: {} | Age: {}".format(
            student_id, student["name"], student["age"]
        ))


def main():
    students = {}
    actions = {
        "1": register_student,
        "2": display_students,
        "3": search_student,
        "4": update_marks,
        "5": remove_student,
        "6": display_students_by_age,
    }
    while True:
        print("\nSTUDENT MANAGEMENT")
        print("1. Register student\n2. Display all students")
        print("3. Search by ID\n4. Update marks\n5. Remove student")
        print("6. Display students by age range\n0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "0":
            print("Goodbye.")
            break
        action = actions.get(choice)
        if action is None:
            print("Invalid menu choice.")
        else:
            action(students)


if __name__ == "__main__":
    main()
