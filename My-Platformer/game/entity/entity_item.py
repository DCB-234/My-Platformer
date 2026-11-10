from game.entity.entitiy import Entity
import pygame

class EntityItem(Entity):
    def __init__(self, item_type):
        super().__init__(hitbox = pygame.Rect(0,0,8,8))
        self.item_type = item_type

    def tick_update(self, world, game_rules) -> None:
        super().tick_update(world, game_rules)
        # check proximity with player to get picked up

    def draw(self, screen_pos: tuple) -> None:
        ...