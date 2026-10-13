# File: stats_buggy


def stats_of_positives(nums):
    count = 0
    total = 0
    mx = 0
    for i in range(len(nums)+1):
        if nums[i] >= 0:
            count += 1
            total += nums[i]
            if nums[i] > mx:
                mx = nums[i]
    avg = total / count
    print("Average of positive numbers:", int(avg))
    print("Max value:", max)

data = [3, -1, 5, 0, 8]
stats_of_positives(data)

# Corrected version 


def stats_of_positives(nums, include_zero=False):
    count = 0
    total = 0.0
    mx = None

    for x in nums:
        if (x > 0) or (include_zero and x == 0):
            count += 1
            total += x
            if mx is None or x > mx:
                mx = x

    if count == 0:
        print("Average of selected numbers: N/A (no values)")
        print("Max value: N/A (no values)")
        return

    avg = total / count
    print("Average of selected numbers:", avg)
    print("Max value:", mx)

# Quick checks
stats_of_positives([], include_zero=False)         # no values
stats_of_positives([-2, -5], include_zero=False)   # no values
stats_of_positives([0, 0.0], include_zero=True)    # zeros allowed
stats_of_positives([1.5, 2.5, 0], include_zero=False)
