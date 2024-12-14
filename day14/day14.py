from dataclasses import dataclass
from typing import List


@dataclass
class Vector:
    x: int
    y: int


@dataclass
class Robot:
    position: Vector
    velocity: Vector


with open("input.txt", "r") as f:
    input_lines = f.readlines()


robots: List[Robot] = []

for line in input_lines:
    line = line.strip()

    position = Vector(0, 0)
    velocity = Vector(0, 0)

    for part in line.split(" "):
        x, y = part[2:].split(",")

        if part[0] == "p":
            position = Vector(int(x), int(y))
        else:
            velocity = Vector(int(x), int(y))

    robots.append(Robot(position, velocity))


WIDTH, HEIGHT = 101, 103


# Part 2
found_tree = False

x = 0
while not found_tree:
    x += 1
    grid = [["." for _ in range(WIDTH)] for _ in range(HEIGHT)]

    for robot in robots:
        robot.position.x += robot.velocity.x
        robot.position.y += robot.velocity.y

        robot.position.x %= WIDTH
        robot.position.y %= HEIGHT

        grid[robot.position.y][robot.position.x] = "#"

    for line in grid:
        line = "".join(line)
        if "########" in line:
            found_tree = True
            break

    if found_tree:
        for line in grid:
            print("".join(line))

print("Found a Christmas tree on iteration", x)


# Part 1

# quadrants: List[List[Robot]] = [[] for _ in range(4)]
#
# for robot in robots:
#     half_width = WIDTH // 2
#     half_height = HEIGHT // 2
#
#     if robot.position.x < half_width and robot.position.y < half_height:
#         quadrants[0].append(robot)
#     elif robot.position.x < half_width and robot.position.y > half_height:
#         quadrants[1].append(robot)
#     elif robot.position.x > half_width and robot.position.y < half_height:
#         quadrants[2].append(robot)
#     elif robot.position.x > half_width and robot.position.y > half_height:
#         quadrants[3].append(robot)
#
#
# answer = 1
#
# for quadrant in quadrants:
#     answer *= len(quadrant)
#
#
# print(answer)
