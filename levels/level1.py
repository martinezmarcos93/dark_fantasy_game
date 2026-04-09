class Level1:
    def __init__(self):
        self.nombre = "La Cueva del Origen"

    def jugar(self, player, engine):
        print("\nTe adentras en la cueva.")
        print("No hay antorchas. No hay sonido.")
        print("Solo oscuridad.\n")

        print("Algo… respira en la profundidad.")
        print("No lo ves, pero lo sentís.\n")

        print("Una voz, o tal vez un pensamiento que no es tuyo, susurra:")
        print("\n\"Antes de la luz… ya estabas aquí.\"")

        print("\n¿Qué hacés?\n")
        print("1. Avanzar hacia la oscuridad")
        print("2. Encender una antorcha")
        print("3. Llamar para saber quién está ahí")

        texto = """
        Te adentras en la cueva.

        No hay luz.
        Solo oscuridad.

        1. Avanzar
        2. Encender antorcha
        3. Llamar
        """

        eleccion = engine.mostrar_nivel(
            "assets/lvl 1 v1.jpg",
            texto
        )

        # -------------------------
        # OPCIÓN 1
        # -------------------------
        if eleccion == "1":
            print("\nCaminás sin ver.")
            print("Cada paso se siente… correcto.")
            print("Como si ya hubieras estado ahí antes.\n")

            print("La oscuridad no te rechaza.")
            print("Te envuelve.\n")

            print("La voz vuelve:")
            print("\"Recordar es descender.\"")

            player.modificar_psique({
                "lucidez": 10,
                "corrupcion": 5
            })

            return "continuar"

        # -------------------------
        # OPCIÓN 2
        # -------------------------
        elif eleccion == "2":
            print("\nEncendés una antorcha.")
            print("La llama tiembla violentamente.\n")

            print("Por un instante, ves las paredes…")
            print("Están cubiertas de marcas.")
            print("No… no son marcas.\n")

            print("Son manos.")
            print("Miles de manos intentando salir.\n")

            print("La llama se apaga sola.")

            print("\nLa voz susurra, ahora más cerca:")
            print("\"La luz no revela… interrumpe.\"")

            player.modificar_psique({
                "miedo": 10,
                "culpa": 5
            })

            return "continuar"

        # -------------------------
        # OPCIÓN 3 (PELIGROSA)
        # -------------------------
        elif eleccion == "3":
            print("\nTu voz rompe el silencio.")

            print("Error.\n")

            print("Algo responde.\n")

            print("No con palabras…")
            print("sino con presencia.\n")

            print("Sentís que algo te escucha desde adentro.")
            print("No desde la cueva… desde vos.\n")

            print("La voz ya no susurra:")
            print("\"Ahora sabe que estás aquí.\"")

            player.modificar_psique({
                "corrupcion": 15,
                "miedo": 15
            })

            # pequeña chance de muerte inmediata (para generar tensión)
            if player.psique["miedo"] > 10:
                print("\nTu mente no soporta lo que acaba de percibir.")
                return "muerte"

            return "continuar"

        # -------------------------
        # INPUT INVÁLIDO
        # -------------------------
        else:
            print("\nDudás demasiado.")
            print("La cueva no espera.\n")

            return "muerte"