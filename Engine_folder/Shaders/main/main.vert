#version 460

layout (location=0) in vec3 position;
layout (location=1) in vec3 colour;

smooth out vec3 theColour;

uniform float offset;

void main()
{
    gl_Position = vec4(position.x + offset, position.y, position.z, 1.0);
    theColour = colour;
}