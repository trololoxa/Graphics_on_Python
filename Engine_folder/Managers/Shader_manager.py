import os

from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from Engine_folder.Shaders.OpenGL_Shader import Shader

from Engine_folder.Logger import log

from Engine_folder.Other.Singleton import Singleton

import pathlib


class ShaderManager:
    def __init__(self):
        self.shaders = {}
        self.fallback_shader = None
        self.custom_path = None
        self.directories = []
        self.path = None
        self._get_subdicts = None
        self._get_subfiles = None

    def initialize(self, asset_manager):
        self.path = asset_manager.shader_dict
        self._get_subfiles, self._get_subdicts = [asset_manager.get_subfiles, asset_manager.get_subfolders]

    def get_shaders_dict(self, shader_directory=None):
        # gets from given directory all directories
        if shader_directory is None:
            shader_directory = self.path
        # Get directories list
        directories = self._get_subdicts(shader_directory)

        # Sort only directories, exclude controller file
        for directory in range(len(directories), 0, -1):
            delete = False
            if str(directories[directory - 1]).endswith('__'):
                delete = True
            elif str(directories[directory - 1]).endswith('FallBack') and shader_directory == self.path:
                self.get_shaders_files([directories[directory - 1]])
                self.compile_shaders()
                self.fallback_shader = self.shaders['FallBack']
                delete = True

            if delete:
                del directories[directory - 1]

        log(f"Found shaders: {[directory.name for directory in directories]}", "Shader controller")

        self.directories += directories

    def initialize_custom_shader_dict(self, custom_dict=None):
        # loads directories from custom directory
        self.custom_path = pathlib.Path(custom_dict).absolute()

        if custom_dict is None:
            log("Can't load custom shader folder without knowing where folder is...",
                "Shader controller", "Warn")
            return -1

        self.get_shaders_dict(self.custom_path)

    def get_shaders_files(self, directories=None):
        # loads files from directories and saves them as shaders
        if directories is None:
            directories = self.directories

        # Get shader file names and types
        shaders_dict = {}
        for directory in directories:
            files = self._get_subfiles(directory)
            file_types = []

            for file in files:
                # Later_TODO: make this check not OpenGL-related, when I implement DirectX or Vulkan
                file = str(file)
                if file.endswith('.frag'):
                    file_types.append(GL_FRAGMENT_SHADER)
                elif file.endswith('.vert'):
                    file_types.append(GL_VERTEX_SHADER)
                else:
                    print('ERROR: unknown shader file type')

            files_code = [open(file).read() for file in files]
            shaders_dict[directory.name] = [[files_code[index], file_types[index]] for index in range(len(files))]

        self.shaders = shaders_dict

    def compile_shaders(self):
        # compiles shaders into shader programs
        for key in self.shaders:
            if type(self.shaders[key]) is not Shader:
                log(f"Compiling shader: {key}", "Shader controller")
                self.shaders[key] = Shader(self.shaders[key])
                self.shaders[key].compile(self.fallback_shader)
            else:
                log(f"Can't compile shader {key} if it is already compiled", "Shader controller", "Warn")

    def set_uniform(self, shader_name, uniform_name, value):
        # sets given uniform in given shader to given value
        # if shader isn't real - error
        if shader_name not in self.shaders:
            log(f"Couldn't set uniform: couldn't find shader with name {shader_name} from shader list "
                f"{self.shaders}", "Shader controller", "Warn")
            return -1

        shader = self.shaders[shader_name]

        # figuring out value type and setting it
        if type(value) == float:
            shader.set_float(uniform_name, value)
        elif type(value) == int:
            shader.set_int(uniform_name, value)
        elif type(value) == bool:
            shader.set_bool(uniform_name, value)
        else:
            log(f"Couldn't set uniform: unknown value type; type({value}) == {type(value)}: "
                f"{type(value) == type(value)}", "Shader controller", "Warn")
