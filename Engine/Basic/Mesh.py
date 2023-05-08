import ctypes

from OpenGL import GL
from numpy import array, float32, uint32


class Mesh:
    """
    Mesh instance, holds vertices and triangles values, called for rendering
    Vertices: vec3 list, storing each points position
    Triangles: int list, holds info about what points connected like [0,1,5,0,5,4]
                                                                     1st tr|2nd tr
    """
    def __init__(self):
        self._vertices = []
        self._triangles = []
        self._num_points = 0
        self.primitive_type = GL.GL_TRIANGLES
        self.EBO = None
        self.VAO = None
        self.VBO = None

    @property
    def num_points(self):
        return self._num_points

    @property
    def vertices(self):
        return self._vertices
    
    @property
    def triangles(self):
        return self._triangles
    
    def apply_points(self, vertices=None, triangles=None):
        if vertices is not None:
            self._vertices = array(vertices, dtype=float32)
        if triangles is not None:
            self._triangles = array(triangles, dtype=uint32)
        else:
            self._triangles = array(range(round(len(self._vertices) / 3 / 2)), dtype=uint32)

        self._num_points = len(self._triangles)

        self.init_arrays()

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

    def set_num_points(self, num):
        self._num_points = num

    def set_primitive_type(self, primitive):
        self.primitive_type = primitive
