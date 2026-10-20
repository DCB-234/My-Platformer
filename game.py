from game.player.entity_player import EntityPlayer
from game.container.containers.container_inventory import ContainerInventory
from game.gamemode import Gamemode
import pygame
import random

class Game:
    def __init__(self, world, camera, world_seed):
        self.world = world
        self.player = EntityPlayer()

        self.timer: float = 0.0
        self.INTERVAL: float = 0.05
        self.partial_tick: float = 0.0

        self.opened_container = None

        self.previous_keys = None
        self.previous_mouse_buttons = None

        self.camera = camera

        self.player_chunk: tuple = (
            self.player.position.x // (16 * 32),
            self.player.position.y // (16 * 32)
        )

        # Game rules
        self.GRAVITY: int = 2
        self.random_tick_speed: int = 1
        self.gamemode: Gamemode = Gamemode.CREATIVE
        self.RENDER_DISTANCE: int = 1
        self.world_seed: int = world_seed

        self.world.chunk_manager.update_chunks(self.player_chunk, self.RENDER_DISTANCE)

    def progress(self, keys, mouse_buttons, dt) -> None:

        self.timer += dt

        # Interpolate movements
        self.partial_tick = self.timer / self.INTERVAL
        self.player.interpolate_entity(self.partial_tick)

        mouse_pos = pygame.mouse.get_pos()
        mouse_world = self.camera.screen_to_world(mouse_pos)
        mouse_world = tuple(int(num) for num in mouse_world)

        # Tick if appriopriate
        if self.timer >= self.INTERVAL:
            self._tick(keys, mouse_buttons, mouse_world)

            self.timer -= self.INTERVAL

    def _tick(self, keys, mouse_buttons, mouse_world) -> None:
        self.tick_player(keys, mouse_buttons, mouse_world)
        self.tick_chunks()
        self.tick_blocks_and_ambience()

    def tick_blocks_and_ambience(self) -> None:
        for _ in range(self.random_tick_speed):
            self.world.tick_random()

    def tick_player(self, keys, mouse_buttons, mouse_world) -> None:
        self.player.tick_update(mouse_world)
        self.handle_player_actions(keys, mouse_buttons, mouse_world)
        self.handle_player_movement(keys, mouse_buttons)

    def tick_chunks(self) -> None:
        current_chunk = (
            self.player.position.x // (16 * 32),
            self.player.position.y // (16 * 32)
        )
        if current_chunk != self.player_chunk:
            self.player_chunk = current_chunk
            self.world.chunk_manager.update_chunks(self.player_chunk, self.RENDER_DISTANCE)

    def handle_player_actions(self, keys, mouse_buttons, mouse_world) -> None:

        # right mouse button action
        if mouse_buttons[2]:

            if not self.previous_mouse_buttons[2]:
                self.player.is_swinging = True
                self.player.handle_single_right_click(self.world, mouse_world)
            else:
                self.player.handle_right_click_hold(self.world)

        # left mouse button action
        if mouse_buttons[0]:
            self.player.is_swinging = True

            if not self.previous_mouse_buttons[0]:
                self.player.handle_single_left_click(self.world, mouse_world)
            else:
                self.player.handle_left_click_hold(self.world, mouse_world)

        # Crouching
        if keys[pygame.K_LSHIFT]:
            self.player.is_crouching = True
        else:
            self.player.is_crouching = False

        self.player.update_physics()

        if self.world.is_colliding(self.player.hitbox):
            self.player.is_crouching = True
            self.player.update_physics()

        # Hotbar keys
        if keys[pygame.K_1]:
            self.player.current_hotbar_slot = 0

        if keys[pygame.K_2]:
            self.player.current_hotbar_slot = 1

        if keys[pygame.K_3]:
            self.player.current_hotbar_slot = 2

        if keys[pygame.K_4]:
            self.player.current_hotbar_slot = 3

        if keys[pygame.K_5]:
            self.player.current_hotbar_slot = 4

        if keys[pygame.K_6]:
            self.player.current_hotbar_slot = 5

        if keys[pygame.K_7]:
            self.player.current_hotbar_slot = 6
        
        if keys[pygame.K_8]:
            self.player.current_hotbar_slot = 7
        
        if keys[pygame.K_9]:
            self.player.current_hotbar_slot = 8

        # Inventory
        if keys[pygame.K_e] and not self.previous_keys[pygame.K_e]:
            self.toggle_player_inventory()

        self.previous_keys = keys
        self.previous_mouse_buttons = mouse_buttons

    def toggle_player_inventory(self) -> None:
        if isinstance(self.opened_container, ContainerInventory):
            self.opened_container = None
            return
        self.opened_container = self.player.inventory

    def handle_player_movement(self, keys, mouse_buttons) -> None:

        self.player.position.prev_x = self.player.position.x
        self.player.position.prev_y = self.player.position.y

        # player vertical movement        
        if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.player.jump()

        # Apply gravity to player
        self.player.speed_y -= self.GRAVITY
        self.player.position.y -= self.player.speed_y
        self.player.update_physics()

        # player vertical collisions
        collisions = self.world.get_collisions(self.player.hitbox)

        if collisions:
            if self.player.speed_y < 0:
                obstacle = min(collisions, key=lambda rect: rect.top)

                self.player.hitbox.bottom = obstacle.top
                self.player.is_in_air = False

            elif self.player.speed_y > 0:
                obstacle = max(collisions, key=lambda rect: rect.bottom)

                self.player.hitbox.top = obstacle.bottom

            self.player.position.y = self.player.hitbox.bottom
            self.player.speed_y = 0

            self.player.update_physics()

        else:
            self.player.is_in_air = True

        # player horizontal movement
        horizontally_moved = False
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.move(-1)
            horizontally_moved = True

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.move(1)
            horizontally_moved = True

        if (
            not horizontally_moved or
            (self.player.is_crouching and
            (self.player.speed_x < -3 or self.player.speed_x > 3))
        ):
            self.player.speed_x += self._determine_friction()

        if horizontally_moved:
            self.player.is_walking = True

        self.player.position.x += self.player.speed_x
        self.player.update_physics()

        # player horizontal collisions
        collisions = self.world.get_collisions(self.player.hitbox)

        if collisions:
            if self.player.speed_x > 0:
                obstacle = min(collisions, key=lambda rect: rect.left)
                self.player.hitbox.right = obstacle.left

            elif self.player.speed_x < 0:
                obstacle = max(collisions, key=lambda rect: rect.right)
                self.player.hitbox.left = obstacle.right

            self.player.position.x = self.player.hitbox.centerx
            self.player.speed_x = 0

    def _determine_friction(self) -> int:
        if self.player.speed_x < 0:
            return 1
        elif self.player.speed_x > 0:
            return -1
        elif self.player.speed_x == 0:
            return 0
