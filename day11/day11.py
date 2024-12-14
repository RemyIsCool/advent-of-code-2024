from functools import cache
from typing import Tuple

with open("input.txt", "r") as f:
    stones = f.read().strip()

stones = [int(n) for n in stones.split(" ")]


@cache
def calculate_single_blink(value: int) -> Tuple[int, int | None]:
    text = str(value)
    num_digits = len(text)

    if value == 0:
        return (1, None)
    elif num_digits % 2 == 0:
        midpoint = num_digits // 2
        return (int(text[:midpoint]), int(text[midpoint:]))
    else:
        return (value * 2024, None)


@cache
def calculate_stone_blinks(stone: int, depth: int) -> int:
    left, right = calculate_single_blink(stone)

    if depth == 1:
        return 1 if right is None else 2

    output = calculate_stone_blinks(left, depth - 1)

    return (
        output if right is None else output + calculate_stone_blinks(right, depth - 1)
    )


answer = 0
for stone in stones:
    answer += calculate_stone_blinks(stone, 75)

print(answer)
