# import numpy
from OpenGL.GL import GL_TRIANGLES
from Engine.Objects.Base import Base as Base_object
# from Engine.Rendering.Render_bases.SDL import SDLBase
# currently I don't want sdl
from Engine.Rendering.Render_bases.GLFW import GLFWBase
from Engine.Shaders.Shader_controller import ShaderController


class Main:
    def __init__(self):
        self.render_base = GLFWBase()
        self.shader_controller = ShaderController()
        self.wireframe_mode = False

    def initialize(self):
        self.render_base.prepare()
        self.shader_controller.get_shaders()
        self.render_base.create_window(800, 600)
        self.shader_controller.compile_shaders()
        if self.wireframe_mode:
            from OpenGL.GL import glPolygonMode, GL_FRONT_AND_BACK, GL_LINE
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)

    def add_object(self, obj=None, triangles=None, vertices=None, primitive=GL_TRIANGLES):
        if obj is not None:
            self.render_base.objects += [obj]
        else:
            obj = Base_object()
            obj.mesh.apply_points(vertices=vertices, triangles=triangles)
            obj.mesh.set_primitive_type(primitive=primitive)
            self.render_base.objects += [obj]

    def start(self):
        # TODO: step func
        self.render_base.infinite_loop(self.shader_controller)
