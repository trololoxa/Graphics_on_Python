class Transform:
    """
    Transform, every object in scene should have that
    position is Vec3
    rotation is Vec3 for euler, vec3(Vec3 for i in range(3)) for shit or vec4 for quaternions
    scale is vec3 for each axis
    matrix is 4x4 matrix for storing any upper values and applying them

    should have move, rotate, scale funcs, and mb matrix should be property
    """
    def __init__(self):
        self.position = None
        self.rotation = None
        self.scale = None
        self.matrix = None
