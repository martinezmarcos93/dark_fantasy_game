class Level4:
    def __init__(self):
        self.nombre = "El Rey de las Sombras"

    def jugar(self, player):
        print("\nEl pasaje se abre hacia una cámara inmensa.")
        print("No hay techo. No hay fondo.\n")

        print("En el centro… una figura sentada en un trono.\n")

        print("No podés verla claramente.")
        print("Pero sabés que te está mirando.\n")

        print("No habla con voz…")
        print("sino con comprensión.\n")

        print("Sentís que algo en vos está siendo leído.\n")

        # -------------------------
        # INTERPRETACIÓN DEL JUGADOR
        # -------------------------
        psique = player.psique

        rasgo_dominante = max(psique, key=psique.get)

        print("La entidad inclina levemente la cabeza.\n")

        if rasgo_dominante == "violencia":
            print("\"Elegís romper antes que entender.\"")
        elif rasgo_dominante == "miedo":
            print("\"Retrocedés incluso cuando no hay peligro.\"")
        elif rasgo_dominante == "culpa":
            print("\"Te castigás incluso cuando nadie te acusa.\"")
        elif rasgo_dominante == "lucidez":
            print("\"Ves… pero aún no aceptás.\"")
        elif rasgo_dominante == "corrupcion":
            print("\"Ya empezaste a disfrutarlo.\"")

        print("\nEl Rey extiende una mano.\n")

        print("\"Puedo mostrarte lo que buscás…")
        print("pero no sin darte algo a cambio.\"")

        print("\n¿Qué hacés?\n")
        print("1. Aceptar el trato")
        print("2. Rechazar y resistir")
        print("3. Atacar a la entidad")

        eleccion = input("\nElegí una opción (1-3): ")

        # -------------------------
        # OPCIÓN 1 — ACEPTAR
        # -------------------------
        if eleccion == "1":
            print("\nTomás su mano.\n")

            print("No sentís contacto…")
            print("sentís exposición.\n")

            print("El entorno desaparece.\n")

            print("Ves algo.\n")

            print("No es una visión…")
            print("es un recuerdo que no querías ver.\n")

            print("La voz del Rey:")
            print("\"El conocimiento siempre revela demasiado.\"")

            player.modificar_psique({
                "lucidez": 20,
                "corrupcion": 10,
                "culpa": 5
            })

            if player.psique["lucidez"] > 40:
                print("\nAhora entendés algo que no podés olvidar.")
                print("Ni ignorar.\n")

            return "continuar"

        # -------------------------
        # OPCIÓN 2 — RESISTIR
        # -------------------------
        elif eleccion == "2":
            print("\nDás un paso atrás.\n")

            print("La figura no se mueve.\n")

            print("Pero el espacio se cierra.\n")

            print("Sentís presión en el pecho.\n")

            print("La voz, firme:")
            print("\"Negar no es escapar.\"")

            player.modificar_psique({
                "miedo": 15,
                "culpa": 5
            })

            if player.psique["miedo"] > 35:
                print("\nTu mente entra en pánico.")
                print("No podés sostener la realidad.\n")
                return "muerte"

            return "continuar"

        # -------------------------
        # OPCIÓN 3 — ATACAR
        # -------------------------
        elif eleccion == "3":
            print("\nAvanzás con intención de atacar.\n")

            print("Pero no hay distancia.\n")

            print("Nunca la hubo.\n")

            print("Tu acción se pliega sobre vos mismo.\n")

            print("Sentís el impacto… desde adentro.\n")

            print("La entidad habla por última vez:")
            print("\"No podés destruir lo que te contiene.\"")

            player.modificar_psique({
                "violencia": 20,
                "corrupcion": 15
            })

            if player.psique["violencia"] > 40:
                print("\nTu propia agresión te desgarra.\n")
                return "muerte"

            return "continuar"

        # -------------------------
        # INPUT INVÁLIDO
        # -------------------------
        else:
            print("\nEl Rey cierra los ojos.\n")
            print("Dejar que el tiempo decida… también es rendirse.\n")

            return "muerte"