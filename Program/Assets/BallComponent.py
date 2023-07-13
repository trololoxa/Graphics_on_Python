from random import uniform, choice
from TSGEngine.Core.Math import vec2


class BallComponent:
    def __init__(self):
        self.speed: float = 1.5
        self.speed_cache = 0
        self.direction = vec2(choice([uniform(0.2, 0.6), uniform(-0.2, -0.6)]),
                              choice([uniform(0.2, 0.6), uniform(-0.2, -0.6)]))
        self.score = [0, 0]
