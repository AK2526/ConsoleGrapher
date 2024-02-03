import math
import re

binary = ["+", "-", "*", "/", "^", "root"]
unary = ["neg", "sin", "cos", "tan", "sqrt", "cbrt", "arctan", "arcsin", "arccos"]
fns = unary[1:]
constants = ["pi", "e"]

all = binary[5:] + unary + constants

p_float = "\d+(?:\.\d+){0,1}"

pattern = "(?:" + '|'.join(all) + ")|\d+(?:\.\d+){0,1}|\S"


class Bracket:
    def __init__(self, eqn: list):
        self.item = get_operation(eqn)

    def __str__(self):
        return "(" + str(self.item) + ")"

    def calculate(self, var):
        return self.item.calculate(var)

    def __repr__(self):
        return str(self)


class Unary:
    def __init__(self, type, item):
        self.item = item
        self.type = type

        # Determine function
        if type == "sqrt":
            self.fn = math.sqrt
        elif type == "sin":
            self.fn = math.sin
        elif type == "cos":
            self.fn = math.cos
        elif type == "tan":
            self.fn = math.tan
        elif type == "arctan":
            self.fn = math.atan
        elif type == "arccos":
            self.fn = math.acos
        elif type == "arcsin":
            self.fn = math.asin
        elif type == "neg":
            self.fn = lambda x: -1 * x
        elif type == "cbrt":
            self.fn = lambda x: x ** (1/3)

    def __str__(self):
        if self.type != "neg":
            return self.type + str(self.item)
        else:
            return "-" + str(self.item)

    def calculate(self, var):
        return self.fn(self.item.calculate(var))

    def __repr__(self):
        return str(self)


class Binary:
    def __init__(self, type, arg1, arg2):
        self.type = type
        self.arg1 = arg1
        self.arg2 = arg2

        if type == "+":
            self.fn = lambda x, y: x + y
        elif type == "-":
            self.fn = lambda x, y: x - y
        elif type == "*":
            self.fn = lambda x, y: x * y
        elif type == "/":
            self.fn = lambda x, y: x / y
        elif type == "root":
            self.fn = lambda x, y: y ** (1/x)
        elif type == "^":
            self.fn = lambda x, y: x ** y

    def __str__(self):
        if self.type == "^":
            return "{}{}{}".format(self.arg1, self.type, self.arg2)
        elif self.type == "root":
            return "({}){}({})".format(self.arg1, self.type, self.arg2)
        return "{} {} {}".format(self.arg1, self.type, self.arg2)

    def calculate(self, var):
        return self.fn(self.arg1.calculate(var), self.arg2.calculate(var))

    def __repr__(self):
        return str(self)


class Value:
    def __init__(self, data):
        self.is_var = False
        self.name = data

        if data[0].isdigit():
            self.value = float(data)

        elif data in ["e", "pi"]:
            if data == "e":
                self.value = math.e
            elif data == "pi":
                self.value = math.pi

        else:
            self.is_var = True
            self.calculate = self.calculate2

    def calculate(self, var):
        return self.value

    def calculate2(self, var):
        if self.name in var:
            return var[self.name]
        return 1

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


def clean_eqn(eqn: str):
    final = re.findall(pattern, eqn)

    i = 0

    # Code to set negations
    while i + 1 < len(final):
        if final[i] == "-" and (i == 0 or final[i-1] in binary or final[i-1] == "(" or final[i-1] in unary):
            final[i] = "neg"
            # if final[i + 1][0].isdigit():
            #
            #     final = final[:i] + ["-" + final[i + 1]] + final[i + 2:]
            # else:
            #     final = final[:i] + ["-1", "*", final[i + 1]] + final[i + 2:]
        i += 1

    i, depth = 0, 0
    add, ignore = {}, {}

    # Insert brackets around unary operations
    while i < len(final):
        if final[i] in unary and final[i + 1] != "(":
            add[depth] = 1
            final.insert(i + 1, "(")
        if final[i] == "(":
            depth += 1
        elif final[i] == ")":
            depth -= 1
            if add.get(depth-1, -1) == 2: # Checks if bracket is open and if there is an item in bracket
                final.insert(i + 1, ")")
                add.pop(depth-1)
        elif final[i] not in unary and depth - 1 in add:
            add.pop(depth-1)
            final.insert(i + 1, ")")
        elif final[i] in unary and depth - 1 in add:
            add[depth-1] = 2
        i += 1

    # Dictionary of Variables
    variables = {}

    # Replace values with value class
    for i in range(len(final)):
        if final[i] not in unary + ["(", ")"] + binary:
            final[i] = Value(final[i])
            if final[i].is_var:
                variables[final[i].name] = 1

    return final, variables


def get_binary(eqn: list, operation: list):
    i = 0
    while i + 1 < len(eqn):
        for op in operation:
            if eqn[i] == op:
                eqn = eqn[:i-1] + [Binary(eqn[i], eqn[i-1], eqn[i + 1])] + eqn[i+2:]
                i -= 1
                break
        i += 1
    return eqn


def get_operation(eqn: list):
    # Convert brackets to bracket object
    i, start, end, depth = 0, -1, -1, 0
    while i < len(eqn):
        if eqn[i] == "(":
            depth += 1
            if depth == 1:
                start = i
        elif eqn[i] == ")":
            depth -= 1
            if depth == 0 and start != -1:
                end = i
                bracket_obj = Bracket(eqn[start + 1: end ])
                eqn = eqn[:start] + [bracket_obj] + eqn[end + 1:]
                i, start, end = start, -1, -1
        i += 1

    # Convert inner functions to classes
    i = 0
    while i < len(eqn):
        if eqn[i] in fns:
            eqn = eqn[:i] + [Unary(eqn[i], eqn[i + 1])] + eqn[i + 2:]
        i += 1

    eqn = get_binary(eqn, ["root"])

    # Convert exponents
    eqn = get_binary(eqn, ["^"])

    # Convert negations
    i = 0
    while i < len(eqn):
        if eqn[i] == "neg":
            eqn = eqn[:i] + [Unary(eqn[i], eqn[i + 1])] + eqn[i + 2:]
        i += 1

    # Add multiplication between terms that are probably being multiplied
    i = 0
    while i + 1 < len(eqn):
        # If consecutive elements are not binary, then multiply them together
        if eqn[i] not in binary and eqn[i + 1] not in binary:
            eqn.insert(i + 1, "*")
        i += 1

    # Convert multiplication and division
    eqn = get_binary(eqn, ["*", "/"])

    # Convert addition and subtraction
    eqn = get_binary(eqn, ["+", "-"])

    return eqn[0]

def get_fn(s: str):
    clean, var = clean_eqn(s)
    return get_operation(clean), var
