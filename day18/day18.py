from math import inf
from typing import TypeAlias

Position: TypeAlias = tuple[int, int]

SIZE = 70


def read_input() -> list[str]:
    with open("input.txt", "r") as file:
        input: list[str] = file.readlines()

    return [line.strip() for line in input]


def parse_input(input: list[str]) -> list[Position]:
    positions: list[Position] = []

    for line in input:
        x_string, y_string = line.split(",")
        positions.append((int(x_string), int(y_string)))

    return positions


def get_neighbors(position: Position, walls: list[Position]) -> list[Position]:
    neighbors: list[Position] = []

    for direction_x, direction_y in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        offsetted_x, offsetted_y = position[0] + direction_x, position[1] + direction_y

        if (
            offsetted_x > SIZE
            or offsetted_y > SIZE
            or offsetted_x < 0
            or offsetted_y < 0
        ):
            continue

        if (offsetted_x, offsetted_y) in walls:
            continue

        neighbors.append((offsetted_x, offsetted_y))

    return neighbors


def find_distance(walls: list[Position]) -> float:
    distances: dict[Position, float] = {}
    previous: dict[Position, Position | None] = {}
    queue: list[Position] = []

    for x in range(SIZE + 1):
        for y in range(SIZE + 1):
            position: Position = (x, y)
            distances[position] = inf
            previous[position] = None
            queue.append(position)

    distances[(0, 0)] = 0

    while queue:
        current = min(queue, key=lambda position: distances[position])
        queue.remove(current)

        for neighbor in get_neighbors(current, walls):
            if neighbor not in queue:
                continue

            distance_from_current = distances[current] + 1

            if distance_from_current < distances[neighbor]:
                distances[neighbor] = distance_from_current
                previous[neighbor] = current

    end_position = (SIZE, SIZE)

    assert distances[end_position] != inf, "No path found"

    return distances[end_position]


def exists_path(walls: list[Position]) -> bool:
    start: Position = (0, 0)
    visited: list[Position] = [start]
    queue: list[Position] = [start]

    while queue:
        current = queue.pop(0)

        for neighbor in get_neighbors(current, walls):
            if neighbor == (SIZE, SIZE):
                return True

            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)

    return False


def find_blocking_byte(walls: list[Position], low: int, high: int) -> int:
    if low + 1 == high:
        return high

    if low == high:
        return high - 1

    midpoint = (high + low) // 2

    if exists_path(walls[:midpoint]):
        return find_blocking_byte(walls, midpoint + 1, high)
    else:
        return find_blocking_byte(walls, low, midpoint - 1)


def part1():
    input = read_input()
    walls = parse_input(input)

    return find_distance(walls[:1024])


def part2():
    input = read_input()
    walls = parse_input(input)
    blocking_index = find_blocking_byte(walls, 0, len(walls) - 1)

    return ",".join(list(map(str, walls[blocking_index])))


print("Part 1:", part1())
print("Part 2:", part2())
