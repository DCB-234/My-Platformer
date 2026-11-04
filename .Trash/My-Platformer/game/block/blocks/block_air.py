from game.block.block_definition import BlockDefinition

class BlockAir(BlockDefinition):
    def __init__(self):
        super().__init__(
            hardness = 0.0,
            can_block_grass = False,
            is_solid_cube = False,
            light_opacity = 0
        )