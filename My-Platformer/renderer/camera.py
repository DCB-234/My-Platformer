from dataclasses import dataclass
import math

@dataclass
class Camera:
    x: float = 0.0
    y: float = 0.0
    SMOOTHING: float = 0.1

    def update(self, player, screen, dt) -> None:
        factor = 1 - math.exp(-self.SMOOTHING + dt)

        target_x = player.position.x - screen.get_width() / 2
        target_y = player.position.y - screen.get_height() / 2

        self.x += (target_x - self.x) * factor
        self.y += (target_y - self.y) * factor

    def world_to_screen(self, position) -> tuple:
        pos_x, pos_y = position
        return (
            pos_x - self.x,
            pos_y - self.y
        )

    def screen_to_world(self, position) -> tuple:
        pos_x, pos_y = position
        return (
            pos_x + self.x,
            pos_y + self.y
        )