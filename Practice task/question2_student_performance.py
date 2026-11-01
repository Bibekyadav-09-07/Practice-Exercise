SUBJECT_COUNT = 5
PASS_MARK = 40


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
    marks = []
    for subject_number in range(1, SUBJECT_COUNT + 1):
        marks.append(read_integer(
            "Marks for subject {} (0-100): ".format(subject_number), 0, 100
        ))
    students[student_id] = {"name": name, "marks": tuple(marks)}
    print("Student registered.")


def calculate_total_marks(marks):
    total = 0
    for mark in marks:
        total += mark
    return total


def calculate_average_marks(marks):
    if not marks:
        return 0
    return calculate_total_marks(marks) / len(marks)


def determine_highest_and_lowest(marks):
    if not marks:
        return None, None
    highest = marks[0]
    lowest = marks[0]
    for mark in marks[1:]:
        if mark > highest:
            highest = mark
        if mark < lowest:
            lowest = mark
    return highest, lowest


def passed_all_subjects(marks):
    for mark in marks:
        if mark < PASS_MARK:
            return False
    return True


def failed_at_least_one_subject(marks):
    return not passed_all_subjects(marks)


def build_ranked_results(students):
    results = []
    for student_id, student in students.items():
        results.append({
            "id": student_id,
            "name": student["name"],
            "total": calculate_total_marks(student["marks"]),
            "average": calculate_average_marks(student["marks"]),
            "highest": determine_highest_and_lowest(student["marks"])[0],
            "lowest": determine_highest_and_lowest(student["marks"])[1],
            "passed": passed_all_subjects(student["marks"]),
        })

    # Insertion sort keeps the program understandable without extra libraries.
    for index in range(1, len(results)):
        current = results[index]
        position = index - 1
        while position >= 0 and results[position]["average"] < current["average"]:
            results[position + 1] = results[position]
            position -= 1
        results[position + 1] = current
    return results


def calculate_class_average(results):
    if not results:
        return 0
    total_averages = 0
    for result in results:
        total_averages += result["average"]
    return total_averages / len(results)


def display_analysis(students):
    if not students:
        print("No students are registered; there is no performance data.")
        return

    results = build_ranked_results(students)
    print("\nRANKED STUDENT RESULTS")
    for rank, result in enumerate(results, start=1):
        status = "Passed all subjects" if result["passed"] else "Failed at least one"
        print(
            "{}. {} (ID: {}) | Total: {} | Average: {:.2f} | "
            "Highest: {} | Lowest: {} | {}".format(
                rank, result["name"], result["id"], result["total"],
                result["average"], result["highest"], result["lowest"], status
            )
        )

    passed_names = []
    failed_names = []
    for result in results:
        if result["passed"]:
            passed_names.append(result["name"])
        elif failed_at_least_one_subject(students[result["id"]]["marks"]):
            failed_names.append(result["name"])
    print("Passed all subjects: {}".format(
        ", ".join(passed_names) if passed_names else "None"
    ))
    print("Failed at least one subject: {}".format(
        ", ".join(failed_names) if failed_names else "None"
    ))
    print("Class average: {:.2f}".format(calculate_class_average(results)))


def main():
    students = {}
    while True:
        print("\nSTUDENT PERFORMANCE ANALYSIS")
        print("1. Register student\n2. Analyze performance\n0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            register_student(students)
        elif choice == "2":
            display_analysis(students)
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid menu choice.")


if __name__ == "__main__":
    main()
