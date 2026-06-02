import random

# ═══════════════════════════════════════════════════════════════
# COMBAT SYSTEM — Descenso al Umbral
# ═══════════════════════════════════════════════════════════════

HECHIZOS = [
    {
        "id": "fuego",
        "nombre": "Palabra de Fuego",
        "descripcion": "Daño directo alto",
        "efecto": "daño_alto",
        "costo_energia": 15,
        "inmune": []
    },
    {
        "id": "velo",
        "nombre": "Velo de Sombra",
        "descripcion": "Reduce daño esta ronda",
        "efecto": "defensa",
        "costo_energia": 10,
        "inmune": []
    },
    {
        "id": "resonancia",
        "nombre": "Resonancia Mental",
        "descripcion": "Ventaja en siguiente tirada",
        "efecto": "ventaja",
        "costo_energia": 10,
        "inmune": []
    },
    {
        "id": "nombre",
        "nombre": "Nombre Verdadero",
        "descripcion": "Paraliza al enemigo una ronda",
        "efecto": "paralizar",
        "costo_energia": 20,
        "inmune": ["sacerdote"]
    },
    {
        "id": "abismo",
        "nombre": "Fragmento del Abismo",
        "descripcion": "Daño masivo — te daña también",
        "efecto": "nuclear",
        "costo_energia": 40,
        "inmune": []
    },
]


class CombatState:
    def __init__(self, player, rondas_max=3):
        self.ronda_actual = 1
        self.rondas_max   = rondas_max

        self.rondas_jugador = 0
        self.rondas_enemigo = 0

        self.en_posicion = False

        nivel = getattr(player, "level", 1)
        desbloqueados = ["fuego", "velo", "resonancia"]
        if nivel >= 3:
            desbloqueados.append("nombre")
        if nivel >= 4:
            desbloqueados.append("abismo")
        self.hechizos_disponibles = [h["id"] for h in HECHIZOS if h["id"] in desbloqueados]
        # Backup para restaurar con Tinta del Abismo
        self._hechizos_originales = list(desbloqueados)

        self.golpe_cargado_disponible = True
        self.furia_disponible         = True
        self.defensas_consecutivas    = 0
        self.contraataque_disponible  = False

        self.defensa_activa     = False
        self.ventaja_activa     = False
        self.enemigo_paralizado = False
        self._paralizado_siguiente = False

        # Garantizar éxito en próximo Defender (Piedra de Eco)
        self.proximo_defender_exito = False

        self.daño_jugador_total  = 0
        self.daño_enemigo_total  = 0

        self.acciones_jugador = []

        # Rastrear si se usaron especiales (para bonus de energía sin especiales)
        self.uso_especiales = False

        # Rastrear si el jugador usó "huir" en este combate
        self.huyo = False


class Enemy:
    def __init__(
        self,
        nombre,
        id_enemigo,
        imagen,
        vida,
        dificultad,
        texto_intro,
        textos_ataque,
        textos_derrota,
        textos_victoria,
        texto_empate,
        psique_victoria_jugador,
        psique_derrota_jugador,
        inmunidades=None,
        rondas_max=3
    ):
        self.nombre     = nombre
        self.id         = id_enemigo
        self.imagen     = imagen
        self.vida       = vida
        self.vida_max   = vida
        self.dificultad = dificultad

        self.texto_intro     = texto_intro
        self.textos_ataque   = textos_ataque
        self.textos_derrota  = textos_derrota
        self.textos_victoria = textos_victoria
        self.texto_empate    = texto_empate

        self.psique_victoria_jugador = psique_victoria_jugador
        self.psique_derrota_jugador  = psique_derrota_jugador
        self.inmunidades = inmunidades or []
        self.rondas_max  = rondas_max

    def esta_debilitado(self):
        return self.vida < self.vida_max * 0.4

    def elegir_accion(self, state, clase_jugador):
        if state.enemigo_paralizado:
            return "paralizado"

        if clase_jugador == "Ladrón" and state.en_posicion:
            if "detectar_sigilo" in self.textos_ataque:
                return "detectar_sigilo"

        if self.esta_debilitado():
            if "desesperado" in self.textos_ataque:
                return "desesperado"

        historial = state.acciones_jugador
        if len(historial) >= 2 and historial[-1] == historial[-2]:
            accion_repetida = historial[-1]
            if accion_repetida in ("defender", "velo", "observar", "respirar"):
                if "presencia_psiquica" in self.textos_ataque:
                    return "presencia_psiquica"
            if accion_repetida in ("golpe_directo", "fuego", "ataque_rapido"):
                if "ataque_pesado" in self.textos_ataque:
                    return "ataque_pesado"

        patrones_normales = [k for k in self.textos_ataque
                             if k not in ("detectar_sigilo", "desesperado", "paralizado")]
        if not patrones_normales:
            return "default"
        idx = (state.ronda_actual - 1) % len(patrones_normales)
        return patrones_normales[idx]


def tirar(stat, dificultad, ventaja=False):
    if ventaja:
        dados = sorted([random.randint(1,6), random.randint(1,6), random.randint(1,6)])
        resultado = dados[1] + dados[2] + stat
    else:
        resultado = random.randint(1,6) + random.randint(1,6) + stat

    umbral = dificultad * 2
    return {
        "exito":   resultado >= umbral,
        "critico": resultado >= umbral + 4,
        "tirada":  resultado,
        "umbral":  umbral
    }


def resolver_accion_jugador(accion, player, enemy, state):
    clase  = player.clase
    stats  = player.stats
    result = {
        "texto": "", "daño_enemigo": 0, "daño_jugador": 0,
        "ronda_ganada": False, "critico": False, "nuevo_estado": {}
    }

    ventaja = state.ventaja_activa
    state.ventaja_activa = False

    # ── ACCIÓN UNIVERSAL: RESPIRAR ────────────────────────────
    if accion == "respirar":
        recuperado = 10
        player.recuperar(energia=recuperado)
        result["texto"] = (
            f"Tomás distancia. Un momento de calma en medio del combate.\n"
            f"[ {player.energia_nombre} +{recuperado} ]"
        )
        result["ronda_ganada"] = False  # Ronda neutral
        return result

    # ── GUERRERO ──────────────────────────────────────────────
    if clase == "Guerrero":

        if accion == "golpe_directo":
            state.defensas_consecutivas = 0
            t = tirar(stats["fuerza"], enemy.dificultad, ventaja)
            if t["exito"]:
                daño = random.randint(1, enemy.dificultad) * 4
                if t["critico"]:
                    daño *= 2
                    result["critico"] = True
                    result["texto"] = f"CRÍTICO — El golpe fue perfecto. Sin margen de error.\n[ Daño infligido: {daño} ]"
                else:
                    result["texto"] = f"Tu golpe conecta. El guardián retrocede.\n[ Daño infligido: {daño} ]"
                result["daño_enemigo"] = daño
                result["ronda_ganada"] = True
            else:
                daño_recibido = random.randint(enemy.dificultad, enemy.dificultad * 2) * 2
                result["texto"] = f"Fallaste la apertura. Te golpea antes de que puedas conectar.\n[ Daño recibido: {daño_recibido} ]"
                result["daño_jugador"] = daño_recibido

        elif accion == "defender":
            # Piedra de Eco: éxito garantizado
            if state.proximo_defender_exito:
                state.proximo_defender_exito = False
                daño_contra = random.randint(1, enemy.dificultad) * 3
                result["critico"] = True
                result["texto"] = (
                    f"La Piedra de Eco. El Defender es perfecto, inevitable.\n"
                    f"[ Contraataque: {daño_contra} ]"
                )
                result["daño_enemigo"] = daño_contra
                result["nuevo_estado"]["defensa_activa"] = True
                state.defensas_consecutivas += 1
                if state.defensas_consecutivas >= 2:
                    result["nuevo_estado"]["contraataque_disponible"] = True
                    result["texto"] += "\n[ Postura: Contraataque Total disponible ]"
            else:
                t = tirar(stats["resistencia"], enemy.dificultad, ventaja)
                daño_bloqueado = random.randint(2, 6) * 2
                if t["exito"]:
                    daño_contra = random.randint(1, enemy.dificultad) * 2
                    if t["critico"]:
                        daño_contra *= 2
                        result["critico"] = True
                        result["texto"] = f"CRÍTICO — Absorbés todo el impacto y contraatacás con fuerza.\n[ Daño bloqueado: {daño_bloqueado} — Contraataque: {daño_contra} ]"
                    else:
                        result["texto"] = f"Absorbés el golpe y contraatacás.\n[ Daño bloqueado: {daño_bloqueado} — Contraataque: {daño_contra} ]"
                    result["daño_enemigo"] = daño_contra
                    result["nuevo_estado"]["defensa_activa"] = True
                    state.defensas_consecutivas += 1
                    if state.defensas_consecutivas >= 2:
                        result["nuevo_estado"]["contraataque_disponible"] = True
                        result["texto"] += "\n[ Postura: Contraataque Total disponible ]"
                else:
                    state.defensas_consecutivas = 0
                    result["nuevo_estado"]["contraataque_disponible"] = False
                    daño_parcial = random.randint(1, enemy.dificultad) * 2
                    result["texto"] = f"Intentás cubrirte pero el impacto pasa igual.\n[ Daño parcial recibido: {daño_parcial} ]"
                    result["daño_jugador"] = daño_parcial

        elif accion == "contraataque_total":
            state.contraataque_disponible = False
            state.defensas_consecutivas   = 0
            state.uso_especiales = True
            t = tirar(stats["fuerza"], enemy.dificultad, ventaja)
            daño = random.randint(enemy.dificultad, enemy.dificultad * 2) * 6
            if t["exito"]:
                if t["critico"]:
                    daño *= 2
                    result["critico"] = True
                    result["texto"] = f"CRÍTICO — Contraataque Total. La postura se convierte en devastación.\n[ Daño infligido: {daño} ]"
                else:
                    result["texto"] = f"Contraataque Total. Dos rondas de aguante convertidas en un golpe.\n[ Daño infligido: {daño} ]"
                result["daño_enemigo"] = daño
                result["ronda_ganada"] = True
            else:
                daño_recibido = random.randint(enemy.dificultad, enemy.dificultad * 2) * 2
                result["texto"] = f"El contraataque no salió. La postura se rompió antes de tiempo.\n[ Daño recibido: {daño_recibido} ]"
                result["daño_jugador"] = daño_recibido

        elif accion == "golpe_cargado":
            state.golpe_cargado_disponible = False
            state.uso_especiales = True
            player.gastar_energia(15)
            t = tirar(stats["fuerza"], enemy.dificultad, ventaja)
            if t["exito"]:
                daño = random.randint(enemy.dificultad, enemy.dificultad * 2) * 5
                if t["critico"]:
                    daño *= 2
                    result["critico"] = True
                    result["texto"] = f"CRÍTICO — El golpe cargado destruye cualquier defensa.\n[ Daño infligido: {daño} — Stamina: -{15} ]"
                else:
                    result["texto"] = f"El golpe cargado encuentra su blanco. Impacto devastador.\n[ Daño infligido: {daño} — Stamina: -{15} ]"
                result["daño_enemigo"] = daño
                result["ronda_ganada"] = True
            else:
                daño_recibido = random.randint(enemy.dificultad, enemy.dificultad * 2) * 3
                result["texto"] = f"El golpe cargado erró. Quedaste expuesto y lo pagaste caro.\n[ Daño recibido: {daño_recibido} — Stamina: -{15} ]"
                result["daño_jugador"] = daño_recibido

        elif accion == "furia":
            state.furia_disponible = False
            state.uso_especiales = True
            player.gastar_energia(20)
            daño = random.randint(enemy.dificultad * 2, enemy.dificultad * 3) * 4
            daño_propio = random.randint(5, 15)
            result["texto"] = f"La furia ignora todo. Golpeás sin control, sin defensa.\n[ Daño infligido: {daño} — Daño propio: {daño_propio} — Stamina: -{20} ]"
            result["daño_enemigo"] = daño
            result["daño_jugador"] = daño_propio
            result["ronda_ganada"] = True

        elif accion == "usar_eco_piedra":
            player.quitar_item("eco_piedra")
            result["texto"] = (
                "La Piedra de Eco vibra y se consume.\n"
                "El próximo Defender será perfecto, sin importar la tirada."
            )
            result["nuevo_estado"]["proximo_defender_exito"] = True
            result["ronda_ganada"] = False

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

        elif accion == "usar_tinta":
            player.quitar_item("tinta")
            player.modificar_psique({"corrupcion": 10})
            # Restaurar un hechizo gastado
            gastados = [h for h in state._hechizos_originales
                        if h not in state.hechizos_disponibles]
            if gastados:
                restaurado = random.choice(gastados)
                state.hechizos_disponibles.append(restaurado)
                hechizo_nombre = next(h["nombre"] for h in HECHIZOS if h["id"] == restaurado)
                result["texto"] = (
                    f"La Tinta del Abismo se consume. Corrupción +10.\n"
                    f"[ {hechizo_nombre} restaurado ]"
                )
            else:
                result["texto"] = "La Tinta del Abismo se consume. No había hechizos que restaurar.\n[ Corrupción +10 ]"
            result["ronda_ganada"] = False
            state.uso_especiales = True

        else:
            hechizo = next((h for h in HECHIZOS if h["id"] == accion), None)
            if not hechizo:
                result["texto"] = "Algo falló. El hechizo no existe."
                return result

            if accion in state.hechizos_disponibles:
                state.hechizos_disponibles.remove(accion)
            player.gastar_energia(hechizo["costo_energia"])
            state.uso_especiales = True

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
            t = tirar(stats["mente"], enemy.dificultad, ventaja)

            if efecto == "daño_alto":
                if t["exito"]:
                    daño = random.randint(enemy.dificultad, enemy.dificultad * 2) * 4
                    if t["critico"]:
                        daño *= 2
                        result["critico"] = True
                        result["texto"] = f"CRÍTICO — La Palabra de Fuego resuena hasta el hueso.\n[ Daño infligido: {daño} ]"
                    else:
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
                result["ronda_ganada"] = False

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
            player.gastar_energia(5)
            t = tirar(stats["resistencia"], enemy.dificultad)
            if t["exito"]:
                result["texto"] = (
                    "Te fundís con la oscuridad. Estudiás cada movimiento.\n"
                    "[ En posición — próxima ronda: Apuñalar o Estrangular disponibles — Ingenio: -5 ]"
                )
                result["nuevo_estado"]["en_posicion"] = True
            else:
                result["texto"] = "Intentás desaparecer pero algo te delata. No lograste posicionarte.\n[ Ingenio: -5 ]"
                result["nuevo_estado"]["en_posicion"] = False

        elif accion == "apuñalar":
            state.en_posicion = False
            state.uso_especiales = True
            player.gastar_energia(15)
            t = tirar(stats["resistencia"], enemy.dificultad, True)
            if t["exito"]:
                daño = random.randint(enemy.dificultad, enemy.dificultad * 2) * 5
                if t["critico"]:
                    daño *= 2
                    result["critico"] = True
                    result["texto"] = f"CRÍTICO — Punto vital. El daño es absoluto.\n[ Daño infligido: {daño} — Ingenio: -15 ]"
                else:
                    result["texto"] = f"Por la espalda. Sin aviso. Sin defensa posible.\n[ Daño infligido: {daño} — Ingenio: -15 ]"
                result["daño_enemigo"] = daño
                result["ronda_ganada"] = True
            else:
                daño_recibido = random.randint(enemy.dificultad, enemy.dificultad * 2) * 3
                result["texto"] = (
                    f"Te vio en el último momento.\nTu ventaja se convirtió en trampa.\n"
                    f"[ Daño recibido: {daño_recibido} — Ingenio: -15 ]"
                )
                result["daño_jugador"] = daño_recibido

        elif accion == "estrangular":
            state.en_posicion = False
            state.uso_especiales = True
            player.gastar_energia(10)
            t = tirar(stats["resistencia"], enemy.dificultad)
            if t["exito"]:
                daño = random.randint(enemy.dificultad, enemy.dificultad * 2) * 3
                result["texto"] = (
                    f"Lo atrapás desde atrás. El agarre es firme.\n"
                    f"No puede atacar la próxima ronda.\n[ Daño infligido: {daño} — Ingenio: -10 ]"
                )
                result["daño_enemigo"] = daño
                result["nuevo_estado"]["_paralizado_siguiente"] = True
                result["ronda_ganada"] = True
            else:
                daño_recibido = random.randint(enemy.dificultad, enemy.dificultad * 2) * 2
                result["texto"] = f"Resiste. Te saca de encima con fuerza bruta.\n[ Daño recibido: {daño_recibido} — Ingenio: -10 ]"
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
            state.huyo = True
            energia_rec = random.randint(10, 20)
            daño_recibido = random.randint(2, enemy.dificultad) * 2
            result["texto"] = (
                f"Te alejás. Ganás distancia y tiempo.\n"
                f"Pero el enemigo no deja ir gratis.\n"
                f"[ Energía recuperada: {energia_rec} — Daño recibido: {daño_recibido} ]"
            )
            result["daño_jugador"] = daño_recibido
            result["nuevo_estado"]["energia_recuperada"] = energia_rec

        elif accion == "improvisar":
            tirada = random.randint(1, 6)
            if tirada >= 5:
                daño = random.randint(enemy.dificultad, enemy.dificultad * 2) * 3
                result["texto"] = (
                    f"Sin plan. Sin recursos. Solo instinto.\n"
                    f"Encontraste un hueco que el enemigo no esperaba.\n"
                    f"[ Daño infligido: {daño} ]"
                )
                result["daño_enemigo"] = daño
                result["ronda_ganada"] = True
            elif tirada >= 3:
                energia_rec = random.randint(5, 15)
                result["texto"] = (
                    f"Nada funciona como debería.\n"
                    f"Pero al menos te recomponés un poco.\n"
                    f"[ Ingenio recuperado: {energia_rec} ]"
                )
                result["nuevo_estado"]["energia_recuperada"] = energia_rec
            else:
                daño_recibido = random.randint(enemy.dificultad, enemy.dificultad * 2) * 2
                result["texto"] = (
                    f"Sin plan es sin plan.\n"
                    f"El error fue costoso.\n"
                    f"[ Daño recibido: {daño_recibido} ]"
                )
                result["daño_jugador"] = daño_recibido

    return result


def _texto_ataque(textos_ataque, accion, clase):
    entry = textos_ataque.get(accion, textos_ataque.get("default", "Ataca."))
    if isinstance(entry, dict):
        return entry.get(clase, entry.get("_", "Ataca."))
    return entry


def resolver_ataque_enemigo(accion_enemigo, enemy, player, state):
    if accion_enemigo == "paralizado":
        return {
            "texto": f"{enemy.nombre} está detenido. No puede actuar.",
            "daño": 0
        }

    texto_base = _texto_ataque(enemy.textos_ataque, accion_enemigo, player.clase)

    if accion_enemigo == "ataque_pesado" or accion_enemigo == "desesperado":
        daño_base = random.randint(enemy.dificultad, enemy.dificultad * 2) * 3
    elif accion_enemigo == "detectar_sigilo":
        daño_base = random.randint(enemy.dificultad, enemy.dificultad * 2) * 3
        state.en_posicion = False
    elif accion_enemigo == "presencia_psiquica":
        daño_base = random.randint(2, enemy.dificultad) * 2
    else:
        daño_base = random.randint(2, enemy.dificultad) * 3

    if state.defensa_activa:
        daño_base = max(1, daño_base // 2)

    return {
        "texto": texto_base,
        "daño": daño_base
    }


def acciones_disponibles(player, state, enemy):
    clase = player.clase
    acciones = []

    if clase == "Guerrero":
        acciones.append(("golpe_directo", "Golpe directo"))
        acciones.append(("defender", "Defender y contraatacar"))
        if state.contraataque_disponible:
            acciones.append(("contraataque_total", "Contraataque Total  [postura ✓ — daño alto, gana ronda]"))
        if state.golpe_cargado_disponible and player.vida >= player.vida_max * 0.6:
            puede = player.energia >= 15
            if puede:
                acciones.append(("golpe_cargado", "Golpe cargado  [1 uso — 15 ST]"))
        if state.furia_disponible and player.vida <= player.vida_max * 0.4:
            puede = player.energia >= 20
            if puede:
                acciones.append(("furia", "Furia ciega  [1 uso — 20 ST, te daña]"))
        # Piedra de Eco
        if player.tiene_item("eco_piedra") and not state.proximo_defender_exito:
            acciones.append(("usar_eco_piedra", "Piedra de Eco  [próximo Defender garantizado]"))

    elif clase == "Hechicero":
        for hid in state.hechizos_disponibles:
            hechizo = next(h for h in HECHIZOS if h["id"] == hid)
            costo = hechizo["costo_energia"]
            if player.energia >= costo:
                acciones.append((hid, f"{hechizo['nombre']} — {hechizo['descripcion']}  [{costo} MP]"))
        # Tinta del Abismo
        if player.tiene_item("tinta"):
            gastados = [h for h in state._hechizos_originales
                        if h not in state.hechizos_disponibles]
            if gastados:
                acciones.append(("usar_tinta", "Tinta del Abismo  [restaura 1 hechizo — +10 Corrupción]"))
        if not acciones or not state.hechizos_disponibles:
            acciones.append(("daga", "Daga  [sin magia, daño mínimo]"))
        else:
            acciones.append(("daga", "Daga  [daño bajo, gratis]"))

    elif clase == "Ladrón":
        if state.en_posicion:
            if player.energia >= 15:
                acciones.append(("apuñalar", "Apuñalar por la espalda  [posición ✓ — 15 IN]"))
            if player.energia >= 10:
                acciones.append(("estrangular", "Estrangular  [posición ✓ — 10 IN]"))
        else:
            if player.energia >= 5:
                acciones.append(("observar", "Observar — preparar posición  [5 IN]"))
        acciones.append(("ataque_rapido", "Ataque rápido  [daño bajo, gratis]"))
        acciones.append(("huir", "Huir y reagruparse  [recupera Ingenio, recibís daño]"))
        if player.energia < 5 and not state.en_posicion:
            acciones.append(("improvisar", "Improvisar  [gratis — efecto aleatorio]"))

    # Respirar: disponible para todos cuando la energía está baja
    if player.energia <= player.energia_max * 0.3:
        acciones.append(("respirar", f"Respirar  [{player.energia_nombre} +10, ronda neutral]"))

    return acciones


def texto_cierre(state, enemy, player):
    rj = state.rondas_jugador
    re = state.rondas_enemigo

    if rj > re:
        return enemy.textos_derrota, "victoria"
    elif re > rj:
        return enemy.textos_victoria, "derrota"
    else:
        return enemy.texto_empate, "empate"


def combate_completo(enemy, player, engine):
    ui = engine.ui
    state = CombatState(player, rondas_max=enemy.rondas_max)

    if enemy.id == "umbral":
        ui.reproducir_musica(nombre="boss")

    # ── Pantalla de intro ─────────────────────────────────────
    engine.mostrar_nivel(enemy.imagen, enemy.texto_intro, opciones=False)

    # ── Bonus de El Viajero Perdido (Round 1 gratis) ─────────
    viajero_bonus_aplicado = False
    if getattr(player, "viajero_activo", False) and not getattr(player, "viajero_usado", False):
        daño_viajero = random.randint(8, 16)
        enemy.vida -= daño_viajero
        player.viajero_activo = False
        player.viajero_usado  = True
        viajero_texto = (
            f"\nEl Viajero Perdido aparece antes de que empiece la primera ronda.\n"
            f"Un golpe rápido, silencioso. Luego desaparece hacia la oscuridad.\n"
            f"[ Daño infligido: {daño_viajero} ]\n"
        )
        ui.esperar_input(
            ui.cargar_imagen("assets/npc_viajero.jpg"),
            viajero_texto,
            opciones=False,
            player=player
        )
        viajero_bonus_aplicado = True

    # ── Loop de rondas ────────────────────────────────────────
    while state.ronda_actual <= state.rondas_max:

        state.enemigo_paralizado = state._paralizado_siguiente
        state._paralizado_siguiente = False
        state.defensa_activa = False

        acciones = acciones_disponibles(player, state, enemy)
        ids      = [a[0] for a in acciones]
        labels   = [a[1] for a in acciones]

        inv_txt = ""
        if player.inventario:
            from game.player import NOMBRES_ITEMS
            inv_txt = "  Inventario: " + ", ".join(NOMBRES_ITEMS.get(i, i) for i in player.inventario) + "\n"

        encabezado = (
            f"═══ RONDA {state.ronda_actual} / {state.rondas_max} ═══\n"
            f"Rondas ganadas — Vos: {state.rondas_jugador}  |  {enemy.nombre}: {state.rondas_enemigo}\n"
            f"Vida: {player.vida}/{player.vida_max}    "
            f"{player.energia_nombre}: {player.energia}/{player.energia_max}"
            f"    Aliento: {player.aliento}/10\n"
            f"{inv_txt}"
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

        try:
            idx = int(eleccion_idx) - 1
            accion_id = ids[idx]
        except (ValueError, IndexError):
            accion_id = ids[0]

        state.acciones_jugador.append(accion_id)
        sc = player.stats_combate
        sc["acciones"][accion_id] = sc["acciones"].get(accion_id, 0) + 1

        # Marcar "huyo en este nivel" en el engine
        if accion_id == "huir":
            engine.huyo_este_nivel = True

        result_jugador = resolver_accion_jugador(accion_id, player, enemy, state)

        for k, v in result_jugador.get("nuevo_estado", {}).items():
            setattr(state, k, v)

        enemy.vida -= result_jugador["daño_enemigo"]
        state.daño_jugador_total += result_jugador["daño_enemigo"]
        player.stats_combate["daño_infligido"] += result_jugador["daño_enemigo"]
        if result_jugador.get("critico"):
            player.stats_combate["criticos"] += 1

        if result_jugador["daño_jugador"] > 0:
            daño_real = player.recibir_daño(result_jugador["daño_jugador"])
            state.daño_enemigo_total += daño_real
            player.stats_combate["daño_recibido"] += daño_real
            ui.flash_daño()

        if "energia_recuperada" in result_jugador.get("nuevo_estado", {}):
            player.recuperar(energia=result_jugador["nuevo_estado"]["energia_recuperada"])

        accion_enemigo = enemy.elegir_accion(state, player.clase)
        result_enemigo = resolver_ataque_enemigo(accion_enemigo, enemy, player, state)

        daño_enemigo_real = 0
        if result_enemigo["daño"] > 0:
            daño_enemigo_real = player.recibir_daño(result_enemigo["daño"])
            state.daño_enemigo_total += daño_enemigo_real
            player.stats_combate["daño_recibido"] += daño_enemigo_real
            ui.flash_daño()

        _psique_por_accion = {
            "furia":    {"violencia": 3},
            "abismo":   {"corrupcion": 4},
            "nombre":   {"lucidez": 3},
            "apuñalar": {"violencia": 2},
            "huir":     {"miedo": 2},
        }
        if accion_id in _psique_por_accion:
            player.modificar_psique(_psique_por_accion[accion_id])

        if result_jugador["ronda_ganada"]:
            state.rondas_jugador += 1
            player.stats_combate["rondas_ganadas"] += 1
        elif daño_enemigo_real > result_jugador["daño_enemigo"]:
            state.rondas_enemigo += 1
            player.stats_combate["rondas_perdidas"] += 1

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

        if not player.alive:
            return "muerte"

        state.ronda_actual += 1

    # ── Cierre narrativo ──────────────────────────────────────
    texto_final, resultado = texto_cierre(state, enemy, player)

    # Bonificaciones de victoria
    bonuses = []
    if resultado == "victoria":
        player.modificar_psique(enemy.psique_victoria_jugador)
        player.recuperar(vida=5)
        bonuses.append("Vida +5")
        player.ganar_aliento(1)
        bonuses.append("Aliento +1")

        # Perfect: 3/3 rondas ganadas
        player.ultimo_combate_perfecto = (state.rondas_jugador >= state.rondas_max)

        # Sin especiales: +5 energía
        if not state.uso_especiales:
            player.recuperar(energia=5)
            bonuses.append(f"{player.energia_nombre} +5")
    else:
        player.modificar_psique(enemy.psique_derrota_jugador)
        player.ultimo_combate_perfecto = False

    if bonuses:
        texto_final += f"\n\n[ {' — '.join(bonuses)} ]"

    ui.esperar_input(
        ui.cargar_imagen(enemy.imagen),
        texto_final,
        opciones=False,
        player=player
    )

    ui.mostrar_cartel_psique()
    return "vivo"
