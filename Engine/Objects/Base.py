from Engine.Basic.Mesh import Mesh
from Engine.Physics.Collider import Collider
from Engine.Basic.Transform import Transform

class Base:
    """
    Basic objects, holds transform, collider and mesh
    transform is transform
    mesh is renders if not none
    collider is created from mesh, from custom vertexes and triangles, or custom everything 4 nerds
    shader if none - use basic
    """
    def __init__(self):
        self.transform = Transform()
        self.mesh = Mesh()
        self.collider = Collider()
        self.shader_id = 0
