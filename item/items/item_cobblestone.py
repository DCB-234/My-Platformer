from game.item.block_item import BlockItem
from game.block.block_type import BlockType

class ItemCobblestone(BlockItem):
    def __init__(self):
        super().__init__(
            block_type = BlockType.COBBLESTONE
        )