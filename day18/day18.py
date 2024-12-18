from math import inf
from typing import TypeAlias

from tqdm import tqdm

Position: TypeAlias = tuple[int, int]
Map: TypeAlias = list[list[bool]]


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


def generate_map(positions: list[Position], byte_count: int, grid_range: int) -> Map:
    memory_map = [[False for _ in range(grid_range + 1)] for _ in range(grid_range + 1)]

    for x, y in positions[:byte_count]:
        memory_map[y][x] = True

    return memory_map


def print_map(map: Map):
    for line in map:
        for place in line:
            print("#" if place else ".", end="")
        print()


def get_neighbors(position: Position, map: Map) -> list[Position]:
    neighbors: list[Position] = []

    for direction_x, direction_y in ((1, 0), (0, 1), (-1, 0), (0, -1)):
        offsetted_x, offsetted_y = position[0] + direction_x, position[1] + direction_y

        if (
            offsetted_x >= len(map[0])
            or offsetted_y >= len(map)
            or offsetted_x < 0
            or offsetted_y < 0
        ):
            continue

        if map[offsetted_y][offsetted_x]:
            continue

        neighbors.append((offsetted_x, offsetted_y))

    return neighbors


def dijkstras(map: Map) -> float:
    distances: dict[Position, float] = {}
    previous: dict[Position, Position | None] = {}
    queue: list[Position] = []

    for y, row in enumerate(map):
        for x in range(len(row)):
            position: Position = (x, y)
            distances[position] = inf
            previous[position] = None
            queue.append(position)

    distances[(0, 0)] = 0

    while queue:
        current = min(queue, key=lambda position: distances[position])
        queue.remove(current)

        for neighbor in get_neighbors(current, map):
            if neighbor not in queue:
                continue

            distance_from_current = distances[current] + 1

            if distance_from_current < distances[neighbor]:
                distances[neighbor] = distance_from_current
                previous[neighbor] = current

    end_position = (len(map[0]) - 1, len(map) - 1)

    assert distances[end_position] != inf, "No path found"

    return distances[end_position]


def bfs(map: Map) -> bool:
    start: Position = (0, 0)
    visited: list[Position] = [start]
    queue: list[Position] = [start]

    while queue:
        current = queue.pop(0)

        for neighbor in get_neighbors(current, map):
            if neighbor == (len(map[0]) - 1, len(map) - 1):
                return True

            if neighbor not in visited:
                visited.append(neighbor)
                queue.append(neighbor)

    return False


def part1():
    input = read_input()
    positions = parse_input(input)

    map = generate_map(positions, 1024, 70)
    return dijkstras(map)


def part2():
    input = read_input()
    positions = parse_input(input)

    for x in tqdm(range(1024, len(positions))):
        map = generate_map(positions, x, 70)
        if not bfs(map):
            return positions[x - 1]


print("Part 1:", part1())
print("Part 2:", part2())
