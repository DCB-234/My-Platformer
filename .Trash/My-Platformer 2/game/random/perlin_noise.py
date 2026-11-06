import math
import random

class PerlinNoise:
    def __init__(self, world_seed):
        self.world_seed: int = world_seed
        self.SCALE: float = 16.0

    def noise_1d(self, x) -> float:
        value = math.sin(x * 12.9898 + self.world_seed * 78.233) * 43758.5453123
        return value - math.floor(value)

    def interpolated_noise(self, x) -> float:
        x_floor = math.floor(x)
        fraction = x - x_floor

        v1 = self.noise_1d(x_floor)
        v2 = self.noise_1d(x_floor + 1)

        mu2 = (1 - math.cos(fraction * math.pi)) / 2
        return v1 * (1 - mu2) + v2 * mu2

    def get_terrain_height(self, world_x) -> int:
        height = self.interpolated_noise(world_x / self.SCALE) * 15
        height += self.interpolated_noise((world_x * 2) / self.SCALE) * 4

        return int(height)