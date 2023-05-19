class Collider:
    """
    Collider, every part is copied from mesh
    vertices from mesh
    triangles from mesh
    AABB from vertices as minmax
    """
    def __init__(self):
        self.vertices = None
        self.triangles = None
        self.AABB = None
