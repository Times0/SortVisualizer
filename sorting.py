#
# ####### Sorts algorithms that yield the next swap to do ####### #
#

def bubble_sort_yield(L) -> iter:
    n = len(L)
    for i in range(n):
        for j in range(n - i - 1):
            if L[j] > L[j + 1]:
                yield j, j + 1


def insertion_sort_yield(L) -> iter:
    n = len(L)
    for i in range(1, n):
        j = i
        while j > 0 and L[j - 1] > L[j]:
            yield j - 1, j
            j -= 1


#
# ####### Sorts algorithms that return the list of swaps to do ####### #
#

def quicksort(og_l):
    L = og_l[:]
    n = len(L)
    return qs(0, n - 1, L, [])


def qs(left, right, nums, changes):
    if len(nums) == 1:  # Terminating Condition for recursion. VERY IMPORTANT!
        return
    if left < right:
        pi, swaps = partition(left, right, nums)
        changes.extend(swaps)
        qs(left, pi - 1, nums, changes)
        qs(pi + 1, right, nums, changes)
    return changes


def partition(left, right, nums):
    swaps = []
    pivot, ptr = nums[right], left
    for i in range(left, right):
        if nums[i] <= pivot:
            if i != ptr:
                nums[i], nums[ptr] = nums[ptr], nums[i]
                swaps.append((i, ptr))
            ptr += 1
    if right != ptr:
        nums[ptr], nums[right] = nums[right], nums[ptr]
        swaps.append((ptr, right))
    return ptr, swaps
