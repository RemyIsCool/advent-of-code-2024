from collections import deque

Program = list[int]


def load_input() -> str:
    with open("input.txt", "r") as file:
        input_string = file.read()

    return input_string


def parse_input(input_string: str) -> tuple[int, int, int, Program]:
    registers_string, program_string = input_string.split("\n\n")

    register_a, register_b, register_c = (
        int(register_string.split(": ")[-1])
        for register_string in registers_string.splitlines()
    )

    program_string = program_string.split(": ")[-1]
    program: Program = [int(number) for number in program_string.split(",")]

    return register_a, register_b, register_c, program


def get_combo_operand(
    register_a: int, register_b: int, register_c: int, operand: int
) -> int:
    if operand <= 3:
        return operand
    if operand == 4:
        return register_a
    if operand == 5:
        return register_b
    if operand == 6:
        return register_c

    raise RuntimeError("Invalid operant!")


def simulate(
    register_a: int, register_b: int, register_c: int, program: Program
) -> list[int]:
    output = []

    instruction_pointer = 0

    while instruction_pointer < len(program) - 1:
        opcode, operand = program[instruction_pointer], program[instruction_pointer + 1]

        match opcode:
            case 0:
                # adv
                register_a //= 2 ** get_combo_operand(
                    register_a, register_b, register_c, operand
                )

            case 1:
                # bxl
                register_b ^= operand

            case 2:
                # bst
                register_b = (
                    get_combo_operand(register_a, register_b, register_c, operand) % 8
                )

            case 3:
                # jnz
                if register_a != 0:
                    instruction_pointer = operand
                    continue

            case 4:
                # bxc
                register_b ^= register_c

            case 5:
                # out
                output.append(
                    get_combo_operand(register_a, register_b, register_c, operand) % 8
                )

            case 6:
                # bdv
                register_b = register_a // 2 ** get_combo_operand(
                    register_a, register_b, register_c, operand
                )

            case 7:
                # cdv
                register_c = register_a // 2 ** get_combo_operand(
                    register_a, register_b, register_c, operand
                )

        instruction_pointer += 2

    return output


def search_for_a(program: list[int]):
    # Thanks to today's submissions page

    queue = deque([0])
    iteration = 0

    while queue:
        expected = program[len(program) - iteration - 1 :]

        if iteration == len(program):
            return min(queue)

        for _ in range(len(queue)):
            value = queue.popleft()

            for number in range(8):
                register_a = 8 * value + number
                output = simulate(register_a, 0, 0, program)

                if output == expected:
                    queue.append(register_a)

        iteration += 1


input_string = load_input()
register_a, register_b, register_c, program = parse_input(input_string)

print(search_for_a(program))
