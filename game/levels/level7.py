from game.enemies import crear_eco

class Level7:

    def __init__(self):
        self.nombre = "La Sala del Juicio"

    def fase_combate(self, player, engine):
        enemy = crear_eco()
        return engine.combate_narrativo(enemy)

    def fase_psicologica(self, player, engine):

        player.recuperar(vida=5, energia=10)

        texto = """
La Sala del Juicio está vacía.

Miles de asientos de piedra.
Ningún juez.
Solo vos en el centro.

El silencio no es ausencia de sonido.
Es la acumulación de todo lo que
dijiste y deberías haber callado.
Y de todo lo que callaste
y deberías haber dicho.

Una voz que es tu voz pero no es tu voz:
"¿Qué testimonio darías de vos mismo?"

¿Qué hacés?
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl7.jpg",
            texto,
            opciones=True,
            opciones_lista=[
                "Hablar. Decir todo.",
                "Guardar silencio.",
                "Negar que haya algo que decir."
            ]
        )

        if eleccion == "1":
            player.registrar_decision("Hablaste. Dijiste todo en la Sala del Juicio.")
            player.psique["lucidez"] += 12
            player.psique["culpa"] += 8
            engine.mostrar_nivel(
                "assets/lvl7.jpg",
                """
Hablás.

Todo.
Sin orden.
Sin filtro.

Las palabras llenan la sala
y rebotan en el vacío.

No hay nadie para escucharte.
Pero el acto de decirlo
cambia algo.

No te absuelve.
Solo te hace más real.
""",
                opciones=False
            )

        elif eleccion == "2":
            player.registrar_decision("Guardaste silencio ante el juicio.")
            player.psique["miedo"] += 10
            player.psique["lucidez"] += 5
            engine.mostrar_nivel(
                "assets/lvl7.jpg",
                """
No decís nada.

El silencio se asienta.

La sala no te juzga por callarte.
No tiene capacidad de juzgar nada.

Pero vos te juzgás a vos mismo.
Y eso ocupa más espacio
que cualquier veredicto externo.
""",
                opciones=False
            )

        elif eleccion == "3":
            player.registrar_decision("Negaste tener algo que decir en el juicio.")
            player.psique["corrupcion"] += 12
            player.psique["violencia"] += 5
            engine.mostrar_nivel(
                "assets/lvl7.jpg",
                """
Decís que no hay nada.

La sala no responde.

Pero algo en el aire
cambia de temperatura.

Lo que negas
no desaparece.
Solo deja de tener nombre.
Y lo sin nombre
es más peligroso.
""",
                opciones=False
            )

    def jugar(self, player, engine):
        resultado = self.fase_combate(player, engine)
        if resultado == "muerte":
            return "muerte"

        self.fase_psicologica(player, engine)
        return "continuar"
