#version 460

smooth in vec3 theColor;
in vec2 TexCoord;

out vec4 fragColor;

uniform sampler2D Texture1;
uniform sampler2D Texture2;

void main()
{
    fragColor = vec4(theColor, 1.0);

    // fragColor = mix(texture(Texture1, TexCoord), texture(Texture2, vec2(TexCoord.x, TexCoord.y)), .2);
}
