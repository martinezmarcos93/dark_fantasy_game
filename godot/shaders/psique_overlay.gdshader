shader_type canvas_item;
// psique_overlay — filtro psíquico sobre la imagen del nivel.
// Reemplaza ui._aplicar_filtro_psique() del Pygame (ADR/roadmap Fase 5).
//
// Equivalente: tinte de color según psique dominante, mezcla 0→~0.35.
// Superior: suma aberración cromática y vignette escaladas por la intensidad,
// que el filtro plano de Pygame no podía hacer.
//
// Parámetros (los setea GameScreen.actualizar_psique):
//   psique_color — color del stat dominante (RGB normalizado)
//   intensidad   — fuerza del tinte 0..~0.35 (misma curva que el alpha original)
//   aberracion   — fuerza de la separación de canales (suele = intensidad)

uniform vec3 psique_color = vec3(0.0);
uniform float intensidad : hint_range(0.0, 1.0) = 0.0;
uniform float aberracion : hint_range(0.0, 1.0) = 0.0;

void fragment() {
	vec2 uv = UV;

	// Aberración cromática: separar el canal R y B horizontalmente.
	float off = aberracion * 0.012;
	vec4 base = texture(TEXTURE, uv);
	float r = texture(TEXTURE, uv + vec2(off, 0.0)).r;
	float b = texture(TEXTURE, uv - vec2(off, 0.0)).b;
	vec3 col = vec3(r, base.g, b);

	// Tinte de psique (mezcla con el color, como el overlay del original).
	col = mix(col, psique_color, intensidad);

	// Vignette según intensidad: oscurece los bordes cuando la psique sube.
	vec2 d = uv - vec2(0.5);
	float vig = smoothstep(0.85, 0.25, length(d));  // 1 al centro, 0 en bordes
	col *= mix(1.0, vig, intensidad);

	COLOR = vec4(col, base.a);
}
