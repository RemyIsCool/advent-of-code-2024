package main

import (
	"fmt"
	"os"
	"regexp"
	"slices"
	"strconv"
	"strings"
)

type position struct {
	row    int
	column int
}

type antenna struct {
	position  position
	frequency string
}

func main() {
	file, _ := os.ReadFile("input.txt")
	input := string(file)
	inputLines := strings.Split(input, "\n")

	r, _ := regexp.Compile("\\d|\\w")

	antennas := []antenna{}

	for row, line := range inputLines {
		antennaMatches := r.FindAllStringIndex(line, -1)

		for _, antennaMatch := range antennaMatches {
			column := antennaMatch[0]

			antennaFrequency := string(line[antennaMatch[0]])
			antennaPosition := position{row, column}
			antenna := antenna{antennaPosition, antennaFrequency}

			antennas = append(antennas, antenna)
		}
	}

	antennaGroups := map[string][]antenna{}

	for _, foundAntenna := range antennas {
		_, groupExists := antennaGroups[foundAntenna.frequency]

		if !groupExists {
			antennaGroups[foundAntenna.frequency] = []antenna{}
		}

		antennaGroups[foundAntenna.frequency] = append(antennaGroups[foundAntenna.frequency], foundAntenna)
	}

	antinodes := []position{}

	for _, antennaGroup := range antennaGroups {
		pairs := [][]antenna{}

		for i := 0; i < len(antennaGroup); i++ {
			for j := i + 1; j < len(antennaGroup); j++ {
				pairs = append(pairs, []antenna{antennaGroup[i], antennaGroup[j]})
			}
		}

		for _, pair := range pairs {
			first, last := pair[0], pair[1]

			offset := position{first.position.row - last.position.row, first.position.column - last.position.column}

			antinodes = append(antinodes, first.position, last.position)

			firstAntinode := position{first.position.row + offset.row, first.position.column + offset.column}
			lastAntinode := position{last.position.row - offset.row, last.position.column - offset.column}

			for firstAntinode.row >= 0 && firstAntinode.row < len(inputLines)-1 && firstAntinode.column >= 0 && firstAntinode.column < len(inputLines[0]) ||
				lastAntinode.row >= 0 && lastAntinode.row < len(inputLines)-1 && lastAntinode.column >= 0 && lastAntinode.column < len(inputLines[0]) {
				antinodes = append(antinodes, firstAntinode, lastAntinode)

				firstAntinode = position{firstAntinode.row + offset.row, firstAntinode.column + offset.column}
				lastAntinode = position{lastAntinode.row - offset.row, lastAntinode.column - offset.column}
			}
		}
	}

	antinodesFinal := []position{}

	for _, antinode := range antinodes {
		if !slices.Contains(antinodesFinal, antinode) && antinode.row >= 0 && antinode.row < len(inputLines)-1 && antinode.column >= 0 && antinode.column < len(inputLines[0]) {
			antinodesFinal = append(antinodesFinal, antinode)
		}
	}

	fmt.Println()

	for i, line := range inputLines {
		lineFinal := []string{}
		for j, char := range line {
			if char == '.' && slices.Contains(antinodesFinal, position{i, j}) {
				lineFinal = append(lineFinal, "\033[0;31m#\033[0m")
			} else if r.Match([]byte{byte(char)}) {
				lineFinal = append(lineFinal, "\033[0;32m"+string(char)+"\033[0m")
			} else {
				lineFinal = append(lineFinal, "\033[0;90m"+string(char)+"\033[0m")
			}
		}
		fmt.Println("  " + strings.Join(lineFinal, ""))
	}

	ending := strconv.Itoa(len(antinodesFinal)) + "\033[0m antinodes found!"
	repeatCount := ((len(inputLines[0]) / 2) - len(ending)/2) + 2
	if repeatCount < 2 {
		repeatCount = 2
	}
	fmt.Println("\033[0;92m" + strings.Repeat(" ", repeatCount) + ending)
}
