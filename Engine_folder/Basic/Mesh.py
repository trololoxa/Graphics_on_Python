import ctypes

from OpenGL import GL
from numpy import array, float32, uint32

from Engine_folder.Logger import log


class Mesh:
    """
    Mesh instance, holds vertices and triangles values, called for rendering \n
    Vertices: numpy array, stores each vertex position. Each vertex has 3 float32 values \n
    Colors: numpy array, stores each vertex color. Each vertex has 3 float32 values \n
    Triangles: numpy array, stores vertex element combinations. Each combination has 3 uint32 values \n
    TexCoords: Not Implemented
    """

    def __init__(self):
        # TODO: mesh not related to OpenGL for future Vulkan and DirectX
        # Main values, stored in buffers
        self._vertices = array([], dtype=float32)
        self._triangles = array([], dtype=uint32)
        self._colors = array([], dtype=float32)
        self._texcoord = array([], dtype=float32)
        # Variables used in final rendering part
        self._num_points = 0
        self.primitive_type = GL.GL_TRIANGLES
        # buffers
        self.EBO = None
        self.VAO = None
        self.VBO = None

        # Creates and initializes all buffers
        self.init_buffers()

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
        log("Texcoord changing not implemented rn", "Mesh", "Warn")

    def init_buffers(self):
        # Creates buffers
        self.VAO = GL.glGenVertexArrays(1)
        self.VBO = GL.glGenBuffers(1)
        self.EBO = GL.glGenBuffers(1)

        # Binds all arrays
        GL.glBindVertexArray(self.VAO)

        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.EBO)

        # pointer to vertices
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 24,
                                 ctypes.c_void_p(0))
        GL.glEnableVertexAttribArray(0)

        # pointer to colors
        GL.glVertexAttribPointer(1, 3, GL.GL_FLOAT, GL.GL_FALSE, 24,
                                 ctypes.c_void_p(12))
        GL.glEnableVertexAttribArray(1)

        # unbind because we don't draw right now
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)
        GL.glBindVertexArray(0)

    def bind_new_vbo(self, vertices=None, colors=None):
        # checks for given colors and vertices
        if vertices is not None:
            vertices = array(vertices, dtype=float32)
        else:
            vertices = self.vertices

        if colors is not None:
            colors = array(colors, dtype=float32)
        else:
            colors = self.colors

        # resizes colors to vertices len
        if len(vertices) > len(colors):
            # noinspection PyTypeChecker
            colors.resize(len(vertices), refcheck=False)

        # creates vbo array cuz renderer use combined array
        arr = []
        for i in range(2, len(vertices), 3):
            arr += [vertices[i - 2], vertices[i - 1], vertices[i], colors[i - 2], colors[i - 1], colors[i]]
        arr = array(arr, dtype=float32)

        # only applies array to vbo if length of vertices is not zero
        if len(arr) > 0:
            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, self.VBO)

            # If buffer size don't changed it just rewrites data
            if len(self._vertices) == len(vertices):
                GL.glBufferSubData(GL.GL_ARRAY_BUFFER, 0, arr.nbytes, arr)
            # Else it just allocates new data
            else:
                GL.glBufferData(GL.GL_ARRAY_BUFFER, arr.nbytes, arr, GL.GL_STATIC_DRAW)

            GL.glBindBuffer(GL.GL_ARRAY_BUFFER, 0)

        # Saves colors and vertices so you can access trough code
        self._vertices = vertices
        self._colors = colors

    def bind_new_ebo(self, ebo):
        # saves ebo as compatible array
        ebo = array(ebo, dtype=uint32)

        # this thing used for rendering, better not to change it yourself
        self.num_points = len(ebo)

        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, self.EBO)

        # Same as vbo checker
        if len(self._triangles) == len(ebo):
            GL.glBufferSubData(GL.GL_ELEMENT_ARRAY_BUFFER, 0, ebo.nbytes, ebo)
        else:
            GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER, ebo.nbytes, ebo, GL.GL_STATIC_DRAW)

        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER, 0)

        # Saves triangles so you can access this trough code
        self._triangles = ebo

    def set_primitive_type(self, primitive):
        # Use this only if your data don't use GL_TRIANGLES
        self.primitive_type = primitive
