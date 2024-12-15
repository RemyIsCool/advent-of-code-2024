from dataclasses import dataclass
from typing import List

import sympy as sp


@dataclass
class Position:
    x: float
    y: float

    def __add__(self, other):
        return Position(self.x + other.x, self.y + other.y)

    def __mul__(self, other: int):
        return Position(self.x * other, self.y * other)

    __rmul__ = __mul__

    def __ge__(self, other):
        return self.x >= other.x and self.y >= other.y


@dataclass
class Machine:
    a: Position
    b: Position
    prize: Position


with open("input.txt", "r") as f:
    input = f.read()


machines: List[Machine] = []

machines_strings = input.split("\n\n")

for machine_string in machines_strings:
    a = Position(0, 0)
    b = Position(0, 0)
    prize = Position(0, 0)

    for line in machine_string.splitlines():
        key, value = line.split(": ")

        position = [int(v[2:]) for v in value.split(", ")]
        position = Position(position[0], position[1])

        match key:
            case "Button A":
                a = position
            case "Button B":
                b = position
            case "Prize":
                # Add 10 trillion for part 2
                ten_trillion = 10_000_000_000_000
                prize = position + Position(ten_trillion, ten_trillion)

    machines.append(Machine(a, b, prize))

answer = 0

for machine in machines:
    a, b = sp.symbols("a b")

    eqx = sp.Eq(a * machine.a.x + b * machine.b.x, machine.prize.x)
    eqy = sp.Eq(a * machine.a.y + b * machine.b.y, machine.prize.y)

    result = sp.solve([eqx, eqy], (a, b))

    sa, sb = map(float, result.values())

    if sa % 1 != 0 or sb % 1 != 0:
        continue

    if (
        Position(
            machine.a.x * sa + machine.b.x * sb, machine.a.y * sa + machine.b.y * sb
        )
        == machine.prize
    ):
        answer += int(sa * 3 + sb)


print(answer)
