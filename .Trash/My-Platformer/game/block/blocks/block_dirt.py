from game.block.block_definition import BlockDefinition
from game.block.block_type import BlockType

class BlockDirt(BlockDefinition):
    def __init__(self):
        super().__init__(
            hardness = 0.5
        )

    def tick_random(self, block, context) -> None:
        if context.above is not None:
            if context.above.definition.can_block_grass:
                return

        surroundings = context.get_surroundings()
        if any(
            neighbor_block is not None and neighbor_block.block_type == BlockType.GRASS 
            for neighbor_block in surroundings
        ):
            block.block_type = BlockType.GRASS