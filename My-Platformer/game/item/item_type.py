from enum import Enum, auto

class ItemType(Enum):
    # Block Items
    BEDROCK = auto()
    COAL_ORE = auto()
    COBBLESTONE = auto()
    DIRT = auto()
    GLASS = auto()
    GRASS = auto()
    IRON_ORE = auto()
    LEAVES_OAK = auto()
    LOG_OAK = auto()
    PLANKS_OAK = auto()
    STONE = auto()

    # Items
    COAL = auto()
    IRON_INGOT = auto()
    RAW_IRON = auto()
    STICK = auto()