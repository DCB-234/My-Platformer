from game.block.block_type import BlockType
import pygame

class BlockRenderer:
    def __init__(self):
        ...

    def draw_block(self, screen, block_type: BlockType, topleft, asset_manager) -> None:
        block_surface = asset_manager.get_block(block_type)
        block_rect = block_surface.get_rect()
        block_rect.topleft = topleft
        screen.blit(block_surface, block_rect)