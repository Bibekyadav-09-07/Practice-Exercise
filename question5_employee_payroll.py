from datetime import datetime

VALID_STATUSES = ("Present", "Absent", "Leave")
WORKING_DAYS = 30


def read_positive_number(prompt):
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Enter an amount greater than zero.")
            else:
                return value
        except ValueError:
            print("Please enter a valid number.")


def read_date(prompt):
    while True:
        value = input(prompt).strip()
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return value
        except ValueError:
            print("Use a valid date in YYYY-MM-DD format.")


def register_employee(employees):
    employee_id = input("Employee ID: ").strip()
    if not employee_id:
        print("Employee ID cannot be empty.")
        return
    if employee_id in employees:
        print("That employee ID is already registered.")
        return
    name = input("Employee name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return
    salary = read_positive_number("Monthly basic salary (Rs.): ")
    employees[employee_id] = {
        "name": name, "basic_salary": salary, "attendance": []
    }
    print("Employee registered successfully.")


def record_attendance(employees):
    employee_id = input("Employee ID: ").strip()
    if employee_id not in employees:
        print("Employee not found.")
        return
    date = read_date("Date (YYYY-MM-DD): ")
    records = employees[employee_id]["attendance"]
    for record in records:
        if record[0] == date:
            print("Attendance has already been recorded for that date.")
            return
    status_text = input("Status (Present/Absent/Leave): ").strip().lower()
    status = None
    for valid_status in VALID_STATUSES:
        if status_text == valid_status.lower():
            status = valid_status
    if status is None:
        print("Invalid status. Choose Present, Absent, or Leave.")
        return
    records.append((date, status))
    print("Attendance recorded.")


def display_attendance(employees):
    employee_id = input("Employee ID: ").strip()
    if employee_id not in employees:
        print("Employee not found.")
        return
    records = employees[employee_id]["attendance"]
    if not records:
        print("No attendance records for this employee.")
        return
    print("Attendance for {}:".format(employees[employee_id]["name"]))
    for date, status in records:
        print("{}: {}".format(date, status))


def count_attendance(records, month=None):
    counts = {"Present": 0, "Absent": 0, "Leave": 0}
    for date, status in records:
        if month is None or date[:7] == month:
            counts[status] += 1
    return counts


def attendance_rate(records):
    if not records:
        return 0.0
    counts = count_attendance(records)
    return (counts["Present"] + counts["Leave"]) / len(records) * 100


def calculate_monthly_salary(employee, month):
    counts = count_attendance(employee["attendance"], month)
    daily_salary = employee["basic_salary"] / WORKING_DAYS
    salary = employee["basic_salary"] - daily_salary * counts["Absent"]
    attendance_rate_for_month = (
        (counts["Present"] + counts["Leave"]) / WORKING_DAYS * 100
    )
    bonus = salary * 0.10 if attendance_rate_for_month >= 95 else 0
    return salary + bonus, counts, attendance_rate_for_month, bonus


def display_attendance_extremes(employees):
    if not employees:
        print("No employees are registered.")
        return
    highest_rate = None
    lowest_rate = None
    highest_names = []
    lowest_names = []
    for employee in employees.values():
        rate = attendance_rate(employee["attendance"])
        if highest_rate is None or rate > highest_rate:
            highest_rate = rate
            highest_names = [employee["name"]]
        elif rate == highest_rate:
            highest_names.append(employee["name"])
        if lowest_rate is None or rate < lowest_rate:
            lowest_rate = rate
            lowest_names = [employee["name"]]
        elif rate == lowest_rate:
            lowest_names.append(employee["name"])
    print("Highest attendance: {} ({:.2f}%)".format(
        ", ".join(highest_names), highest_rate
    ))
    print("Lowest attendance: {} ({:.2f}%)".format(
        ", ".join(lowest_names), lowest_rate
    ))


def generate_payroll_report(employees):
    if not employees:
        print("No employees are registered.")
        return
    month = input("Payroll month (YYYY-MM): ").strip()
    try:
        datetime.strptime(month + "-01", "%Y-%m-%d")
    except ValueError:
        print("Enter the month in YYYY-MM format.")
        return
    print("\nPAYROLL REPORT FOR {}".format(month))
    for employee_id, employee in employees.items():
        salary, counts, rate, bonus = calculate_monthly_salary(employee, month)
        print(
            "{} | {} | Present: {} | Absent: {} | Leave: {} | "
            "Attendance: {:.2f}% | Bonus: Rs. {:.2f} | Net salary: Rs. {:.2f}"
            .format(
                employee_id, employee["name"], counts["Present"],
                counts["Absent"], counts["Leave"], rate, bonus, salary
            )
        )


def main():
    employees = {}
    while True:
        print("\nEMPLOYEE PAYROLL AND ATTENDANCE")
        print("1. Register employee\n2. Record attendance")
        print("3. Display attendance history\n4. Attendance rates")
        print("5. Monthly payroll report\n0. Exit")
        choice = input("Choose an option: ").strip()
        if choice == "1":
            register_employee(employees)
        elif choice == "2":
            record_attendance(employees)
        elif choice == "3":
            display_attendance(employees)
        elif choice == "4":
            display_attendance_extremes(employees)
        elif choice == "5":
            generate_payroll_report(employees)
        elif choice == "0":
            print("Goodbye.")
            break
        else:
            print("Invalid menu choice.")


if __name__ == "__main__":
    main()
