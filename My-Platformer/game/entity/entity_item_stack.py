from game.entity.entity import Entity
from game.item.item_type import ItemType
import pygame

class EntityItemStack(Entity):
    def __init__(
        self,
        item_type: ItemType,
        start_pos: pygame.Vector2=pygame.Vector2(0,0),
        start_speed: pygame.Vector2=pygame.Vector2(0,0),
        stack_size: int = 1
    ):
        super().__init__(hitbox=pygame.Rect(0,0,16,16), start_pos=start_pos, start_speed=start_speed)
        self.item_type = item_type

    def tick_update(self, world, game_rules) -> None:
        super().tick_update(world, game_rules)
        # check proximity with player to get picked up

    def draw(self, screen, midbottom: tuple, asset_manager) -> None:
        entity_surface = asset_manager.get_item(self.item_type)

        entity_rect = entity_surface.get_rect()
        entity_rect.midbottom = midbottom

        screen.blit(entity_surface, entity_rect)
