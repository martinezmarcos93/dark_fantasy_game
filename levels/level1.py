class Level1:
    def __init__(self):
        self.nombre = "La Cueva del Origen"

class Level1:

    def jugar(self, player, engine):

        texto = """
Te adentras en la cueva.

No hay antorchas. No hay sonido.
Solo oscuridad.

Algo… respira en la profundidad.
No lo ves, pero lo sentís.

Una voz, o tal vez un pensamiento que no es tuyo, susurra:

"Antes de la luz… ya estabas aquí."

¿Qué hacés?

1. Avanzar hacia la oscuridad
2. Encender una antorcha
3. Llamar para saber quién está ahí
"""

        eleccion = engine.mostrar_nivel("assets/lvl1.jpg", texto)

        # -------------------------
        # DECISIONES
        # -------------------------

        if eleccion == "1":
            player.psique["corrupcion"] += 10

            texto_resultado = """
Caminás sin ver.

Cada paso se siente… correcto.
Como si ya hubieras estado ahí antes.

La oscuridad no te rechaza.
Te envuelve.

La voz vuelve:
"Recordar es descender."
"""

            engine.mostrar_nivel("assets/lvl1.jpg", texto_resultado)
            return "continuar"

        elif eleccion == "2":
            player.psique["lucidez"] += 10

            texto_resultado = """
La antorcha enciende.

La luz revela paredes húmedas…
y marcas.

No son naturales.

Son manos.

Cientos de ellas.

Marcadas desde adentro.

La voz susurra:
"La luz no revela. Delata."
"""

            engine.mostrar_nivel("assets/lvl1.jpg", texto_resultado)
            return "continuar"

        elif eleccion == "3":
            player.psique["miedo"] += 15

            texto_resultado = """
Tu voz se pierde.

Pero algo responde.

No con sonido.

Con presencia.

Ahora sabés que no estás solo.

Y nunca lo estuviste.
"""

            engine.mostrar_nivel("assets/lvl1.jpg", texto_resultado)
            return "continuar"

        return "muerte"
