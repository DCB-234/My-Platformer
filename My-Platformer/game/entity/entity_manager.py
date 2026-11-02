class EntityManager:
    def __init__(self, world):
        self.world = world

    def construct_entity(self) -> 'Entity':
        ...

    def spawn_entity(self) -> None:
        ...

    def despawn_entity(self) -> None:
        ...

    def is_valid_entity_spawn(self) -> bool:
        ...
