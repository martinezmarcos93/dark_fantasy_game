from game.enemies import crear_archivista

class Level8:

    def __init__(self):
        self.nombre = "El Rio de Recuerdos"

    def fase_combate(self, player, engine):
        enemy = crear_archivista()
        return engine.combate_narrativo(enemy)

    def fase_psicologica(self, player, engine):

        player.recuperar(vida=4, energia=8)

        texto = f"""
El río no tiene corriente.

Sus aguas reflejan momentos
que reconocés sin querer recordar.

Hay algo flotando.
Un objeto.
No sabés qué es hasta que lo ves.

Es algo que perdiste.
O que abandonaste.
La diferencia importa
y no la sabés.

La voz del río:
"¿Lo tomás?"

¿Qué hacés?
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl8.jpg",
            texto,
            opciones=True,
            opciones_lista=[
                "Entrar al rio y tomarlo.",
                "Observarlo desde la orilla sin tocarlo.",
                "Hundirlo deliberadamente."
            ]
        )

        if eleccion == "1":
            player.registrar_decision("Entraste al rio de recuerdos y recuperaste lo que estaba flotando.")
            player.psique["lucidez"] += 10
            player.psique["culpa"] += 10
            engine.mostrar_nivel(
                "assets/lvl8.jpg",
                """
Entrás.

El agua es fría pero no duele.

Tomás el objeto.
Al sostenerlo recordás
no solo qué era
sino quién eras cuando lo tenías.

No es el mismo.
No sos el mismo.

Pero ahora ambos están en el mismo lugar.
""",
                opciones=False
            )

        elif eleccion == "2":
            player.registrar_decision("Observaste desde la orilla lo que flotaba en el rio.")
            player.psique["miedo"] += 8
            player.psique["lucidez"] += 8
            engine.mostrar_nivel(
                "assets/lvl8.jpg",
                """
Te quedás en la orilla.

Lo mirás.

El objeto flota sin alejarse.
Como si esperara.

No tomarlo también es una decisión.
Una que entendés
solo parcialmente.

El río sigue.
El objeto también.
""",
                opciones=False
            )

        elif eleccion == "3":
            player.registrar_decision("Hundiste deliberadamente lo que flotaba en el rio.")
            player.psique["violencia"] += 10
            player.psique["corrupcion"] += 8
            engine.mostrar_nivel(
                "assets/lvl8.jpg",
                """
Lo hundís.

Con intención.

El objeto desaparece bajo el agua.
El reflejo no.

Sigue ahí.
Mirándote desde abajo.

Algunas cosas no se hunden.
Solo se profundizan.
""",
                opciones=False
            )

    def jugar(self, player, engine):
        resultado = self.fase_combate(player, engine)
        if resultado == "muerte":
            return "muerte"

        self.fase_psicologica(player, engine)
        return "continuar"
