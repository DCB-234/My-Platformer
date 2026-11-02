from game.block.block import Block
from game.block.block_type import BlockType
import random
import pygame

# Make chunks own its entities

class Chunk:
    CHUNK_SIZE = 16

    def __init__(self, chunk_pos, world_seed, terrain_generator, cave_generator):
        self.chunk_pos: tuple = chunk_pos
        self.is_modified: bool = False
        self.entities: list = []

        self.blocks: list = [
            [Block(BlockType.AIR) for _ in range(self.CHUNK_SIZE)]
            for _ in range(self.CHUNK_SIZE)
        ]

        self.generate_chunk(world_seed, terrain_generator, cave_generator)

    def generate_chunk(self, world_seed, terrain_generator, cave_generator) -> None:
        chunk_x, chunk_y = self.chunk_pos

        chunk_start_x = chunk_x * self.CHUNK_SIZE
        chunk_start_y = chunk_y * self.CHUNK_SIZE
        chunk_end_y = chunk_start_y + self.CHUNK_SIZE

        height_values = [
            terrain_generator.get_terrain_height(chunk_start_x+local_x)
            for local_x in range(self.CHUNK_SIZE)
        ]

        # if chunk_start_y < min(height_values):
        #     return

        caves = cave_generator.generate_cave_chunk(chunk_x, chunk_y)

        # Generate chunk based on height map
        for local_x in range(self.CHUNK_SIZE):
            surface_y = height_values[local_x]

            for local_y in range(self.CHUNK_SIZE):
                world_y = chunk_start_y + local_y

                if world_y < surface_y:
                    continue

                if caves[local_y][local_x]:
                    self.blocks[local_y][local_x] = Block(BlockType.AIR)
                    continue

                if world_y <= surface_y + 3:
                    self.blocks[local_y][local_x] = Block(BlockType.GRASS)
                else:
                    self.blocks[local_y][local_x] = Block(BlockType.STONE)

    def block_tick_random(self, coord, context) -> None:
        block = self.get_block(coord)
        block.tick_random(context)

    def insert_block(self, block_type: BlockType, pos: tuple) -> None:
        ix, iy = pos
        self.blocks[iy][ix] = Block(block_type)
        self.is_modified = True

    def get_block(self, pos: tuple) -> Block:
        ix, iy = pos
        if 0 <= ix < self.CHUNK_SIZE and 0 <= iy < self.CHUNK_SIZE:
            return self.blocks[iy][ix]

    def break_block(self, pos) -> None:
        ix, iy = pos
        self.blocks[iy][ix] = Block(BlockType.AIR)
        self.is_modified = True
