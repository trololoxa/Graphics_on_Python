from Engine_folder.Basic.Mesh import Mesh
from Engine_folder.Components.Transform import Transform
from Engine_folder.Physics.Collider import Collider


class Base:
    """
    Basic objects, holds transform, collider and mesh \n
    transform is transform \n
    mesh is renders if not none \n
    collider is created from mesh, from custom vertexes and triangles, or custom everything 4 nerds \n
    shader if none - use basic \n
    """
    def __init__(self):
        # I don't know what I should add to this
        self.transform = Transform()
        self.mesh = Mesh()
        self.collider = Collider()
        self.shader_id = 0
