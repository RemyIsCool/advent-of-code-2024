from __future__ import annotations

from dataclasses import dataclass, field
from math import inf
from typing import List, Set, Tuple

Position = Tuple[int, int]


@dataclass
class Node:
    position: Position
    previous_node: Node | None = None
    distance_to_start: float = field(default=inf)


with open("input.txt", "r") as file:
    maze_strings = file.readlines()


walls: Set[Position] = set()
start = (0, 0)
end = (0, 0)

maze_width, maze_height = len(maze_strings[0]), len(maze_strings)

for row, line in enumerate(maze_strings):
    for column, character in enumerate(line):
        position = (row, column)
        match character:
            case "#":
                walls.add(position)
            case "S":
                start = position
            case "E":
                end = position


def find_lowest_score_path(
    walls: Set[Position], start: Position, end: Position, width: int, height: int
):
    nodes: List[Node] = []

    for i in range(width - 1):
        for j in range(height - 1):
            position = (i, j)

            if position in walls:
                continue

            new_node = Node(position)

            if position == start:
                new_node.distance_to_start = 0

            nodes.append(new_node)

    queue: List[Node] = nodes.copy()

    while len(queue) > 0:
        closest_node = queue[0]

        for node in queue:
            if node.distance_to_start < closest_node.distance_to_start:
                closest_node = node

        queue.remove(closest_node)

        for direction_row, direction_column in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            new_position = (
                closest_node.position[0] + direction_row,
                closest_node.position[1] + direction_column,
            )

            for i, node in enumerate(nodes):
                if node.position == new_position:
                    score = 1001

                    if closest_node.previous_node is not None and (
                        node.position[0]
                        == closest_node.position[0]
                        == closest_node.previous_node.position[0]
                        or node.position[1]
                        == closest_node.position[1]
                        == closest_node.previous_node.position[1]
                    ):
                        score = 1

                    if closest_node.previous_node is None:
                        if (direction_row, direction_column) == (0, 1):
                            score = 1

                    distance = closest_node.distance_to_start + score

                    if distance < node.distance_to_start:
                        nodes[i].distance_to_start = distance
                        nodes[i].previous_node = closest_node

    for node in nodes:
        if node.position == end:
            print(node.distance_to_start)
            return node.distance_to_start


find_lowest_score_path(walls, start, end, maze_width, maze_height)
