shader_type canvas_item;

uniform float state;

void vertex() {
	// Called for every vertex the material is visible on.
}

void fragment() {
	COLOR = texture(TEXTURE, UV);
	if(UV[0] > 0.19 && UV[1] < 0.8) {
		COLOR.r = 1.0 - state;
		COLOR.g = state;
	}
	// Called for every pixel the material is visible on.
}

//void light() {
	// Called for every pixel for every light affecting the CanvasItem.
	// Uncomment to replace the default light processing function with this one.
//}
