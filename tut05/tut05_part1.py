#finding triplest

def f(nums):
    nums.sort()
    triplets = []  # Initialize the list
    for i in range(len(nums) - 2):
        if i > 0 and nums[i] == nums[i - 1]:
            continue
        left = i + 1
        right = len(nums) - 1
        while left < right:
            curr_sum = nums[i] + nums[left] + nums[right]
            if curr_sum == 0:
                triplets.append([nums[i], nums[left], nums[right]])
                left += 1
                right -= 1
                while left < right and nums[left] == nums[left - 1]:
                    left += 1
                while left < right and nums[right] == nums[right + 1]:
                    right -= 1
            elif curr_sum < 0:
                left += 1
            else:
                right -= 1
    return triplets

n = list(map(int, input("Enter list separated by spaces: ").split()))
result = f(n)
print("Unique triplets are:", result)
