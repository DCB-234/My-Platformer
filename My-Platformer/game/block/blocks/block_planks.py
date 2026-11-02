from game.block.block_definition import BlockDefinition

class BlockPlanks(BlockDefinition):
    def __init__(self):
        super().__init__(
            hardness = 1.0
        )