from game.item.item_type import ItemType
from game.item.items.item_bedrock import ItemBedrock
from game.item.items.item_coal import ItemCoal
from game.item.items.item_coal_ore import ItemCoalOre
from game.item.items.item_cobblestone import ItemCobblestone
from game.item.items.item_dirt import ItemDirt
from game.item.items.item_glass import ItemGlass
from game.item.items.item_grass import ItemGrass
from game.item.items.item_iron_ingot import ItemIronIngot
from game.item.items.item_iron_ore import ItemIronOre
from game.item.items.item_leaves_oak import ItemLeavesOak
from game.item.items.item_log_oak import ItemLogOak
from game.item.items.item_planks_oak import ItemPlanksOak
from game.item.items.item_raw_iron import ItemRawIron
from game.item.items.item_stick import ItemStick
from game.item.items.item_stone import ItemStone

ITEM_DEFINITIONS = {
    ItemType.BEDROCK: ItemBedrock(),
    ItemType.COAL: ItemCoal(),
    ItemType.COAL_ORE: ItemCoalOre(),
    ItemType.COBBLESTONE: ItemCobblestone(),
    ItemType.DIRT: ItemDirt(),
    ItemType.GLASS: ItemGlass(),
    ItemType.GRASS: ItemGrass(),
    ItemType.IRON_INGOT: ItemIronIngot(),
    ItemType.IRON_ORE: ItemIronOre(),
    ItemType.LEAVES_OAK: ItemLeavesOak(),
    ItemType.LOG_OAK: ItemLogOak(),
    ItemType.PLANKS_OAK: ItemPlanksOak(),
    ItemType.RAW_IRON: ItemRawIron(),
    ItemType.STICK: ItemStick(),
    ItemType.STONE: ItemStone()
}