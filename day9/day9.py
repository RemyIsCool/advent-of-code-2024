from typing import List, Tuple

with open("input.txt", "r") as file:
	input = file.read()

input = input.strip()

files: List[Tuple[int|None, int]] = []

id = 0
for index, digit in enumerate(input):
	digit = int(digit)

	if index % 2 == 0:
		files.append((id, digit))
		id += 1
	else:
		files.append((None, digit))

files_sorted = files

for x in range(len(files)-1, -1, -1):
	outer_file = files[x]
	outer_file_id, outer_file_count = outer_file

	if outer_file_id == None:
		continue

	for y, (inner_file_id, inner_file_count) in enumerate(files[:x]):
		if inner_file_count < outer_file_count or inner_file_id != None:
			continue

		files_sorted[x] = (None, outer_file_count)

		files_sorted[y] = outer_file

		if inner_file_count > outer_file_count:
			files_sorted.insert(y+1, (None, inner_file_count - outer_file_count))	

		break

flattened: List[int|None] = []
	
for x, (file_id, file_count) in enumerate(files_sorted):
	for y in range(file_count):
		flattened.append(file_id)

answer = 0

for x, y in enumerate(flattened):
	if y == None:
		continue

	answer += x * y

print(answer)
