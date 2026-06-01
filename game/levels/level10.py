from game.enemies import crear_testigo, crear_umbral_encarnado

class Level10:

    def __init__(self):
        self.nombre = "El Espejo Final"

    def fase_combate_testigo(self, player, engine):
        """Primera fase: El Testigo. Combate normal de 3 rondas."""
        enemy = crear_testigo()
        return engine.combate_narrativo(enemy)

    def fase_combate_boss(self, player, engine):
        """Segunda fase: El Umbral Encarnado. 5 rondas. Solo si el jugador sigue vivo."""
        player.recuperar(vida=20, energia=20)

        engine.mostrar_nivel(
            "assets/lvl10.jpg",
            f"""
{player.name}.

Pasaste al Testigo.

Pero lo que el Testigo guardaba
ahora esta frente a vos.

No es una recompensa.
No es un castigo.

Es lo que siempre estuvo
al final de este camino.

El Umbral Encarnado.

Cinco rondas.
No porque sean necesarias.
Sino porque esto
no termina rapido.


[ ESPACIO para continuar ]
""",
            opciones=False
        )

        enemy = crear_umbral_encarnado()
        return engine.combate_narrativo(enemy)

    def jugar(self, player, engine):
        # Fase 1: El Testigo
        resultado = self.fase_combate_testigo(player, engine)
        if resultado == "muerte":
            return "muerte"

        # Si sobrevivio al Testigo: El Espejo
        engine.mostrar_nivel(
            "assets/lvl10.jpg",
            f"""
El Testigo se hace a un lado.

Frente a vos hay un espejo.

No refleja la caverna.
Refleja un mundo con luz natural.
Con gente.
Con ruido de fondo.
Con el olor de algo cocinandose.

Todo lo que dejaste afuera.

Y en el centro del reflejo
hay algo que tiene tu forma
pero que no sos vos.

O si lo es.
""",
            opciones=False
        )

        # Fase 2: El boss
        resultado = self.fase_combate_boss(player, engine)
        if resultado == "muerte":
            return "muerte"

        # Escena final despues del boss
        engine.mostrar_nivel(
            "assets/lvl10.jpg",
            f"""
{player.name}.

El Umbral Encarnado no desaparecio.

Nunca iba a desaparecer.

Pero ya no bloquea el camino.

No porque lo hayas vencido.
Sino porque algo en el reconocio
que llegaste hasta aca.

Y eso es suficiente para pasar.

Por ahora.
""",
            opciones=False
        )

        return "continuar"
