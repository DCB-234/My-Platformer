from dataclasses import dataclass

@dataclass(frozen=True)
class BlockDefinition:
    hardness: float
    can_block_grass: bool = True
    is_solid_cube: bool = True
    light_opacity: int = 15

    def tick_random(self, block, context) -> None:
        return