from game.item.item_type import ItemType
from game.block.block_type import BlockType

class BlockItemConversion:
    def __init__(self) -> None:
        self.BLOCK_TO_ITEM = {
            BlockType.BEDROCK: ItemType.BEDROCK,
            BlockType.COAL_ORE: ItemType.COAL_ORE,
            BlockType.COBBLESTONE: ItemType.COBBLESTONE,
            BlockType.DIRT: ItemType.DIRT,
            BlockType.GLASS: ItemType.GLASS,
            BlockType.GRASS: ItemType.GRASS,
            BlockType.IRON_ORE: ItemType.IRON_ORE,
            BlockType.LEAVES_OAK: ItemType.LEAVES_OAK,
            BlockType.LOG_OAK: ItemType.LOG_OAK,
            BlockType.PLANKS_OAK: ItemType.PLANKS_OAK,
            BlockType.STONE: ItemType.STONE
        }
        
        self.ITEM_TO_BLOCK = {
            ItemType.BEDROCK: BlockType.BEDROCK,
            ItemType.COAL_ORE: BlockType.COAL_ORE,
            ItemType.COBBLESTONE: BlockType.COBBLESTONE,
            ItemType.DIRT: BlockType.DIRT,
            ItemType.GLASS: BlockType.GLASS,
            ItemType.GRASS: BlockType.GRASS,
            ItemType.IRON_ORE: BlockType.IRON_ORE,
            ItemType.LEAVES_OAK: BlockType.LEAVES_OAK,
            ItemType.LOG_OAK: BlockType.LOG_OAK,
            ItemType.PLANKS_OAK: BlockType.PLANKS_OAK,
            ItemType.STONE: BlockType.STONE
        }

    def block_to_item(self, block_type: BlockType) -> ItemType:
        return self.BLOCK_TO_ITEM[block_type]

    def item_to_block(self, item_type: ItemType) -> BlockType:
        return self.ITEM_TO_BLOCK[item_type]