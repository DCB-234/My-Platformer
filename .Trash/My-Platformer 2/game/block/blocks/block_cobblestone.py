from game.block.block_definition import BlockDefinition

class BlockCobblestone(BlockDefinition):
    def __init__(self):
        super().__init__(
            hardness = 2.0
        )