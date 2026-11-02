from game.entity.entity_position import EntityPosition
from game.helper.helper_entity import HelperEntity

class Entity(HelperEntity):
    def __init__(self):
        self.position = EntityPosition()

    def on_despawn(self) -> None:
        ...

    def interpolate_entity(self, partial_tick) -> None:
        # Interpolate position
        self.position.interp_x = (
            self.position.prev_x + (self.position.x - self.position.prev_x) * partial_tick
        )
        self.position.interp_y = (
            self.position.prev_y + (self.position.y - self.position.prev_y) * partial_tick
        )
