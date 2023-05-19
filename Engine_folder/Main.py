# import numpy
# from Engine_folder.Rendering.Render_bases.SDL import SDLBase
# currently I don't want sdl
from Engine_folder.Managers import ShaderManager, AssetManager, RenderManager, InputManager, SceneManager
from Engine_folder.Logger import Logger, log
import time
from Engine_folder.Objects.Base_object import Base as Base_object


class Main:
    def __init__(self):
        self.logger = Logger()

        self.asset_manager = AssetManager()
        self.physics_manager = None
        self.render_manager = RenderManager()
        self.scene_manager = SceneManager()
        self.shader_manager = ShaderManager()
        self.texture_manager = None
        self.input_manager = InputManager()
        self.fps = 0

    def initialize(self, window_width=800, window_height=600):
        """
        initializes render api, base, shaders and window
        """
        self.asset_manager.initialize_dictionaries()
        self.asset_manager.init_custom_dict('G:/Programming/Python/graphic_nigger/Assets')
        self.asset_manager.init_settings()

        self.logger.initialize(self.asset_manager)

        self.render_manager.initialize(asset_manager=self.asset_manager,
                                       set_key_state_func=self.input_manager.set_key_state)
        self.render_manager.create_window(window_width, window_height)

        self.scene_manager.create_scene('main_scene', True, True)

        self.shader_manager.initialize(self.asset_manager)
        self.shader_manager.get_shaders_dict()
        self.shader_manager.get_shaders_files()
        self.shader_manager.compile_shaders()

        self.input_manager.add_action('escape', self.render_manager.base.close_window, 1)
        self.input_manager.add_action('space', self.render_manager.api.set_wireframe_mode, 1, True)
        self.input_manager.add_action('space', self.render_manager.api.set_wireframe_mode, 0, False)

    def add_object(self, obj=None, triangles=None, vertices=None, colors=None, primitive=None):
        if primitive is None:
            primitive = self.render_manager.api.triangles_primitive
        if obj is not None:
            # if given object: just adds this object to render base
            self.scene_manager.scenes_list[self.scene_manager.selected_scene_name].append(obj)
        else:
            # else creates a new object and adds it to render base, mb I should delete this
            obj = Base_object()
            obj.mesh.vertices = vertices
            obj.mesh.triangles = triangles
            obj.mesh.colors = colors
            obj.mesh.set_primitive_type(primitive=primitive)
            self.scene_manager.scenes_list[self.scene_manager.selected_scene_name].append(obj)
            return obj

    def start(self):
        # starts render loop
        log("Started render loop", "Main")

        try:
            frames = 0
            reset_fps = True
            start_time = time.time()

            while not self.render_manager.base.should_close():
                if reset_fps:
                    start_time = time.time()
                    frames = 0

                frames += 1

                self.input_manager.do_actions()
                self.asset_manager.execute_scripts()
                self.render_manager.step(self.scene_manager.active_scenes_children, self.shader_manager)

                end_time = time.time()
                elapsed_time = end_time - start_time

                if elapsed_time > 0:
                    self.fps = (frames / elapsed_time)
                    reset_fps = True
                else:
                    reset_fps = False

                # print(self.fps)

            self.render_manager.base.terminate()
        except KeyboardInterrupt as e:
            log(f"Caught {type(e)}", "Main Loop", "Error")
            self.start()

        # TODO: cleanups, closing and saving
        log("Render loop exited", "Main")
