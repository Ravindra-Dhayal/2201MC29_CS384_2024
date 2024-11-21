import re

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


print("Select criteria to check:")
print("1 - Uppercase letters (A-Z)")
print("2 - Lowercase letters (a-z)")
print("3 - Numbers (0-9)")
print("4 - Special characters (!, @, #)")
criteria_input = input("Enter your criteria (comma-separated, e.g., 1,3,4): ")
criteria = list(map(int, criteria_input.split(',')))

password_list = []
print("Enter passwords to validate (type 'done' when finished):")
while True:
    password = input("Password: ")
    if password.lower() == 'done':
        break
    password_list.append(password)

for password in password_list:
    validate_password(password, criteria)