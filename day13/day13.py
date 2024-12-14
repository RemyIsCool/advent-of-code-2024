from dataclasses import dataclass
from typing import List


@dataclass
class Position:
    x: int
    y: int

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
    a = int(
        (machine.prize.x * machine.b.y - machine.prize.y * machine.b.x)
        / (machine.a.x * machine.b.y - machine.a.y * machine.b.x)
    )
    b = int(
        (machine.a.x * machine.prize.y - machine.a.y * machine.prize.x)
        / (machine.a.x * machine.b.y - machine.a.y * machine.b.x)
    )

    if (
        Position(machine.a.x * a + machine.b.x * b, machine.a.y * a + machine.b.y * b)
        == machine.prize
    ):
        answer += a * 3 + b


print(answer)
