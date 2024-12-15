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
        position = (row, column)

        match character:
            case "#":
                walls.add(position)
            case "O":
                boxes.add(position)
            case "@":
                robot = position


def push_box(direction: Position, box: Position):
    global boxes

    boxes.remove(box)

    pushed_position = (box[0] + direction[0], box[1] + direction[1])

    if pushed_position in walls:
        return False

    if pushed_position in boxes:
        if not push_box(direction, pushed_position):
            return False

    boxes.add(pushed_position)

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

    if robot in boxes:
        if not push_box(direction, robot):
            boxes = original_boxes
            robot = original_robot


# GPS Position: 100 * row + column
print(sum((100 * box[0] + box[1] for box in boxes)))
