#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
  FILE *input = fopen("input.txt", "r");

  char line[100];

  int safeCount = 0;

  while (fgets(line, sizeof(line), input)) {
    char *numberToken = strtok(line, " ");

    int previous = -1;

    int increasing = -1;

    int safe = 1;

    while (numberToken != NULL) {
      if (!strcmp(numberToken, "\n")) {
        break;
      }

      int number = atoi(numberToken);

      if (previous == -1) {
        previous = number;

        numberToken = strtok(NULL, " ");
        continue;
      }

      if (increasing == -1) {
        if (number < previous) {
          increasing = 0;
        } else {
          increasing = 1;
        }
      }
      if ((increasing && previous >= number) ||
          ((!increasing) && previous <= number) ||
          (abs(previous - number) > 3)) {
        safe = 0;
      }

      previous = number;

      numberToken = strtok(NULL, " ");
    }

    if (safe) {
      safeCount++;
    }
  }
  printf("%i\n", safeCount);
}
