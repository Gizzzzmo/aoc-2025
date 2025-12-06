import sys

total = 0
total2 = 0
while True:
    line = sys.stdin.readline().rstrip()
    if line == "":
        break

    nums = [int(x) for x in line]
    subtotal = 0
    prev_arg_max = 0
    for j in range(11, -1, -1):
        max_num = 0
        arg_max = -1
        end = -j if j > 0 else None
        for i, x in enumerate(nums[prev_arg_max:end]):
            if x > max_num:
                arg_max = i + prev_arg_max
                max_num = x
        prev_arg_max = arg_max + 1
        subtotal += max_num * 10**j

    total2 += subtotal
    print(subtotal)

    max_num = 0
    arg_max = -1
    for i, x in enumerate(nums[:-1]):
        if x > max_num:
            arg_max = i
            max_num = x
    print(line)
    print(" " * (arg_max) + "^")
    firstdigit = max_num
    seconddigit = max(nums[arg_max + 1 :])
    total += 10 * firstdigit + seconddigit

print(f"solution 1: {total}")
print(f"solution 2: {total2}")
