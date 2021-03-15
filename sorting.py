#!/bin/python3
'''
Python provides built-in sort/sorted functions that use timsort internally.
You cannot use these built-in functions anywhere in this file.

Every function in this file takes a comparator `cmp` as input
which controls how the elements of the list
should be compared against each other:
If cmp(a, b) returns -1, then a < b;
if cmp(a, b) returns  1, then a > b;
if cmp(a, b) returns  0, then a == b.
'''

from copy import deepcopy


def cmp_standard(a, b):
    '''
    used for sorting from lowest to highest

    >>> cmp_standard(125, 322)
    -1
    >>> cmp_standard(523, 322)
    1
    '''
    if a < b:
        return -1
    if b < a:
        return 1
    return 0


def cmp_reverse(a, b):
    '''
    used for sorting from highest to lowest

    >>> cmp_reverse(125, 322)
    1
    >>> cmp_reverse(523, 322)
    -1
    '''
    if a < b:
        return 1
    if b < a:
        return -1
    return 0


def cmp_last_digit(a, b):
    '''
    used for sorting based on the last digit only

    >>> cmp_last_digit(125, 322)
    1
    >>> cmp_last_digit(523, 322)
    1
    '''
    return cmp_standard(a % 10, b % 10)


def _merged(xs, ys, cmp=cmp_standard):
    '''
    Assumes that both xs and ys are sorted,
    and returns a new list containing the elements of both xs and ys.
    Runs in linear time.

    NOTE:
    In python, helper functions are frequently prepended
    with the _.
    This is a signal to users of a library that these
    functions are for "internal use only",
    and not part of the "public interface".


    This _merged function could be implemented as a local function
    within the merge_sorted scope rather than a global function.
    The downside of this is that the function can
    then not be tested on its own.
    Typically, you should only implement a function as a local
    function if it cannot function on its own
    (like the go functions from binary search).
    If it's possible to make a function stand-alone,
    then you probably should do that and write test
    cases for the stand-alone function.

    >>> _merged([1, 3, 5], [2, 4, 6])
    [1, 2, 3, 4, 5, 6]
    '''

    list_compiled = []
    i = 0
    j = 0

    while i < len(xs) and j < len(ys):
        sorting = cmp(xs[i], ys[j])
        if sorting == -1:
            list_compiled.append(xs[i])
            i += 1
        if sorting == 0:
            list_compiled.append(xs[i])
            list_compiled.append(ys[j])
            i += 1
            j += 1
        if sorting == 1:
            list_compiled.append(ys[j])
            j += 1
    while i < len(xs):
        list_compiled.append(xs[i])
        i += 1
    while j < len(ys):
        list_compiled.append(ys[j])
        j += 1
    return list_compiled


def merge_sorted(xs, cmp=cmp_standard):
    '''
    Merge sort is the standard O(n log n) sorting algorithm.
    Recall that the merge sort pseudo code is:

        if xs has 1 element
            it is sorted, so return xs
        else
            divide the list into two halves left,right
            sort the left
            sort the right
            merge the two sorted halves

    You should return a sorted version of the input list xs.
    You should not modify the input list xs in any way.
    '''
    dc_xs = deepcopy(xs)
    middle = len(dc_xs) // 2

    if len(xs) == 1 or len(xs) == 0:
        return xs
    else:
        left = dc_xs[0:middle]
        right = xs[middle:]
        left_sort = merge_sorted(left, cmp)
        right_sort = merge_sorted(right, cmp)
        return _merged(left_sort, right_sort, cmp)


def quick_sorted(xs, cmp=cmp_standard):
    '''
    Quicksort is like mergesort,
    but it uses a different strategy to split the list.
    Instead of splitting the list down the middle,
    a "pivot" value is randomly selected,
    and the list is split into a "less than"
    sublist and a "greater than" sublist.

    The pseudocode is:

        if xs has 1 element
            it is sorted, so return xs
        else
            select a pivot value p
            put all the values less than p in a list
            put all the values greater than p in a list
            put all the values equal to p in a list
            sort the greater/less than lists recursively
            return the concatenation of (less than, equal, greater than)

    You should return a sorted version of the input list xs.
    You should not modify the input list xs in any way.
    '''
    higher = []
    lower = []
    equal = []

    if len(xs) == 1:
        return xs
    else:
        pivot = xs[1]
        for i in xs:
            if i > pivot:
                higher.append(i)
            if i < pivot:
                lower.append(i)
            else:
                equal.append(i)
        less_than = quick_sorted(lower, cmp=cmp_standard)
        greater_than = quick_sorted(higher, cmp=cmp_standard)

    return less_than + equal + greater_than


def quick_sort(xs, cmp=cmp_standard):
    '''
    EXTRA CREDIT:
    The main advantage of quick_sort is that it can be implemented "in-place".
    This means that no extra lists are allocated,
    or that the algorithm uses Theta(1) additional memory.
    Merge sort, on the other hand, must allocate
    intermediate lists for the merge step,
    and has a Theta(n) memory requirement.
    Even though quick sort and merge sort both
    have the same Theta(n log n) runtime,
    this more efficient memory usage typically
    makes quick sort faster in practice.
    (We say quick sort has a lower "constant factor" in its runtime.)
    The downside of implementing quick sort in this way
    is that it will no longer be a
    [stable sort](https://en.wikipedia.org/wiki/Sorting_algorithm#Stability),
    but this is typically inconsequential.

    Follow the pseudocode of the Lomuto partition scheme given on wikipedia
    (https://en.wikipedia.org/wiki/Quicksort#Algorithm)
    to implement quick_sort as an in-place algorithm.
    You should directly modify the input xs
    variable instead of returning a copy of the list.
    '''
    if len(xs) == 1 or len(xs) == 0:
        return xs
    else:
        hi = len(xs) - 1
        lo = 0

        while lo < hi:
            for j in range(len(xs) - 1):
                if cmp(xs[j], xs[hi]) == -1:
                    t = xs[j]
                    xs[j] = xs[lo]
                    xs[lo] = t
                    lo += 1
            t = xs[hi]
            xs[hi] = xs[lo]
            xs[lo] = t
            xs[:lo] = quick_sort(xs[:lo], cmp)
            xs[lo + 1:] = quick_sort(xs[lo + 1], cmp)
            return xs
