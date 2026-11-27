import pygame
import pathlib
from game.block.block_type import BlockType
from game.container.container_type import ContainerType
from renderer.block_renderer import BlockRenderer
from renderer.gui_renderer import GuiRenderer
from renderer.item_renderer import ItemRenderer
from renderer.asset_manager import AssetManager
from game.item.item_type import ItemType

class GameRenderer:
    def __init__(self, screen, game, world, camera):
        BASE_DIR = pathlib.Path(__file__).parents[1]

        self.screen = screen
        self.game = game
        self.world = world
        self.fps = None

        self.camera = camera
        self.asset_manager = AssetManager()

        self.block_renderer = BlockRenderer()
        self.item_renderer = ItemRenderer()
        self.gui_renderer = GuiRenderer(self.item_renderer)

        FONT_DIR = BASE_DIR / 'assets' / 'fonts' / 'mojangles.otf'
        self.DEFAULT_FONT = pygame.font.Font(FONT_DIR, 20)

        # Load images
        CURSOR_PATH = BASE_DIR / 'assets' / 'textures' / 'cross_cursor.png'
        cursor_png = pygame.image.load(CURSOR_PATH).convert_alpha()
        self.cursor_png = pygame.transform.scale(cursor_png, (30,30))

        pygame.mouse.set_visible(False)

    def draw(self, dt) -> None:
        player = self.game.player

        self.camera.update(player, self.screen, dt)

        screen_width = self.screen.get_width()

        self.screen.fill((178, 200, 247))

        # Draw blocks
        for chunk_pos, chunk in self.world.chunk_manager.chunks.items():
            self.draw_chunk_blocks(chunk_pos, chunk)

        # Draw entities
        for chunk in self.world.chunk_manager.chunks.values():
            self.draw_chunk_entities(chunk)

        # Container or hotbar
        if self.game.opened_container:
            self.gui_renderer.draw_container(self.screen, self.game.opened_container, self.asset_manager)
        else:
            self.gui_renderer.draw_hotbar(self.screen, player, self.asset_manager)

        # FPS text
        fps_text = self.DEFAULT_FONT.render(f'FPS {self.fps}', True, 'White')
        self.screen.blit(fps_text, (screen_width-80, 5))

        # Player coordinates
        text_player_x = self.DEFAULT_FONT.render(f'X {int(player.position.pos.x // 32)}', True, 'White')
        text_player_y = self.DEFAULT_FONT.render(f'Y {int(player.position.pos.y // 32)}', True, 'White')
        self.screen.blit(text_player_x, (10, 10))
        self.screen.blit(text_player_y, (10, 30))

        # Mouse cursor
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.screen.blit(
            self.cursor_png, (
                mouse_x - self.cursor_png.get_width() // 2,
                mouse_y - self.cursor_png.get_height() // 2
            )
        )

    def draw_chunk_blocks(self, chunk_pos: tuple, chunk) -> None:

        # Draw blocks
        chunk_x, chunk_y = tuple(num * 16 * 32 for num in chunk_pos)
        for iy, row in enumerate(chunk.blocks):
            for ix, block in enumerate(row):
                block = chunk.get_block((ix, iy))
                if block.block_type == BlockType.AIR:
                    continue

                self.block_renderer.draw_block(
                    self.screen,
                    block.block_type,
                    (
                        (ix * 32 + chunk_x) - self.camera.pos.x,
                        (iy * 32 + chunk_y) - self.camera.pos.y
                    ),
                    self.asset_manager
                )

    def draw_chunk_entities(self, chunk) -> None:
        for entity in chunk.get_entities():
            entity.draw(self.screen, self.camera.world_to_screen(entity.position.interp), self.asset_manager)

    def render_entity_item(self, midbottom: tuple, item_type: ItemType) -> None:
        self.item_renderer.render_entity_item(self.screen, midbottom, item_type, self.asset_manager)