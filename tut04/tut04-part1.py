def add_student(students, name, grades):
    students[name.lower()] = grades

def update_grades(students, name, grades):
    students[name.lower()] = grades

def calculate_average(grades):
    return sum(grades) / len(grades)

def print_averages(students):
    averages = {name: calculate_average(grades) for name, grades in students.items()}
    sorted_averages = sorted(averages.items(), key=lambda x: x[1], reverse=True)
    for name, avg in sorted_averages:
        print(f"{name.capitalize()} - Average: {avg:.2f}")

def sort_students(students):
    sorted_students = sorted(students.items(), key=lambda x: calculate_average(x[1]), reverse=True)
    return sorted_students

def get_student_data():
    students = {}
    while True:
        name = input("Enter student name (or 'done' to finish): ").strip()
        if name.lower() == 'done':
            break
        grades = input("Enter grades separated by spaces: ").strip().split()
        grades = list(map(int, grades))
        add_student(students, name, grades)
    return students

# Get student data
students = get_student_data()

# Print averages sorted
print("\nStudent Averages:")
print_averages(students)

# Sort students by average
print("\nSorted Students by Average:")
sorted_students = sort_students(students)
for name, grades in sorted_students:
    print(f"{name.capitalize()} - Grades: {grades}")