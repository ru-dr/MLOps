import sys
import os
import math
import unittest

# Get the path to the project's root directory
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)

from src import calculator


class TestCalculator(unittest.TestCase):

    def test_fun1(self):
        self.assertEqual(calculator.fun1(2, 3), 5)
        self.assertEqual(calculator.fun1(5, 0), 5)
        self.assertEqual(calculator.fun1(-1, 1), 0)
        self.assertEqual(calculator.fun1(-1, -1), -2)

    def test_fun2(self):
        self.assertEqual(calculator.fun2(2, 3), -1)
        self.assertEqual(calculator.fun2(5, 0), 5)
        self.assertEqual(calculator.fun2(-1, 1), -2)
        self.assertEqual(calculator.fun2(-1, -1), 0)

    def test_fun3(self):
        self.assertEqual(calculator.fun3(2, 3), 6)
        self.assertEqual(calculator.fun3(5, 0), 0)
        self.assertEqual(calculator.fun3(-1, 1), -1)
        self.assertEqual(calculator.fun3(-1, -1), 1)

    def test_fun4(self):
        self.assertEqual(calculator.fun4(2, 3, 5), 10)
        self.assertEqual(calculator.fun4(5, 0, -1), 4)
        self.assertEqual(calculator.fun4(-1, -1, -1), -3)
        self.assertEqual(calculator.fun4(-1, -1, 100), 98)

    def test_divide(self):
        self.assertEqual(calculator.divide(10, 2), 5)
        self.assertEqual(calculator.divide(7, 2), 3.5)
        self.assertEqual(calculator.divide(-9, 3), -3)
        self.assertAlmostEqual(calculator.divide(1, 3), 1 / 3)

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            calculator.divide(5, 0)

    def test_power(self):
        self.assertEqual(calculator.power(2, 3), 8)
        self.assertEqual(calculator.power(5, 0), 1)
        self.assertEqual(calculator.power(2, -1), 0.5)
        self.assertEqual(calculator.power(-2, 3), -8)
        self.assertAlmostEqual(calculator.power(9, 0.5), 3)

    def test_power_invalid(self):
        with self.assertRaises(ValueError):
            calculator.power(-8, 0.5)
        with self.assertRaises(ZeroDivisionError):
            calculator.power(0, -2)

    def test_square_root(self):
        self.assertEqual(calculator.square_root(16), 4)
        self.assertEqual(calculator.square_root(0), 0)
        self.assertAlmostEqual(calculator.square_root(2), math.sqrt(2))

    def test_square_root_negative(self):
        with self.assertRaises(ValueError):
            calculator.square_root(-1)

    def test_mean(self):
        self.assertEqual(calculator.mean([1, 2, 3, 4]), 2.5)
        self.assertEqual(calculator.mean([5]), 5)
        self.assertAlmostEqual(calculator.mean([0.1, 0.2, 0.3]), 0.2)

    def test_mean_empty(self):
        with self.assertRaises(ValueError):
            calculator.mean([])

    def test_invalid_inputs(self):
        cases = [
            (calculator.fun1, ("2", 3)),
            (calculator.fun2, (2, None)),
            (calculator.fun3, ([1], 2)),
            (calculator.fun4, (1, 2, "3")),
            (calculator.fun1, (True, 1)),
            (calculator.divide, (1, "0")),
            (calculator.power, ("2", 2)),
            (calculator.square_root, ("4",)),
            (calculator.mean, ([1, "2", 3],)),
        ]
        for func, args in cases:
            with self.subTest(func=func.__name__, args=args):
                with self.assertRaises(ValueError):
                    func(*args)


if __name__ == '__main__':
    unittest.main()
