# import pydx12


class DirectX:
    @staticmethod
    def render(shader_mesh_array):
        for key in shader_mesh_array:
            print(f"DirectX is not implemented, so I'll just return object array: \n"
                  f"{key}: {shader_mesh_array[key]}")
