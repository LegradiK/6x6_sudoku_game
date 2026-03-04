import pygame


class GameState:
    def __init__(self, grid, original_grid, cell_size, font_big, font_medium, font_small):
        self.grid = grid
        self.original_grid = original_grid
        self.solution = None
        self.cell_size = cell_size
        self.font_big = font_big
        self.font_medium = font_medium
        self.font_small = font_small
        self.selected_row = 0
        self.selected_col = 0
        self.wrong_cells = set()


def draw_background(screen):
    screen.fill((255, 255, 255))


def draw_grid_lines(screen, state):
    dif = state.cell_size

    for i in range(7):
        thickness = 4 if i % 3 == 0 else 1

        # Horizontal lines
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (0, i * dif),
            (dif * 4, i * dif),
            thickness
        )

        # Vertical lines
        pygame.draw.line(
            screen,
            (0, 0, 0),
            (i * dif, 0),
            (i * dif, dif * 4),
            thickness
        )


def draw_numbers(screen, state):
    dif = state.cell_size

    for row in range(6):
        for col in range(6):
            value = state.grid[row][col]

            if value != 0:
                # background color for original fixed cells
                if state.original_grid[row][col] != 0:
                    pygame.draw.rect(
                        screen,
                        (221, 221, 231),
                        (col * dif, row * dif, dif, dif)
                    )
                # background color if user entry is wrong
                if (row, col) in state.wrong_cells:
                    color = (255, 0, 0)
                else:
                    color = (0, 0, 0)

                text = state.font_big.render(str(value), True, color)
                text_rect = text.get_rect(center=(
                    col * dif + dif / 2,
                    row * dif + dif / 2
                ))

                screen.blit(text, text_rect)


def draw_selection(screen, state):
    dif = state.cell_size
    row = state.selected_row
    col = state.selected_col

    pygame.draw.rect(
        screen,
        (255, 222, 33),
        (col * dif, row * dif, dif, dif),
        4
    )


def draw_instructions(screen, font, height):
    text1 = font.render(
        "Arrow Keys: Move",
        True,
        (0, 0, 0)
    )
    text2 = font.render(
        "1-6: Input",
        True,
        (0, 0, 0)
    )
    text3 = font.render(
        "Backspace, Delete, e, d: Erase input",
        True,
        (0, 0, 0)
    )
    text4 = font.render(
        "ENTER: Submit your answer",
        True,
        (0, 0, 0)
    )   
    text5 = font.render(
        "New Game / Restart: Press buttons",
        True,
        (0, 0, 0)
    )

    screen.blit(text1, (20, height - 120))
    screen.blit(text2, (20, height - 100))
    screen.blit(text3, (20, height - 80))
    screen.blit(text4, (20, height - 60))
    screen.blit(text5, (20, height - 40))


def draw_result(screen, font, height):
    text = font.render("PUZZLE SOLVED!", True, (0,150, 0))
    screen.blit(text, (20, height - 90))

def draw_warning(screen, font, height):
    text = font.render("Wrong answers", True, (200, 0, 0))
    screen.blit(text, (20, height - 90))

def draw_fill_warning(screen, font, height):
    text = font.render("Fill all cells", True, (255, 191, 0))
    screen.blit(text, (20, height - 90))