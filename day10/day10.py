from typing import List, Tuple

with open("input.txt", "r") as file:
    input = [s.strip() for s in file.readlines()]


found_nines: List[List[Tuple[int, int]]] = []


def search_around(position: Tuple[int, int], zero_index_found_nines: int):
    value_string = input[position[0]][position[1]]

    if not value_string.isdigit():
        return

    value = int(value_string)

    found_positions: List[Tuple[int, int]] = []

    for around_pos in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        x = position[0] + around_pos[0]
        y = position[1] + around_pos[1]

        if x >= len(input) or y >= len(input[0]) or x < 0 or y < 0:
            continue

        around_value_string = input[x][y]

        if not around_value_string.isdigit():
            continue

        around_value = int(around_value_string)

        if around_value != value + 1:
            continue

        if around_value == 9:
            found_nines[zero_index_found_nines].append((x, y))
        else:
            found_positions.append((x, y))

    for position in found_positions:
        search_around(position, zero_index_found_nines)


for x, line in enumerate(input):
    for y, numStr in enumerate(line):
        if not numStr.isdigit():
            continue

        num = int(numStr)
        position = (x, y)

        if num == 0:
            found_nines.append([])
            search_around(position, len(found_nines) - 1)

deduplicated = [list(set(nines)) for nines in found_nines]

answer1 = 0

for l in deduplicated:
    answer1 += len(l)

answer2 = 0

for l in found_nines:
    answer2 += len(l)

print("Part 1:", answer1)
print("Part 2:", answer2)
