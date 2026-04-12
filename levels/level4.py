class Level4:

    def __init__(self):
        self.nombre = "El Rey de las Sombras"

    # ─────────────────────────────────────────
    # FASE 1 — COMBATE (diferenciado por clase)
    # Enemigo: La Sombra Soberana
    # El más difícil de los 4 — dificultad 6
    # ─────────────────────────────────────────
    def fase_combate(self, player, engine):

        engine.mostrar_nivel(
            "assets/enemy4.jpg",
            f"""
Antes de que llegues a la grieta…
ella ya está ahí.

La Sombra Soberana.

No es tu sombra.
Es la de todos los que descendieron antes que vos
y no pudieron continuar.

Las absorbió.
Las hizo suyas.
Y ahora tiene el peso
de todas esas derrotas acumuladas.

Te mira.
Te conoce.
Sabe exactamente cuánto podés aguantar.


[ ESPACIO para continuar ]
""",
            opciones=False
        )

        clase = player.clase

        if clase == "Guerrero":
            intro = """
Pelear contra una sombra.

No es imposible.
Las sombras tienen forma.
Y la forma puede ser golpeada.

Pero esta forma cambia.
Tenés que ser más rápido que el cambio.


[ ESPACIO para pelear ]
"""
            stat = "fuerza"
            dificultad = 6
            exito = """
La seguiste.
Cada cambio de forma, un paso tuyo.
Hasta que encontraste el centro.

La sombra no grita cuando cae.
Solo se adelgaza.
Se vuelve plana.

Y se queda en el suelo,
donde siempre debería haber estado.
"""
            fallo = """
Cambió demasiado rápido.
Cada golpe tuyo pasó por donde ya no estaba.

Y cuando finalmente te alcanzó…
fue desde adentro.
Como si la sombra ya viviera en vos
y solo hubiera salido un momento a saludarte.

Caíste.
Te levantás.
Pero algo quedó afuera.
"""

        elif clase == "Hechicero":
            intro = """
La luz no destruye las sombras.
Las define.

Y lo que está definido
puede ser contenido.

No intentás eliminarla.
Intentás nombrar sus bordes.
Fijarla.


[ ESPACIO para hechizar ]
"""
            stat = "mente"
            dificultad = 6
            exito = """
La nombraste entera.
Cada borde, cada pliegue, cada historia absorbida.

La sombra se detuvo.
No porque no pudiera moverse.
Sino porque al ser nombrada
perdió la voluntad de hacerlo.

Las cosas nombradas obedecen.
Por un rato.
"""
            fallo = """
Había demasiadas historias en ella.
No podías nombrarlas todas.

Y las que no nombraste
te encontraron primero.

El impacto no fue físico.
Fue conceptual.
Algo en tu mente se apagó.
Solo por un instante.
Pero suficiente.
"""

        else:  # Ladrón
            intro = """
No podés robarle la forma a una sombra.
Ya no tiene nada que no sea forma.

Pero podés hacer algo distinto:
darle lo que busca.

Un objetivo falso.
Algo tuyo que no sea vos.


[ ESPACIO para evadir ]
"""
            stat = "resistencia"
            dificultad = 5
            exito = """
Le diste un señuelo.
Un hábito tuyo.
Un miedo reconocible.

La sombra fue por eso.
Y mientras lo perseguía…
vos ya habías pasado.

Perdiste algo.
Pero lo elegiste vos.
Eso hace diferencia.
"""
            fallo = """
No te creyó.
O vio a través del señuelo.

La sombra no fue por el cebo.
Fue por vos directamente.

Y sabía exactamente dónde estabas.
Como si hubiera estado adentro tuyo
antes de que empezara la pelea.
"""

        resultado = engine.combate_narrativo(
            "assets/enemy4.jpg",
            intro,
            dificultad,
            stat,
            exito,
            fallo,
            psique_exito={"lucidez": 10, "corrupcion": 5},
            psique_fallo={"miedo": 12, "violencia": 8}
        )

        return resultado

    # ─────────────────────────────────────────
    # FASE 2 — DECISIÓN PSICOLÓGICA (original)
    # El nombre del jugador aparece aquí — momento dramático
    # ─────────────────────────────────────────
    def fase_psicologica(self, player, engine):

        player.recuperar(vida=5, energia=10)

        texto = f"""
El camino se estrecha.
Las paredes ya no son piedra.
Son… carne.
Respiran.
Late algo dentro.
Avanzás igual.
Llegás a una grieta.
Y ahí… los ves.
Versiones tuyas.
Distintas.
Una llora.
Otra sonríe.
Otra te observa con desprecio.

La voz dice:
"{player.name}. No sos uno. Elegí."

¿Qué hacés?
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl4.jpg",
            texto,
            opciones=True,
            opciones_lista=[
                "Aceptar todas las versiones",
                "Rechazar las versiones",
                "Atacar a las versiones"
            ]
        )

        if eleccion == "1":
            player.psique["lucidez"] += 20
            engine.mostrar_nivel(
                "assets/lvl4.jpg",
                """
No elegís.
Las aceptás.
Todas.
Las que duelen.
Las que avergüenzan.
Las que ocultabas.
No desaparecen.
Se alinean.
Y por un instante…
sos completo.
""",
                opciones=False
            )

        elif eleccion == "2":
            player.psique["culpa"] += 15
            player.psique["miedo"] += 10
            engine.mostrar_nivel(
                "assets/lvl4.jpg",
                """
Negás.
Una por una.
Intentás borrar lo que no te gusta.
Pero no se van.
Se deforman.
Se vuelven más intensas.
Más presentes.

La voz susurra:
"Negar es alimentar."
""",
                opciones=False
            )

        elif eleccion == "3":
            player.psique["violencia"] += 20
            player.psique["corrupcion"] += 10
            engine.mostrar_nivel(
                "assets/lvl4.jpg",
                """
Atacás.
Golpeás.
Destruís.
Pero cada versión rota…
se multiplica.
Ahora son más.
Más agresivas.
Más reales.
Y ya no esperan.
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
