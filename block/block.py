from dataclasses import dataclass
from game.block.block_type import BlockType
from game.block.block_registry import BLOCK_DEFINITIONS

@dataclass
class Block:
    block_type: BlockType
    state: object | None = None

    @property
    def definition(self):
        return BLOCK_DEFINITIONS[self.block_type]

    def tick_random(self, context):
        self.definition.tick_random(self, context)
