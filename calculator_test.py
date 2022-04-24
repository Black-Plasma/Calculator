import unittest

from calculator import *


class CalculatorTestCase(unittest.TestCase):

    def test_peek(self):
        self.assertEqual(5, peek([1, 2, 3, 5]))
        self.assertEqual(None, peek([]))

    def test_get_precedence(self):
        self.assertEqual(1, get_precedence("+"))
        self.assertEqual(1, get_precedence("-"))
        self.assertEqual(2, get_precedence("*"))
        self.assertEqual(2, get_precedence("/"))

    def test_tokenize(self):
        self.assertEqual(["10", "+", "20", "-", "30"], tokenize("10+20-30"))
        self.assertEqual(["(", "5", "-", "15", ")", "/", "25"], tokenize("(5-15)/25"))
        self.assertEqual(["50", "^", "10"], tokenize("50^10"))
        self.assertEqual(["-5", "*", "3"], tokenize("-5*3"))
        self.assertIsNone(tokenize(""))

    def test_to_rpn(self):
        self.assertEqual(["30", "40", "+"], to_rpn(["30", "+", "40"]))
        self.assertEqual(["30", "40", "2", "/", "+"], to_rpn(["30", "+", "40", "/", "2"]))
        self.assertEqual(["30", "40", "+", "2", "/"], to_rpn(["(", "30", "+", "40", ")", "/", "2"]))
        self.assertEqual(["3", "2", "^"], to_rpn(["3", "^", "2"]))
        self.assertEqual(["-3", "4", "+"], to_rpn(["-3", "+", "4"]))

        with self.assertRaises(AssertionError):
            to_rpn(["12", "+", "22", ")"])
        with self.assertRaises(AssertionError):
            to_rpn(["21", "-", "(", "11", "+", "31"])

    def test_calculate_rpn(self):
        self.assertEqual(50, calculate_rpn(["20", "30", "+"]))
        self.assertEqual(-10, calculate_rpn(["20", "30", "-"]))
        self.assertEqual(600, calculate_rpn(["20", "30", "*"]))
        self.assertEqual(6, calculate_rpn(["18", "3", "/"]))
        self.assertEqual(8, calculate_rpn(["2", "3", "^"]))
        self.assertEqual(-16, calculate_rpn(["-20", "4", "+"]))


if __name__ == '__main__':
    unittest.main()
