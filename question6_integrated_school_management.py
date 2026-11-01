from datetime import datetime


SUBJECTS = ("English", "Mathematics", "Science", "Social Studies", "Computer")
PASS_MARK = 40
ATTENDANCE_STATUSES = ("Present", "Absent", "Leave")


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


def read_valid_date(prompt):
    while True:
        date = input(prompt).strip()
        try:
            datetime.strptime(date, "%Y-%m-%d")
            return date
        except ValueError:
            print("Use a valid date in YYYY-MM-DD format.")


def register_student(students):
    student_id = input("Student ID: ").strip()
    if not student_id:
        print("Student ID cannot be empty.")
        return
    if student_id in students:
        print("That student ID already exists.")
        return
    name = input("Student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    age = read_integer("Age: ", 1)
    marks = []
    for subject in SUBJECTS:
        marks.append(read_integer("{} marks (0-100): ".format(subject), 0, 100))
    students[student_id] = {
        "name": name,
        "age": age,
        "marks": tuple(marks),
        "attendance": [],
    }
    print("Student registered.")


def update_student_marks(students):
    student_id = input("Student ID: ").strip()
    if student_id not in students:
        print("Student not found.")
        return
    marks = []
    for subject in SUBJECTS:
        marks.append(read_integer("{} marks (0-100): ".format(subject), 0, 100))
    students[student_id]["marks"] = tuple(marks)
    print("Marks updated.")


def register_teacher(teachers):
    teacher_id = input("Teacher ID: ").strip()
    if not teacher_id:
        print("Teacher ID cannot be empty.")
        return
    if teacher_id in teachers:
        print("That teacher ID already exists.")
        return
    name = input("Teacher name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    print("Subjects: {}".format(", ".join(SUBJECTS)))
    subject = input("Assigned subject: ").strip().lower()
    assigned_subject = None
    for valid_subject in SUBJECTS:
        if subject == valid_subject.lower():
            assigned_subject = valid_subject
    if assigned_subject is None:
        print("Choose a subject from the listed subjects.")
        return
    teachers[teacher_id] = {"name": name, "subjects": [assigned_subject]}
    print("Teacher registered and subject assigned.")


def add_book(books):
    book_id = input("Book ID: ").strip()
    if not book_id:
        print("Book ID cannot be empty.")
        return
    if book_id in books:
        print("That book ID already exists.")
        return
    title = input("Title: ").strip()
    author = input("Author: ").strip()
    if not title or not author:
        print("Title and author cannot be empty.")
        return
    copies = read_integer("Number of copies: ", 1)
    books[book_id] = {"title": title, "author": author, "available": copies}
    print("Book added.")


def borrow_book(students, books, borrowed_records):
    student_id = input("Student ID: ").strip()
    book_id = input("Book ID: ").strip()
    if student_id not in students:
        print("Student not found.")
        return
    if book_id not in books:
        print("Book not found.")
        return
    if books[book_id]["available"] <= 0:
        print("No copies are available.")
        return
    books[book_id]["available"] -= 1
    borrowed_records.append((student_id, book_id))
    print("Book borrowed by {}.".format(students[student_id]["name"]))


def return_book(students, books, borrowed_records):
    student_id = input("Student ID: ").strip()
    book_id = input("Book ID: ").strip()
    record = (student_id, book_id)
    if record not in borrowed_records:
        print("No matching borrowing record was found.")
        return
    borrowed_records.remove(record)
    books[book_id]["available"] += 1
    print("Book returned.")


def record_student_attendance(students):
    student_id = input("Student ID: ").strip()
    if student_id not in students:
        print("Student not found.")
        return
    date = read_valid_date("Date (YYYY-MM-DD): ")
    records = students[student_id]["attendance"]
    for record in records:
        if record[0] == date:
            print("Attendance is already recorded for that date.")
            return
    entered_status = input("Status (Present/Absent/Leave): ").strip().lower()
    status = None
    for valid_status in ATTENDANCE_STATUSES:
        if entered_status == valid_status.lower():
            status = valid_status
    if status is None:
        print("Invalid attendance status.")
        return
    records.append((date, status))
    print("Attendance recorded.")


def student_results(students):
    results = []
    for student_id, student in students.items():
        total = 0
        passed = True
        for mark in student["marks"]:
            total += mark
            if mark < PASS_MARK:
                passed = False
        average = total / len(student["marks"])
        present_count = 0
        recorded_count = len(student["attendance"])
        for date, status in student["attendance"]:
            if status == "Present":
                present_count += 1
        attendance_percentage = (
            present_count / recorded_count * 100 if recorded_count else 0
        )
        results.append({
            "id": student_id,
            "name": student["name"],
            "total": total,
            "average": average,
            "passed": passed,
            "attendance": attendance_percentage,
        })

    for index in range(1, len(results)):
        current = results[index]
        position = index - 1
        while position >= 0 and results[position]["average"] < current["average"]:
            results[position + 1] = results[position]
            position -= 1
        results[position + 1] = current
    return results


def display_student_report(students):
    if not students:
        print("No students are registered.")
        return
    results = student_results(students)
    passed_count = 0
    class_average_total = 0
    print("\nSTUDENT REPORT")
    for rank, result in enumerate(results, start=1):
        status = "Passed" if result["passed"] else "Failed"
        if result["passed"]:
            passed_count += 1
        class_average_total += result["average"]
        print(
            "{}. {} (ID: {}) | Total: {} | Average: {:.2f} | {} | "
            "Attendance: {:.2f}%".format(
                rank, result["name"], result["id"], result["total"],
                result["average"], status, result["attendance"]
            )
        )
    failed_count = len(results) - passed_count
    print("Class average: {:.2f}".format(class_average_total / len(results)))
    print("Passed: {} | Failed: {}".format(passed_count, failed_count))


def display_books(books):
    if not books:
        print("No books are registered.")
        return
    for book_id, book in books.items():
        print("{} | {} by {} | Available: {}".format(
            book_id, book["title"], book["author"], book["available"]
        ))


def main():
    students = {}
    teachers = {}
    books = {}
    borrowed_records = []
    while True:
        print("\nINTEGRATED SCHOOL MANAGEMENT")
        print("1. Register student\n2. Update student marks")
        print("3. Register teacher and assign subject\n4. Add book")
        print("5. Borrow book\n6. Return book\n7. Record student attendance")
        print("8. Student performance and class report\n9. Display books")
        print("0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            register_student(students)
        elif choice == "2":
            update_student_marks(students)
        elif choice == "3":
            register_teacher(teachers)
        elif choice == "4":
            add_book(books)
        elif choice == "5":
            borrow_book(students, books, borrowed_records)
        elif choice == "6":
            return_book(students, books, borrowed_records)
        elif choice == "7":
            record_student_attendance(students)
        elif choice == "8":
            display_student_report(students)
        elif choice == "9":
            display_books(books)
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid menu choice.")


if __name__ == "__main__":
    main()
