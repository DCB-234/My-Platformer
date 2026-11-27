class ItemDefinition:
    def __init__(self, MAX_STACK_SIZE: int = 64):
        self.MAX_STACK_SIZE: int = MAX_STACK_SIZE

    def on_item_use(self, item_stack, world, entity_player) -> None:
        item_stack.stack_size -= 1

    def on_item_right_click(self, item_stack, world, entity_player, mouse_world) -> None:
        return