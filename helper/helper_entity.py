import math

class HelperEntity:
    @staticmethod
    def find_angle(pos_1, pos_2) -> float:
        x1, y1 = pos_1
        x2, y2 = pos_2
        dx, dy = x1-x2, y1-y2
        angle_rad = math.atan2(dy, dx)
        return math.degrees(angle_rad)