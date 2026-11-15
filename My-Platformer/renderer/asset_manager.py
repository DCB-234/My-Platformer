from game.item.item_type import ItemType
from game.block.block_type import BlockType
import pathlib
import pygame

class AssetManager:
    def __init__(self):
        BASE_DIR = pathlib.Path(__file__).parents[1]
        BLOCK_DIR = BASE_DIR / 'assets' / 'textures' / 'blocks'
        BLOCK_SCALE = (32, 32)

        # Define block textures
        self.BLOCKS = {
            BlockType.BEDROCK: (
                pygame.image.load(BLOCK_DIR/'bedrock.png').convert_alpha()
            ),
            BlockType.COAL_ORE: (
                pygame.image.load(BLOCK_DIR/'coal_ore.png').convert_alpha()
            ),
            BlockType.COBBLESTONE: (
                pygame.image.load(BLOCK_DIR/'cobblestone.png').convert_alpha()
            ),
            BlockType.DIRT: (
                pygame.image.load(BLOCK_DIR/'dirt.png').convert_alpha()
            ),
            BlockType.GLASS: (
                pygame.image.load(BLOCK_DIR/'glass.png').convert_alpha()
            ),
            BlockType.GRASS: (
                pygame.image.load(BLOCK_DIR/'grass.png').convert_alpha()
            ),
            BlockType.IRON_ORE: (
                pygame.image.load(BLOCK_DIR/'iron_ore.png').convert_alpha()
            ),
            BlockType.LEAVES_OAK: (
                pygame.image.load(BLOCK_DIR/'leaves_oak.png').convert_alpha()
            ),
            BlockType.LOG_OAK: (
                pygame.image.load(BLOCK_DIR/'log_oak.png').convert_alpha()
            ),
            BlockType.PLANKS_OAK: (
                pygame.image.load(BLOCK_DIR/'planks_oak.png').convert_alpha()
            ),
            BlockType.STONE: (
                pygame.image.load(BLOCK_DIR/'stone.png').convert_alpha()
            )
        }

        # Resize each block
        for block, texture in self.BLOCKS.items():
            self.BLOCKS[block] = (
                pygame.transform.scale(texture, BLOCK_SCALE)
            )

        ITEM_DIR = BASE_DIR / 'assets' / 'textures' / 'items'
        ITEM_SCALE = (16,16)

        # Define item textures
        self.ITEMS = {
            ItemType.BEDROCK: (
                pygame.image.load(BLOCK_DIR/'bedrock.png').convert_alpha()
            ),
            ItemType.COAL: (
                pygame.image.load(ITEM_DIR/'coal.png').convert_alpha()
            ),
            ItemType.COAL_ORE: (
                pygame.image.load(BLOCK_DIR/'coal_ore.png').convert_alpha()
            ),
            ItemType.COBBLESTONE: (
                pygame.image.load(BLOCK_DIR/'cobblestone.png').convert_alpha()
            ),
            ItemType.DIRT: (
                pygame.image.load(BLOCK_DIR/'dirt.png').convert_alpha()
            ),
            ItemType.GLASS: (
                pygame.image.load(BLOCK_DIR/'glass.png').convert_alpha()
            ),
            ItemType.GRASS: (
                pygame.image.load(BLOCK_DIR/'grass.png').convert_alpha()
            ),
            ItemType.IRON_INGOT: (
                pygame.image.load(ITEM_DIR/'iron_ingot.png').convert_alpha()
            ),
            ItemType.IRON_ORE: (
                pygame.image.load(BLOCK_DIR/'iron_ore.png').convert_alpha()
            ),
            ItemType.LEAVES_OAK: (
                pygame.image.load(BLOCK_DIR/'leaves_oak.png').convert_alpha()
            ),
            ItemType.LOG_OAK: (
                pygame.image.load(BLOCK_DIR/'log_oak.png').convert_alpha()
            ),
            ItemType.PLANKS_OAK: (
                pygame.image.load(BLOCK_DIR/'planks_oak.png').convert_alpha()
            ),
            ItemType.RAW_IRON: (
                pygame.image.load(ITEM_DIR/'raw_iron.png').convert_alpha()
            ),
            ItemType.STICK: (
                pygame.image.load(ITEM_DIR/'stick.png').convert_alpha()
            ),
            ItemType.STONE: (
                pygame.image.load(BLOCK_DIR/'stone.png').convert_alpha()
            )
        }

        # Resize each item
        for item, texture in self.ITEMS.items():
            self.ITEMS[item] = (
                pygame.transform.scale(texture, ITEM_SCALE)
            )

    def get_item(self, item_type: ItemType) -> pygame.Surface | None:
        return self.ITEMS.get(item_type, None)

    def get_block(self, block_type: BlockType) -> pygame.Surface | None:
        return self.BLOCKS.get(block_type, None)