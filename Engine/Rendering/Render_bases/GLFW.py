import glfw
import numpy

from glfw.GLFW import glfwWindowHint, GLFW_CONTEXT_VERSION_MAJOR, GLFW_CONTEXT_VERSION_MINOR, GLFW_OPENGL_PROFILE, \
                      GLFW_OPENGL_CORE_PROFILE, GLFW_OPENGL_FORWARD_COMPAT
from OpenGL.GL import glViewport, glClear, glClearColor, GL_COLOR_BUFFER_BIT

from Engine.Rendering.Rendering_API.OpenGLAPI import OpenGLRender

import time


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

    def create_window(self, width=800, height=600, name="OpenGL demo"):
        # Create a windowed mode window and its OpenGL context
        self.window = glfw.create_window(width, height, name, None, None)
        if not self.window:
            glfw.terminate()
            return

        # Make the window's context current
        glfw.make_context_current(self.window)

        glViewport(0, 0, width, height)

        glfw.set_framebuffer_size_callback(self.window, self._framebuffer_size_callback)

    @staticmethod
    def _framebuffer_size_callback(window, width, height):
        glViewport(0, 0, width, height)

    def infinite_loop(self, shader_controller):
        start_time = time.time_ns()
        while not glfw.window_should_close(self.window):
            glClearColor(0.2, 0.3, 0.3, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            self.render_api.render(self.create_mesh_objects_array(shader_controller))

            glfw.swap_buffers(self.window)
            glfw.poll_events()

            end_time = time.time_ns()
            elapsed_time = end_time-start_time

            if elapsed_time > 0:
                self.fps = (1/elapsed_time) * 1000000000
                print(self.fps)
            else:
                self.fps = numpy.inf
                print('too much fps')

            start_time = end_time

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
