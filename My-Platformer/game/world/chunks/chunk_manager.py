from game.world.chunks.chunk import Chunk
from game.random.perlin_noise import PerlinNoise
from game.random.cave_generator import CaveGenerator
from typing import Set
import pygame
import math

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

    def get_chunk(self, chunk_pos: tuple) -> Chunk | None:
        return self.chunks.get(chunk_pos, None)

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
        new_chunk_pos = self.world.world_to_chunk_pos(entity.position.world_pos)

        chunk = self.get_chunk(new_chunk_pos)

        if chunk is None:
            return

        chunk.entities.append(entity)

    def spawn_entity(self, entity) -> None:
        if entity is None:
            return

        self.transfer_entity(entity)

    def interpolate_entities(self, partial_tick: float) -> None:
        for chunk in self.chunks.values():
            chunk.interpolate_entities(partial_tick)

    def get_chunks_in_radius(self, start_pos: pygame.Vector2, radius: int) -> list[Chunk]:
        CHUNK_SIZE = 16
        BLOCK_SIZE = 32
        CHUNK_PIXELS = CHUNK_SIZE * BLOCK_SIZE

        chunk_radius = math.ceil(radius / CHUNK_PIXELS) + 1

        start_chunk_x = math.floor(start_pos.x / CHUNK_PIXELS)
        start_chunk_y = math.floor(start_pos.y / CHUNK_PIXELS)

        chunks = []

        for x in range(start_chunk_x - chunk_radius, start_chunk_x + chunk_radius + 1):
            for y in range(start_chunk_y - chunk_radius, start_chunk_y + chunk_radius + 1):
                left = x * CHUNK_PIXELS
                right = left + CHUNK_PIXELS
                top = y * CHUNK_PIXELS
                bottom = top + CHUNK_PIXELS

                closest_x = max(left, min(start_pos.x, right))
                closest_y = max(top, min(start_pos.y, bottom))

                dx = start_pos.x - closest_x
                dy = start_pos.y - closest_y

                if dx ** 2 + dy ** 2 <= radius ** 2:
                    chunk = self.get_chunk((x,y))
                    if chunk is not None:
                        chunks.append(chunk)

        return chunks

    def get_entities_in_radius(self, start_pos: pygame.Vector2, radius: int) -> list:
        chunks = self.get_chunks_in_radius(start_pos, radius)

        entities = []

        for chunk in chunks:
            for entity in chunk.get_entities():

                if entity.position.pos.distance_to(start_pos) <= radius:
                    entities.append(entity)

        return entities