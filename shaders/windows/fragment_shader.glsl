#version 130

in vec3 normal_view_space;
in vec3 position_view_space;
in vec3 fragment_texCoord;
out vec4 final_color;

uniform samplerCube sampler_cube;
uniform mat4 PVM; 	// the Perspective-View-Model matrix is received as a Uniform
uniform mat4 VM; 	// the View-Model matrix is received as a Uniform
uniform mat3 VMiT;  // The inverse-transpose of the view model matrix, used for normals
uniform mat3 VT;

void main(void)
{
	vec3 normal_view_space_normalized = normalize(normal_view_space);
	vec3 reflected = reflect(normalize(position_view_space), normal_view_space_normalized);

    reflected.y *= -1;

    vec4 colour_multiplier;
    colour_multiplier.x = 0.66;
    colour_multiplier.y = 0.94;
    colour_multiplier.z = 0.985;
    colour_multiplier.w = 0;
	final_color = colour_multiplier * texture(sampler_cube, normalize(reflect(VT*reflected, vec3(1,0,0))));
	//final_color = texture(sampler_cube, normalize(reflected));


	//final_color = texture(sampler_cube, fragment_texCoord);
//	frag_data = texture(sampler_cube, vec3(1,0,0));
	//final_color = vec4( fragment_texCoord, 1.0f );
}
