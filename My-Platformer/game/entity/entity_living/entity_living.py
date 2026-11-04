from game.entity.entity import Entity

class EntityLiving(Entity):
    def __init__(self, hitbox, start_x:int=0, start_y:int=0, start_speed_x:int=0, start_speed_y:int=0):
        super().__init__(
            hitbox=hitbox,
            start_x=start_x,
            start_y=start_y,
            start_speed_x=start_speed_x,
            start_speed_y=start_speed_y
        )

        self.walk_time: int = 0
        self.walk_progress: float = 0.0
        self.is_walking: bool = False
        self.max_walk_time: int = 15
        self.max_walk_progress: int = 45

        self.prev_walk_progress: float = 0.0
        self.interp_walk_progress: float = 0.0

    def tick_update(self, world, game_rules) -> None:
        super().tick_update(world, game_rules)
        self.update_walk_progress()
    
    def update_walk_progress(self) -> None:
        if self.is_walking:
            self.walk_time += 1
            if self.walk_time >= self.max_walk_time / 2:
                self.is_walking = False
                self.walk_time = 0
        else:
            self.walk_time = 0

        self.prev_walk_progress = self.walk_progress
        self.walk_progress = self.walk_time / self.max_walk_time

    def interpolate_entity(self, partial_tick) -> None:
        super().interpolate_entity(partial_tick)
        # Interpolate walk progress
        self.interp_walk_progress = (
            self.prev_walk_progress + 
            (self.walk_progress - self.prev_walk_progress) * partial_tick
        )