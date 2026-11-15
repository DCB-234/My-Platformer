from dataclasses import dataclass
from game.block.block import Block
from itertools import product
import pygame

class BlockContext:
    def __init__(self, world, x: int, y: int, block_item_conversion):
        self.world = world
        self.world_pos = pygame.Vector2(x,y)
        self.block_item_conversion = block_item_conversion

    def get(self, dx: int, dy: int) -> Block:
        return self.world.get_block((self.world_pos.x + dx, self.world_pos.y + dy))

    @property
    def left(self) -> Block:
        return self.world.get_block((self.world_pos.x - 1, self.world_pos.y))

    @property
    def right(self) -> Block:
        return self.world.get_block((self.world_pos.x + 1, self.world_pos.y))

    @property
    def above(self) -> Block:
        return self.world.get_block((self.world_pos.x, self.world_pos.y - 1))

    @property
    def bottom(self) -> Block:
        return self.world.get_block((self.world_pos.x, self.world_pos.y + 1))

    def get_surroundings(self) -> list[Block]:
        return [
            self.get(dx, dy)
            for dx, dy in product((-1, 0, 1), repeat=2)
            if not (dx == 0 and dy == 0)
        ]

    def world_to_pixel_coord(self, world_coord: pygame.Vector2) -> pygame.Vector2:
        return pygame.Vector2(
            world_coord.x * 32,
            world_coord.y * 32
        )