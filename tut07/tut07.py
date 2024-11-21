import re

passwords = """abc12345
abc
123456789
"""

with open('input.txt', 'w') as f:
    f.write(passwords)
def validate_password(password, criteria):
    if len(password) < 8:
        print(f"'{password}' - Invalid password. Less than 8 Characters.")
        return False

    checks = {
        1: r'[A-Z]',
        2: r'[a-z]',
        3: r'[0-9]',
        4: r'[!@#]'
    }

    for criterion in criteria:
        if not re.search(checks[criterion], password):
            print(f"'{password}' - Invalid password. Missing ", end="")
            if 1 in criteria and not re.search(checks[1], password):
                print("Uppercase letters, ", end="")
            if 2 in criteria and not re.search(checks[2], password):
                print("Lowercase letters, ", end="")
            if 3 in criteria and not re.search(checks[3], password):
                print("Numbers, ", end="")
            if 4 in criteria and not re.search(checks[4], password):
                print("Special characters, ", end="")
            print()
            return False

    print(f"'{password}' - Valid password.")
    return True

def validate_password_from_file(filename, criteria):
    valid_count = 0
    invalid_count = 0

    with open(filename, 'r') as file:
        for password in file:
            password = password.strip()
            if validate_password(password, criteria):
                valid_count += 1
            else:
                invalid_count += 1

    print(f"Total Valid Passwords: {valid_count}")
    print(f"Total Invalid Passwords: {invalid_count}")

print("Select criteria to check:")
print("1 - Uppercase letters (A-Z)")
print("2 - Lowercase letters (a-z)")
print("3 - Numbers (0-9)")
print("4 - Special characters (!, @, #)")
criteria_input = input("Enter your criteria (comma-separated, e.g., 1,3,4): ")
criteria = list(map(int, criteria_input.split(',')))

validate_password_from_file('input.txt', criteria)