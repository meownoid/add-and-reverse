from _fast import check, check_range


def test_algorithm():
    for i in range(12):
        assert check(i) == 0

    assert check(13) == 0
    assert check(14) == 1
    assert check(61919232478) == 121
    assert check(179169803) == 92
    assert check(100000) == 6
