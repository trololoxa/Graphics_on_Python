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

                GL.glDrawElements(mesh.primitive_type, mesh.num_points, GL.GL_UNSIGNED_INT, None)

                # GL.glBindVertexArray(0)
            GL.glUseProgram(0)
