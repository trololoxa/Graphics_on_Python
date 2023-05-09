import ctypes

import numpy
from OpenGL import GL
from numpy import array, float32, uint32

from Engine.Logger import Logger


class Mesh:
    """
    Mesh instance, holds vertices and triangles values, called for rendering
    Vertices: vec3 list, storing each points position
    Triangles: int list, holds info about what points connected like [0,1,5,0,5,4]
                                                                     1st tr|2nd tr
    """

    def __init__(self):
        self._vertices = array([], dtype=float32)
        self._triangles = array([], dtype=uint32)
        self._colors = array([], dtype=float32)
        self._texcoord = array([], dtype=float32)
        self._num_points = 0
        self.primitive_type = GL.GL_TRIANGLES
        self.EBO = None
        self.VAO = None
        self.VBO = None

        self.init_arrays()

    @property
    def num_points(self):
        return self._num_points

    @num_points.setter
    def num_points(self, num):
        self._num_points = num

    @property
    def vertices(self):
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        self.bind_new_vbo(vertices=vertices)

    @property
    def triangles(self):
        return self._triangles

    @triangles.setter
    def triangles(self, indexes):
        self.bind_new_ebo(indexes)

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, colors):
        self.bind_new_vbo(colors=colors)

    @property
    def texcoord(self):
        return self._texcoord

    @texcoord.setter
    def texcoord(self, texcoord):
        Logger().log("Texcoord changing not implemented rn", "Mesh", "Warn")

    def init_arrays(self):
        self.VAO = GL.glGenVertexArrays(1)
        self.VBO = GL.glGenBuffers(1)
        self.EBO = GL.glGenBuffers(1)

        GL.glBindVertexArray(self.VAO)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self._vertices.nbytes, self._vertices,
                        GL.GL_STATIC_DRAW)

        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, self._triangles.nbytes, self._triangles,
                        GL.GL_STATIC_DRAW)

        # vertices
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 24,
                                 ctypes.c_void_p(0))
        GL.glEnableVertexAttribArray(0)

        # colors
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 24,
                                 ctypes.c_void_p(12))
        GL.glEnableVertexAttribArray(1)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindVertexArray(0)

    def bind_new_vbo(self, vertices=None, colors=None):
        if vertices is not None:
            vertices = array(vertices, dtype=float32)
        else:
            vertices = self.vertices

        if colors is not None:
            colors = array(colors, dtype=float32)
        else:
            colors = self.colors

        if len(vertices) > len(colors):
            colors.resize(len(vertices), refcheck=False)

        arr = []
        for i in range(2, len(vertices), 3):
            arr += [vertices[i-2], vertices[i-1], vertices[i], colors[i-2], colors[i-1], colors[i]]
        arr = array(arr, dtype=float32)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)

        if len(self._vertices) == len(vertices):
            GL.glBufferSubData(GL.GL_ARRAY_BUFFER, 0, arr.nbytes, arr)
        else:
            GL.glBufferData(GL.GL_ARRAY_BUFFER, arr.nbytes, arr, GL.GL_STATIC_DRAW)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

        self._vertices = vertices
        self._colors = colors

    def bind_new_ebo(self, ebo):
        ebo = array(ebo, dtype=uint32)

        self.num_points = len(ebo)

        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.EBO)

        if len(self._triangles) == len(ebo):
            GL.glBufferSubData(GL.GL_ELEMENT_ARRAY_BUFFER, 0, ebo.nbytes, ebo)
        else:
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, ebo.nbytes, ebo, GL.GL_STATIC_DRAW)

        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)

        self._triangles = ebo

    def set_primitive_type(self, primitive):
        self.primitive_type = primitive
