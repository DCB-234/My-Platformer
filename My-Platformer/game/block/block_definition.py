from game.entity.entity_item_stack import EntityItemStack
from dataclasses import dataclass
import pygame
import random

@dataclass(frozen=True)
class BlockDefinition:
    hardness: float
    can_block_grass: bool = True
    is_solid_cube: bool = True
    light_opacity: int = 15

    def tick_random(self, block, context) -> None:
        return

    def get_drop_item(self, block, context) -> ItemType | None:
        return context.block_item_conversion.block_to_item(block.block_type)

    def on_block_break(self, block, context) -> None:
        item_type = self.get_drop_item(block, context)

        if item_type is None:
            return

        block_pos = pygame.Vector2(context.world_to_pixel_coord(context.world_pos))
        entity_item_stack = EntityItemStack(
            item_type = item_type,
            start_pos = pygame.Vector2(block_pos.x + 16, block_pos.y + 16),
            start_speed = pygame.Vector2(random.randint(-3,3), 10)
        )
        context.world.spawn_entity(entity_item_stack)