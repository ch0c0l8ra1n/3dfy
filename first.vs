#version 330
	layout(location=0) in vec4 position;
	layout(location=1) in vec3 color;
	layout(location=2) in vec2 inTexCoords;
	uniform mat4 transform;

	uniform mat4 view;
	uniform mat4 model;
	uniform mat4 projection;


	out vec2 outTexCoords;
	out vec3 newColor;
	void main()
	{
		gl_Position = projection * view * model * transform * position;
		newColor = color;
		outTexCoords = inTexCoords;
	} 