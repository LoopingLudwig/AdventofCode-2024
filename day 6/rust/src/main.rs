use std::fs::File;
use std::io::{BufRead, BufReader, Read};

const INPATH: &str = "../input/input.txt";

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

#[derive(Clone, PartialEq)]
enum Field {
    Untouched,
    Walked,
    Obstacle,
}
impl From<char> for Field {
    fn from(item: char) -> Self {
        match item {
            'X' | '^' => Self::Walked,
            '#' => Self::Obstacle,
            '.' | _ => Self::Untouched,
        }
    }
}

enum Direction {
    North,
    East,
    South,
    West,
}
impl Direction {
    fn turn_right(&self) -> Self {
        match self {
            Self::North => Self::East,
            Self::East => Self::South,
            Self::South => Self::West,
            Self::West => Self::North,
        }
    }
}

enum GuardPath {
    Looped,
    Ended(usize),
}

#[derive(PartialEq, Clone)]
struct Position {
    row: usize,
    column: usize,
}
impl Position {
    fn next_in_dir(&self, dir: &Direction) -> Option<Self> {
        match dir {
            Direction::North if self.row > 0 => Some(Position {
                row: self.row - 1,
                column: self.column,
            }),
            Direction::East => Some(Position {
                row: self.row,
                column: self.column + 1,
            }),
            Direction::South => Some(Position {
                row: self.row + 1,
                column: self.column,
            }),
            Direction::West if self.column > 0 => Some(Position {
                row: self.row,
                column: self.column - 1,
            }),
            _ => None,
        }
    }
    fn in_bound(&self, row_max: usize, column_max: usize) -> bool {
        self.row <= row_max && self.column <= column_max
    }
}

fn parse_file<R: Sized + Read>(buf: &mut BufReader<R>) -> (Vec<Vec<Field>>, Position) {
    let mut rows: Vec<Vec<Field>> = Vec::new();
    let mut start_pos = Position { row: 0, column: 0 };

    for (i, line) in buf.lines().flatten().enumerate() {
        //Startposition finden
        if let Some(col) = line.find('^') {
            start_pos = Position {
                row: i,
                column: col,
            };
        }
        rows.push(line.chars().map(Field::from).collect());
    }

    (rows, start_pos)
}

fn walk_guard(map_in: &Vec<Vec<Field>>, start_pos: &Position) -> GuardPath {
    let mut map = map_in.to_vec();

    let bounds = (map.len() - 1, map[0].len() - 1);

    let mut walk_dir = Direction::North;
    let mut cur_pos = start_pos.clone();
    let mut turns_on_walked_path = 0;

    loop {
        //In den Grenzen
        match cur_pos.next_in_dir(&walk_dir) {
            // Wäre mit if-let-chains schöner, aber noch nicht stabil
            Some(next_pos) if next_pos.in_bound(bounds.0, bounds.1) => {
                match map[next_pos.row][next_pos.column] {
                    Field::Obstacle => {
                        walk_dir = walk_dir.turn_right();

                        // Für Teil 2 Endlospfade erkennen
                        turns_on_walked_path += 1;
                        if turns_on_walked_path > 4 {
                            break GuardPath::Looped;
                        }
                    }
                    Field::Untouched => {
                        map[next_pos.row][next_pos.column] = Field::Walked;
                        cur_pos = next_pos;

                        turns_on_walked_path = 0;
                    }
                    Field::Walked => cur_pos = next_pos,
                }
            }

            // Grenze erreicht
            _ => {
                let walked_fields = map
                    .iter()
                    .map(|row| row.iter())
                    .flatten()
                    .filter(|field| Field::Walked == **field)
                    .count();
                break GuardPath::Ended(walked_fields);
            }
        }
    }
}

fn calc_2(map_in: &Vec<Vec<Field>>, start_pos: &Position) -> usize {
    let mut map = map_in.to_vec();
    let mut possible_obsacles = 0;

    for row in 0..map.len() {
        for column in 0..map[0].len() {
            let cur_pos = Position {
                row: row,
                column: column,
            };
            if cur_pos == *start_pos {
                continue;
            }

            //Hindernis termporär plazieren
            let orig_field = map[row][column].clone();
            map[row][column] = Field::Obstacle;

            if let GuardPath::Looped = walk_guard(&map, &start_pos) {
                possible_obsacles += 1;
            }
            map[row][column] = orig_field;
        }
    }
    possible_obsacles
}

fn main() {
    let mut buffer = open_file();

    let (map, start_pos) = parse_file(&mut buffer);

    let res_1 = walk_guard(&map, &start_pos);
    if let GuardPath::Ended(field_count) = res_1 {
        println!("Result part one: {:}", field_count);
    }
    //
    let res_2 = calc_2(&map, &start_pos);
    println!("Result part two: {}", res_2);
}
