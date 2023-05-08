import glfw
import numpy

from glfw.GLFW import glfwWindowHint, GLFW_CONTEXT_VERSION_MAJOR, GLFW_CONTEXT_VERSION_MINOR, GLFW_OPENGL_PROFILE, \
                      GLFW_OPENGL_CORE_PROFILE, GLFW_OPENGL_FORWARD_COMPAT

from Engine.Rendering.Rendering_API.OpenGLAPI import OpenGLRender

import time

from Engine.Logger import Logger


class GLFWBase:
    """
    Basic GLFW loop
    render_api renders
    objects list can be changed with scene
    """
    def __init__(self):
        self.render_api = OpenGLRender()
        self.objects = []
        self.window = None
        self.context = None
        self.fps = 0

    @staticmethod
    def prepare():
        # Initialize the library
        if not glfw.init():
            return

        # Force OpenGL 4.6 'core' context.
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4)
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 6)
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, True)

        Logger().log("Using GLFW Render Base", "Renderer")

    def create_window(self, width=800, height=600, name="OpenGL demo"):
        # Create a windowed mode window and set callbacks
        self.window = glfw.create_window(width, height, name, None, None)
        if not self.window:
            Logger().log("Failed to create GLFW window", "Renderer", "Critical")
            self.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)

        self.render_api.set_viewport(None, width, height)

        # set callbacks
        glfw.set_framebuffer_size_callback(self.window, self.render_api.set_viewport)

        Logger().log("Created GLFW window", "Renderer")

    def process_input(self, window):
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)
        if glfw.get_key(window, glfw.KEY_SPACE) == glfw.PRESS:
            self.render_api.set_wireframe_mode(True)
        elif glfw.get_key(window, glfw.KEY_SPACE) == glfw.RELEASE:
            self.render_api.set_wireframe_mode(False)

    def infinite_loop(self, shader_controller):
        while not self.should_close():
            self.step(shader_controller)

        self.terminate()

    def step(self, shader_controller):
        start_time = time.time_ns()

        self.process_input(window=self.window)

        self.render_api.clear_background()

        # render
        self.render_api.render(self.create_mesh_objects_array(shader_controller))

        glfw.swap_buffers(self.window)
        glfw.poll_events()

        end_time = time.time_ns()
        elapsed_time = end_time - start_time

        # get program fps
        if elapsed_time > 0:
            self.fps = (1 / elapsed_time) * 1000000000
            # print(self.fps)
        else:
            self.fps = numpy.inf
            # print('too much fps')

    def should_close(self):
        return glfw.window_should_close(self.window)

    @staticmethod
    def terminate():
        glfw.terminate()

    def create_mesh_objects_array(self, shader_controller):
        return_array = {}
        for obj in self.objects:
            program = shader_controller.shaders[shader_controller.directories[obj.shader_id]]
            if program not in return_array:
                return_array[program] = [obj.mesh]
            else:
                return_array[program] += [obj.mesh]

        return return_array
