from dataclasses import dataclass
from game.block.block_type import BlockType
from game.block.blocks.block_air import BlockAir
from game.block.blocks.block_bedrock import BlockBedrock
from game.block.blocks.block_coal_ore import BlockCoalOre
from game.block.blocks.block_cobblestone import BlockCobblestone
from game.block.blocks.block_dirt import BlockDirt
from game.block.blocks.block_glass import BlockGlass
from game.block.blocks.block_grass import BlockGrass
from game.block.blocks.block_iron_ore import BlockIronOre
from game.block.blocks.block_leaves import BlockLeaves
from game.block.blocks.block_log import BlockLog
from game.block.blocks.block_planks import BlockPlanks
from game.block.blocks.block_stone import BlockStone

BLOCK_DEFINITIONS = {
    BlockType.AIR: BlockAir(),
    BlockType.BEDROCK: BlockBedrock(),
    BlockType.COAL_ORE: BlockCoalOre(),
    BlockType.COBBLESTONE: BlockCobblestone(),
    BlockType.DIRT: BlockDirt(),
    BlockType.GLASS: BlockGlass(),
    BlockType.IRON_ORE: BlockIronOre(),
    BlockType.GRASS: BlockGrass(),
    BlockType.LEAVES_OAK: BlockLeaves(),
    BlockType.LOG_OAK: BlockLog(),
    BlockType.PLANKS_OAK: BlockPlanks(),
    BlockType.STONE: BlockStone()
}