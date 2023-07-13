import glfw
from glfw import GLFW

from imgui.integrations.glfw import GlfwRenderer
import imgui


class GLFWWindowHandler:
    def __init__(self):
        self.window = None
        self.callback_funcs = {'key': glfw.set_key_callback, 'framebuffer_size': glfw.set_framebuffer_size_callback}
        self.impl = None
        self.height, self.width = 0, 0

    @staticmethod
    def initialize():
        if not glfw.init():
            return

        # Force OpenGL 4.6 'core' context.
        GLFW.glfwWindowHint(GLFW.GLFW_CONTEXT_VERSION_MAJOR, 4)
        GLFW.glfwWindowHint(GLFW.GLFW_CONTEXT_VERSION_MINOR, 6)
        GLFW.glfwWindowHint(GLFW.GLFW_OPENGL_PROFILE, GLFW.GLFW_OPENGL_CORE_PROFILE)
        GLFW.glfwWindowHint(GLFW.GLFW_OPENGL_FORWARD_COMPAT, True)

        GLFW.glfwWindowHint(GLFW.GLFW_RESIZABLE, False)

        imgui.create_context()

    def create_window(self, width=800, height=600, title='Example Title'):
        self.window = glfw.create_window(width, height, title, None, None)

        self.width, self.height = width, height
        if not self.window:
            self.terminate()

        glfw.make_context_current(self.window)

        self.impl = GlfwRenderer(self.window)

    def set_callback(self, name, callback):
        if name not in self.callback_funcs:
            return

        self.callback_funcs[name](self.window, callback)

    @staticmethod
    def pool_events():
        glfw.poll_events()

    def gui_new_frame(self):
        self.impl.process_inputs()

        imgui.new_frame()

    def swap_buffers(self):
        imgui.render()
        self.impl.render(imgui.get_draw_data())

        glfw.swap_buffers(self.window)

    def should_close(self):
        return glfw.window_should_close(self.window)

    def terminate(self):
        self.impl.shutdown()
        glfw.terminate()

    def set_framebuffer_size_callback(self, draw_function, viewport_function):
        viewport_function(0, 0, self.width, self.height)

        def framebuffer_callback(window, width, height):
            if width > 0 and height > 0:
                viewport_function(0, 0, width, height)
                self.width, self.height = width, height

            draw_function()

        self.set_callback('framebuffer_size', framebuffer_callback)
