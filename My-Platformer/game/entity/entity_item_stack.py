from game.entity.entity import Entity
from game.item.item_type import ItemType
import time
import pygame
import math

class EntityItemStack(Entity):
    MAX_STACK_SIZE = 64

    def __init__(
        self,
        item_type: ItemType,
        start_pos: pygame.Vector2=pygame.Vector2(0,0),
        start_speed: pygame.Vector2=pygame.Vector2(0,0),
        stack_size: int = 1
    ):
        super().__init__(hitbox=pygame.Rect(0,0,16,16), start_pos=start_pos, start_speed=start_speed)
        self.stack_size = stack_size
        self.item_type = item_type
        self.spawn_time = time.time()

        self.max_anim_time: int = 20
        self.anim_time: int = 0
        self.anim_progress: float = 0.0
        self.prev_anim_progress: float = 0.0
        self.interp_anim_progress: float = 0.0

    def tick_update(self, world, game_rules) -> None:
        if time.time() - self.spawn_time > 300.0 or self.stack_size <= 0:
            self.needs_removal = True
            return

        super().tick_update(world, game_rules)
        self.update_anim_progress()

        if time.time() - self.spawn_time < 5.0:
            return

        SEARCH_RADIUS = 32
        near_entities = world.get_entities_in_radius(self.position.pos, SEARCH_RADIUS)

        if near_entities is None:
            return

        for entity in near_entities:
            if entity == self:
                continue

            if isinstance(entity, EntityItemStack) and self.stack_size <= self.MAX_STACK_SIZE:
                self.attempt_combine_entity_item_stack(entity)

        # check proximity with player to get picked up

    def attempt_combine_entity_item_stack(self, entity_item_stack) -> None:

        if time.time() - entity_item_stack.spawn_time < 5.0:
            return

        new_stack_size = min(self.stack_size + entity_item_stack.stack_size, 64)

        d_stack_size = new_stack_size - self.stack_size
        entity_item_stack.stack_size -= d_stack_size

        self.stack_size = new_stack_size

    def update_anim_progress(self) -> None:
        self.anim_time += 1

        if self.anim_time == self.max_anim_time:
            self.anim_time = 0

        self.prev_anim_progress = self.anim_progress
        self.anim_progress = self.anim_time / self.max_anim_time

    def interpolate(self, partial_tick: float) -> None:
        super().interpolate(partial_tick)

        self.interp_anim_progress = pygame.math.lerp(self.prev_anim_progress, self.anim_progress, partial_tick)

        self.position.interp.y -= 4 + 8 * ((math.sin(self.interp_anim_progress * math.pi * 2) + 1) / 2)

    def draw(self, screen, midbottom: tuple, asset_manager) -> None:
        entity_surface = asset_manager.get_item(self.item_type)

        entity_rect = entity_surface.get_rect()
        entity_rect.midbottom = midbottom

        screen.blit(entity_surface, entity_rect)
