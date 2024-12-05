package main

import (
	"fmt"
	"os"
	"strings"
)

func main() {
	rawInput, _ := os.ReadFile("input.txt")
	inputString := string(rawInput)
	// Input must be padded with 4 "." characters.
	input := strings.Split(inputString, "\n")

	xmases := 0

	for row, line := range input {
		for col, letter := range line {
			if letter == 'A' {
				if (input[row-1][col-1] == 'M' && input[row-1][col+1] == 'S' && input[row+1][col-1] == 'M' && input[row+1][col+1] == 'S') || (input[row-1][col-1] == 'S' && input[row-1][col+1] == 'M' && input[row+1][col-1] == 'S' && input[row+1][col+1] == 'M') || (input[row-1][col-1] == 'M' && input[row-1][col+1] == 'M' && input[row+1][col-1] == 'S' && input[row+1][col+1] == 'S') || (input[row-1][col-1] == 'S' && input[row-1][col+1] == 'S' && input[row+1][col-1] == 'M' && input[row+1][col+1] == 'M') {
					xmases++
				}
			}
		}
	}

	fmt.Println(xmases)
}
