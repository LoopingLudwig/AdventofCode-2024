use std::fs::File;
use std::io::{BufRead, BufReader, Read};

use itertools::Itertools;

const INPATH: &str = "../input.txt";

fn open_file() -> BufReader<File> {
    let infile = match File::open(INPATH) {
        Ok(file) => file,
        Err(error) => panic!(
            "Problem beim Öffnen der Eingabedatei >{}< {:?}",
            INPATH, error
        ),
    };

    BufReader::new(infile)
}

fn parse_file<R: Sized + Read>(buf: &mut BufReader<R>) -> (Vec<i32>, Vec<i32>) {
    buf.lines()
        .map(|line| {
            line.unwrap()
                .split_whitespace()
                .map(|x| x.parse::<i32>().unwrap())
                .collect_tuple()
                .unwrap()
        })
        .unzip()
}

fn calc_1(left: &Vec<i32>, right: &Vec<i32>) -> i32 {
    let mut left_s = left.to_vec();
    let mut right_s = right.to_vec();

    left_s.sort();
    right_s.sort();
    left_s
        .into_iter()
        .zip(right_s.into_iter())
        .map(|(x, y)| (x - y).abs())
        .sum()
}

fn calc_2(left: &Vec<i32>, right: &Vec<i32>) -> i32 {
    let right_counts = right.into_iter().counts();

    left.into_iter()
        .map(|x| x * i32::try_from(*right_counts.get(x).unwrap_or(&0)).unwrap())
        .sum()
}

fn main() {
    let mut buffer = open_file();

    let (left, right) = parse_file(&mut buffer);

    let res_1 = calc_1(&left, &right);
    println!("Result part one: {}", res_1);

    let res_2 = calc_2(&left, &right);
    println!("Result part two: {}", res_2);
}
