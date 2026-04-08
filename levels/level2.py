class Level2:
    def __init__(self):
        self.nombre = "El Espejo de las Formas"

    def jugar(self, player):
        print("\nAvanzás más profundo en la cueva.")
        print("El aire cambia. Es más denso.\n")

        print("Llegás a una cámara circular.")
        print("En el centro… hay un espejo.\n")

        print("Pero no refleja tu cuerpo.")
        print("Refleja… algo más.\n")

        print("La voz regresa:")
        print("\"No sos lo que creés. Mirá.\"")

        print("\n¿Qué hacés?\n")
        print("1. Mirar fijamente el espejo")
        print("2. Romper el espejo")
        print("3. Dar la espalda y seguir")

        eleccion = input("\nElegí una opción (1-3): ")

        # -------------------------
        # OPCIÓN 1 — VER LA VERDAD
        # -------------------------
        if eleccion == "1":
            print("\nTe acercás al espejo.\n")

            print("No ves tu rostro.")
            print("Ves decisiones.")
            print("Ves miedo.")
            print("Ves violencia.\n")

            print("Cada cosa que hiciste… te observa.\n")

            print("No podés apartar la mirada.\n")

            print("La voz susurra:")
            print("\"Esto sos cuando nadie te ve.\"")

            player.modificar_psique({
                "lucidez": 15,
                "culpa": 10
            })

            # Si la culpa es muy alta, puede quebrarse
            if player.psique["culpa"] > 20:
                print("\nLa verdad te resulta insoportable.")
                print("Tu mente colapsa ante su propio reflejo.")
                return "muerte"

            return "continuar"

        # -------------------------
        # OPCIÓN 2 — NEGACIÓN VIOLENTA
        # -------------------------
        elif eleccion == "2":
            print("\nGolpeás el espejo.\n")

            print("Se rompe.\n")

            print("Pero cada fragmento sigue reflejando algo distinto.\n")

            print("Ahora hay cien versiones de vos mirándote.\n")

            print("La voz ríe por primera vez:")
            print("\"Podés romper la forma… pero no lo que contiene.\"")

            player.modificar_psique({
                "violencia": 15,
                "corrupcion": 10
            })

            return "continuar"

        # -------------------------
        # OPCIÓN 3 — EVASIÓN
        # -------------------------
        elif eleccion == "3":
            print("\nDesviás la mirada.\n")

            print("Decidís no ver.\n")

            print("El espejo… sigue ahí.\n")

            print("Sentís que algo quedó pendiente.\n")

            print("La voz, ahora distante:")
            print("\"Lo que evitás… te espera más adelante.\"")

            player.modificar_psique({
                "miedo": 10
            })

            return "continuar"

        # -------------------------
        # INPUT INVÁLIDO
        # -------------------------
        else:
            print("\nEl espejo tiembla.\n")
            print("No decidir… también es una decisión.\n")

            print("Tu reflejo sonríe sin vos hacerlo.\n")

            return "muerte"