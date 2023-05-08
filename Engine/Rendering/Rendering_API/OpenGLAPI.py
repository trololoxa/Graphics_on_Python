from OpenGL import GL
import ctypes
from Engine.Logger import Logger


class OpenGLRender:
    """Renders any given object using opengl"""
    def __init__(self):
        self.wireframe_mode = False
        Logger().log("Using OpenGL Rendering API", "Renderer")

    @staticmethod
    def render(shader_mesh_array):
        for key in shader_mesh_array:
            key.activate()
            for mesh in shader_mesh_array[key]:
                if mesh.VAO is None:
                    continue

                GL.glBindVertexArray(mesh.VAO)

                GL.glDrawElements(mesh.primitive_type, mesh.num_points, GL.GL_UNSIGNED_INT, ctypes.c_void_p(0))

                # GL.glBindVertexArray(0)
            GL.glUseProgram(0)

    @staticmethod
    def clear_background(background_color=None):
        if background_color is None:
            background_color = (0.2, 0.3, 0.3, 1.0)
        # clear window and set background color
        GL.glClearColor(*background_color)
        GL.glClear(GL.GL_COLOR_BUFFER_BIT)

    @staticmethod
    def set_viewport(window, width, height):
        GL.glViewport(0, 0, width, height)

    def set_wireframe_mode(self, mode: bool):
        if mode and not self.wireframe_mode:
            Logger().log("Wireframe mode rendering enabled", "Renderer")
            self.wireframe_mode = mode
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_LINE)
        if not mode and self.wireframe_mode:
            Logger().log("Wireframe mode rendering disabled", "Renderer")
            self.wireframe_mode = mode
            GL.glPolygonMode(GL.GL_FRONT_AND_BACK, GL.GL_FILL)
