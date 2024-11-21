def generate_permutations(string):
    n = len(string)
    permutations = []
    indices = list(range(n))
    cycles = list(range(n, 0, -1))

    permutations.append(''.join(string[i] for i in indices))

    while True:
        for i in reversed(range(n)):
            cycles[i] -= 1
            if cycles[i] == 0:
                indices[i:] = indices[i + 1:] + indices[i:i + 1]
                cycles[i] = n - i
            else:
                j = cycles[i]
                indices[i], indices[-j] = indices[-j], indices[i]
                permutations.append(''.join(string[i] for i in indices))
                break
        else:
            return permutations

input_string = input("Enter string: ")

print(f"Permutations of '{input_string}':")
permutations = generate_permutations(input_string)
for perm in permutations:
    print(perm)
