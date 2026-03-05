import pygame
import requests
from button import Button
from ui import (
    GameState,
    draw_background,
    draw_grid_lines,
    draw_numbers,
    draw_selection,
    draw_instructions,
    draw_result,
    draw_warning,
    draw_fill_warning
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 940
GRID_SIZE = 6

pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("6x6 Sudoku")

font_big = pygame.font.SysFont("comicsans", 120)
font_medium = pygame.font.SysFont("Arial", 40, bold=True)
font_small = pygame.font.SysFont("Arial", 18)

new_game_button = Button("New Game", 420, 845, 180, 60)
restart_button = Button("Restart", 610, 845, 180, 60)

cell_size = SCREEN_WIDTH // GRID_SIZE

def load_new_game(size=6, num_clues=16):
    # sudoku generating from Docker jotools/sudoku
    url = "http://localhost:8080/api/sudoku/generate"

    params = {
        "size": size,
        "numClues": num_clues,
        "format": "json",
        "addSolution": "true"
    }

    response = requests.get(url, params=params)
    data = response.json()

    puzzle_cells = data['sudoku']
    solution_cells = data['solution']

    size = 6

    puzzle_grid = [[0] * size for i in range(size)]
    solution_grid = [[0] * size for i in range(size)]
    locked_grid = [[False] * size for i in range(size)]

    for cell in puzzle_cells:
        row = cell['row'] - 1
        col = cell['col'] - 1
        puzzle_grid[row][col] = cell['value']
        locked_grid[row][col] = cell['locked']

    for cell in solution_cells:
        row = cell['row'] - 1
        col = cell['col'] - 1
        solution_grid[row][col] = cell['value'] 
    
    # print('Puzzle: ')
    # for row in puzzle_grid:
    #     print(row)

    # print('\nSolution: ')
    # for row in solution_grid:
    #     print(row)
    
    return puzzle_grid, solution_grid, locked_grid

quiz, solution, locked = load_new_game()
original_grid = [row[:] for row in quiz]


state = GameState(
    grid=quiz,
    original_grid=original_grid,
    cell_size=cell_size,
    font_big=font_big,
    font_medium=font_medium,
    font_small=font_small
)

state.solution = solution

is_solved = False
show_warning = False
show_fill_warning = False
running = True


def is_valid(state, row, col, val):
    if state.solution is None:
        return False
    elif val == state.solution[row][col]:
        return True


def find_empty(board):
    for r in range(GRID_SIZE):
        for c in range(GRID_SIZE):
            if board[r][c] == 0:
                return r, c
    return None


def solve(board):
    empty = find_empty(board)
    if not empty:
        return True

    row, col = empty

    for num in range(1, 7):
        if is_valid(board, row, col, num):
            board[row][col] = num

            if solve(board):
                return True

            board[row][col] = 0

    return False


   

def validate_against_solution(state):
    state.wrong_cells.clear()
    if state.solution is None:
        return
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            current = state.grid[row][col]
            correct = state.solution[row][col]
            if current == 0:
                continue
            if current != correct:
                state.wrong_cells.add((row, col))



while running:
    draw_background(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if new_game_button.is_clicked(event):
                quiz, solution, locked = load_new_game()
                state.grid = [row[:] for row in quiz]
                state.original_grid = [row[:] for row in quiz]
                state.solution = solution
                state.wrong_cells.clear()
                is_solved = False
                show_warning = False
                show_fill_warning = False

            elif restart_button.is_clicked(event):
                state.grid = [row[:] for row in state.original_grid]
                state.wrong_cells.clear()
                is_solved = False
                show_warning = False
                show_fill_warning = False

            else:
                x, y = event.pos
                if y < SCREEN_WIDTH:
                    state.selected_row = y // cell_size
                    state.selected_col = x // cell_size

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_LEFT:
                state.selected_col = max(0, state.selected_col - 1)

            if event.key == pygame.K_RIGHT:
                state.selected_col = min(3, state.selected_col + 1)

            if event.key == pygame.K_UP:
                state.selected_row = max(0, state.selected_row - 1)

            if event.key == pygame.K_DOWN:
                state.selected_row = min(3, state.selected_row + 1)

            if event.key in (
                pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4,pygame.K_5, pygame.K_6,
                pygame.K_KP1, pygame.K_KP2, pygame.K_KP3, pygame.K_KP4, pygame.K_KP5, pygame.K_KP6
            ):
                value = int(event.unicode)
                row = state.selected_row
                col = state.selected_col

                if state.original_grid[row][col] == 0 or state.solution[row][col] != state.grid[row][col]:
                    state.grid[row][col] = value
                    if state.solution and value == state.solution[row][col]:
                        state.wrong_cells.discard((row, col))
                    else:
                        state.wrong_cells.add((row, col))

            if event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                board_full = all(
                    state.grid[row][col] != 0
                     for row in range(GRID_SIZE)
                     for col in range(GRID_SIZE)
                )
                if not board_full:
                    show_fill_warning = True
                    is_solved = False
                    show_warning = False
                else: 
                    validate_against_solution(state)
                    if not state.wrong_cells:
                        is_solved = True
                        show_warning = False
                    else:
                        is_solved = False
                        show_warning = True

            if event.key in (
                pygame.K_BACKSPACE,
                pygame.K_DELETE,
                pygame.K_e,
                pygame.K_d
            ):
                row = state.selected_row
                col = state.selected_col

                # Only allow erasing user-entered cells
                if state.original_grid[row][col] == 0:
                    state.grid[row][col] = 0
                    state.wrong_cells.discard((row, col))

    # Draw everything
    draw_numbers(screen, state)
    draw_grid_lines(screen, state)
    draw_selection(screen, state)

    if is_solved:
        draw_result(screen, font_medium, SCREEN_HEIGHT)
    elif show_warning:
        draw_warning(screen, font_medium, SCREEN_HEIGHT)
    elif show_fill_warning:
        draw_fill_warning(screen, font_medium, SCREEN_HEIGHT)
    else:
        draw_instructions(screen, font_small, SCREEN_HEIGHT)

    mouse_pos = pygame.mouse.get_pos()
    new_game_button.draw(screen, mouse_pos)
    restart_button.draw(screen, mouse_pos)

    pygame.display.update()

pygame.quit()