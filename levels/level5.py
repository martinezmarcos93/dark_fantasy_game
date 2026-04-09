class Level5:
    def __init__(self):
        self.nombre = "Las Moradas de los Muertos"

    def distorsionar_texto(self, texto, player):
        psique = player.psique

        # Distorsión por miedo
        if psique["miedo"] > 30:
            texto = texto.replace(" ", "  ")
            texto = texto.lower()

        # Distorsión por corrupción
        if psique["corrupcion"] > 40:
            texto = texto.replace("a", "á").replace("e", "ë")

        # Distorsión por lucidez (más críptico)
        if psique["lucidez"] > 40:
            texto = "..." + texto + "..."

        return texto

    def jugar(self, player, engine):
        print("\nCruzás un umbral.\n")

        print("Ya no hay cueva.")
        print("Ya no hay camino.\n")

        print("Solo puertas.\n")

        print("Muchas.\n")

        print("Demasiadas.\n")

        print("Cada una… conduce a algo distinto.\n")

        print("Pero sabés algo.\n")
        print("No todas son para vos.\n")

        psique = player.psique

        # -------------------------
        # DETERMINAR MORADA
        # -------------------------
        if psique["violencia"] > 30:
            destino = "guerra"
        elif psique["miedo"] > 30:
            destino = "vacío"
        elif psique["corrupcion"] > 40:
            destino = "abismo"
        elif psique["lucidez"] > 40:
            destino = "verdad"
        else:
            destino = "olvido"

        # -------------------------
        # DESCRIPCIONES
        # -------------------------
        descripciones = {
            "guerra": "Escuchás acero. Gritos. Un campo infinito donde la lucha nunca termina.",
            "vacío": "No hay sonido. No hay forma. Solo una extensión sin límites.",
            "abismo": "Algo te observa desde la oscuridad. Y sonríe.",
            "verdad": "Una luz inmóvil. No cálida. No fría. Solo… real.",
            "olvido": "Nada te espera. Ni siquiera vos mismo."
        }

        descripcion = descripciones[destino]
        descripcion = self.distorsionar_texto(descripcion, player)

        print("Una puerta se abre frente a vos.\n")
        print(descripcion + "\n")

        print("¿Entrás?\n")
        print("1. Sí")
        print("2. No")

        eleccion = input("\nElegí una opción (1-2): ")

        # -------------------------
        # ENTRAR
        # -------------------------
        if eleccion == "1":
            print("\nCruzás el umbral.\n")

            if destino == "guerra":
                print("La lucha te consume.\n")
                return "muerte"

            elif destino == "vacío":
                print("Te disolvés lentamente.\n")
                return "muerte"

            elif destino == "abismo":
                print("Algo en vos despierta.\n")
                player.modificar_psique({"corrupcion": 20})
                return "continuar"

            elif destino == "verdad":
                print("Entendés.\n")
                player.modificar_psique({"lucidez": 20})
                return "continuar"

            elif destino == "olvido":
                print("Desaparecés.\n")
                return "muerte"

        # -------------------------
        # RECHAZAR
        # -------------------------
        elif eleccion == "2":
            print("\nIntentás retroceder.\n")

            print("Pero ya cruzaste algo.\n")

            print("La voz final dice:")
            print("\"Nadie sale igual.\"")

            player.modificar_psique({
                "miedo": 10,
                "culpa": 5
            })

            if player.psique["miedo"] > 40:
                print("\nTu mente colapsa.")
                return "muerte"

            return "continuar"

        # -------------------------
        # INPUT INVÁLIDO
        # -------------------------
        else:
            print("\nLas puertas se cierran.\n")
            print("No decidir… también es un destino.\n")

            return "muerte"