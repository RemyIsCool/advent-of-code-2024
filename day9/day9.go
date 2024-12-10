package main

import (
	"fmt"
	"os"
	"strings"
)

func isSpaces(file []int) bool {
	for _, i := range file {
		if i != -1 {
			return false
		}
	}
	return true
}

func main() {
	inputFile, _ := os.ReadFile("input.txt")
	input := string(inputFile)

	files := [][]int{}

	id := 0

	for i, char := range strings.Trim(input, "\n") {
		if char != '0' {
			files = append(files, []int{})
		}

		if i%2 == 0 {
			for j := 0; j < int(char-'0'); j++ {
				files[len(files)-1] = append(files[len(files)-1], id)
			}
			id++
		} else {
			for j := 0; j < int(char-'0'); j++ {
				files[len(files)-1] = append(files[len(files)-1], -1)
			}
		}
	}

	fmt.Println(files)

	for filledFileIndex := len(files) - 1; filledFileIndex >= 0; filledFileIndex-- {
		filledFile := files[filledFileIndex]

		if isSpaces(filledFile) {
			continue
		}

		for emptyFileIndex, emptyFile := range files {
			if emptyFileIndex >= filledFileIndex {
				break
			}

			if !isSpaces(emptyFile) || len(filledFile) > len(emptyFile) {
				continue
			}

			files[emptyFileIndex] = filledFile

			justFilledExtraSpaces := []int{}
			for i := 0; i < len(emptyFile)-len(filledFile); i++ {
				justFilledExtraSpaces = append(justFilledExtraSpaces, -1)
			}

			justRemovedExtraSpaces := []int{}
			for i := 0; i < len(filledFile); i++ {
				justRemovedExtraSpaces = append(justRemovedExtraSpaces, -1)
			}

			files[filledFileIndex] = justRemovedExtraSpaces

			if len(justFilledExtraSpaces) > 0 {
				files = append(files[:emptyFileIndex+1], append([][]int{justFilledExtraSpaces}, files[emptyFileIndex+1:]...)...)
			}

			fmt.Println(files)

			break
		}
	}

	flattened := []int{}
	for _, file := range files {
		for _, block := range file {
			flattened = append(flattened, block)
		}
	}

	answer := 0

	for i, block := range flattened {
		if block == -1 {
			continue
		}
		answer += i * block
	}

	fmt.Println(answer)
}
