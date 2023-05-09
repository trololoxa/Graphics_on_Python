from OpenGL.GL import shaders, glUseProgram, glUniform1i, glUniform1f, glGetUniformLocation
from Engine.Logger import Logger


class Shader:
    def __init__(self, *shader_sources):
        self.sources = shader_sources[0]
        self.shaders = []
        self.program = None

    def compile(self, fallback_shader):
        error = False
        for part in self.sources:
            try:
                self.shaders.append(shaders.compileShader(part[0], part[1]))
                Logger().log(f"{part[1]} compilation successful", "Shader Compiler")
            except RuntimeError as exception:
                Logger().log(f"{part[1]} compilation error", "Shader Compiler", "Error")
                Logger().log(exception, "Shader Compiler", "Error")
                error = True
        try:
            if not error:
                self.program = shaders.compileProgram(*self.shaders)
                Logger().log("Program compilation successful", "Shader Program Compiler")
            else:
                raise RuntimeError("One or more shader parts compilation failed, throwing exception")
        except RuntimeError as exception:
            Logger().log(f"Error compiling shader program: {exception}", "Shader Program Compiler", "Error")
            Logger().log("Using FallBack Shader", "Shader Program Compiler", "Warn")
            self.program = fallback_shader.program

    def activate(self):
        if self.program is not None:
            glUseProgram(self.program)
        else:
            Logger().log("Couldn't activate shader program", "Shader", "Error")

    @staticmethod
    def deactivate():
        glUseProgram(0)

    def get_uniform_name(self, name):
        self.activate()
        location = glGetUniformLocation(self.program, name)
        if location == -1:
            Logger().log(f"Couldn't find uniform location {name}", "Shader", "Warn")

        return location

    def set_bool(self, name, boolean):
        glUniform1i(self.get_uniform_name(name), int(boolean))
        self.deactivate()

    def set_int(self, name, integer):
        glUniform1i(self.get_uniform_name(name), integer)
        self.deactivate()

    def set_float(self, name, float_var):
        glUniform1f(self.get_uniform_name(name), float_var)
        self.deactivate()
