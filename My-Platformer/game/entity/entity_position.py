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