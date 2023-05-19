"""
saves all scenes, scene objects and other things related to scene
"""
from Engine_folder.Other.Singleton import Singleton


class SceneManager:
    def __init__(self):
        self._scenes = {}
        self._active_scenes = []
        self._selected_scene = None

    @property
    def scenes_list(self):
        return self._scenes

    @property
    def active_scene_names(self):
        return self._active_scenes

    @property
    def selected_scene_name(self):
        return self._selected_scene

    @property
    def active_scenes_children(self):
        return [self._scenes[current_scene] for current_scene in self.active_scene_names]

    def create_scene(self, name, set_scene_active=False, set_scene_current=False):
        self._scenes[name] = []
        if set_scene_active:
            self.activate_scene(name)
        if set_scene_current:
            self.select_scene(name)

    def activate_scene(self, name):
        if name not in self.scenes_list:
            return -1
        self._active_scenes.append(name)

    def deactivate_scene(self, name):
        if name not in self.active_scene_names:
            if name not in self.scenes_list:
                return -1
            return -1

        self._active_scenes.remove(name)

    def select_scene(self, name):
        if name not in self.scenes_list:
            return -1

        self._selected_scene = name
