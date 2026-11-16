from game.block.block_definition import BlockDefinition
from game.block.block_type import BlockType
from game.item.item_type import ItemType

class BlockGrass(BlockDefinition):
    def __init__(self):
        super().__init__(
            hardness = 0.5
        )
    
    def tick_random(self, block, context) -> None:
        if context.above is not None:
            if context.above.definition.can_block_grass:
                block.block_type = BlockType.DIRT

    def get_drop_item(self, block, context) -> ItemType:
        return ItemType.DIRT