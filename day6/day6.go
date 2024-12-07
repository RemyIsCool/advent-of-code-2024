package main

import (
	"fmt"
	"os"
	"slices"
	"strings"
)

type position struct {
	row    int
	column int
}

// thx stack overflow
func replaceAtIndex(in string, r rune, i int) string {
	out := []rune(in)
	out[i] = r
	return string(out)
}

func isInfiniteLoop(guardPosition position, obstacles []position, inputLines []string) bool {
	guardDirection := "up"

	for counter := 0; counter < 100_000; counter++ {
		previousPosition := guardPosition

		switch guardDirection {
		case "up":
			guardPosition.row--
		case "down":
			guardPosition.row++
		case "left":
			guardPosition.column--
		case "right":
			guardPosition.column++
		}

		if slices.Contains(obstacles, guardPosition) {
			guardPosition = previousPosition

			switch guardDirection {
			case "up":
				guardDirection = "right"
			case "down":
				guardDirection = "left"
			case "left":
				guardDirection = "up"
			case "right":
				guardDirection = "down"
			}

		}

		if !(guardPosition.row >= 0 && guardPosition.row < len(inputLines[0]) && guardPosition.column >= 0 && guardPosition.column < len(inputLines)) {
			return false
		}
	}

	return true
}

func main() {
	inputFile, _ := os.ReadFile("input.txt")
	inputString := string(inputFile)
	inputLines := strings.Split(inputString, "\n")

	var guardPosition position
	obstacles := []position{}

	for row, inputLine := range inputLines {
		for column, inputRune := range inputLine {
			switch inputRune {
			case '^':
				guardPosition = position{row, column}
			case '#':
				obstacles = append(obstacles, position{row, column})
			}
		}
	}

	infiniteLoops := 0

	for row, inputLine := range inputLines {
		for column, inputRune := range inputLine {
			if inputRune == '.' {
				if isInfiniteLoop(guardPosition, append(obstacles, position{row, column}), inputLines) {
					infiniteLoops++
				}
			}
		}
	}

	fmt.Println(infiniteLoops)
}
