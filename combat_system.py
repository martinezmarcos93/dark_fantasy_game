import random

# ═══════════════════════════════════════════════════════════════
# COMBAT SYSTEM — Descenso al Umbral
#
# Arquitectura:
#   CombatState  — estado mutable de una pelea
#   Enemy        — configuración estática de un enemigo
#   combate_completo() — entry point que llama game_engine y niveles
# ═══════════════════════════════════════════════════════════════


# ───────────────────────────────────────────────────────────────
# HECHIZOS DISPONIBLES PARA EL HECHICERO
# Cada hechizo es un dict con nombre, descripción corta (para el
# botón), efecto (string interno) e immunidades por enemigo.
# ───────────────────────────────────────────────────────────────
HECHIZOS = [
    {
        "id": "fuego",
        "nombre": "Palabra de Fuego",
        "descripcion": "Daño directo alto",
        "efecto": "daño_alto",
        "inmune": []
    },
    {
        "id": "velo",
        "nombre": "Velo de Sombra",
        "descripcion": "Reduce daño próxima ronda",
        "efecto": "defensa",
        "inmune": []
    },
    {
        "id": "resonancia",
        "nombre": "Resonancia Mental",
        "descripcion": "Ventaja en siguiente tirada",
        "efecto": "ventaja",
        "inmune": []
    },
    {
        "id": "nombre",
        "nombre": "Nombre Verdadero",
        "descripcion": "Paraliza al enemigo una ronda",
        "efecto": "paralizar",
        "inmune": ["sacerdote"]  # El Sacerdote Sin Rostro no tiene nombre
    },
    {
        "id": "abismo",
        "nombre": "Fragmento del Abismo",
        "descripcion": "Daño masivo — te daña también",
        "efecto": "nuclear",
        "inmune": []
    },
]


# ───────────────────────────────────────────────────────────────
# ESTADO DE COMBATE
# Se crea al inicio de cada pelea y se destruye al terminar.
# ───────────────────────────────────────────────────────────────
class CombatState:
    def __init__(self, player):
        self.ronda_actual = 1
        self.rondas_max   = 3

        # Marcador de rondas ganadas (jugador vs enemigo)
        self.rondas_jugador = 0
        self.rondas_enemigo = 0

        # Estado del ladrón
        self.en_posicion = False   # True tras Observar exitoso

        # Hechizos disponibles (copias para no mutar la lista global)
        self.hechizos_disponibles = [h["id"] for h in HECHIZOS]

        # Acciones especiales del guerrero
        self.golpe_cargado_disponible = True
        self.furia_disponible         = True

        # Modificadores activos esta ronda
        self.defensa_activa    = False   # Velo de Sombra
        self.ventaja_activa    = False   # Resonancia Mental
        self.enemigo_paralizado = False  # Nombre Verdadero

        # Daño total infligido (para narrativa de cierre)
        self.daño_jugador_total  = 0
        self.daño_enemigo_total  = 0


# ───────────────────────────────────────────────────────────────
# CONFIGURACIÓN DE ENEMIGO
# Los niveles instancian Enemy con sus propios textos y patrones.
# ───────────────────────────────────────────────────────────────
class Enemy:
    def __init__(
        self,
        nombre,
        id_enemigo,
        imagen,
        vida,
        dificultad,
        texto_intro,           # Pantalla antes del combate
        textos_ataque,         # dict: situacion → texto narrativo del ataque enemigo
        textos_derrota,        # Texto si el jugador gana la pelea (2/3 rondas)
        textos_victoria,       # Texto si el enemigo gana
        texto_empate,          # Texto si 1-1 en rondas (cierre por estadística)
        psique_victoria_jugador,  # Psique si jugador gana
        psique_derrota_jugador,   # Psique si jugador pierde
        inmunidades=None       # Lista de efectos a los que es inmune
    ):
        self.nombre     = nombre
        self.id         = id_enemigo
        self.imagen     = imagen
        self.vida       = vida
        self.vida_max   = vida
        self.dificultad = dificultad

        self.texto_intro  = texto_intro
        self.textos_ataque = textos_ataque
        self.textos_derrota = textos_derrota
        self.textos_victoria = textos_victoria
        self.texto_empate   = texto_empate

        self.psique_victoria_jugador = psique_victoria_jugador
        self.psique_derrota_jugador  = psique_derrota_jugador
        self.inmunidades = inmunidades or []

    def esta_debilitado(self):
        return self.vida < self.vida_max * 0.4

    def elegir_accion(self, state, clase_jugador):
        """
        Decide qué hace el enemigo esta ronda según contexto.
        Devuelve string: clave de textos_ataque + parámetros de daño.
        """
        if state.enemigo_paralizado:
            return "paralizado"

        # Reacciona al ladrón en posición
        if clase_jugador == "Ladrón" and state.en_posicion:
            if "detectar_sigilo" in self.textos_ataque:
                return "detectar_sigilo"

        # Cuando está muy dañado, ataca más fuerte
        if self.esta_debilitado():
            if "desesperado" in self.textos_ataque:
                return "desesperado"

        # Patrón por ronda (cíclico)
        patrones_normales = [k for k in self.textos_ataque
                             if k not in ("detectar_sigilo", "desesperado", "paralizado")]
        if not patrones_normales:
            return "default"
        idx = (state.ronda_actual - 1) % len(patrones_normales)
        return patrones_normales[idx]


# ───────────────────────────────────────────────────────────────
# TIRADA DE DADOS
# ───────────────────────────────────────────────────────────────
def tirar(stat, dificultad, ventaja=False):
    """
    2d6 + stat vs dificultad * 2.
    Con ventaja: 3d6 toma los 2 mejores.
    Devuelve dict {exito, tirada, umbral}.
    """
    if ventaja:
        dados = sorted([random.randint(1,6), random.randint(1,6), random.randint(1,6)])
        resultado = dados[1] + dados[2] + stat
    else:
        resultado = random.randint(1,6) + random.randint(1,6) + stat

    umbral = dificultad * 2
    return {
        "exito":  resultado >= umbral,
        "tirada": resultado,
        "umbral": umbral
    }


# ───────────────────────────────────────────────────────────────
# RESOLVER ACCIÓN DEL JUGADOR
# Devuelve dict con texto narrativo, daño al enemigo, daño al
# jugador (por efectos propios), y si la ronda fue ganada.
# ───────────────────────────────────────────────────────────────
def resolver_accion_jugador(accion, player, enemy, state):
    clase  = player.clase
    stats  = player.stats
    result = {"texto": "", "daño_enemigo": 0, "daño_jugador": 0, "ronda_ganada": False, "nuevo_estado": {}}

    # ── GUERRERO ──────────────────────────────────────────────
    if clase == "Guerrero":

        if accion == "golpe_directo":
            t = tirar(stats["fuerza"], enemy.dificultad, state.ventaja_activa)
            if t["exito"]:
                daño = random.randint(1, enemy.dificultad) * 4
                result["texto"] = f"Tu golpe conecta. El guardián retrocede.\n[ Daño infligido: {daño} ]"
                result["daño_enemigo"] = daño
                result["ronda_ganada"] = True
            else:
                daño_recibido = random.randint(enemy.dificultad, enemy.dificultad * 2) * 2
                result["texto"] = f"Fallaste la apertura. Te golpea antes de que puedas conectar.\n[ Daño recibido: {daño_recibido} ]"
                result["daño_jugador"] = daño_recibido

        elif accion == "defender":
            t = tirar(stats["resistencia"], enemy.dificultad, state.ventaja_activa)
            daño_bloqueado = random.randint(2, 6) * 2
            if t["exito"]:
                daño_contra = random.randint(1, enemy.dificultad) * 2
                result["texto"] = f"Absorbés el golpe y contraatacás.\n[ Daño bloqueado: {daño_bloqueado} — Contraataque: {daño_contra} ]"
                result["daño_enemigo"] = daño_contra
                result["nuevo_estado"]["defensa_activa"] = True
            else:
                daño_parcial = random.randint(1, enemy.dificultad) * 2
                result["texto"] = f"Intentás cubrirte pero el impacto pasa igual.\n[ Daño parcial recibido: {daño_parcial} ]"
                result["daño_jugador"] = daño_parcial

        elif accion == "golpe_cargado":
            state.golpe_cargado_disponible = False
            t = tirar(stats["fuerza"], enemy.dificultad, state.ventaja_activa)
            if t["exito"]:
                daño = random.randint(enemy.dificultad, enemy.dificultad * 2) * 5
                result["texto"] = f"El golpe cargado encuentra su blanco. Impacto devastador.\n[ Daño infligido: {daño} ]"
                result["daño_enemigo"] = daño
                result["ronda_ganada"] = True
            else:
                daño_recibido = random.randint(enemy.dificultad, enemy.dificultad * 2) * 3
                result["texto"] = f"El golpe cargado erró. Quedaste expuesto y lo pagaste caro.\n[ Daño recibido: {daño_recibido} ]"
                result["daño_jugador"] = daño_recibido

        elif accion == "furia":
            state.furia_disponible = False
            daño = random.randint(enemy.dificultad * 2, enemy.dificultad * 3) * 4
            daño_propio = random.randint(5, 15)
            result["texto"] = f"La furia ignora todo. Golpeás sin control, sin defensa.\n[ Daño infligido: {daño} — Daño propio: {daño_propio} ]"
            result["daño_enemigo"] = daño
            result["daño_jugador"] = daño_propio
            result["ronda_ganada"] = True

    # ── HECHICERO ─────────────────────────────────────────────
    elif clase == "Hechicero":

        if accion == "daga":
            t = tirar(stats["fuerza"], enemy.dificultad)
            if t["exito"]:
                daño = random.randint(1, 3) * 2
                result["texto"] = f"La daga encuentra un hueco. No es mucho, pero es algo.\n[ Daño infligido: {daño} ]"
                result["daño_enemigo"] = daño
            else:
                daño_recibido = random.randint(enemy.dificultad, enemy.dificultad * 2) * 2
                result["texto"] = f"Sin magia, la daga no alcanza. Te golpea sin piedad.\n[ Daño recibido: {daño_recibido} ]"
                result["daño_jugador"] = daño_recibido

        else:
            # Es un hechizo
            hechizo = next((h for h in HECHIZOS if h["id"] == accion), None)
            if not hechizo:
                result["texto"] = "Algo falló. El hechizo no existe."
                return result

            state.hechizos_disponibles.remove(accion)

            # Verificar inmunidad del enemigo
            if enemy.id in hechizo["inmune"]:
                daño_recibido = random.randint(enemy.dificultad, enemy.dificultad * 2) * 2
                result["texto"] = (
                    f"'{hechizo['nombre']}' no encuentra donde aferrarse.\n"
                    f"Este ser no tiene lo que buscás.\nEl rebote te golpea a vos.\n"
                    f"[ Daño recibido: {daño_recibido} ]"
                )
                result["daño_jugador"] = daño_recibido
                return result

            efecto = hechizo["efecto"]
            t = tirar(stats["mente"], enemy.dificultad, state.ventaja_activa)

            if efecto == "daño_alto":
                if t["exito"]:
                    daño = random.randint(enemy.dificultad, enemy.dificultad * 2) * 4
                    result["texto"] = f"La Palabra de Fuego consume lo que toca.\n[ Daño infligido: {daño} ]"
                    result["daño_enemigo"] = daño
                    result["ronda_ganada"] = True
                else:
                    daño_recibido = random.randint(2, enemy.dificultad) * 2
                    result["texto"] = f"El fuego se apaga antes de llegar. Te quema a vos.\n[ Daño recibido: {daño_recibido} ]"
                    result["daño_jugador"] = daño_recibido

            elif efecto == "defensa":
                result["texto"] = "El Velo de Sombra te envuelve. Próxima ronda: daño reducido."
                result["nuevo_estado"]["defensa_activa"] = True
                result["ronda_ganada"] = False  # Defensivo no gana ronda

            elif efecto == "ventaja":
                if t["exito"]:
                    result["texto"] = "Resonancia Mental. Encontraste la frecuencia. Próxima tirada con ventaja."
                    result["nuevo_estado"]["ventaja_activa"] = True
                else:
                    result["texto"] = "La resonancia rebotó. Ruido en tu mente."
                    daño_recibido = random.randint(2, 5) * 2
                    result["daño_jugador"] = daño_recibido

            elif efecto == "paralizar":
                if t["exito"]:
                    result["texto"] = "Lo nombraste. Se detiene. Una ronda de silencio absoluto."
                    result["nuevo_estado"]["enemigo_paralizado"] = True
                    result["ronda_ganada"] = True
                else:
                    daño_recibido = random.randint(enemy.dificultad, enemy.dificultad * 2) * 2
                    result["texto"] = f"El nombre no lo alcanzó. Te encontró a vos en cambio.\n[ Daño recibido: {daño_recibido} ]"
                    result["daño_jugador"] = daño_recibido

            elif efecto == "nuclear":
                daño = random.randint(enemy.dificultad * 2, enemy.dificultad * 3) * 5
                daño_propio = random.randint(15, 30)
                result["texto"] = (
                    f"El Fragmento del Abismo no distingue.\nDestruye todo lo que toca, incluido vos.\n"
                    f"[ Daño infligido: {daño} — Daño propio: {daño_propio} ]"
                )
                result["daño_enemigo"] = daño
                result["daño_jugador"] = daño_propio
                result["ronda_ganada"] = True

    # ── LADRÓN ────────────────────────────────────────────────
    elif clase == "Ladrón":

        if accion == "observar":
            t = tirar(stats["resistencia"], enemy.dificultad)
            if t["exito"]:
                result["texto"] = (
                    "Te fundís con la oscuridad. Estudiás cada movimiento.\n"
                    "[ En posición — próxima ronda: Apuñalar o Estrangular disponibles ]"
                )
                result["nuevo_estado"]["en_posicion"] = True
            else:
                result["texto"] = "Intentás desaparecer pero algo te delata. No lograste posicionarte."
                result["nuevo_estado"]["en_posicion"] = False

        elif accion == "apuñalar":
            state.en_posicion = False
            t = tirar(stats["resistencia"], enemy.dificultad, ventaja=True)
            if t["exito"]:
                daño = random.randint(enemy.dificultad, enemy.dificultad * 2) * 5
                result["texto"] = f"Por la espalda. Sin aviso. Sin defensa posible.\n[ Daño infligido: {daño} ]"
                result["daño_enemigo"] = daño
                result["ronda_ganada"] = True
            else:
                daño_recibido = random.randint(enemy.dificultad, enemy.dificultad * 2) * 3
                result["texto"] = (
                    f"Te vio en el último momento.\nTu ventaja se convirtió en trampa.\n"
                    f"[ Daño recibido: {daño_recibido} ]"
                )
                result["daño_jugador"] = daño_recibido

        elif accion == "estrangular":
            state.en_posicion = False
            t = tirar(stats["resistencia"], enemy.dificultad)
            if t["exito"]:
                daño = random.randint(enemy.dificultad, enemy.dificultad * 2) * 3
                result["texto"] = (
                    f"Lo atrapás desde atrás. El agarre es firme.\n"
                    f"No puede atacar la próxima ronda.\n[ Daño infligido: {daño} ]"
                )
                result["daño_enemigo"] = daño
                result["nuevo_estado"]["enemigo_paralizado"] = True
                result["ronda_ganada"] = True
            else:
                daño_recibido = random.randint(enemy.dificultad, enemy.dificultad * 2) * 2
                result["texto"] = f"Resiste. Te saca de encima con fuerza bruta.\n[ Daño recibido: {daño_recibido} ]"
                result["daño_jugador"] = daño_recibido

        elif accion == "ataque_rapido":
            t = tirar(stats["resistencia"], enemy.dificultad)
            if t["exito"]:
                daño = random.randint(1, enemy.dificultad) * 2
                result["texto"] = f"Golpe rápido, daño limitado. Pero conectó.\n[ Daño infligido: {daño} ]"
                result["daño_enemigo"] = daño
            else:
                daño_recibido = random.randint(enemy.dificultad, enemy.dificultad * 2) * 2
                result["texto"] = f"Demasiado lento. Te devuelve el doble.\n[ Daño recibido: {daño_recibido} ]"
                result["daño_jugador"] = daño_recibido

        elif accion == "huir":
            energia_rec = random.randint(10, 20)
            daño_recibido = random.randint(2, enemy.dificultad) * 2
            result["texto"] = (
                f"Te alejás. Ganás distancia y tiempo.\n"
                f"Pero el enemigo no deja ir gratis.\n"
                f"[ Energía recuperada: {energia_rec} — Daño recibido: {daño_recibido} ]"
            )
            result["daño_jugador"] = daño_recibido
            result["nuevo_estado"]["energia_recuperada"] = energia_rec

    return result


# ───────────────────────────────────────────────────────────────
# RESOLVER ATAQUE DEL ENEMIGO
# ───────────────────────────────────────────────────────────────
def resolver_ataque_enemigo(accion_enemigo, enemy, player, state):
    """
    Calcula el daño del enemigo al jugador.
    Aplica reducción si defensa_activa.
    Devuelve dict {texto, daño}.
    """
    if accion_enemigo == "paralizado":
        return {
            "texto": f"{enemy.nombre} está detenido. No puede actuar.",
            "daño": 0
        }

    texto_base = enemy.textos_ataque.get(accion_enemigo, enemy.textos_ataque.get("default", "Ataca."))

    # Calcular daño base según acción
    if accion_enemigo == "ataque_pesado" or accion_enemigo == "desesperado":
        daño_base = random.randint(enemy.dificultad, enemy.dificultad * 2) * 3
    elif accion_enemigo == "detectar_sigilo":
        daño_base = random.randint(enemy.dificultad, enemy.dificultad * 2) * 3
        state.en_posicion = False  # Cancela el setup del ladrón
    elif accion_enemigo == "presencia_psiquica":
        daño_base = random.randint(2, enemy.dificultad) * 2
    else:
        daño_base = random.randint(2, enemy.dificultad) * 3

    # Reducción por defensa activa
    if state.defensa_activa:
        daño_base = max(1, daño_base // 2)

    return {
        "texto": texto_base,
        "daño": daño_base
    }


# ───────────────────────────────────────────────────────────────
# CONSTRUIR LISTA DE ACCIONES DISPONIBLES
# Para pasar a ui.esperar_input como opciones_lista
# ───────────────────────────────────────────────────────────────
def acciones_disponibles(player, state, enemy):
    """
    Devuelve lista de tuplas (id_accion, texto_boton).
    """
    clase = player.clase
    acciones = []

    if clase == "Guerrero":
        acciones.append(("golpe_directo", "Golpe directo"))
        acciones.append(("defender", "Defender y contraatacar"))
        if state.golpe_cargado_disponible and player.vida >= player.vida_max * 0.6:
            acciones.append(("golpe_cargado", "Golpe cargado  [1 uso]"))
        if state.furia_disponible and player.vida <= player.vida_max * 0.4:
            acciones.append(("furia", "Furia ciega  [1 uso — te daña]"))

    elif clase == "Hechicero":
        for hid in state.hechizos_disponibles:
            hechizo = next(h for h in HECHIZOS if h["id"] == hid)
            acciones.append((hid, f"{hechizo['nombre']} — {hechizo['descripcion']}"))
        if not state.hechizos_disponibles:
            acciones.append(("daga", "Daga  [sin magia, daño mínimo]"))
        # La daga siempre disponible como último recurso si quedan hechizos también
        elif "daga" not in [a[0] for a in acciones]:
            acciones.append(("daga", "Daga  [fallback]"))

    elif clase == "Ladrón":
        if state.en_posicion:
            acciones.append(("apuñalar", "Apuñalar por la espalda  [requería posición ✓]"))
            acciones.append(("estrangular", "Estrangular  [requería posición ✓]"))
        else:
            acciones.append(("observar", "Observar — preparar posición  [habilita ataques especiales]"))
        acciones.append(("ataque_rapido", "Ataque rápido  [daño bajo, sin setup]"))
        acciones.append(("huir", "Huir y reagruparse  [recupera energía, recibís daño]"))

    return acciones


# ───────────────────────────────────────────────────────────────
# TEXTO DE CIERRE NARRATIVO
# Según resultado de las 3 rondas
# ───────────────────────────────────────────────────────────────
def texto_cierre(state, enemy, player):
    rj = state.rondas_jugador
    re = state.rondas_enemigo

    if rj > re:
        # Jugador ganó
        return enemy.textos_derrota, "victoria"
    elif re > rj:
        # Enemigo ganó
        return enemy.textos_victoria, "derrota"
    else:
        # Empate 1-1
        return enemy.texto_empate, "empate"


# ───────────────────────────────────────────────────────────────
# COMBATE COMPLETO — entry point
#
# Llamado desde game_engine.combate_narrativo() (reemplaza a la
# versión anterior).
# Devuelve "vivo" o "muerte".
# ───────────────────────────────────────────────────────────────
def combate_completo(enemy, player, engine):
    """
    Orquesta el combate de 3 rondas.
    Muestra intro del enemigo, loop de rondas, cierre narrativo.
    """
    ui = engine.ui
    state = CombatState(player)

    # ── Pantalla de intro del enemigo ─────────────────────────
    engine.mostrar_nivel(enemy.imagen, enemy.texto_intro, opciones=False)

    # ── Loop de rondas ────────────────────────────────────────
    while state.ronda_actual <= state.rondas_max:

        # Resetear modificadores de ronda
        state.defensa_activa   = False
        state.ventaja_activa   = False
        state.enemigo_paralizado = False

        # Construir opciones para esta ronda
        acciones = acciones_disponibles(player, state, enemy)
        ids      = [a[0] for a in acciones]
        labels   = [a[1] for a in acciones]

        encabezado = (
            f"═══ RONDA {state.ronda_actual} / {state.rondas_max} ═══\n"
            f"Rondas ganadas — Vos: {state.rondas_jugador}  |  {enemy.nombre}: {state.rondas_enemigo}\n"
            f"Vida: {player.vida}/{player.vida_max}    "
            f"{player.energia_nombre}: {player.energia}/{player.energia_max}\n"
        )

        if state.en_posicion and player.clase == "Ladrón":
            encabezado += "\n[ En posición — podés apuñalar o estrangular ]\n"

        texto_ronda = encabezado + "\n¿Qué hacés?\n"

        eleccion_idx = ui.esperar_input(
            ui.cargar_imagen(enemy.imagen),
            texto_ronda,
            opciones=True,
            opciones_lista=labels,
            player=player
        )

        # Convertir "1","2"... a id de acción
        try:
            idx = int(eleccion_idx) - 1
            accion_id = ids[idx]
        except (ValueError, IndexError):
            accion_id = ids[0]

        # ── Resolver acción del jugador ───────────────────────
        result_jugador = resolver_accion_jugador(accion_id, player, enemy, state)

        # Aplicar nuevos estados
        for k, v in result_jugador.get("nuevo_estado", {}).items():
            setattr(state, k, v)

        # Aplicar daño al enemigo
        enemy.vida -= result_jugador["daño_enemigo"]
        state.daño_jugador_total += result_jugador["daño_enemigo"]

        # Aplicar daño al jugador (por acciones propias)
        if result_jugador["daño_jugador"] > 0:
            daño_real = player.recibir_daño(result_jugador["daño_jugador"])
            state.daño_enemigo_total += daño_real

        # Recuperar energía si huir
        if "energia_recuperada" in result_jugador.get("nuevo_estado", {}):
            player.recuperar(energia=result_jugador["nuevo_estado"]["energia_recuperada"])

        # ── Resolver ataque del enemigo ───────────────────────
        accion_enemigo = enemy.elegir_accion(state, player.clase)
        result_enemigo = resolver_ataque_enemigo(accion_enemigo, enemy, player, state)

        # Aplicar daño del enemigo al jugador
        daño_enemigo_real = 0
        if result_enemigo["daño"] > 0:
            daño_enemigo_real = player.recibir_daño(result_enemigo["daño"])
            state.daño_enemigo_total += daño_enemigo_real

        # ── Determinar ganador de la ronda ────────────────────
        if result_jugador["ronda_ganada"]:
            state.rondas_jugador += 1
        elif result_enemigo["daño"] > result_jugador["daño_enemigo"] or not result_jugador["ronda_ganada"]:
            # El enemigo gana la ronda si hizo más daño y el jugador no la ganó
            if daño_enemigo_real > result_jugador["daño_enemigo"]:
                state.rondas_enemigo += 1

        # ── Pantalla de resultado de ronda ────────────────────
        resultado_visual = (
            f"═══ RESULTADO RONDA {state.ronda_actual} ═══\n\n"
            f"— Tu acción:\n{result_jugador['texto']}\n\n"
            f"— {enemy.nombre}:\n{result_enemigo['texto']}\n"
            f"[ Daño recibido: {daño_enemigo_real} ]\n\n"
            f"Vida restante: {player.vida}/{player.vida_max}\n"
        )

        ui.esperar_input(
            ui.cargar_imagen(enemy.imagen),
            resultado_visual,
            opciones=False,
            player=player
        )

        # ── Chequear muerte del jugador ───────────────────────
        if not player.alive:
            return "muerte"

        state.ronda_actual += 1
        state.enemigo_paralizado = False  # Se resetea al inicio de la próxima ronda

    # ── Cierre narrativo por estadística ─────────────────────
    texto_final, resultado = texto_cierre(state, enemy, player)

    if resultado == "victoria":
        player.modificar_psique(enemy.psique_victoria_jugador)
    else:
        player.modificar_psique(enemy.psique_derrota_jugador)

    ui.esperar_input(
        ui.cargar_imagen(enemy.imagen),
        texto_final,
        opciones=False,
        player=player
    )

    if resultado == "victoria" or resultado == "empate":
        ui.mostrar_cartel_psique()
        return "vivo"
    else:
        # Derrota narrativa: el jugador sobrevive pero pagó un precio
        ui.mostrar_cartel_psique()
        return "vivo"  # Nunca muere por derrota narrativa, solo por vida = 0
