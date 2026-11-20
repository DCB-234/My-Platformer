from game.block.block_definition import BlockDefinition
from game.item.item_type import ItemType
import random

class BlockLeaves(BlockDefinition):
    def __init__(self):
        super().__init__(
            hardness = 0.2,
            can_block_grass = False,
            light_opacity = 2
        )

    def get_drop_item(self, block, context) -> ItemType | None:
        if random.random() < 0.1:
            return ItemType.STICK