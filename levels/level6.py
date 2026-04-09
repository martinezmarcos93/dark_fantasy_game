class Level6:
    def __init__(self):
        self.nombre = "El Umbral Final"

    def distorsionar_texto(self, texto, player):
        psique = player.psique

        # Distorsión más intensa que en level 5
        if psique["miedo"] > 40:
            texto = texto.lower()
            texto = texto.replace(" ", "...")

        if psique["corrupcion"] > 50:
            texto = texto.replace("o", "ø").replace("e", "ë")

        if psique["lucidez"] > 50:
            texto = "/// " + texto + " ///"

        return texto

    def jugar(self, player, engine):
        print("\nNo hay puerta.\n")
        print("No hay sala.\n")

        print("Solo estás vos.\n")

        print("Y algo más.\n")

        print("No frente a vos.\n")
        print("No detrás.\n")

        print("Sino… coincidiendo.\n")

        print("No podés verlo.")
        print("Porque no está separado.\n")

        print("La voz final no habla.\n")

        print("Pensás algo…\n")
        print("y responde.\n")

        psique = player.psique

        # Construcción del “yo reflejado”
        print("Eso que sos… se manifiesta.\n")

        rasgos = []
        for clave, valor in psique.items():
            if valor > 20:
                rasgos.append(clave)

        if not rasgos:
            rasgos.append("vacío")

        descripcion = "Te enfrentás a: " + ", ".join(rasgos)
        descripcion = self.distorsionar_texto(descripcion, player)

        print(descripcion + "\n")

        print("No hay opciones correctas.\n")

        print("¿Qué hacés?\n")
        print("1. Aceptarlo")
        print("2. Negarlo")
        print("3. Destruirlo")

        eleccion = input("\nElegí una opción (1-3): ")

        # -------------------------
        # ACEPTACIÓN
        # -------------------------
        if eleccion == "1":
            print("\nNo luchás.\n")

            print("No escapás.\n")

            print("Permitís.\n")

            print("Todo lo que viste…")
            print("todo lo que hiciste…")
            print("todo lo que sos…\n")

            print("permanece.\n")

            print("Pero ya no te define.\n")

            player.modificar_psique({
                "lucidez": 30
            })

            return "continuar"

        # -------------------------
        # NEGACIÓN
        # -------------------------
        elif eleccion == "2":
            print("\nRetrocedés.\n")

            print("Intentás separarte.\n")

            print("Pero no hay distancia.\n")

            print("Nunca la hubo.\n")

            print("Cuanto más negás…")
            print("más fuerte se vuelve.\n")

            player.modificar_psique({
                "miedo": 20,
                "culpa": 10
            })

            if player.psique["miedo"] > 60:
                print("\nTe perdés en tu propia evasión.\n")
                return "muerte"

            return "continuar"

        # -------------------------
        # DESTRUCCIÓN
        # -------------------------
        elif eleccion == "3":
            print("\nIntentás eliminarlo.\n")

            print("Pero eso implica eliminarte.\n")

            print("Sentís cómo todo se desgarra.\n")

            print("La identidad colapsa.\n")

            player.modificar_psique({
                "violencia": 30,
                "corrupcion": 20
            })

            if player.psique["corrupcion"] > 70:
                print("\nAlgo nuevo ocupa tu lugar.\n")
                return "continuar"

            return "muerte"

        # -------------------------
        # INPUT INVÁLIDO
        # -------------------------
        else:
            print("\nNo actuar… también es una forma de desaparecer.\n")
            return "muerte"