# cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, nonecheck=False, cdivision=True
from typing import Dict, List
import numpy as np

DEF MAX_ITERS = 200
DEF MAX_SIZE = 1000

MAX_ITERS_TEST = MAX_ITERS


cdef int _reverse_and_add(int[:] xs, int ptr) nogil:
    """
    Reverses digits of the input number and adds resulting number to the
    input number in place. Number is represented by the array of digits
    in base 12. Array must be large enough to fit result of the function.
    Second argument points to the last digit in the array. For example, if
    number is 1B8A then input array is [1, 11, 8, 10, 0, 0, 0, 0, ...] and 
    second argument equals 3.
    
    :param xs: input number represented by the array of digits in base 12
    :param ptr: index of the last digit in the array
    :return: new index of the last digit in the array
    """
    cdef int i, j
    cdef int temp
    cdef int current_curry
    cdef int current_digit

    for i in range(ptr // 2 + 1):
        j = ptr - i
        xs[i] += xs[j]
        xs[j] = xs[i]

    current_curry = 0

    for i in range(ptr + 1):
        current_digit = xs[i] + current_curry
        current_curry = current_digit // 12
        xs[i] = current_digit % 12

    if current_curry > 0:
        ptr += 1
        xs[ptr] = current_curry

    return ptr


cdef int _is_palindrome(int[:] xs, int ptr) nogil:
    """
    Checks if input number is a palindrome. Number is 
    represented by the array of digits in base 12. Second
    argument points to the last digit in the array.
    
    :param xs: input number represented by the array of digits in base 12
    :param ptr: index of the last digit in the array
    :return: True if input number is a palindrome, False otherwise
    """
    cdef int i, j

    for i in range(ptr // 2 + 1):
        j = ptr - i
        if xs[i] != xs[j]:
            return False

    return True


cdef int _check(long n, int[:] xs) nogil:
    """
    Performs reverse and add operation on the input number and
    returns number of iterations in which this input
    number becomes a palindrome. Returns -1 if the MAX_ITERS iterations
    is reached and condition is not met.
    
    :param n: input number
    :param xs: pre-allocated array where number digits will be stored
    :return: number of iterations in which n will become a palindrome (-1 if none)
    """
    cdef int ptr
    cdef int i, j, t

    ptr = 0

    # Transform number to digits in duodecimal system
    while n:
        xs[ptr] = n % 12
        n //= 12
        ptr += 1

    ptr -= 1

    # Reverse digits to obtain the right order
    for i in range(ptr // 2):
        j = ptr - i
        xs[i] ^= xs[j]
        xs[j] ^= xs[i]
        xs[i] ^= xs[j]

    for i in range(MAX_ITERS):
        if _is_palindrome(xs, ptr):
            return i

        ptr = _reverse_and_add(xs, ptr)

    return -1


def check(n: int) -> int:
    """
    Performs reverse and add operation on the input number and
    returns number of iterations in which this input
    number becomes a palindrome. Returns -1 if the MAX_ITERS iterations
    is reached and condition is not met.

    :param n: input number
    :return: number of iterations in which n will become a palindrome (-1 if none)
    """
    assert n > 0, 'n must be positive'

    xs = np.zeros(MAX_SIZE, dtype=np.int32)

    return _check(n, xs)


def check_range(a: int, b: int) -> Dict[int, int]:
    """
    Checks range of numbers from a to b and for every number of iterations
    reports smallest number from that range that becomes a palindrome
    in that number of iterations.

    :param a: beginning of the range
    :param b: end of the range
    :return: dictionary of results
    """
    assert a > 0, 'a must be positive'
    assert b > a, 'b must be greater than a'

    result = {}

    xs = np.zeros(MAX_SIZE, dtype=np.int32)

    for n in range(a, b):
        r = _check(n, xs)

        if r == -1:
            continue

        if r in result:
            continue

        result[r] = n

    return result

def reverse_and_add_test(n: int) -> int:
    """
    Exports the _reverse_and_add function for testing.

    :param n: input number
    :return: number obtained after the reverse and add operation
    """

    xs = np.zeros(MAX_SIZE, dtype=np.int32)
    ptr = 0

    while n:
        xs[ptr] = n % 12
        n //= 12
        ptr += 1

    ptr -= 1

    for i in range(ptr // 2):
        j = ptr - i
        xs[i] ^= xs[j]
        xs[j] ^= xs[i]
        xs[i] ^= xs[j]

    ptr = _reverse_and_add(xs, ptr)

    result = 0
    for i, d in enumerate(xs[:ptr+1].tolist()):
        result += d * 12 ** i

    print(result)

    return result


def is_palindrome_test(n: int) -> int:
    """
    Exports _is_palindrome function for testing.
    
    :param n: input number
    :return: True if input number is a palindrome, False otherwise
    """

    xs = np.zeros(MAX_SIZE, dtype=np.int32)
    ptr = 0

    while n:
        xs[ptr] = n % 12
        n //= 12
        ptr += 1

    ptr -= 1

    for i in range(ptr // 2):
        j = ptr - i
        xs[i] ^= xs[j]
        xs[j] ^= xs[i]
        xs[i] ^= xs[j]

    # _is_palindrome returns integer
    return _is_palindrome(xs, ptr) == True
