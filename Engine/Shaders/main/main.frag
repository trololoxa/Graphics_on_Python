#version 460

smooth in vec3 theColour;
out vec4 outputColour;

vec4 positivecolor;

void main()
{
    if (theColour.x < 0) positivecolor.x = theColour.x * -1;
    else positivecolor.x = theColour.x;

    if (theColour.y < 0) positivecolor.y = theColour.y * -1;
    else positivecolor.y = theColour.y;

    if (theColour.z < 0) positivecolor.z = theColour.z * -1;
    else positivecolor.z = theColour.z;

    positivecolor.w = 1.0;

    //positivecolor = vec4(theColour, 1.0);

    outputColour = positivecolor;
}