from game.entity.entity_position import EntityPosition
from game.helper.helper_entity import HelperEntity
import pygame

class Entity(HelperEntity):
    def __init__(self, hitbox, start_x:int, start_y:int, start_speed_x:int=0, start_speed_y:int=0):
        self.position = EntityPosition(
            start_x=start_x, start_y=start_y, start_speed_x=start_speed_x, start_speed_y=start_speed_y
        )
        self.hitbox: pygame.Rect = hitbox

    def tick_update(self, world, game_rules) -> None:
        self.apply_physics(world, game_rules)

    def apply_physics(self, world, game_rules) -> None:
        self.position.prev.x = self.position.pos.x
        self.position.prev.y = self.position.pos.y

        self.apply_vertical_physics(world, game_rules)
        self.apply_horizontal_physics(world, game_rules)

    def apply_horizontal_physics(self, world, game_rules) -> None:
        if not self.position.is_in_air:
            self.position.speed.x += self.determine_friction()

        self.position.pos.x += self.position.speed.x
        self.update_physics()

        # Resolve horizontal collisions
        collisions = world.get_collisions(self.hitbox)

        if collisions:
            if self.position.speed.x > 0:
                obstacle = min(collisions, key=lambda rect: rect.left)
                self.hitbox.right = obstacle.left

            elif self.position.speed.x < 0:
                obstacle = max(collisions, key=lambda rect: rect.right)
                self.hitbox.left = obstacle.right

            self.position.pos.x = self.hitbox.centerx
            self.position.speed.x = 0

    def apply_vertical_physics(self, world, game_rules) -> None:

        # Apply gravity
        self.position.speed.y -= game_rules.GRAVITY
        self.position.pos.y -= self.position.speed.y
        self.update_physics()

        # Resolve vertical collisions
        collisions = world.get_collisions(self.hitbox)

        if collisions:
            if self.position.speed.y < 0:
                obstacle = min(collisions, key=lambda rect: rect.top)

                self.hitbox.bottom = obstacle.top
                self.position.is_in_air = False

            elif self.position.speed.y > 0:
                obstacle = max(collisions, key=lambda rect: rect.bottom)

                self.hitbox.top = obstacle.bottom

            self.position.pos.y = self.hitbox.bottom
            self.position.speed.y = 0

            self.update_physics()

        else:
            self.position.is_in_air = True

    def determine_friction(self) -> int:
        if self.position.speed.x < 0:
            return 1
        elif self.position.speed.x > 0:
            return -1
        elif self.position.speed.x == 0:
            return 0

    def update_physics(self) -> None:
        self.hitbox.midbottom = (self.position.pos.x, self.position.pos.y)

    def interpolate_entity(self, partial_tick: float) -> None:
        self.position.interp = self.position.prev.lerp(self.position.pos, partial_tick)
