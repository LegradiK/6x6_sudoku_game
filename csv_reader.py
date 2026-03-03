import random
import csv

def parse_line(line):
    board_str, solution_str = line.strip().split("\t")

    board = [int(char) for char in board_str]
    solution = [int(char) for char in solution_str]

    return board, solution

def to_grid(lst, size=4):
    grid = []
    for i in range(0, len(lst), size):
        row = lst[i:i+size]
        grid.append(row)
    return grid

def load_random_puzzle():

    with open("4x4-Sudoku-Dataset-master/4x4_sudoku_unique_solution.csv") as sudoku_file:
        board_solution_pairs = []
        next(sudoku_file)  # skip header

        for line in sudoku_file:
            board, solution = parse_line(line)
            board_grid = to_grid(board)
            solution_grid = to_grid(solution)

            board_solution_pairs.append((board_grid, solution_grid))

    random_item_num = random.randint(2, 289)

    random_item = board_solution_pairs[random_item_num]
    quiz = random_item[0]
    answer = random_item[1]

    return quiz, answer
