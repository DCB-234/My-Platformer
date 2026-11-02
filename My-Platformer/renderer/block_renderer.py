from game.block.block_type import BlockType
import pygame
import pathlib

class BlockRenderer:
    def __init__(self):
        BASE_DIR = pathlib.Path(__file__).parents[1]
        BLOCK_DIR = BASE_DIR / 'assets' / 'textures' / 'blocks'
        BLOCK_SCALE = (32, 32)

        # Define block textures
        self.BLOCK_TEXTURE = {
            BlockType.BEDROCK: (
                pygame.image.load(BLOCK_DIR/'bedrock.png').convert_alpha()
            ),
            BlockType.COAL_ORE: (
                pygame.image.load(BLOCK_DIR/'coal_ore.png').convert_alpha()
            ),
            BlockType.COBBLESTONE: (
                pygame.image.load(BLOCK_DIR/'cobblestone.png').convert_alpha()
            ),
            BlockType.DIRT: (
                pygame.image.load(BLOCK_DIR/'dirt.png').convert_alpha()
            ),
            BlockType.GLASS: (
                pygame.image.load(BLOCK_DIR/'glass.png').convert_alpha()
            ),
            BlockType.GRASS: (
                pygame.image.load(BLOCK_DIR/'grass.png').convert_alpha()
            ),
            BlockType.IRON_ORE: (
                pygame.image.load(BLOCK_DIR/'iron_ore.png').convert_alpha()
            ),
            BlockType.LEAVES_OAK: (
                pygame.image.load(BLOCK_DIR/'leaves_oak.png').convert_alpha()
            ),
            BlockType.LOG_OAK: (
                pygame.image.load(BLOCK_DIR/'log_oak.png').convert_alpha()
            ),
            BlockType.PLANKS_OAK: (
                pygame.image.load(BLOCK_DIR/'planks_oak.png').convert_alpha()
            ),
            BlockType.STONE: (
                pygame.image.load(BLOCK_DIR/'stone.png').convert_alpha()
            )
        }

        # Resize each block
        for block, texture in self.BLOCK_TEXTURE.items():
            self.BLOCK_TEXTURE[block] = (
                pygame.transform.scale(texture, BLOCK_SCALE)
            )

    def draw_block(self, screen, block_type: BlockType, topleft) -> None:
        screen.blit(self.BLOCK_TEXTURE[block_type], topleft)