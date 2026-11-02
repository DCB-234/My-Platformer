from dataclasses import dataclass

@dataclass
class EntityPosition:
    prev_x: int = 0
    prev_y: int = 0
    x: int = 0
    y: int = 0
    interp_x: float = 0.0
    interp_y: float = 0.0