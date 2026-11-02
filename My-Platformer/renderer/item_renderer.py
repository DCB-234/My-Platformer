import pygame
import pathlib
from game.item.item_type import ItemType

class ItemRenderer:
    def __init__(self):
        BASE_DIR = pathlib.Path(__file__).parents[1]
        BLOCK_DIR = BASE_DIR / 'assets' / 'textures' / 'blocks'
        ITEM_DIR = BASE_DIR / 'assets' / 'textures' / 'items'
        ITEM_SCALE = (16,16)

        # Define item textures
        self.ITEM_TEXTURE = {
            ItemType.BEDROCK: (
                pygame.image.load(BLOCK_DIR/'bedrock.png').convert_alpha()
            ),
            ItemType.COAL: (
                pygame.image.load(ITEM_DIR/'coal.png').convert_alpha()
            ),
            ItemType.COAL_ORE: (
                pygame.image.load(BLOCK_DIR/'coal_ore.png').convert_alpha()
            ),
            ItemType.COBBLESTONE: (
                pygame.image.load(BLOCK_DIR/'cobblestone.png').convert_alpha()
            ),
            ItemType.DIRT: (
                pygame.image.load(BLOCK_DIR/'dirt.png').convert_alpha()
            ),
            ItemType.GLASS: (
                pygame.image.load(BLOCK_DIR/'glass.png').convert_alpha()
            ),
            ItemType.GRASS: (
                pygame.image.load(BLOCK_DIR/'grass.png').convert_alpha()
            ),
            ItemType.IRON_INGOT: (
                pygame.image.load(ITEM_DIR/'iron_ingot.png').convert_alpha()
            ),
            ItemType.IRON_ORE: (
                pygame.image.load(BLOCK_DIR/'iron_ore.png').convert_alpha()
            ),
            ItemType.LEAVES_OAK: (
                pygame.image.load(BLOCK_DIR/'leaves_oak.png').convert_alpha()
            ),
            ItemType.LOG_OAK: (
                pygame.image.load(BLOCK_DIR/'log_oak.png').convert_alpha()
            ),
            ItemType.PLANKS_OAK: (
                pygame.image.load(BLOCK_DIR/'planks_oak.png').convert_alpha()
            ),
            ItemType.RAW_IRON: (
                pygame.image.load(ITEM_DIR/'raw_iron.png').convert_alpha()
            ),
            ItemType.STICK: (
                pygame.image.load(ITEM_DIR/'stick.png').convert_alpha()
            ),
            ItemType.STONE: (
                pygame.image.load(BLOCK_DIR/'stone.png').convert_alpha()
            )
        }

        # Resize each item
        for item, texture in self.ITEM_TEXTURE.items():
            self.ITEM_TEXTURE[item] = (
                pygame.transform.scale(texture, ITEM_SCALE)
            )

        # Text font
        FONT_DIR = BASE_DIR / 'assets' / 'fonts' / 'mojangles.otf'
        self.DEFAULT_FONT = pygame.font.Font(FONT_DIR, 10)

    def render_item_in_container(self, screen, item_stack, topleft: tuple) -> None:
        if item_stack is None:
            return

        # Draw item
        screen.blit(self.ITEM_TEXTURE[item_stack.item_type], topleft)

        # Draw number
        if item_stack.stack_size > 1:
            x, y = topleft
            text = self.DEFAULT_FONT.render(str(item_stack.stack_size), True, 'White')
            text_rect = text.get_rect()
            text_rect.bottomright = (x + 18, y + 18)
            screen.blit(text, text_rect)

    def render_item_in_world(self) -> None:
        ...