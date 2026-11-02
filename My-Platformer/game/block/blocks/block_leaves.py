from game.block.block_definition import BlockDefinition

class BlockLeaves(BlockDefinition):
    def __init__(self):
        super().__init__(
            hardness = 0.2,
            can_block_grass = False,
            light_opacity = 2
        )