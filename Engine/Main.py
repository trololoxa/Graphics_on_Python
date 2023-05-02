from Engine.Rendering.Render_bases.SDL import SDLBase
from Engine.Objects.Base import Base as Base_object
from Engine.Shaders.Shader_controller import ShaderController
import numpy


class Main:
    def __init__(self):
        self.render_base = SDLBase()
        self.shader_controller = ShaderController()

    def initialize(self):
        self.render_base.prepare()
        self.shader_controller.get_shaders()
        self.render_base.create_window(800, 600)
        self.shader_controller.compile_shaders()

    def add_object(self, obj=None, triangles=None, vertices=None):
        if obj is not None:
            self.render_base.objects += [obj]
        else:
            obj = Base_object()
            obj.mesh.apply_points(vertices=vertices, triangles=triangles)
            obj.mesh.set_num_triangles(3)
            self.render_base.objects += [obj]

    def start(self):
        self.render_base.infinite_loop(self.shader_controller)


if __name__ == '__main__':
    main = Main()
    main.initialize()

    main.add_object(vertices=numpy.array([
        # Vertex Positions
        0.0, 0.5, 0.0, 1.0,
        0.5, -0.366, 0.0, 1.0,
        -0.5, -0.366, 0.0, 1.0,

        # Vertex Colours
        1.0, 0.0, 0.0, 1.0,
        0.0, 1.0, 0.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
    ], dtype=numpy.float32))
    main.add_object(vertices=numpy.array([
        # Vertex Positions
        0.0, -0.5, 0.0, 1.0,
        0.5, 0.366, 0.0, 1.0,
        -0.5, 0.366, 0.0, 1.0,

        # Vertex Colours
        1.0, 0.0, 0.0, 1.0,
        0.0, 1.0, 0.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
    ], dtype=numpy.float32))
    main.start()
