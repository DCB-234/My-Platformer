from game.block.block_type import BlockType
from game.block.block_registry import BLOCK_DEFINITIONS
from game.block.block import Block
from game.world.block_context import BlockContext
from game.world.chunks.chunk import Chunk
from game.world.chunks.chunk_manager import ChunkManager
from game.entity.entity_manager import EntityManager
import pygame
import random

class World():
    def __init__(self, world_seed):
        self.MAX_WORLD_HEIGHT =  256
        self.MIN_WORLD_HEIGHT = -256
        self.chunk_manager = ChunkManager(self, world_seed)
        self.entity_manager = EntityManager(self)

    def get_chunk(self, chunk_pos) -> Chunk | None:
        return self.chunk_manager.get_chunk(chunk_pos)

    def get_block(self, block_pos: tuple) -> Block:
        chunk = self.get_chunk(self.world_to_chunk_pos(block_pos))
        if chunk is None:
            return None
        chunk_coord = self.world_to_local_chunk_coord(block_pos)
        return chunk.get_block(chunk_coord)

    def world_to_local_chunk_coord(self, world_coord) -> tuple:
        x, y = world_coord
        return (
            x % 16,
            y % 16
        )

    def world_to_chunk_pos(self, world_coord) -> tuple:
        x, y = world_coord
        return(
            x // 16,
            y // 16
        )

    def insert_block(self, block_type: BlockType, pos: tuple) -> None:
        chunk = self.get_chunk(self.world_to_chunk_pos(pos))
        relative_coord = self.world_to_local_chunk_coord(pos)
        chunk.insert_block(block_type, relative_coord)

    def break_block(self, pos: tuple) -> None:
        chunk = self.get_chunk(self.world_to_chunk_pos(pos))
        relative_coord = self.world_to_local_chunk_coord(pos)
        chunk.break_block(relative_coord)

    def construct_block_context(self, block_pos: tuple) -> BlockContext:
        x, y = block_pos
        return BlockContext(world = self, x = x, y = y)

    def tick_random(self) -> None:
        for chunk_pos, chunk in self.chunk_manager.chunks.items():
            rand_x = random.randrange(16)
            rand_y = random.randrange(16)
            rand_coord = (rand_x, rand_y)

            chunk_x, chunk_y = chunk_pos
            world_pos = (
                chunk_x * 16 + rand_x,
                chunk_y * 16 + rand_y
            )

            block_context = self.construct_block_context(world_pos)
            chunk.block_tick_random(rand_coord, block_context)

    def get_coord_from_click(self, mouse_world) -> tuple:
        mouse_x, mouse_y = mouse_world
        return (mouse_x // 32, mouse_y // 32)

    def is_valid_block_placement(self, coord: tuple, player_rect) -> bool:

        # Check if spot is already occupied by block
        ix, iy = coord
        block = self.get_block(coord)
        if block.definition.is_solid_cube:
            return False

        # Check if colliding with player
        block_rect = pygame.Rect(ix*32,iy*32,32,32)
        if block_rect.colliderect(player_rect):
            return False

        # Check if floating
        surrounding_blocks = [(ix+dx, iy+dy) for dx, dy in
            [(1,0),(0,1),(-1,0),(0,-1)]
        ]

        if not any(
            self.get_block(block_coord).definition.is_solid_cube
            for block_coord in surrounding_blocks
        ):
            return False

        return True

    def is_colliding(self, rect_obj) -> bool:
        collisions = self.get_collisions(rect_obj)
        if collisions:
            return True
        return False

    def get_collisions(self, rect_obj) -> list:
        collisions = []

        left = rect_obj.left // 32
        right = (rect_obj.right - 1) // 32
        top = rect_obj.top // 32
        bottom = (rect_obj.bottom - 1) // 32

        for iy in range(top, bottom + 1):
            for ix in range(left, right + 1):
                block = self.get_block((ix, iy))

                if not block or not block.definition.is_solid_cube:
                    continue

                block_rect = pygame.Rect(ix * 32, iy * 32, 32, 32)
                collisions.append(block_rect)

        return collisions