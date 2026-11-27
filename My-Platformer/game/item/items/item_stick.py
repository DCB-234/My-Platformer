from game.item.item_definition import ItemDefinition

class ItemStick(ItemDefinition):
    def __init__(self):
        super().__init__(MAX_STACK_SIZE = 16)