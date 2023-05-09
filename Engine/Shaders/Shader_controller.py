import os

from OpenGL.GL import GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from Engine.Shaders.OpenGL_Shader import Shader

from Engine.Logger import Logger


class ShaderController:
    def __init__(self):
        self.shaders = {}
        self.fallback_shader = None
        self.custom_path = None
        self.directories = []
        self.path = os.path.dirname(__file__)

    def get_shaders_dict(self, shader_directory=None):
        if shader_directory is None:
            shader_directory = self.path
        # Get directories list
        directories = os.fsencode(shader_directory)
        directories = os.listdir(directories)
        directories = [os.fsdecode(directory) for directory in directories]

        # Sort only directories, exclude controller file
        for directory in range(len(directories), 0, -1):
            delete = False
            if directories[directory - 1].endswith('.py') or directories[directory - 1].endswith('__'):
                delete = True
            elif directories[directory - 1].endswith('FallBack') and shader_directory == self.path:
                self.get_shaders_files([directories[directory - 1]])
                self.compile_shaders()
                self.fallback_shader = self.shaders['FallBack']
                delete = True
            if delete:
                del directories[directory - 1]

        Logger().log(f"Found shaders: {directories}", "Shader controller")

        self.directories += directories

    def initialize_custom_shader_dict(self, custom_dict=None):
        if custom_dict is not None:
            self.custom_path = custom_dict

        if self.custom_path is None:
            Logger().log("Can't load custom shader folder without knowing where folder is...",
                         "Shader controller", "Warn")
            return -1

        self.get_shaders_dict(self.custom_path)

    def get_shaders_files(self, directories=None):
        if directories is None:
            directories = self.directories

        # Get shader file names and types
        shaders_dict = {}
        for directory in directories:
            files = os.fsencode(self.path + '\\' + directory)
            files = os.listdir(files)
            files = [os.fsdecode(file) for file in files]
            file_types = []

            for file in files:
                if file.endswith('.frag'):
                    file_types.append(GL_FRAGMENT_SHADER)
                elif file.endswith('.vert'):
                    file_types.append(GL_VERTEX_SHADER)
                else:
                    print('ERROR: unknown shader file type')

            files_code = [open(self.path + '\\' + directory + '\\' + file).read() for file in files]
            shaders_dict[directory] = [[files_code[index], file_types[index]] for index in range(len(files))]

        self.shaders = shaders_dict

    def compile_shaders(self):
        for key in self.shaders:
            Logger().log(f"Compiling shader: {key}", "Shader controller")
            self.shaders[key] = Shader(self.shaders[key])
            self.shaders[key].compile(self.fallback_shader)

    def set_uniform(self, shader_name, uniform_name, value):
        if shader_name not in self.shaders:
            Logger().log(f"Couldn't set uniform: couldn't find shader with name {shader_name} from shader list "
                         f"{self.shaders}", "Shader controller", "Warn")
            return -1

        shader = self.shaders[shader_name]

        if type(value) == float:
            shader.set_float(uniform_name, value)
        elif type(value) == int:
            shader.set_int(uniform_name, value)
        elif type(value) == bool:
            shader.set_bool(uniform_name, value)
        else:
            Logger().log(f"Couldn't set uniform: unknown value type; type({value}) == {type(value)}: "
                         f"{value == type(value)}", "Shader controller", "Warn")


if __name__ == '__main__':
    import sdl2
    from sdl2 import video

    if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
        print(sdl2.SDL_GetError())
        exit(-1)

    window = sdl2.SDL_CreateWindow(b"OpenGL demo",
                                   sdl2.SDL_WINDOWPOS_UNDEFINED,
                                   sdl2.SDL_WINDOWPOS_UNDEFINED, 800, 600,
                                   sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_RESIZABLE)
    if not window:
        print(sdl2.SDL_GetError())
        exit(-1)

    video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, 4)
    video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, 6)
    video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_PROFILE_MASK,
                              video.SDL_GL_CONTEXT_PROFILE_CORE)

    context = sdl2.SDL_GL_CreateContext(window)

    controller = ShaderController()
    controller.get_shaders_dict()
    controller.compile_shaders()
