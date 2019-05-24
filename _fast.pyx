# cython: language_level=3, boundscheck=False, wraparound=False, initializedcheck=False, nonecheck=False, cdivision=True
import numpy as np

DEF MAX_ITERS = 200
DEF TOTAL_SIZE = 1000


cdef int _reverse_and_add(int[:] xs, int ptr) nogil:
    cdef int current_digit, current_curry, temp, i

    for i in range(ptr//2+1):
        temp = xs[i] + xs[ptr-i]
        xs[i] = temp
        xs[ptr-i] = temp

    current_curry = 0

    for i in range(ptr+1):
        current_digit = xs[i] + current_curry
        current_curry = current_digit // 12
        xs[i] = current_digit % 12

    if current_curry > 0:
        ptr += 1
        xs[ptr] = current_curry

    return ptr


cdef int _is_palindrome(int[:] xs, int ptr) nogil:
    cdef int i

    for i in range(ptr//2+1):
        if xs[i] != xs[ptr-i]:
            return False

    return True


cdef int _check(long n, int[:] xs) nogil:
    cdef int ptr = -1
    cdef int temp, i

    while n:
        ptr += 1
        xs[ptr] = n % 12
        n //= 12

    for i in range(ptr//2+1):
        temp = xs[i]
        xs[i] = xs[ptr-i]
        xs[ptr-i] = temp

    for i in range(MAX_ITERS):
        if _is_palindrome(xs, ptr):
            return i

        ptr = _reverse_and_add(xs, ptr)

    return -1


def check(n: int) -> int:
    return _check(n, np.zeros(TOTAL_SIZE, dtype=np.int32))
