from game.player.entity_player import EntityPlayer
from game.container.containers.container_inventory import ContainerInventory
from game.gamemode import Gamemode
from game.game_rules import GameRules
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
            int(self.player.position.pos.x // (16 * 32)),
            int(self.player.position.pos.y // (16 * 32))
        )

        self.game_rules = GameRules(GRAVITY = 2, RANDOM_TICK_SPEED = 1, GAMEMODE = Gamemode.CREATIVE, RENDER_DISTANCE = 1)
        self.world_seed: int = world_seed

        self.world.chunk_manager.update_chunks(self.player_chunk, self.game_rules.RENDER_DISTANCE)

    def progress(self, keys, mouse_buttons, dt) -> None:

        self.timer += dt

        mouse_pos = pygame.mouse.get_pos()
        mouse_world = self.camera.screen_to_world(mouse_pos)
        mouse_world = tuple(int(num) for num in mouse_world)

        if self.timer >= self.INTERVAL:
            self._tick(keys, mouse_buttons, mouse_world)

            self.timer -= self.INTERVAL

        self.partial_tick = min(1.0, self.timer / self.INTERVAL)
        self.player.interpolate_entity(self.partial_tick)

    def _tick(self, keys, mouse_buttons, mouse_world) -> None:
        self.tick_player(keys, mouse_buttons, mouse_world)
        self.tick_chunks()
        self.tick_blocks_and_ambience()

    def tick_blocks_and_ambience(self) -> None:
        for _ in range(self.game_rules.RANDOM_TICK_SPEED):
            self.world.tick_random()

    def tick_player(self, keys, mouse_buttons, mouse_world) -> None:
        self.player.tick_update(self.world, self.game_rules, mouse_world)
        self.handle_player_actions(keys, mouse_buttons, mouse_world)

    def tick_chunks(self) -> None:
        current_chunk = (
            int(self.player.position.pos.x // (16 * 32)),
            int(self.player.position.pos.y // (16 * 32))
        )
        if current_chunk != self.player_chunk:
            self.player_chunk = current_chunk
            self.world.update_chunks(self.player_chunk, self.game_rules.RENDER_DISTANCE)

        self.world.tick_chunks(self.game_rules)

    def handle_player_actions(self, keys, mouse_buttons, mouse_world) -> None:

        # Movement
        if keys[pygame.K_w] or keys[pygame.K_UP] or keys[pygame.K_SPACE]:
            self.player.jump()

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player.move(-1)
            self.player.is_walking = True

        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player.move(1)
            self.player.is_walking = True

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

        if keys[pygame.K_LSHIFT]:
            self.player.is_crouching = True
        else:
            self.player.is_crouching = False

        self.player.update_physics()

        if self.world.is_colliding(self.player.hitbox):
            self.player.is_crouching = True
            self.player.update_physics()

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

        if keys[pygame.K_e] and not self.previous_keys[pygame.K_e]:
            self.toggle_player_inventory()

        # Drop item from hotbar
        if keys[pygame.K_q] and not self.previous_keys[pygame.K_q]:
            print('Dropping item')
            ...

        self.previous_keys = keys
        self.previous_mouse_buttons = mouse_buttons

    def toggle_player_inventory(self) -> None:
        if isinstance(self.opened_container, ContainerInventory):
            self.opened_container = None
            return
        self.opened_container = self.player.inventory