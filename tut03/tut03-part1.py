def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def get_rotations(n):
    rotations = []
    str_n = str(n)
    length = len(str_n)
    for i in range(length):
        rotated_number = int(str_n[i:] + str_n[:i])
        rotations.append(rotated_number)
    return rotations

def is_rotational_prime(n):
    rotations = get_rotations(n)
    for rotation in rotations:
        if not is_prime(rotation):
            return False
    return True

num = int(input("Enter the number: "))
if is_rotational_prime(num):
    print(f"{num} is a rotational prime.")
else:
    print(f"{num} is not a rotational prime.")
