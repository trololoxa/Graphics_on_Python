from Engine.Main import Main
from Engine.Objects.Camera import Camera


if __name__ == '__main__':
    main = Main()
    main.initialize()

    camera = Camera()
    main.add_object(obj=camera)

    main.add_object(vertices=[
        #  Vertices                 Colors
        -0.5, -0.5, 0.0,        1.0, 0.0, 0.0,
        0.5, -0.5, 0.0,         0.0, 1.0, 0.0,
        0.5, 0.5, 0.0,          0.0, 0.0, 1.0,
        -0.5, 0.5, 0.0,         1.0, 0.0, 1.0,
    ], triangles=[
        0, 1, 3,
        1, 2, 3,
    ])

    main.render_base.objects[1].mesh.vertices = [
        #  Vertices
        -0.5, -0.5, 0.0,
        0.5, -0.5, 0.0,
        0.5, 0.5, 0.0,
        -0.5, 0.5, 0.0,
        1.0, 0.5, 0.0,
    ]
    main.render_base.objects[1].mesh.colors = [
        1.0, 0.0, 0.0,
        0.0, 1.0, 0.0,
        0.0, 0.0, 1.0,
        1.0, 0.0, 1.0,
        1.0, 0.0, 1.0,
    ]
    main.render_base.objects[1].mesh.triangles = [
        0, 1, 3,
        1, 2, 3,
        3, 1, 4
    ]
    #main.shader_controller.set_uniform('main', 'offset', 0.0)

    main.start()
