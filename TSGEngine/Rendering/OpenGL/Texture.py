import cv2
from OpenGL import GL
from pathlib import Path


class Texture:
    def __init__(self, file_path, fallback_texture=None, wrap_mode=None, auto_compile=True):
        self.file_path = str(Path(file_path).absolute())

        self.image = None
        self.texture = None

        self.fallback_texture = fallback_texture

        self.channels = None
        self.height = None
        self.width = None

        self.wrap_mode = wrap_mode

        self.error = False

        if auto_compile:
            self.initialize()

    def initialize(self):
        try:
            self.load_images()
            self.generate_texture()

            if not self.fallback_texture:
                return self
        except KeyError:
            self.error = True

            self.image = self.fallback_texture.image
            self.channels = self.fallback_texture.channels
            self.height = self.fallback_texture.height
            self.width = self.fallback_texture.width
            self.texture = self.fallback_texture.texture

    def load_images(self):
        self.image = cv2.imread(self.file_path)
        self.image = cv2.flip(self.image, 0)
        # self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        self.width, self.height, self.channels = self.image.shape

    def generate_texture(self):
        self.texture = GL.glGenTextures(1)

        self.bind()

        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_LINEAR_MIPMAP_LINEAR)
        GL.glTexParameteri(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_LINEAR)

        GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, GL.GL_RGB, self.width, self.height, 0, GL.GL_BGR, GL.GL_UNSIGNED_BYTE, self.image)
        GL.glGenerateMipmap(GL.GL_TEXTURE_2D)

        self.unbind()

    def bind(self):
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)

    @staticmethod
    def unbind():
        GL.glBindTexture(GL.GL_TEXTURE_2D, 0)