class PlatformComponent:
    def __init__(self, up_button_name='w', down_button_name='s'):
        self.speed = 1
        self.speed_cache = 0
        self.up = up_button_name
        self.down = down_button_name
