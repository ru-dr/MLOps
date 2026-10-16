import math

import pytest
from src import calculator


def test_fun1():
    assert calculator.fun1(2, 3) == 5
    assert calculator.fun1(5, 0) == 5
    assert calculator.fun1(-1, 1) == 0
    assert calculator.fun1(-1, -1) == -2


def test_fun2():
    assert calculator.fun2(2, 3) == -1
    assert calculator.fun2(5, 0) == 5
    assert calculator.fun2(-1, 1) == -2
    assert calculator.fun2(-1, -1) == 0


def test_fun3():
    assert calculator.fun3(2, 3) == 6
    assert calculator.fun3(5, 0) == 0
    assert calculator.fun3(-1, 1) == -1
    assert calculator.fun3(-1, -1) == 1


def test_fun4():
    assert calculator.fun4(2, 3, 5) == 10
    assert calculator.fun4(5, 0, -1) == 4
    assert calculator.fun4(-1, -1, -1) == -3
    assert calculator.fun4(-1, -1, 100) == 98


@pytest.mark.parametrize(
    "x, y, expected",
    [
        (10, 2, 5),
        (7, 2, 3.5),
        (-9, 3, -3),
        (0, 5, 0),
        (1, 3, 1 / 3),
    ],
)
def test_divide(x, y, expected):
    assert calculator.divide(x, y) == pytest.approx(expected)


@pytest.mark.parametrize("x", [1, 0, -4, 2.5])
def test_divide_by_zero_raises(x):
    with pytest.raises(ZeroDivisionError):
        calculator.divide(x, 0)


@pytest.mark.parametrize(
    "base, exponent, expected",
    [
        (2, 3, 8),
        (5, 0, 1),
        (2, -1, 0.5),
        (-2, 3, -8),
        (9, 0.5, 3),
        (0, 0, 1),
    ],
)
def test_power(base, exponent, expected):
    assert calculator.power(base, exponent) == pytest.approx(expected)


def test_power_negative_base_fractional_exponent_raises():
    with pytest.raises(ValueError):
        calculator.power(-8, 0.5)


def test_power_zero_negative_exponent_raises():
    with pytest.raises(ZeroDivisionError):
        calculator.power(0, -2)


@pytest.mark.parametrize(
    "x, expected",
    [(0, 0), (1, 1), (16, 4), (2, math.sqrt(2)), (0.25, 0.5)],
)
def test_square_root(x, expected):
    assert calculator.square_root(x) == pytest.approx(expected)


def test_square_root_negative_raises():
    with pytest.raises(ValueError):
        calculator.square_root(-1)


@pytest.mark.parametrize(
    "values, expected",
    [
        ([1, 2, 3, 4], 2.5),
        ([5], 5),
        ((-1, 1), 0),
        ([0.1, 0.2, 0.3], 0.2),
    ],
)
def test_mean(values, expected):
    assert calculator.mean(values) == pytest.approx(expected)


def test_mean_empty_raises():
    with pytest.raises(ValueError):
        calculator.mean([])


@pytest.mark.parametrize(
    "func, args",
    [
        (calculator.fun1, ("2", 3)),
        (calculator.fun2, (2, None)),
        (calculator.fun3, ([1], 2)),
        (calculator.fun4, (1, 2, "3")),
        (calculator.fun1, (True, 1)),
        (calculator.divide, (1, "0")),
        (calculator.power, ("2", 2)),
        (calculator.square_root, ("4",)),
        (calculator.mean, ([1, "2", 3],)),
    ],
)
def test_invalid_input_raises_value_error(func, args):
    with pytest.raises(ValueError):
        func(*args)
