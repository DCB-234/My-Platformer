from game.item.item_type import ItemType
from game.item.item_registry import ITEM_DEFINITIONS

class ItemStack:
    def __init__(self, stack_size, item_type):
        self.stack_size: int = stack_size
        self.item_type: ItemType = item_type

    def get_item(self):
        return ITEM_DEFINITIONS[self.item_type]

    def on_item_right_click(self, world, entity_player, mouse_world) -> None:
        self.get_item().on_item_right_click(self, world, entity_player, mouse_world)

    def add_item(self, amount=1) -> int:
        if self.is_full():
            return amount

        max_stack_size = self.get_item().max_stack_size
        new_stack_size = self.stack_size + amount

        if new_stack_size > max_stack_size:
            self.stack_size = max_stack_size
            return new_stack_size - max_stack_size

        self.stack_size = new_stack_size
        return 0

    def remove_item(self, amount=1) -> None:
        if self.stack_size > 0:
            self.stack_size -= amount

    def is_full(self) -> bool:
        return self.stack_size >= self.get_item().max_stack_size