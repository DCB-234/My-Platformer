import pygame
import pathlib
from game.item.item_type import ItemType

class ItemRenderer:
    def __init__(self):
        BASE_DIR = pathlib.Path(__file__).parents[1]

        # Text font
        FONT_DIR = BASE_DIR / 'assets' / 'fonts' / 'mojangles.otf'
        self.DEFAULT_FONT = pygame.font.Font(FONT_DIR, 10)

    def render_item_in_container(self, screen, item_stack, topleft: tuple, asset_manager) -> None:
        if item_stack is None:
            return

        # Draw item
        item_surface = asset_manager.get_item(item_stack.item_type)
        item_rect = item_surface.get_rect()
        item_rect.topleft = topleft
        screen.blit(item_surface, item_rect)

        # Draw number
        if item_stack.stack_size > 1:
            x, y = topleft
            text = self.DEFAULT_FONT.render(str(item_stack.stack_size), True, 'White')
            text_rect = text.get_rect()
            text_rect.bottomright = (x + 18, y + 18)
            screen.blit(text, text_rect)
