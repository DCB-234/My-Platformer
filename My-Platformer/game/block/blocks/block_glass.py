from game.block.block_definition import BlockDefinition

class BlockGlass(BlockDefinition):
    def __init__(self):
        super().__init__(
            hardness = 0.5,
            can_block_grass = False,
            light_opacity = 0
        )