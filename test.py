from _fast import check, reverse_and_add_test, is_palindrome_test, MAX_ITERS_TEST, check_range

digits = '0123456789AB'
reverse_digits = {d: i for i, d in enumerate(digits)}


def to_duodecimal(n: int) -> str:
    if n == 0:
        return '0'

    if n < 0:
        return f'-{to_duodecimal(-n)}'

    xs = []
    while n:
        xs.append(n % 12)
        n //= 12
    return ''.join(map(lambda x: digits[x], reversed(xs)))


def from_duodecimal(n: str) -> int:
    if n[0] == '-':
        return -from_duodecimal(n[1:])

    return sum(map(lambda p: reverse_digits[p[1]] * 12 ** p[0], enumerate(reversed(n))))


def reverse_and_add_simple(n: int) -> int:
    return n + from_duodecimal(''.join(reversed(to_duodecimal(n))))


def is_palindrome_simple(n: int) -> bool:
    d = to_duodecimal(n)
    return d == ''.join(reversed(d))


def check_simple(n: int) -> int:
    for i in range(MAX_ITERS_TEST):
        if is_palindrome_simple(n):
            return i
        n = reverse_and_add_simple(n)

    return -1


def test_to_duodecimal():
    assert to_duodecimal(0) == '0'
    assert to_duodecimal(1) == '1'
    assert to_duodecimal(9) == '9'
    assert to_duodecimal(10) == 'A'
    assert to_duodecimal(11) == 'B'
    assert to_duodecimal(12) == '10'
    assert to_duodecimal(13) == '11'
    assert to_duodecimal(23) == '1B'

    for i in range(1, 42):
        assert to_duodecimal(-i) == '-' + to_duodecimal(i)


def test_from_duodecimal():
    for i in range(-1000, 1000):
        assert i == from_duodecimal(to_duodecimal(i))


def test_reverse_and_add():
    for i in range(1, 1000):
        assert reverse_and_add_test(i) == reverse_and_add_simple(i)


def test_is_palindrome():
    for i in range(1, 100000):
        assert is_palindrome_test(i) == is_palindrome_simple(i)


def test_check():
    for i in range(1, 100):
        assert check(i) == check_simple(i)


def test_check_range():
    for i, n in check_range(1, 100).items():
        for _ in range(i):
            n = reverse_and_add_simple(n)
        assert is_palindrome_simple(n)
