from game.block.block_definition import BlockDefinition

class BlockIronOre(BlockDefinition):
    def __init__(self):
        super().__init__(
            hardness = 2.0
        )