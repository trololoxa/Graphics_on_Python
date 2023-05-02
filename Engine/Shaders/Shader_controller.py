from OpenGL.GL import shaders, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER, glDeleteShader
import os


class ShaderController:
    def __init__(self):
        self.shaders = {}
        self.directories = []
        self.path = os.path.dirname(__file__)

    def get_shaders(self):
        # Get directories list
        directories = os.fsencode(self.path)
        directories = os.listdir(directories)
        directories = [os.fsdecode(directory) for directory in directories]

        # Sort only directories, exclude controller file
        for directory in range(len(directories), 0, -1):
            if directories[directory - 1].endswith('.py') or directories[directory - 1].endswith('__'):
                del directories[directory - 1]

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

        self.directories = directories
        self.shaders = shaders_dict

    def compile_shaders(self):
        for key in self.shaders:
            shader_parts = []
            for part in self.shaders[key]:
                shader_parts.append(shaders.compileShader(part[0], part[1]))
            temp_shader_program = shaders.compileProgram(*shader_parts)
            for part in shader_parts:
                glDeleteShader(part)
            self.shaders[key] = temp_shader_program


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
    controller.get_shaders()
    controller.compile_shaders()
