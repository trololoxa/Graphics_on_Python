from pathlib import Path

from TSGEngine.World import World
from TSGEngine.Window import GLFWWindowHandler
from TSGEngine.Input import InputHandler
from TSGEngine.World.Systems.Render_system import RenderSystem

import time


class Main:
    def __init__(self):
        self.core_assets_folder = None

        self.window = GLFWWindowHandler()
        self.settings = None
        self.logger = None

        # world and handler
        self.world = World()
        self.input_handler = InputHandler()

        self._gui_func = lambda: None

    def set_gui_func(self, func):
        self._gui_func = func if func else self._gui_func

    def initialize(self, core_assets_folder):
        self.core_assets_folder = Path(core_assets_folder).absolute()

        self.window.initialize()
        self.world.initialize()

    def past_window_initialize(self):
        self.world.shader_manager.initialize()
        self.window.set_callback('key', self.input_handler.input_callback)
        self.window.set_framebuffer_size_callback(self.step, self.world.get_system(RenderSystem).renderer.viewport())
        self.world.input_manager = self.input_handler
        self.world.past_window_initialize(self.core_assets_folder.joinpath('fallback.jpg'))

    def loop(self, gui_func=None):
        self.set_gui_func(gui_func)

        while not self.window.should_close():
            self.pooled_step()

    def pooled_step(self):
        self.window.pool_events()

        self.step()

        # print(1 / self.world.dt)  # print fps

    def step(self):
        start_time = time.perf_counter()

        self.window.gui_new_frame()

        self.world.step()

        self._gui_func()

        self.window.swap_buffers()

        self.world.dt = time.perf_counter() - start_time
# TODO: unsure about funcs? Do it in the main class
