# import vulkan
from Engine_folder.Logger import log


class Vulkan:
    """Renders any given object using Vulkan"""
    def __init__(self):
        log("Using Vulkan Rendering API", "Renderer")

    @staticmethod
    def render(shader_mesh_array):
        for key in shader_mesh_array:
            print(f"Vulkan is not implemented, so I'll just return object array: \n"
                  f"{key}: {shader_mesh_array[key]}")
