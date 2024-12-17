# Thanks to Josiah Winslow for this blog post, it was very helpful (I copied it exactly ¯\_(ツ)_/¯)
# https://winslowjosiah.com/blog/2024/12/16/advent-of-code-2024-day-16/

from collections import defaultdict
from functools import partial
from heapq import heappop, heappush
from typing import Callable, Iterable, Iterator

Position = tuple[int, int]
PathState = tuple[Position, Position]

with open("input.txt", "r") as file:
    maze_strings = file.readlines()


walls: set[Position] = set()
start = (0, 0)
end = (0, 0)

maze_width, maze_height = len(maze_strings[0]), len(maze_strings)

for row, line in enumerate(maze_strings):
    for column, character in enumerate(line):
        position = (row, column)
        match character:
            case "S":
                start = position
            case "E":
                end = position


maze = list(map(list, maze_strings))


def next_states(
    state: PathState, maze: list[list[str]]
) -> Iterator[tuple[int, PathState]]:
    (node_row, node_column), (direction_row, direction_column) = state

    yield 1000, ((node_row, node_column), (direction_column, -direction_row))

    yield 1000, ((node_row, node_column), (-direction_column, direction_row))

    next = (node_row + direction_row, node_column + direction_column)
    if maze[next[0]][next[1]] != "#":
        yield 1, (next, (direction_row, direction_column))


def find_shortest_paths(
    start_state: PathState,
    end_pos: Position,
    get_next_states: Callable[[PathState], Iterable[tuple[int, PathState]]],
) -> Iterator[list[PathState]]:
    costs: dict[PathState, int] = {}
    priority_queue: list[tuple[int, PathState]] = [(0, start_state)]
    prev_states: defaultdict[PathState, set[PathState]] = defaultdict(set)

    while priority_queue:
        cost, state = heappop(priority_queue)
        pos, *_ = state
        if pos == end_pos:
            break

        for weight, next_state in get_next_states(state):
            prev_cost = costs.get(next_state, float("inf"))
            next_cost = cost + weight

            if next_cost < prev_cost:
                costs[next_state] = next_cost
                heappush(priority_queue, (next_cost, next_state))
                prev_states[next_state] = {state}
            elif next_cost == prev_cost:
                prev_states[next_state].add(state)
    else:
        raise RuntimeError("no path exists!")

    start_node, *_ = start_state

    def walk(state: PathState) -> Iterator[list[PathState]]:
        node, *_ = state
        if node == start_node:
            yield [state]
            return
        for prev_state in prev_states[state]:
            for path in walk(prev_state):
                yield path + [state]

    return walk(state)


paths = find_shortest_paths(
    # The reindeer starts moving east
    start_state=(start, (0, 1)),
    end_pos=end,
    get_next_states=partial(next_states, maze=maze),
)
print(len({pos for path in paths for pos, _ in path}))
