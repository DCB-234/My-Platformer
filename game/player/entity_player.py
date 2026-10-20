import pygame
import math
import pathlib
from game.entity.skin_base import SkinBase
from game.block.block_type import BlockType
from game.item.item_type import ItemType
from game.container.containers.container_inventory import ContainerInventory
from game.helper.helper_entity import HelperEntity
from game.entity.entity_position import EntityPosition
from game.entity.entity_living.entity_living import EntityLiving

class EntityPlayer(EntityLiving):
    def __init__(self):
        super().__init__()
        self.speed_y: int = 0
        self.speed_x: int = 0
        self.terminal_velocity: int = 50
        self.direction: int = -1
        self.is_in_air: bool = False
        self.is_crouching: bool = False
        self.head_angle: float = 0

        self.swing_progress: float = 0.0
        self.swing_time: int = 0
        self.is_swinging: bool = False

        self.prev_swing_progress: float = 0.0
        self.interp_swing_progress: float = 0.0

        self.hitbox = pygame.Rect(0, 0, 8, 64)
        self.hitbox.midbottom = (self.position.x, self.position.y)

        self.current_hotbar_slot: int = 0

        self.inventory = ContainerInventory()

        self.inventory.add_item(ItemType.BEDROCK, amount=2)
        self.inventory.add_item(ItemType.DIRT, amount=5)
        self.inventory.add_item(ItemType.GLASS, amount=10)
        self.inventory.add_item(ItemType.GRASS, amount=15)
        self.inventory.add_item(ItemType.LEAVES_OAK, amount=20)
        self.inventory.add_item(ItemType.LOG_OAK, amount=25)
        self.inventory.add_item(ItemType.PLANKS_OAK, amount=30)
        self.inventory.add_item(ItemType.COBBLESTONE, amount=35)
        self.inventory.add_item(ItemType.STONE, amount=64)
        self.inventory.add_item(ItemType.COAL_ORE, amount=45)
        self.inventory.add_item(ItemType.IRON_ORE, amount=50)
        self.inventory.add_item(ItemType.COAL, amount=61)
        self.inventory.add_item(ItemType.IRON_INGOT, amount=64)
        self.inventory.add_item(ItemType.RAW_IRON)
        self.inventory.add_item(ItemType.STICK)

        # NOTE: only .png images work
        BASE_DIR = pathlib.Path(__file__).resolve().parents[1]
        SKIN_PATH = BASE_DIR.parent/'assets'/'textures'/'entity'/'steve.png'
        steve = pygame.image.load(SKIN_PATH).convert_alpha()
        steve_crop = pygame.Rect(0,0, steve.get_width(), steve.get_height() // 2)
        steve_skin = steve.subsurface(steve_crop)
        self.skin = SkinBase(steve_skin)

    def move(self, value: int) -> None:
        if self.is_crouching:
            min_x, max_x = -3, 3
        else:
            min_x, max_x = -6, 6

        new_speed_x = self.speed_x + value
        if new_speed_x < min_x or new_speed_x > max_x:
            return

        self.speed_x = new_speed_x

    def jump(self) -> None:
        if not self.is_in_air:
            self.is_in_air = True
            self.speed_y = 14

    def draw(self, screen, position) -> None:
        centerx, y = position
        facing = self.direction
        back_side = -facing

        if self.is_walking:
            max_leg_angle = self.max_walk_progress
            min_leg_angle = -self.max_walk_progress

            max_arm_angle = self.max_walk_progress - 10
            min_arm_angle = -self.max_walk_progress + 10

            sin_val = (math.sin(self.walk_progress * 2 * math.pi) + 1) / 2
            leg_angle = min_leg_angle + (max_leg_angle - min_leg_angle) * sin_val
            arm_angle = min_arm_angle + (max_arm_angle - min_arm_angle) * sin_val
        else:
            leg_angle = 0
            arm_angle = 0

        if self.is_swinging:
            sin_val = math.sin(math.sqrt(self.swing_progress) * 3.15)
            swing_arm_angle = 0 + (70 - 0) * sin_val
        else:
            swing_arm_angle = arm_angle

        # Back leg
        self.skin.draw_leg(screen, back_side, facing, (centerx,y-24), leg_angle)

        # Back arm
        back_arm_angle = -swing_arm_angle if facing == -1 else -arm_angle
        self.skin.draw_arm(screen, back_side, facing, (centerx,y-48), back_arm_angle)

        # Torso
        self.skin.draw_body(screen, facing, (centerx,y-24))

        # Front leg
        self.skin.draw_leg(screen, facing, facing, (centerx,y-24), -leg_angle)

        # Head
        self.skin.draw_head(screen, facing, (centerx,y-48), -self.head_angle)

        # Front arm
        front_arm_angle = swing_arm_angle if facing == 1 else arm_angle
        self.skin.draw_arm(screen, facing, facing, (centerx,y-48), front_arm_angle)

    def update_physics(self) -> None:
        super().update_physics()
        if self.is_crouching:
            self.hitbox.height = 48
            self.max_walk_time = 25
            self.max_walk_progress = 30
        else:
            self.hitbox.height = 60
            self.max_walk_time = 15
            self.max_walk_progress = 45

    def tick_update(self, mouse_world) -> None:
        super().tick_update()
        self.update_arm_swing_progress()
        self.update_head(mouse_world)

    def update_head(self, mouse_world) -> None:
        mouse_x, _ = mouse_world
        if mouse_x < self.position.x:
            self.direction = -1
        elif mouse_x > self.position.x:
            self.direction = 1

        centerx, y = self.position.x, self.position.y
        head_pos = (centerx, y - 56)
        p1, p2 = (mouse_world, head_pos) if self.direction == 1 else (head_pos, mouse_world)
        self.head_angle = self.find_angle(p1, p2)

    def update_arm_swing_progress(self) -> None:
        max_swing_time = 6
        if self.is_swinging:

            self.swing_time += 1
            if self.swing_time >= max_swing_time:
                self.is_swinging = False
                self.swing_time = 0
        else:
            self.swing_time = 0

        self.prev_swing_progress = self.swing_progress
        self.swing_progress = self.swing_time / max_swing_time

    def handle_single_right_click(self, world, mouse_world) -> None:
        current_item_stack = self.inventory.slots[self.current_hotbar_slot]
        if current_item_stack:
            current_item_stack.on_item_right_click(world, self, mouse_world)
            if current_item_stack.stack_size < 1:
                self.inventory.slots[self.current_hotbar_slot] = None

    def handle_right_click_hold(self, world) -> None:
        ...

    def handle_single_left_click(self, world, mouse_world) -> None:
        # Break block
        coord = world.get_coord_from_click(mouse_world)
        world.break_block(coord)

    def handle_left_click_hold(self, world, mouse_world) -> None:
        coord = world.get_coord_from_click(mouse_world)
        world.break_block(coord)

    def interpolate_entity(self, partial_tick) -> None:
        super().interpolate_entity(partial_tick)

        # Interpolate player limb swing
        self.interp_swing_progress = (
            self.prev_swing_progress +
            (self.swing_progress - self.prev_swing_progress) * partial_tick
        )
