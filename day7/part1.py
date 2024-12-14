f = open("input.txt", "r")
lines = f.readlines()

answer = 0

for line in lines:
    test, equation = line.split(":")
    test = int(test)
    equation = equation.strip()
    space_count = equation.count(" ")
    binary_operators_max = int("1" * space_count, 2)

    possible = False

    for x in range(binary_operators_max + 1):
        binary_string = bin(x)[2:]
        if len(binary_string) < space_count:
            binary_string = "0" * (space_count - len(binary_string)) + binary_string
        operators_string = binary_string.replace("0", "*").replace("1", "+")

        with_operators = "(" * space_count

        for char in equation:
            if char != " ":
                with_operators += char
                continue

            with_operators += ")" + operators_string[0]

            operators_string = operators_string[1:]

        if eval(with_operators) == test:
            possible = True
            break

    if possible:
        answer += test

print(answer)
