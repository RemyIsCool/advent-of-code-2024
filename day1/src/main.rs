use std::fs::read_to_string;

fn main() {
    let mut left_column: Vec<i32> = vec![];
    let mut right_column: Vec<i32> = vec![];

    for line in read_to_string("input.txt").unwrap().lines() {
        for (i, str) in line.split(" ").filter(|n| !n.is_empty()).enumerate() {
            let number = str.parse::<i32>().unwrap();

            if i == 0 {
                left_column.push(number);
            } else {
                right_column.push(number);
            }
        }
    }

    left_column.sort();
    right_column.sort();

    let mut score: i32 = 0;

    for num in left_column {
        score += num
            * right_column
                .clone()
                .into_iter()
                .filter(|&n| n == num)
                .count() as i32;
    }

    println!("{}", score);
}
