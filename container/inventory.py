from game.item.item_stack import ItemStack
from game.item.item_type import ItemType

class Inventory:
    def __init__(self, INVENTORY_SIZE):
        self.INVENTORY_SIZE: int = INVENTORY_SIZE
        self.slots: list = [None for _ in range(self.INVENTORY_SIZE)]

    def add_item(self, item_type:ItemType, slot_index:int=None, amount=1) -> int:

        if amount <= 0:
            return 0

        if slot_index is not None:
            if slot_index >= self.INVENTORY_SIZE:
                return amount

            slot = self.slots[slot_index]

            # Empty slot
            if not slot:
                self.create_new_stack(amount, item_type, slot_index)
                return 0

            # Add to existing stack
            if slot.item_type == item_type:
                return slot.add_item(amount=amount)

            return amount

        # Find if same item type already exists
        for slot in self.slots:
            if not slot:
                continue

            if slot.item_type == item_type and not slot.is_full():
                amount = slot.add_item(amount=amount)
                if amount == 0:
                    return 0

        # Choose first available empty slot
        for i, slot in enumerate(self.slots):
            if not slot:
                self.create_new_stack(amount, item_type, i)
                return 0

        return amount

    def transfer_stack(self, slot_index: int, new_slot_index: int, container=None) -> None:
        if container is None:
            container = self

        if not self.is_in_boundary(slot_index) or not container.is_in_boundary(new_slot_index):
            return

        slot = self.slots[slot_index]
        if slot is None:
            return

        remaining_amount = container.add_item(slot.item_type, new_slot_index, slot.stack_size)
        if remaining_amount == 0:
            self.slots[slot_index] = None
        else:
            slot.stack_size = remaining_amount

    def create_new_stack(
        self, stack_size: int, item_type: ItemType, slot_index: int
    ) -> None:
        self.slots[slot_index] = ItemStack(
            stack_size=stack_size, item_type=item_type
        )

    def is_in_boundary(self, *indexes) -> bool:
        return all(0<=index<self.INVENTORY_SIZE for index in indexes)