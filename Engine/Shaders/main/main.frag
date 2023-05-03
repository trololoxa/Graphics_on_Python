#version 460

smooth in vec3 theColour;
out vec4 outputColour;

void main()
{
    outputColour = vec4(theColour.x, theColour.y, theColour.z, 1.0);
}