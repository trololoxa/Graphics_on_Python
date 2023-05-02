import sys
import ctypes
import numpy

from OpenGL import GL, GLU
from OpenGL.GL import shaders
from OpenGL.arrays import vbo

import sdl2
from sdl2 import video
from numpy import array


class OpenGLRender:
    """Renders any given object using opengl"""
    def render(self, shader_mesh_array):
        for key in shader_mesh_array:
            GL.glUseProgram(key)
            for mesh in shader_mesh_array[key]:
                GL.glBindVertexArray(mesh.VAO)

                GL.glDrawArrays(GL.GL_TRIANGLES, 0, mesh.num_triangles)

                GL.glBindVertexArray(0)
            GL.glUseProgram(0)
