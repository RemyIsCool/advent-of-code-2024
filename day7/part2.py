import multiprocessing

from numpy import array_split


def to_base_3(n):
    if n == 0:
        return "0"
    base_3 = ""
    is_negative = n < 0
    n = abs(n)
    while n > 0:
        base_3 = str(n % 3) + base_3
        n //= 3
    return "-" + base_3 if is_negative else base_3


def calculate(lines):
    this_answer = 0

    for line in lines:
        test, equation = line.split(":")
        test = int(test)
        equation = equation.strip()
        space_count = equation.count(" ")
        binary_operators_max = int("2" * space_count, 3)

        possible = False

        for x in range(binary_operators_max + 1):
            binary_string = to_base_3(x)
            if len(binary_string) < space_count:
                binary_string = "0" * (space_count - len(binary_string)) + binary_string
            operators_string = (
                binary_string.replace("0", "*").replace("1", "+").replace("2", "|")
            )

            with_operators = ""

            for char in equation:
                if char != " ":
                    with_operators += char
                    continue

                with_operators += f" {operators_string[0]} "

                operators_string = operators_string[1:]

            prev_operator = ""
            prev_number = 0

            for token in with_operators.split(" "):
                if token == "|" or token == "+" or token == "*":
                    prev_operator = token
                    continue

                if prev_operator == "":
                    prev_number = int(token)
                    continue

                if prev_operator == "|":
                    prev_number = int(str(prev_number) + token)
                elif prev_operator == "*":
                    prev_number *= int(token)
                else:
                    prev_number += int(token)

            if prev_number == test:
                possible = True
                break

        if possible:
            this_answer += test

    return this_answer


f = open("input.txt", "r")
lines = f.readlines()

answer = 0

pool = multiprocessing.Pool()
splitted = [*array_split(lines, 16)]
results = pool.map(calculate, splitted)


print(sum(results))
