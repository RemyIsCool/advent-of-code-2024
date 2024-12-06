package main

import (
	"fmt"
	"os"
	"reflect"
	"sort"
	"strconv"
	"strings"
)

func main() {
	inputFile, _ := os.ReadFile("input.txt")
	input := string(inputFile)
	inputParts := strings.Split(input, "\n\n")
	rulesString, updatesString := inputParts[0], inputParts[1]
	ruleStrings, updates := strings.Split(rulesString, "\n"), strings.Split(updatesString, "\n")

	rules := make([][]int, 0)

	for _, ruleString := range ruleStrings {
		parts := strings.Split(ruleString, "|")
		first, last := parts[0], parts[1]
		firstint, _ := strconv.Atoi(first)
		lastint, _ := strconv.Atoi(last)
		rules = append(rules, []int{firstint, lastint})
	}

	updatesNumbers := make([][]int, 0)

	for _, updateString := range updates {
		update := strings.Split(updateString, ",")

		line := make([]int, 0)

		for _, pageString := range update {
			page, err := strconv.Atoi(pageString)
			if err == nil {
				line = append(line, page)
			}
		}

		if len(line) != 0 {
			updatesNumbers = append(updatesNumbers, line)
		}
	}

	answer := 0

	for _, update := range updatesNumbers {
		beforeChange := append([]int(nil), update...)
		sort.Slice(update, func(i, j int) bool {
			prev, next := update[i], update[j]

			for _, rule := range rules {
				if rule[0] == next && rule[1] == prev {
					return false
				}
			}

			return true
		})

		if !reflect.DeepEqual(beforeChange, update) {
			answer += update[(len(update)-1)/2]
		}
	}

	fmt.Println(answer)
}
