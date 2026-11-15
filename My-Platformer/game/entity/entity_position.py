from dataclasses import dataclass
import pygame

class EntityPosition:
    def __init__(
        self, 
        start_pos: pygame.Vector2 = pygame.Vector2(0,0), 
        start_speed: pygame.Vector2 = pygame.Vector2(0,0)
    ):
        self.prev = start_pos
        self.pos = start_pos
        self.interp = start_pos
        self.speed = start_speed
        self.direction: int = -1
        self.is_in_air: bool = False

    @property
    def world_pos(self) -> pygame.Vector2:
        return pygame.Vector2(int(self.pos.x // 32), int(self.pos.y // 32))