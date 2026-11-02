from game.block.block_definition import BlockDefinition

class BlockBedrock(BlockDefinition):
    def __init__(self):
        super().__init__(
            hardness = 99999999.0
        )