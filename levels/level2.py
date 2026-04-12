class Level2:

    def __init__(self):
        self.nombre = "El Espejo de las Formas"

    # ─────────────────────────────────────────
    # FASE 1 — COMBATE (diferenciado por clase)
    # Enemigo: El Reflejo Armado
    # ─────────────────────────────────────────
    def fase_combate(self, player, engine):

        engine.mostrar_nivel(
            "assets/enemy2.jpg",
            """
Antes de llegar al espejo…
el espejo viene a vos.

El Reflejo Armado.

Tiene tu cara.
Tu postura.
Tus movimientos, un instante antes de que los hagas.

No es un eco.
Es una anticipación.

Y viene hacia vos.


[ ESPACIO para continuar ]
""",
            opciones=False
        )

        clase = player.clase

        if clase == "Guerrero":
            intro = """
Pelear contra alguien que te copia
es pelear contra vos mismo.

Pero vos tenés algo que él no tiene:
la voluntad de dar el primer golpe.


[ ESPACIO para pelear ]
"""
            stat = "fuerza"
            dificultad = 5
            exito = """
Lo sorprendiste.
Rompiste el patrón antes de que se estableciera.

El reflejo se fragmentó.
No desapareció.
Pero dejó de anticiparte.

Por ahora.
"""
            fallo = """
Te copió demasiado bien.
Cada movimiento tuyo, reflejado y devuelto más fuerte.

Caíste dos veces antes de poder avanzar.
El cuerpo lo paga.
La mente también.
"""

        elif clase == "Hechicero":
            intro = """
Un reflejo no tiene mente propia.
Solo imita.

Y la imitación tiene un límite:
no puede originar.

Le das algo que no puede copiar.


[ ESPACIO para hechizar ]
"""
            stat = "mente"
            dificultad = 5
            exito = """
Le enviaste un patrón imposible.
Una contradicción pura.

El reflejo intentó procesarla.
No pudo.

Se detuvo.
Y en ese instante, pasaste.
"""
            fallo = """
También imitó el hechizo.
Y lo amplificó.

La descarga te golpeó de vuelta.
Tu propio conjuro, multiplicado.

El umbral cobra por la soberbia.
"""

        else:  # Ladrón
            intro = """
Un reflejo necesita algo que mirar.

Si no lo das…
no tiene forma.

Te disolvés en la sombra.
Dejás de ser un objetivo.


[ ESPACIO para evadir ]
"""
            stat = "resistencia"
            dificultad = 4
            exito = """
Te hiciste invisible para él.
Sin forma, sin silueta, sin ruido.

El reflejo giró en el vacío
buscando algo que copiar.

Pasaste a su lado como aire.
"""
            fallo = """
Te encontró igual.
Algo tuyo lo guió.
Un sonido, una sombra, un hábito.

Te golpeó desde atrás.
Como si siempre hubiera sabido adónde ibas.
"""

        resultado = engine.combate_narrativo(
            "assets/enemy2.jpg",
            intro,
            dificultad,
            stat,
            exito,
            fallo,
            psique_exito={"lucidez": 8},
            psique_fallo={"miedo": 10, "culpa": 5}
        )

        return resultado

    # ─────────────────────────────────────────
    # FASE 2 — DECISIÓN PSICOLÓGICA (original)
    # ─────────────────────────────────────────
    def fase_psicologica(self, player, engine):

        player.recuperar(vida=8, energia=15)

        texto = """
Avanzás más profundo en la cueva.
El aire cambia. Es más denso.
Llegás a una cámara circular.
En el centro… hay un espejo.
Pero no refleja tu cuerpo.
Refleja… algo más.
La voz regresa:
"No sos lo que creés. Mirá."

¿Qué hacés?
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl2.jpg",
            texto,
            opciones=True,
            opciones_lista=[
                "Mirar fijamente el espejo",
                "Romper el espejo",
                "Dar la espalda y seguir"
            ]
        )

        if eleccion == "1":
            player.psique["lucidez"] += 15
            engine.mostrar_nivel(
                "assets/lvl2.jpg",
                """
Te acercás.
Tu reflejo no te copia.
Se adelanta.
Sonríe antes que vos.
Y entonces entendés…
No estás mirando.
Estás siendo observado.
""",
                opciones=False
            )

        elif eleccion == "2":
            player.psique["violencia"] += 15
            engine.mostrar_nivel(
                "assets/lvl2.jpg",
                """
Golpeás el espejo.
Se rompe.
Pero no desaparece.
Cada fragmento sigue reflejando.
Versiones tuyas.
Peores.
Más sinceras.

La voz:
"Romper no elimina."
""",
                opciones=False
            )

        elif eleccion == "3":
            player.psique["miedo"] += 10
            engine.mostrar_nivel(
                "assets/lvl2.jpg",
                """
Das la espalda.
Pero sentís la mirada.
El reflejo no depende del espejo.
Ahora está en vos.
Y no podés dejar de sentirlo.
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
