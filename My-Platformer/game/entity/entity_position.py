from dataclasses import dataclass
import pygame

class EntityPosition:
    def __init__(self, start_x:int=0, start_y:int=0, start_speed_x:int=0, start_speed_y:int=0):
        self.prev = pygame.Vector2(start_x, start_y)
        self.pos = pygame.Vector2(start_x, start_y)
        self.interp = pygame.Vector2(start_x, start_y)
        self.speed = pygame.Vector2(start_speed_x, start_speed_y)
        self.direction: int = -1
        self.is_in_air: bool = False

        self._world_pos = pygame.Vector2(start_x, start_y)

    @property
    def world_pos(self) -> pygame.Vector2:
        return pygame.Vector2(int(self.pos.x * 32), int(self.pos.y * 32))