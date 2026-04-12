class Intro:

    def __init__(self, ui):
        self.ui = ui

    def mostrar(self):
        pantallas = [
            {
                "imagen": "assets/intro1.jpg",
                "texto": """
Yerma no murió.

Solo olvidó para qué servía
estar viva.

Los dioses se fueron sin aviso.
Sin guerra.
Sin profecía.
Un día sostenían el orden.
Al siguiente, no estaban.

El mundo siguió girando por inercia.

Vos naciste en esa inercia.


[ ESPACIO para continuar ]
"""
            },
            {
                "imagen": "assets/intro2.jpg",
                "texto": """
Existe un lugar debajo de todo.

No en los mapas.
No en los libros sagrados
que quedaron.

Solo en los sueños de los que
están a punto de perder algo.

Lo llaman el Umbral.

Dicen que es una cueva.
Dicen que es una mente.

Dicen que es lo mismo.


[ ESPACIO para continuar ]
"""
            },
            {
                "imagen": "assets/intro3.jpg",
                "texto": """
Hace tres noches
escuchaste algo.

No con los oídos.
Desde adentro.

Una palabra sin sonido.
Una dirección sin nombre.

Esta mañana te encontraste
caminando hacia las afueras.

Sin provisiones.
Sin plan.

Como si una parte de vos
ya hubiera decidido
antes que vos.


[ ESPACIO para continuar ]
"""
            },
            {
                "imagen": "assets/lvl1.jpg",
                "texto": """
La entrada está frente a vos.

Piedra antigua.
Oscuridad total.

El aire que sale de ahí
no huele a tierra ni a muerte.

Huele a algo que no tiene
nombre todavía.

Podés darte vuelta.
Nadie te obliga.

Pero ya sabés
que no vas a hacerlo.


[ ESPACIO para comenzar ]
"""
            }
        ]

        for pantalla in pantallas:
            imagen = self.ui.cargar_imagen(pantalla["imagen"])
            self.ui.esperar_input(
                imagen,
                pantalla["texto"],
                opciones=False,
                opciones_lista=None,
                player=None
            )
