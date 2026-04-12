class Level3:

    def __init__(self):
        self.nombre = "El Ritual de la Entrega"

    # ─────────────────────────────────────────
    # FASE 1 — COMBATE (diferenciado por clase)
    # Enemigo: El Sacerdote Sin Rostro
    # ─────────────────────────────────────────
    def fase_combate(self, player, engine):

        engine.mostrar_nivel(
            "assets/enemy3.jpg",
            """
El altar no estaba vacío.

El Sacerdote Sin Rostro lo custodia.

No tiene facciones.
Solo una superficie lisa donde debería haber una cara.
Como si algo hubiera borrado todo
antes de que pudiera formarse.

No ataca.
Pero tampoco deja pasar.
Extiende las manos.
Y el aire se vuelve espeso.


[ ESPACIO para continuar ]
""",
            opciones=False
        )

        clase = player.clase

        if clase == "Guerrero":
            intro = """
Lo que no tiene cara
tampoco tiene miedo.

Pero lo que no tiene miedo
tampoco esquiva.

Sabés exactamente qué hacer.


[ ESPACIO para pelear ]
"""
            stat = "fuerza"
            dificultad = 5
            exito = """
Lo golpeaste directo.
Sin dudas.
Sin preguntas.

Cayó.
No con dolor.
Con algo parecido al alivio.

El camino al altar quedó libre.
"""
            fallo = """
El aire espeso te ralentizó.
Cada golpe tuyo llegó tarde.

El sacerdote te tocó en el pecho.
No fue un golpe.
Fue una extracción.

Algo salió de vos.
No sabés qué.
"""

        elif clase == "Hechicero":
            intro = """
Sin rostro, sin nombre, sin forma estable.

Pero todo lo que existe
tiene una frecuencia.

Buscás la suya.
La que lo define aunque no quiera ser definido.


[ ESPACIO para hechizar ]
"""
            stat = "mente"
            dificultad = 5
            exito = """
Lo nombraste.

Eso fue suficiente.
Lo que no tiene nombre no puede resistir
cuando alguien le da uno.

Se detuvo.
Se encogió.
Dejó pasar.
"""
            fallo = """
No encontraste su frecuencia.
O tal vez no tiene ninguna.

El hechizo se disolvió en el aire espeso.
Y el sacerdote te tocó igual.

Algo salió de vos.
Un recuerdo, quizás.
O una certeza.
"""

        else:  # Ladrón
            intro = """
Lo que no tiene ojos
no puede seguirte con la vista.

Pero este sacerdote siente.
El calor, el movimiento, la intención.

Tenés que no tener ninguna.
Moverte sin querer moverte.


[ ESPACIO para evadir ]
"""
            stat = "resistencia"
            dificultad = 4
            exito = """
Te vaciaste.
Sin plan, sin destino, sin urgencia.

El sacerdote te buscó en el aire
y no encontró nada.

Pasaste a su lado como humo.
"""
            fallo = """
Sentiste la intención antes de poder borrarla.
Demasiado tarde.

Las manos sin dedos te encontraron igual.
Te tocaron en algún lugar que no es el cuerpo.

Algo quedó marcado.
"""

        resultado = engine.combate_narrativo(
            "assets/enemy3.jpg",
            intro,
            dificultad,
            stat,
            exito,
            fallo,
            psique_exito={"lucidez": 5, "corrupcion": 5},
            psique_fallo={"culpa": 10, "miedo": 5}
        )

        return resultado

    # ─────────────────────────────────────────
    # FASE 2 — DECISIÓN PSICOLÓGICA (original)
    # ─────────────────────────────────────────
    def fase_psicologica(self, player, engine):

        player.recuperar(vida=6, energia=12)

        texto = """
La cueva se abre en una sala amplia.
El aire es pesado.
Antiguo.
En el centro hay un altar de piedra.
Encima… un libro.
Sus páginas están en blanco.
Pero algo se escribe lentamente.
No con tinta.
Con algo más denso.

La voz susurra:
"Para comprender… tenés que entregar."

¿Qué hacés?
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl3.jpg",
            texto,
            opciones=True,
            opciones_lista=[
                "Leer el libro",
                "Ofrecer tu sangre",
                "Ignorar el altar y seguir"
            ]
        )

        if eleccion == "1":
            player.psique["lucidez"] += 15
            player.psique["corrupcion"] += 5
            engine.mostrar_nivel(
                "assets/lvl3.jpg",
                """
Leés.
Las palabras no están escritas.
Se forman mientras las mirás.
Y hablan de vos.
De cosas que no recordabas…
pero que son ciertas.
Cada línea te revela.
Pero también te cambia.
""",
                opciones=False
            )

        elif eleccion == "2":
            player.psique["corrupcion"] += 20
            engine.mostrar_nivel(
                "assets/lvl3.jpg",
                """
Apoyás tu mano.
La piedra está tibia.
La sangre fluye.
El libro responde.
Las páginas se llenan.
Pero no con conocimiento.
Con aceptación.
Algo en vos… ya eligió.
""",
                opciones=False
            )

        elif eleccion == "3":
            player.psique["miedo"] += 10
            engine.mostrar_nivel(
                "assets/lvl3.jpg",
                """
Te alejás.
Pero el altar no desaparece.
Lo sentís.
Como una decisión no tomada.
Como algo pendiente.
Y sabés…
que lo vas a volver a ver.
""",
                opciones=False
            )

    # ─────────────────────────────────────────
    # ENTRY POINT
    # ─────────────────────────────────────────
    def jugar(self, player, engine):
        resultado = self.fase_combate(player, engine)
        if resultado == "muerte":
            return "muerte"

        self.fase_psicologica(player, engine)
        return "continuar"
