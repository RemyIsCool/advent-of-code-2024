package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func main() {
	data, _ := os.ReadFile("input.txt")

	r, _ := regexp.Compile("mul\\(\\d+,\\d+\\)|don't\\(\\)|do\\(\\)")
	commands := r.FindAllString(string(data), -1)

	sum := 0

	do := true

	for _, command := range commands {
		if command == "don't()" {
			do = false
			continue
		}
		if command == "do()" {
			do = true
			continue
		}
		if !do {
			continue
		}

		first, _ := strconv.Atoi(strings.Split(command, ",")[0][4:])
		secondstr := strings.Split(command, ",")[1]
		second, _ := strconv.Atoi(secondstr[:len(secondstr)-1])

		sum += first * second
	}

	fmt.Println(sum)
}
