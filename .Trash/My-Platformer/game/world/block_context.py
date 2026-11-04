from dataclasses import dataclass
from game.block.block import Block
from itertools import product

@dataclass
class BlockContext:
    world: "World"
    x: int
    y: int

    def get(self, dx: int, dy: int) -> Block:
        return self.world.get_block((self.x + dx, self.y + dy))

    @property
    def left(self) -> Block:
        return self.world.get_block((self.x - 1, self.y))

    @property
    def right(self) -> Block:
        return self.world.get_block((self.x + 1, self.y))

    @property
    def above(self) -> Block:
        return self.world.get_block((self.x, self.y - 1))

    @property
    def bottom(self) -> Block:
        return self.world.get_block((self.x, self.y + 1))

    def get_surroundings(self) -> list[Block]:
        return [
            self.get(dx, dy)
            for dx, dy in product((-1, 0, 1), repeat=2)
            if not (dx == 0 and dy == 0)
        ]