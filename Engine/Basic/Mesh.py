# import ctypes

from OpenGL import GL
from numpy import array, float32


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
        self._applied_vertices = []
        self._num_points = 0
        self.primitive_type = GL.GL_TRIANGLES
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
            self._vertices = vertices
        if triangles is not None:
            self._triangles = triangles

        if len(self._vertices) != len(self._triangles) and triangles is not None:
            raise Exception("vertices len != triangles len")

        if triangles is not None:
            self._applied_vertices = array([self._vertices[index] for index in self._triangles], dtype=float32)
        else:
            self._applied_vertices = array(self._vertices, dtype=float32)

        self.init_arrays()

    def init_arrays(self):
        self.VAO = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.VAO)

        # Need VBO for triangle vertices and colours
        self.VBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self._applied_vertices.nbytes, self._applied_vertices,
                        GL.GL_STATIC_DRAW)

        # enable array and set up data
        GL.glEnableVertexAttribArray(0)
        # GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0,
                                 None)
        # the last parameter is a pointer
        # GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 0,
        #                          ctypes.c_void_p(48))

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindVertexArray(0)

    def set_num_points(self, num):
        self._num_points = num

    def set_primitive_type(self, primitive):
        self.primitive_type = primitive
