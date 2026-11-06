import pygame
import pathlib
from game.container.container_type import ContainerType

class GuiRenderer:
    def __init__(self, item_renderer):
        self.item_renderer = item_renderer

        BASE_DIR = pathlib.Path(__file__).parents[1]
        GUI_DIR = BASE_DIR / 'assets' / 'textures' / 'gui'

        # Define container textures
        CONTAINER_DIR = GUI_DIR / 'container'

        self.CONTAINER_TEXTURES = {
            ContainerType.CRAFTING_TABLE: (
                pygame.image.load(CONTAINER_DIR/'crafting_table.png').convert_alpha().subsurface(pygame.Rect(0,0,16*11,16*10+6))
            ),
            ContainerType.INVENTORY: (
                pygame.image.load(CONTAINER_DIR/'inventory.png').convert_alpha().subsurface(pygame.Rect(0,0,16*11,16*10+6))
            ),
            ContainerType.DOUBLE_CHEST: (
                pygame.image.load(CONTAINER_DIR/'double_chest.png').convert_alpha().subsurface(pygame.Rect(0,0,16*11,16*13+14))
            )
        }

        GUI_PNG = pygame.image.load(GUI_DIR/'gui.png').convert_alpha()
        self.HOTBAR_PNG = GUI_PNG.subsurface(pygame.Rect(0,0,180,20))
        self.HIGHLIGHTED_SLOT_PNG = GUI_PNG.subsurface(pygame.Rect(0,22,24,22))

    def draw_container(self, screen, container) -> None:
        container_type = container.container_type
        container_texture = self.CONTAINER_TEXTURES[container_type]

        center = (screen.get_width() // 2, screen.get_height() // 2)
        container_rect = container_texture.get_rect()
        container_rect.center = center

        screen.blit(container_texture, container_rect)

        # draw items in container
        for i, slot in enumerate(container.slots):
            item_pos = (
                container_rect.left+((i%9)*18+8),
                container_rect.bottom+((i//9)*-18-24) if i//9==0 else
                container_rect.bottom+((i//9)*-18-28)
            )
            self.item_renderer.render_item_in_container(screen, slot, item_pos)

    def draw_hotbar(self, screen, player) -> None:
        container = player.inventory
    
        # draw hotbar
        hotbar_rect = self.HOTBAR_PNG.get_rect()
        hotbar_rect.midbottom = (screen.get_width() // 2, screen.get_height())
        screen.blit(self.HOTBAR_PNG, hotbar_rect)

        highlighted_slot_rect = self.HIGHLIGHTED_SLOT_PNG.get_rect()
        highlighted_slot_rect.bottomleft = (
            ((player.current_hotbar_slot) * 20 - 2) + hotbar_rect.left,
            hotbar_rect.bottom
        )
        screen.blit(self.HIGHLIGHTED_SLOT_PNG, highlighted_slot_rect)

        # draw items in hotbar
        for i, slot in enumerate(container.slots[:9]):
            if slot is None:
                continue

            self.item_renderer.render_item_in_container(
                screen,
                slot,
                (i*20+2+hotbar_rect.left, hotbar_rect.top+2)
            )