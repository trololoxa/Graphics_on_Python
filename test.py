from Engine_folder.Main import Main
from Engine_folder.Objects.Camera import Camera

try:
    if __name__ == '__main__':
        main = Main()
        main.initialize()

        camera = Camera()
        main.add_object(obj=camera)
        camera.mesh.vertices = [
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.5, 0.5, 0.0,
            -0.5, 0.5, 0.0,
            1.0, 0.5, 0.0,
        ]
        camera.mesh.colors = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
            1.0, 0.0, 1.0,
            1.0, 0.0, 1.0,
        ]
        camera.mesh.triangles = [
            0, 1, 3,
            1, 2, 3,
            3, 1, 4
        ]

        camera2 = Camera()
        main.add_object(obj=camera2)
        camera2.mesh.vertices = [
            -0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.5, 0.5, 0.0,
            -0.5, 0.5, 0.0,
            1.0, 0.5, 0.0,
        ]
        camera2.mesh.colors = [
            1.0, 0.0, 0.0,
            0.0, 1.0, 0.0,
            0.0, 0.0, 1.0,
            1.0, 0.0, 1.0,
            1.0, 0.0, 1.0,
        ]
        camera2.mesh.triangles = [
            0, 1, 3,
            1, 2, 3,
            3, 1, 4
        ]
        main.start()
except KeyboardInterrupt as e:

    input()

    """main.add_object(vertices=[
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
    ]"""
    # main.shader_manager.set_uniform('main', 'offset', 0.0)
