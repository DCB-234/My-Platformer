from game.world.chunks.chunk import Chunk
from game.random.perlin_noise import PerlinNoise
from game.random.cave_generator import CaveGenerator
from typing import Set
import random

class ChunkManager:
    def __init__(self, world, world_seed):
        self.chunks: dict = {}
        self.dirty_chunks: dict = {}
        self.cached_chunks: dict = {}

        self.world = world
        self.world_seed: int = world_seed
        self.terrain_generator = PerlinNoise(self.world_seed)
        self.cave_generator = CaveGenerator(self.world_seed, self.terrain_generator)

    def update_chunks(self, player_chunk, render_distance) -> None:
        chunk_x, chunk_y = player_chunk

        needed_chunks = {
            (x, y)
            for x in range(chunk_x - render_distance, chunk_x + render_distance + 1)
            for y in range(chunk_y - render_distance, chunk_y + render_distance + 1)
        }
        current_chunks = set(self.chunks.keys())

        chunks_to_load = needed_chunks - current_chunks
        chunks_to_unload = current_chunks - needed_chunks

        for pos in chunks_to_load:
            self.load_chunk(pos)

        if chunks_to_unload:
            self.unload_chunks(chunks_to_unload)

    def unload_chunks(self, chunk_list: Set) -> None:
        for chunk_pos in chunk_list:
            chunk = self.chunks.pop(chunk_pos, None)
            if chunk is None:
                continue

            if chunk.is_modified:
                self.dirty_chunks[chunk_pos] = chunk
            else:
                self.cached_chunks[chunk_pos] = chunk

    def load_chunk(self, chunk_pos: tuple) -> None:

        if chunk_pos in self.cached_chunks:
            chunk = self.cached_chunks.pop(chunk_pos)
        elif chunk_pos in self.dirty_chunks:
            chunk = self.dirty_chunks.pop(chunk_pos)
        else:
            chunk = Chunk(chunk_pos, self.world_seed, self.terrain_generator, self.cave_generator)
        self.chunks[chunk_pos] = chunk

    def get_chunk(self, chunk_pos: tuple) -> Chunk:
        return self.chunks.get(chunk_pos)

    def chunk_to_world_coord(self, chunk_coord: tuple) -> tuple:
        x, y = chunk_coord
        return (
            x * 16,
            y * 16
        )

    def tick(self, world, game_rules) -> None:
        for chunk in self.chunks.values():
            chunk.tick(world, game_rules)

    def transfer_entity(self, entity) -> None:
        new_chunk_pos = self.world.world_to_chunk_pos(entity.position.pos)

        chunk = self.chunks[new_chunk_pos]

        if chunk is None:
            return

        chunk.entities.append(entity)

    def spawn_entity(self, entity) -> None:
        self.transfer_entity(entity)