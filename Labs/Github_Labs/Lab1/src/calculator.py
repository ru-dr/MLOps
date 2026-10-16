import math


def _validate_numbers(*args):
    """
    Ensures every argument is an int or float.
    Booleans are rejected even though bool is a subclass of int.
    Args:
        *args: Values to check.
    Raises:
        ValueError: If any value is not a number.
    """
    for value in args:
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError("All inputs must be numbers.")


def fun1(x, y):
    """
    Adds two numbers together.
    Args:
        x (int/float): First number.
        y (int/float): Second number.
    Returns:
        int/float: Sum of x and y.
    Raises:
        ValueError: If x or y is not a number.
    """
    _validate_numbers(x, y)
    return x + y


def fun2(x, y):
    """
    Subtracts two numbers.
    Args:
        x (int/float): First number.
        y (int/float): Second number.
    Returns:
        int/float: Difference of x and y.
    Raises:
        ValueError: If x or y is not a number.
    """
    _validate_numbers(x, y)
    return x - y


def fun3(x, y):
    """
    Multiplies two numbers together.
    Args:
        x (int/float): First number.
        y (int/float): Second number.
    Returns:
        int/float: Product of x and y.
    Raises:
        ValueError: If either x or y is not a number.
    """
    _validate_numbers(x, y)
    return x * y


def fun4(x, y, z):
    """
    Adds three numbers together.
    Args:
        x (int/float): First number.
        y (int/float): Second number.
        z (int/float): Third number.
    Returns:
        int/float: Sum of x, y and z.
    Raises:
        ValueError: If x, y or z is not a number.
    """
    _validate_numbers(x, y, z)
    return x + y + z


def divide(x, y):
    """
    Divides x by y.
    Args:
        x (int/float): Dividend.
        y (int/float): Divisor.
    Returns:
        float: Quotient of x and y.
    Raises:
        ValueError: If x or y is not a number.
        ZeroDivisionError: If y is zero.
    """
    _validate_numbers(x, y)
    if y == 0:
        raise ZeroDivisionError("Cannot divide by zero.")
    return x / y


def power(base, exponent):
    """
    Raises base to the given exponent.
    Args:
        base (int/float): Base number.
        exponent (int/float): Exponent.
    Returns:
        int/float: base ** exponent.
    Raises:
        ValueError: If inputs are not numbers, or the result would be complex
            (negative base with a fractional exponent).
        ZeroDivisionError: If base is zero and exponent is negative.
    """
    _validate_numbers(base, exponent)
    if base < 0 and not float(exponent).is_integer():
        raise ValueError("Negative base with fractional exponent is not supported.")
    if base == 0 and exponent < 0:
        raise ZeroDivisionError("Zero cannot be raised to a negative power.")
    return base ** exponent


def square_root(x):
    """
    Computes the square root of a non-negative number.
    Args:
        x (int/float): Number to take the square root of.
    Returns:
        float: Square root of x.
    Raises:
        ValueError: If x is not a number or is negative.
    """
    _validate_numbers(x)
    if x < 0:
        raise ValueError("Cannot take the square root of a negative number.")
    return math.sqrt(x)


def mean(values):
    """
    Computes the arithmetic mean of a list of numbers.
    Args:
        values (list/tuple): Numbers to average.
    Returns:
        float: Mean of the values.
    Raises:
        ValueError: If values is empty or contains a non-number.
    """
    if not values:
        raise ValueError("Cannot compute the mean of an empty sequence.")
    _validate_numbers(*values)
    return sum(values) / len(values)
