from Engine.Main import Main


if __name__ == '__main__':
    main = Main()
    main.initialize()

    main.add_object(vertices=[
        # Vertex Positions
        0.0, 0.5, 0.0, 1.0,
        0.5, -0.366, 0.0, 1.0,
        -0.5, -0.366, 0.0, 1.0,

        # Vertex Colours
        1.0, 0.0, 0.0, 1.0,
        0.0, 1.0, 0.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
    ])
    main.add_object(vertices=[
        # Vertex Positions
        0.0, -0.5, 0.0, 1.0,
        -0.5, 0.366, 0.0, 1.0,
        0.5, 0.366, 0.0, 1.0,

        # Vertex Colours
        1.0, 0.0, 0.0, 1.0,
        0.0, 1.0, 0.0, 1.0,
        0.0, 0.0, 1.0, 1.0,
    ])
    main.start()
