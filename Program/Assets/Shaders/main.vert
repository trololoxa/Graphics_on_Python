#version 460

layout (location=0) in vec3 position;
layout (location=1) in vec3 color;
layout (location = 2) in vec2 inputTexCoord;

smooth out vec3 theColor;
out vec2 TexCoord;

uniform mat4 transform;

void main()
{
    gl_Position = transform * vec4(position, 1.0f);
    theColor = color;
    TexCoord = inputTexCoord;
}