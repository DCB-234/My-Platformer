from dataclasses import dataclass
import math
import pygame

@dataclass
class Camera:
    pos = pygame.Vector2(0.0, 0.0)
    SMOOTHING: float = 3

    def update(self, player, screen, dt) -> None:
        factor = 1 - math.exp(-self.SMOOTHING * dt)

        target_x = player.position.pos.x - screen.get_width() / 2
        target_y = player.position.pos.y - screen.get_height() / 2

        self.pos.x += (target_x - self.pos.x) * factor
        self.pos.y += (target_y - self.pos.y) * factor

    def world_to_screen(self, position: tuple) -> tuple:
        pos_x, pos_y = position
        return (
            pos_x - self.pos.x,
            pos_y - self.pos.y
        )

    def screen_to_world(self, position: tuple) -> tuple:
        pos_x, pos_y = position
        return (
            pos_x + self.pos.x,
            pos_y + self.pos.y
        )