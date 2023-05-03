import ctypes

import sdl2
from sdl2 import video

from Engine.Rendering.Rendering_API.OpenGLAPI import OpenGLRender
from OpenGL.GL import glViewport, glClear, glClearColor, GL_COLOR_BUFFER_BIT


class SDLBase:
    """
        Basic SDL loop
        render_api renders
        objects list can be changed with scene
        """
    def __init__(self):
        self.render_api = OpenGLRender()
        self.objects = []
        self.window = None
        self.context = None

    @staticmethod
    def prepare():
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) != 0:
            print(sdl2.SDL_GetError())
            return -1

        # Force OpenGL 4.6 'core' context.
        # Must set *before* creating GL context!
        video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MAJOR_VERSION, 4)
        video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_MINOR_VERSION, 6)
        video.SDL_GL_SetAttribute(video.SDL_GL_CONTEXT_PROFILE_MASK,
                                  video.SDL_GL_CONTEXT_PROFILE_CORE)

    def create_window(self, width=800, height=600, name="OpenGL demo"):
        self.window = sdl2.SDL_CreateWindow(name.encode("UTF-8"),
                                            sdl2.SDL_WINDOWPOS_UNDEFINED,
                                            sdl2.SDL_WINDOWPOS_UNDEFINED, width, height,
                                            sdl2.SDL_WINDOW_OPENGL | sdl2.SDL_WINDOW_RESIZABLE)
        if not self.window:
            print(sdl2.SDL_GetError())
            return -1

        self.context = sdl2.SDL_GL_CreateContext(self.window)

        glViewport(0, 0, width, height)

    def infinite_loop(self, shader_controller):
        event = sdl2.SDL_Event()
        running = True
        while running:
            while sdl2.SDL_PollEvent(ctypes.byref(event)) != 0:
                if event.type == sdl2.SDL_QUIT:
                    running = False

            glClearColor(0.2, 0.3, 0.3, 1.0)
            glClear(GL_COLOR_BUFFER_BIT)

            self.render_api.render(self.create_mesh_objects_array(shader_controller))

            sdl2.SDL_GL_SwapWindow(self.window)
            sdl2.SDL_Delay(10)

        sdl2.SDL_GL_DeleteContext(self.context)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()
        return 0

    def create_mesh_objects_array(self, shader_controller):
        return_array = {}
        for obj in self.objects:
            program = shader_controller.shaders[shader_controller.directories[obj.shader_id]]
            if program not in return_array:
                return_array[program] = [obj.mesh]
            else:
                return_array[program] += [obj.mesh]

        return return_array
