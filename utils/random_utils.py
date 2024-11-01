import random


def get_random_int(min_val, max_val):
    return random.randint(min_val, max_val)


def randomize(arr):
    for i in range(len(arr) - 1, 0, -1):
        j = random.randint(0, i)
        arr[i], arr[j] = arr[j], arr[i]
    return arr
