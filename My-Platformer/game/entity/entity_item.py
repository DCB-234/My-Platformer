from game.entity.entity import Entity
import pygame

class EntityItem(Entity):
    def __init__(self):
        super().__init__(hitbox = pygame.Rect(0,0,8,8))