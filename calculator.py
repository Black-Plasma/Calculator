#!/usr/bin/python3
import sys
import re


def to_rpn(tokens):
    out_queue = []
    stack = []

    for token in tokens:
        if is_number(token):
            out_queue.append(token)
        elif is_operator(token):
            while len(stack) != 0\
                    and is_operator(peek(stack))\
                    and token != "^"\
                    and get_precedence(token) <= get_precedence(peek(stack)):
                out_queue.append(stack.pop())
            stack.append(token)
        elif token == "(":
            stack.append(token)
        elif token == ")":
            while peek(stack) != "(":
                assert len(stack) != 0, "There is a closing bracket without an opening one before!"
                out_queue.append(stack.pop())
            stack.pop()

    for _ in range(len(stack)):
        assert peek(stack) != "(", "There are more opening than closing brackets!"
        out_queue.append(stack.pop())
    return out_queue


def calculate_rpn(tokens):
    stack = []
    for token in tokens:
        if is_number(token):
            stack.append(token)
        elif is_operator(token):
            right = int(stack.pop())
            left = int(stack.pop())
            temp = 0

            if token == "+":
                temp = left + right
            elif token == "-":
                temp = left - right
            elif token == "*":
                temp = left * right
            elif token == "/":
                temp = left / right
            elif token == "^":
                temp = pow(left, right)

            stack.append(temp)

    return stack.pop()


def tokenize(expression):
    if expression == "":
        return None

    tokens = []
    stack = []
    negative = False

    for i, c in enumerate(expression):
        if re.match("[0-9]", c):
            if negative:
                stack.append("-" + c)
                negative = False
            else:
                stack.append(c)
        elif re.match("[+-/*^()]", c):
            if (peek(stack) == "(" or i == 0) and c == "-":
                negative = True
            else:
                if len(stack) != 0:
                    tokens.append("".join(stack))
                    stack = []
                tokens.append(c)
    tokens.append("".join(stack))
    return tokens


def get_precedence(operator):
    return 2 if re.match("[*/]", operator) else 1


def is_number(s):
    return re.match("-?[0-9]+", s)


def is_operator(c):
    return re.match("^[+-/*^]$", c)


def peek(stack):
    if len(stack) == 0:
        return None
    return stack[len(stack) - 1]


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit("Usage: {} <expression>".format(sys.argv[0]))

    target = sys.argv[1]
    print(calculate_rpn(to_rpn(tokenize(target))))
