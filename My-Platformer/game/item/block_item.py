import pygame
from game.item.item_definition import ItemDefinition
from game.block.block_type import BlockType

class BlockItem(ItemDefinition):
    def __init__(self, block_type: BlockType):
        super().__init__()
        self.block_type: BlockType = block_type
        self.is_placeable = True

    def on_item_right_click(self, item_stack, world, entity_player, mouse_world) -> None:
        super().on_item_right_click(item_stack, world, entity_player, mouse_world)
        coord = world.get_coord_from_click(mouse_world)
        if world.is_valid_block_placement(coord, entity_player.hitbox):
            world.insert_block(self.block_type, coord)
            super().on_item_use(item_stack, world, entity_player)