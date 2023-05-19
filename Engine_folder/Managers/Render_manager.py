"""
chooses render type, render api and does something with that
"""
from Engine_folder.Other.Singleton import Singleton
from Engine_folder.Rendering.Render_bases.GLFW import GLFWBase
from Engine_folder.Rendering.Rendering_API.OpenGLAPI import OpenGLRender
from Engine_folder.Logger import log


class RenderManager:
    api_dict = {'OpenGL': OpenGLRender}
    base_dict = {'GLFW': GLFWBase}

    def __init__(self):
        self.api = None
        self.base = None
        self.fps = 0

    def initialize(self, asset_manager, set_key_state_func):
        if asset_manager.settings is None:
            self.api = OpenGLRender()
            self.base = GLFWBase()
        else:
            self.api = self.api_dict[asset_manager.settings['api']]()
            self.base = self.base_dict[asset_manager.settings['base']]()

        self.base.prepare(set_key_state_func)

    def create_window(self, w=800, h=600, name="NoName"):
        self.base.create_window(width=w, height=h, name=name, render_api=self.api)
        log(f'Created window {w}x{h} with name {name}', 'Renderer')

    @staticmethod
    def create_mesh_objects_array(scenes_children, shader_manager):
        # returns shader:[objects] array for optimization purpose
        return_array = {}
        for scene in scenes_children:
            for obj in scene:
                program = shader_manager.shaders[shader_manager.directories[obj.shader_id].name]
                if program not in return_array:
                    return_array[program] = [obj.mesh]
                else:
                    return_array[program] += [obj.mesh]

        return return_array

    def step(self, scenes_children_list,  shader_manager):
        # 1 render step

        # clear window
        self.api.clear_background()

        # renders
        self.api.render(self.create_mesh_objects_array(scenes_children_list, shader_manager))

        # processes events
        self.base.swap_buffers()
