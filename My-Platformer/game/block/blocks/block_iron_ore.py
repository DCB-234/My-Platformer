from game.block.block_definition import BlockDefinition
from game.item.item_type import ItemType

class BlockIronOre(BlockDefinition):
    def __init__(self):
        super().__init__(
            hardness = 2.0
        )

    def get_drop_item(self, block, context) -> ItemType | None:
        return ItemType.RAW_IRON