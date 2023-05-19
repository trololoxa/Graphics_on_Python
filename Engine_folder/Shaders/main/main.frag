#version 460

smooth in vec3 theColour;
out vec4 outputColour;

void main()
{
    outputColour = vec4(theColour, 1.0);
}