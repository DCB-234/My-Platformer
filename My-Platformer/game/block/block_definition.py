from game.entity.entity_item import EntityItem
from dataclasses import dataclass
import pygame

@dataclass(frozen=True)
class BlockDefinition:
    hardness: float
    can_block_grass: bool = True
    is_solid_cube: bool = True
    light_opacity: int = 15

    def tick_random(self, block, context) -> None:
        return

    def on_block_break(self, block, context) -> None:
        block_pos = pygame.Vector2(context.world_to_pixel_coord(context.world_pos))
        entity_item = EntityItem(
            item_type = context.block_item_conversion.block_to_item(block.block_type),
            start_pos = pygame.Vector2(block_pos.x + 16, block_pos.y + 16),
            start_speed = pygame.Vector2(0,0)
        )
        context.world.spawn_entity(entity_item)