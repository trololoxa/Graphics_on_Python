from TSGEngine.Rendering import Texture


class TextureHandler:
    def __init__(self):
        self.textures = {}
        self.fallback_texture = None

    def initialize(self, fallback_texture_path):
        self.fallback_texture = fallback_texture_path
        self._add_fallback_texture()

    def add_texture(self, name: str, *files):
        self.textures[name] = Texture(*files, fallback_texture=self.fallback_texture)

    def _add_fallback_texture(self):
        texture = Texture(self.fallback_texture, auto_compile=False)
        self.fallback_texture = texture.initialize()
