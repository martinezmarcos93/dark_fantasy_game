from game.enemies import crear_grieta

class Level9:

    def __init__(self):
        self.nombre = "La Biblioteca del Olvido"

    def distorsionar_texto(self, texto, player):
        """Distorsion extrema en el nivel mas profundo antes del boss."""
        psique = player.psique

        # Miedo alto: texto en minusculas con pausas entre palabras
        if psique["miedo"] > 25:
            texto = texto.lower()
            texto = "\n".join(
                "  ".join(l.split()) if l.strip() else l
                for l in texto.split("\n")
            )

        # Corrupcion alta: corromper vocales en palabras largas
        if psique["corrupcion"] > 35:
            _MAP = str.maketrans("aeiou", "áëïøù")
            lineas = []
            for linea in texto.split("\n"):
                palabras = linea.split(" ")
                nueva = []
                for i, p in enumerate(palabras):
                    if len(p) > 4 and i % 2 == 0:
                        p = p.translate(_MAP)
                    nueva.append(p)
                lineas.append(" ".join(nueva))
            texto = "\n".join(lineas)

        # Lucidez alta: marco de meta-consciencia doble
        if psique["lucidez"] > 35:
            texto = "[[ " + texto.strip() + " ]]"

        return texto

    def fase_combate(self, player, engine):
        enemy = crear_grieta()
        return engine.combate_narrativo(enemy)

    def fase_psicologica(self, player, engine):

        player.recuperar(vida=3, energia=6)

        texto = """
Los libros no tienen titulos.

Las paginas estan en blanco.

Pero cuando los abris,
algo se escribe.
No con tinta.
Con ausencia.

Cada libro contiene
algo que olvidaste.
O que decidiste no recordar.

Hay uno que brilla mas que los otros.

¿Que hacés?
"""

        eleccion = engine.mostrar_nivel(
            "assets/lvl9.jpg",
            self.distorsionar_texto(texto, player),
            opciones=True,
            opciones_lista=[
                "Abrir el libro que brilla.",
                "Leer un libro al azar.",
                "Cerrar los ojos y salir sin leer ninguno."
            ]
        )

        if eleccion == "1":
            player.registrar_decision("Abriste el libro que brillaba en la Biblioteca del Olvido.")
            player.psique["lucidez"] += 15
            player.psique["corrupcion"] += 8
            texto_r = """
Lo abris.

El libro contiene
lo que elegiste no saber.

No porque no pudieras saberlo.
Sino porque saber
hubiera requerido cambiar.

Ahora lo sabes.

No cambia lo que hiciste.
Pero cambia lo que sos.
"""
            engine.mostrar_nivel(
                "assets/lvl9.jpg",
                self.distorsionar_texto(texto_r, player),
                opciones=False
            )

        elif eleccion == "2":
            player.registrar_decision("Leiste un libro al azar en la Biblioteca del Olvido.")
            player.psique["culpa"] += 10
            player.psique["miedo"] += 8
            texto_r = """
Abris uno sin pensar.

El contenido no tiene sentido
en el orden en que aparece.

Pero tiene sentido
en un orden que no controlás.

No encontraste lo que buscabas.
Encontraste algo peor:
lo que no sabias que buscabas.
"""
            engine.mostrar_nivel(
                "assets/lvl9.jpg",
                self.distorsionar_texto(texto_r, player),
                opciones=False
            )

        elif eleccion == "3":
            player.registrar_decision("Saliste de la Biblioteca del Olvido sin leer nada.")
            player.psique["corrupcion"] += 15
            texto_r = """
Cerrás los ojos.

Salis.

Lo que no leiste
no desaparece.
Solo pierde nombre.

Y lo sin nombre
crece en los espacios
donde no mirás.

La biblioteca sigue ahi.
Con todos sus libros.
Con el tuyo.
"""
            engine.mostrar_nivel(
                "assets/lvl9.jpg",
                self.distorsionar_texto(texto_r, player),
                opciones=False
            )

    def jugar(self, player, engine):
        resultado = self.fase_combate(player, engine)
        if resultado == "muerte":
            return "muerte"

        self.fase_psicologica(player, engine)
        return "continuar"
