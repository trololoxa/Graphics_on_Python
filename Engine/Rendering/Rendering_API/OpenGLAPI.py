from OpenGL import GL


class OpenGLRender:
    """Renders any given object using opengl"""
    @staticmethod
    def render(shader_mesh_array):
        for key in shader_mesh_array:
            GL.glUseProgram(key)
            for mesh in shader_mesh_array[key]:
                if mesh.VAO is None:
                    continue

                GL.glBindVertexArray(mesh.VAO)

                GL.glDrawArrays(mesh.primitive_type, 0, mesh.num_points)

                GL.glBindVertexArray(0)
            GL.glUseProgram(0)
