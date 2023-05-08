# import numpy
from OpenGL.GL import GL_TRIANGLES
from Engine.Objects.Base import Base as Base_object
# from Engine.Rendering.Render_bases.SDL import SDLBase
# currently I don't want sdl
from Engine.Rendering.Render_bases.GLFW import GLFWBase
from Engine.Shaders.Shader_controller import ShaderController
from Engine.Logger import Logger


class Main:
    def __init__(self):
        self.logger = Logger()
        self.logger.create_file()
        # render base, can be changed do SDL
        self.render_base = GLFWBase()
        self.shader_controller = ShaderController()
        # set this before initialize

    def initialize(self):
        """
        initializes render api, base, shaders and window
        """
        self.render_base.prepare()
        self.render_base.create_window(800, 600)
        self.shader_controller.get_shaders_dict()
        self.shader_controller.get_shaders_files()
        self.shader_controller.compile_shaders()

    def add_object(self, obj=None, triangles=None, vertices=None, primitive=GL_TRIANGLES):
        if obj is not None:
            self.render_base.objects += [obj]
        else:
            obj = Base_object()
            obj.mesh.apply_points(vertices=vertices, triangles=triangles)
            obj.mesh.set_primitive_type(primitive=primitive)
            self.render_base.objects += [obj]

    def start(self):
        Logger().log("Started render loop", "Main")

        while not self.render_base.should_close():
            self.render_base.step(self.shader_controller)

        self.render_base.terminate()

        Logger().log("Render loop exited", "Main")
