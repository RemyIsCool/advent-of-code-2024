from typing import List, Set, Tuple

with open("input.txt", "r") as file:
    input = file.readlines()

input = [list(line.strip()) for line in input]

Position = Tuple[int, int]


def is_within_bounds(position: Position) -> bool:
    return (
        position[0] >= 0
        and position[0] < len(input[0])
        and position[1] >= 0
        and position[1] < len(input)
    )


def add_positions(position_a: Position, position_b: Position):
    return (position_a[0] + position_b[0], position_a[1] + position_b[1])


regions: List[List[Position]] = []


def expand_region(plant_type: str, region: int, plant: Position):
    for offset in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        offsetted = add_positions(plant, offset)
        offsetted_x, offsetted_y = offsetted

        if (
            offsetted in regions[region]
            or not is_within_bounds(offsetted)
            or input[offsetted_x][offsetted_y] != plant_type
        ):
            continue

        regions[region].append(offsetted)

        expand_region(plant_type, region, offsetted)


current_region = 0

for x, line in enumerate(input):
    for y, plant in enumerate(line):
        position = (x, y)

        for region in regions:
            if position in region:
                break
        else:
            regions.append([position])

            expand_region(plant, current_region, position)

            current_region += 1


def count_sides(cells: List[Position]) -> int:
    max_x = max(cell[0] for cell in cells)
    max_y = max(cell[1] for cell in cells)

    side_count = 0

    for x in range(max_x + 1):
        slice: List[Position] = []

        for cell in cells:
            if not cell[0] == x or (cell[0] - 1, cell[1]) in cells:
                continue

            slice.append(cell)

        slice = sorted(slice)
        if len(slice) > 0:
            side_count += 1

        for y, cell in enumerate(slice):
            if y == 0:
                continue

            if slice[y - 1][1] != cell[1] - 1:
                side_count += 1

    for x in range(max_x + 1):
        slice: List[Position] = []

        for cell in cells:
            if not cell[0] == x or (cell[0] + 1, cell[1]) in cells:
                continue

            slice.append(cell)

        slice = sorted(slice)
        if len(slice) > 0:
            side_count += 1

        for y, cell in enumerate(slice):
            if y == 0:
                continue

            if slice[y - 1][1] != cell[1] - 1:
                side_count += 1

    for x in range(max_y + 1):
        slice: List[Position] = []

        for cell in cells:
            if not cell[1] == x or (cell[0], cell[1] - 1) in cells:
                continue

            slice.append(cell)

        slice = sorted(slice)
        if len(slice) > 0:
            side_count += 1

        for y, cell in enumerate(slice):
            if y == 0:
                continue

            if slice[y - 1][0] != cell[0] - 1:
                side_count += 1

    for x in range(max_y + 1):
        slice: List[Position] = []

        for cell in cells:
            if not cell[1] == x or (cell[0], cell[1] + 1) in cells:
                continue

            slice.append(cell)

        slice = sorted(slice)
        if len(slice) > 0:
            side_count += 1

        for y, cell in enumerate(slice):
            if y == 0:
                continue

            if slice[y - 1][0] != cell[0] - 1:
                side_count += 1

    return side_count


side_counts: List[int] = []


for region in regions:
    side_counts.append(count_sides(region))


total_price = 0

for side_count, region in zip(side_counts, regions):
    total_price += side_count * len(region)

print(total_price)
