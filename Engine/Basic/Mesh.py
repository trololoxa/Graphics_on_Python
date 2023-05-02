from OpenGL import GL
import ctypes
from numpy import array


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
        self._num_triangles = 0
        self.VAO = None
        self.VBO = None

    @property
    def num_triangles(self):
        return self._num_triangles

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

        if self._triangles is not None:
            self._applied_vertices = array([self._vertices[index] for index in self._triangles])
        else:
            self._applied_vertices = array(self._vertices)

        self.init_arrays()

    def init_arrays(self):
        self.VAO = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(self.VAO)

        # Need VBO for triangle vertices and colours
        self.VBO = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, self.vertices.nbytes, self.vertices,
                        GL.GL_STATIC_DRAW)

        # enable array and set up data
        GL.glEnableVertexAttribArray(0)
        GL.glEnableVertexAttribArray(1)
        GL.glVertexAttribPointer(0, 4, GL.GL_FLOAT, GL.GL_FALSE, 0,
                                 None)
        # the last parameter is a pointer
        GL.glVertexAttribPointer(1, 4, GL.GL_FLOAT, GL.GL_FALSE, 0,
                                 ctypes.c_void_p(48))

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindVertexArray(0)

    def set_num_triangles(self, num):
        self._num_triangles = num
