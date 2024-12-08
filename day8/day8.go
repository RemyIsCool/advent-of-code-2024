package main

import (
	"fmt"
	"math/rand"
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

type antinode struct {
	position position
	antenna  antenna
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

	antinodes := []antinode{}

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

			antinodes = append(antinodes, antinode{first.position, first}, antinode{last.position, last})

			firstAntinode := position{first.position.row + offset.row, first.position.column + offset.column}
			lastAntinode := position{last.position.row - offset.row, last.position.column - offset.column}

			for firstAntinode.row >= 0 && firstAntinode.row < len(inputLines)-1 && firstAntinode.column >= 0 && firstAntinode.column < len(inputLines[0]) ||
				lastAntinode.row >= 0 && lastAntinode.row < len(inputLines)-1 && lastAntinode.column >= 0 && lastAntinode.column < len(inputLines[0]) {
				antinodes = append(antinodes, antinode{firstAntinode, first}, antinode{lastAntinode, last})

				firstAntinode = position{firstAntinode.row + offset.row, firstAntinode.column + offset.column}
				lastAntinode = position{lastAntinode.row - offset.row, lastAntinode.column - offset.column}
			}
		}
	}

	antinodesFinal := []antinode{}

	for _, antinode := range antinodes {
		if !slices.Contains(antinodesFinal, antinode) && antinode.position.row >= 0 && antinode.position.row < len(inputLines)-1 && antinode.position.column >= 0 && antinode.position.column < len(inputLines[0]) {
			antinodesFinal = append(antinodesFinal, antinode)
		}
	}

	currentColour := 0
	colours := []string{"31", "32", "33", "34", "35", "36", "91", "92", "93", "94", "95", "96"}

	for i := range colours {
		j := rand.Intn(i + 1)
		colours[i], colours[j] = colours[j], colours[i]
	}

	coloursMap := map[string]string{}

	fmt.Println()

	for i, line := range inputLines {
		lineFinal := []string{}
		for j, char := range line {
			color := ""

			for _, antinode := range antinodesFinal {
				if antinode.position == (position{i, j}) {
					_, exists := coloursMap[antinode.antenna.frequency]
					if !exists {
						coloursMap[antinode.antenna.frequency] = colours[currentColour]
						currentColour = (currentColour + 1) % len(colours)
					}
					color = coloursMap[antinode.antenna.frequency]
				}
			}

			if char == '.' && color != "" {
				lineFinal = append(lineFinal, "\033[0;"+color+"m#\033[0m")
			} else if r.Match([]byte{byte(char)}) {
				_, exists := coloursMap[string(char)]
				if !exists {
					coloursMap[string(char)] = colours[currentColour]
					currentColour = (currentColour + 1) % len(colours)
				}
				lineFinal = append(lineFinal, "\033[0;"+coloursMap[string(char)]+"m"+string(char)+"\033[0m")
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
