const fs = require("node:fs");

const input = fs.readFileSync("./input.txt", "utf8");

const lines = input.trim().split("\n");

function checkNumbers(numbers) {
  let previous = numbers[0];
  let increasing = false;

  let hasIssue = false;

  numbers.forEach((number, i) => {
    if (i === 0) {
      return;
    }

    if (i === 1) {
      increasing = previous < number;
    }

    if (
      (increasing && previous >= number) ||
      (!increasing && previous <= number) ||
      Math.abs(previous - number) > 3
    ) {
      hasIssue = true;
    }

    previous = number;
  });

  return !hasIssue;
}

let sum = 0;

for (const line of lines) {
  const numbers = line
    .trim()
    .split(" ")
    .map((n) => parseInt(n));

  if (checkNumbers(numbers)) {
    sum++;
  } else {
    if (
      numbers
        .map((_, i) => checkNumbers(numbers.toSpliced(i, 1)))
        .some((b) => b)
    ) {
      sum++;
    }
  }
}

console.log(sum);
