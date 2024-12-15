from typing import Set, Tuple

# row, column
Position = Tuple[int, int]

with open("input.txt", "r") as f:
    input = f.read()

grid_string, movements_string = input.split("\n\n")

walls: Set[Position] = set()
boxes: Set[Position] = set()
robot: Position = (0, 0)

for row, line in enumerate(grid_string.strip().splitlines()):
    for column, character in enumerate(line):
        position_x, position_y = row, column * 2

        match character:
            case "#":
                walls.add((position_x, position_y))
                walls.add((position_x, position_y + 1))
            case "O":
                boxes.add((position_x, position_y))
            case "@":
                robot = (position_x, position_y)


def print_grid():
    lines = grid_string.strip().splitlines()
    width, height = len(lines[0]) * 2, len(lines)
    grid = [[" " for _ in range(width)] for _ in range(height)]
    for box in boxes:
        grid[box[0]][box[1]] = "["
        grid[box[0]][box[1] + 1] = "]"
    for wall in walls:
        grid[wall[0]][wall[1]] = "#"
    grid[robot[0]][robot[1]] = "@"
    grid = ["".join(line) for line in grid]
    print("\n".join(grid))


def get_box_at_position(position: Position):
    return (
        position
        if position in boxes
        else (
            (position[0], position[1] - 1)
            if (position[0], position[1] - 1) in boxes
            else None
        )
    )


def get_overlapping_boxes(box: Position):
    overlapping: Set[Position] = set()

    if (box[0], box[1] - 1) in boxes:
        overlapping.add((box[0], box[1] - 1))
    if (box[0], box[1] + 1) in boxes:
        overlapping.add((box[0], box[1] + 1))
    if box in boxes:
        overlapping.add(box)

    return overlapping


def push_box(direction: Position, position: Position):
    global boxes

    box = get_box_at_position(position)

    if box is None:
        return True

    boxes.remove(box)

    pushed_box = (box[0] + direction[0], box[1] + direction[1])

    if pushed_box in walls or (pushed_box[0], pushed_box[1] + 1) in walls:
        return False

    overlapping = get_overlapping_boxes(pushed_box)

    for overlapping_box in overlapping:
        if not push_box(direction, overlapping_box):
            return False

    boxes.add(pushed_box)

    return True


for character in movements_string:
    direction: Position = (0, 0)

    match character:
        case "<":
            direction = (0, -1)
        case ">":
            direction = (0, 1)
        case "^":
            direction = (-1, 0)
        case "v":
            direction = (1, 0)

    original_boxes = boxes.copy()
    original_robot = robot

    direction_x, direction_y = direction

    robot = (robot[0] + direction_x, robot[1] + direction_y)

    if robot in walls:
        robot = original_robot
        continue

    overlapping_box = get_box_at_position(robot)

    if overlapping_box is not None:
        if not push_box(direction, robot):
            boxes = original_boxes
            robot = original_robot


# GPS Position: 100 * row + column
print(sum((100 * box[0] + box[1] for box in boxes)))
