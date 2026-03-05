import pygame
import sys

WHITE = (255, 255, 255)
BLUE = (70, 130, 180)
DARK_BLUE = (40, 90, 140)
HIGHLIGHT = (30, 60, 110)  # darker shade for selected difficulty
BLACK = (0, 0, 0)

class Button:
    def __init__(self, text, x, y, width, height, font_size=36):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = pygame.font.SysFont(None, font_size)
    
    def draw(self, surface, mouse_position, highlighted=False):
        if highlighted:
            color = HIGHLIGHT
        elif self.rect.collidepoint(mouse_position):
            color = DARK_BLUE
        else:
            color = BLUE
        pygame.draw.rect(surface, color, self.rect, border_radius=0)
    
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    def is_clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)