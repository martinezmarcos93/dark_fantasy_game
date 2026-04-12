class Level1:

    def __init__(self):
        self.nombre = "La Cueva del Origen"

    # ─────────────────────────────────────────
    # FASE 1 — COMBATE (diferenciado por clase)
    # Enemigo: El Guardián de Piedra
    # ─────────────────────────────────────────
    def fase_combate(self, player, engine):

        # Intro del enemigo — igual para todos
        engine.mostrar_nivel(
            "assets/enemy1.jpg",
            """
Antes de que la oscuridad te reciba…
algo la bloquea.

El Guardián de Piedra.

No fue puesto aquí por nadie.
Creció solo.
Del mismo material que la cueva.
De la misma necesidad de no dejar pasar.

No tiene ojos.
Pero te ve.


[ ESPACIO para continuar ]
""",
            opciones=False
        )

        clase = player.clase

        if clase == "Guerrero":
            intro = """
No necesitás pensar.
Tu cuerpo ya sabe.

Tomás el arma.
La piedra también conoce el peso del acero.


[ ESPACIO para pelear ]
"""
            stat = "fuerza"
            dificultad = 4
            exito = """
Lo golpeaste donde debía ceder.
La piedra se fracturó.
El guardián retrocedió.

No sin antes marcarte.
Pero seguís en pie.
Eso es suficiente.
"""
            fallo = """
Te aplastó contra la pared.
Sentiste algo ceder adentro.

Te arrastrás.
No te detiene.
Pero tu cuerpo no lo olvidará.
"""

        elif clase == "Hechicero":
            intro = """
La fuerza bruta no es tu camino.

La piedra tiene memoria.
Y toda memoria tiene una grieta.

Buscás la frecuencia correcta.
Extendés la mano.


[ ESPACIO para hechizar ]
"""
            stat = "mente"
            dificultad = 4
            exito = """
Encontraste la grieta.
Una palabra, una intención, una resonancia.

La piedra se fragmentó desde adentro.
El pasaje quedó libre.

Solo te costó claridad.
"""
            fallo = """
El conjuro rebotó.
La piedra no tenía la grieta que buscabas.

El guardián te barrió con un brazo.
Caíste lejos.

Algo en tu mente crujió.
"""

        else:  # Ladrón
            intro = """
Los ojos de piedra no ven igual que los de carne.

Hay sombras.
Hay ángulos.
Hay un lado que siempre existe.

Te movés despacio.
Sin ruido.


[ ESPACIO para evadir ]
"""
            stat = "resistencia"
            dificultad = 3
            exito = """
Pasaste por el borde.
Pegado a la pared.

El guardián miró hacia adelante
mientras vos ya estabas del otro lado.

Eso también tiene un costo.
Saber que podés desaparecer.
"""
            fallo = """
El guardián te vio igual.
No se puede engañar a todo.

Te golpeó de costado.
No fue mortal.
Fue un aviso.
"""

        resultado = engine.combate_narrativo(
            "assets/enemy1.jpg",
            intro,
            dificultad,
            stat,
            exito,
            fallo,
            psique_exito={"lucidez": 5},
            psique_fallo={"miedo": 8}
        )

        return resultado  # "vivo" o "muerte"

    # ─────────────────────────────────────────
    # FASE 2 — DECISIÓN PSICOLÓGICA (original)
    # ─────────────────────────────────────────
    def fase_psicologica(self, player, engine):

        # Recuperación parcial entre fases
        player.recuperar(vida=8, energia=15)

        texto = """
Te adentras en la cueva.
No hay antorchas. No hay sonido.
Solo oscuridad.
Algo… respira en la profundidad.
No lo ves, pero lo sentís.
Una voz, o tal vez un pensamiento que no es tuyo, susurra:
"Antes de la luz… ya estabas aquí."

¿Qué hacés?
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl1.jpg",
            texto,
            opciones=True,
            opciones_lista=[
                "Avanzar hacia la oscuridad",
                "Encender una antorcha",
                "Llamar para saber quién está ahí"
            ]
        )

        if eleccion == "1":
            player.psique["corrupcion"] += 10
            engine.mostrar_nivel(
                "assets/lvl1.jpg",
                """
Caminás sin ver.
Cada paso se siente… correcto.
Como si ya hubieras estado ahí antes.
La oscuridad no te rechaza.
Te envuelve.

La voz vuelve:
"Recordar es descender."
""",
                opciones=False
            )

        elif eleccion == "2":
            player.psique["lucidez"] += 10
            engine.mostrar_nivel(
                "assets/lvl1.jpg",
                """
La antorcha enciende.
La luz revela paredes húmedas…
y marcas.
No son naturales.
Son manos.
Cientos de ellas.
Marcadas desde adentro.

La voz susurra:
"La luz no revela. Delata."
""",
                opciones=False
            )

        elif eleccion == "3":
            player.psique["miedo"] += 15
            engine.mostrar_nivel(
                "assets/lvl1.jpg",
                """
Tu voz se pierde.
Pero algo responde.
No con sonido.
Con presencia.
Ahora sabés que no estás solo.
Y nunca lo estuviste.
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
