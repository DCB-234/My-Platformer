class ItemDefinition:
    def __init__(self):
        self.is_stackable: bool = True
        self.max_stack_size: int = 64

    def on_item_use(self, item_stack, world, entity_player) -> None:
        item_stack.stack_size -= 1

    def on_item_right_click(self, item_stack, world, entity_player, mouse_world) -> None:
        return