class Level3:
    def __init__(self):
        self.nombre = "El Ritual de la Entrega"

    def jugar(self, player):
        print("\nEl túnel desemboca en una sala amplia.")
        print("Las paredes están cubiertas de símbolos.\n")

        print("En el centro hay un altar de piedra.")
        print("Sobre él… un libro abierto.\n")

        print("Las páginas no están escritas.")
        print("Esperan.\n")

        print("La voz regresa, pero ya no parece externa:")
        print("\"Todo conocimiento exige un precio.\"")

        print("\nSentís que el altar… te reconoce.\n")

        print("¿Qué ofrecés?\n")
        print("1. Tu sangre (sacrificio físico)")
        print("2. Un recuerdo (sacrificio mental)")
        print("3. Nada (rechazar el ritual)")

        eleccion = input("\nElegí una opción (1-3): ")

        # -------------------------
        # OPCIÓN 1 — SANGRE
        # -------------------------
        if eleccion == "1":
            print("\nCortás tu mano y dejás caer la sangre sobre el libro.\n")

            print("Las páginas se llenan solas.")
            print("Símbolos que no entendés… pero sentís.\n")

            print("Algo en vos se fortalece.")
            print("Algo en vos se rompe.\n")

            print("La voz susurra:")
            print("\"El cuerpo es la primera puerta.\"")

            player.modificar_psique({
                "violencia": 10,
                "corrupcion": 15
            })

            player.modificar_stats({
                "fuerza": 2
            })

            return "continuar"

        # -------------------------
        # OPCIÓN 2 — RECUERDO
        # -------------------------
        elif eleccion == "2":
            print("\nCerrás los ojos.\n")

            print("Un recuerdo emerge…")
            print("algo importante… algo tuyo.\n")

            print("El altar lo toma.\n")

            print("Intentás recordarlo otra vez…")
            print("pero ya no está.\n")

            print("Sentís un vacío.\n")

            print("La voz habla con calma:")
            print("\"La mente también sangra.\"")

            player.modificar_psique({
                "lucidez": 15,
                "culpa": 10
            })

            player.modificar_stats({
                "mente": 2
            })

            # riesgo si ya viene cargado emocionalmente
            if player.psique["culpa"] > 25:
                print("\nIntentás aferrarte a lo que perdiste…")
                print("pero ya no existe.\n")

                print("Algo en tu identidad colapsa.")
                return "muerte"

            return "continuar"

        # -------------------------
        # OPCIÓN 3 — RECHAZO
        # -------------------------
        elif eleccion == "3":
            print("\nRetrocedés.\n")

            print("El altar permanece en silencio.\n")

            print("Pero el entorno cambia.\n")

            print("Las paredes laten.")
            print("El aire se vuelve espeso.\n")

            print("La voz ya no es amable:")
            print("\"Rechazar también es elegir.\"")

            player.modificar_psique({
                "miedo": 15
            })

            # castigo: el juego empieza a volverse hostil
            if player.psique["miedo"] > 20:
                print("\nEl espacio se distorsiona.")
                print("No encontrás la salida.\n")

                print("El dungeon no acepta tu negativa.")
                return "muerte"

            return "continuar"

        # -------------------------
        # INPUT INVÁLIDO
        # -------------------------
        else:
            print("\nEl libro se cierra de golpe.\n")
            print("Elegir tarde… es no elegir.\n")

            return "muerte"