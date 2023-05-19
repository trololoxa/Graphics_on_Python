class AABB:
    """
    AABB created from any vertices
    min is vec3
    max is vec3
    x,y,z = [[vertex.x for vertex in vertices], [vertex.y for vertex in vertices], [vertex.z for vertex in vertices]]
    min = vec3(min(x), min(y), min(z))
    max = vec3(max(x), max(y), max(z))
    """
    def __init__(self):
        self.min = None
        self.max = None
