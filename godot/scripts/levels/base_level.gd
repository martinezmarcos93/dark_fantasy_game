class_name BaseLevel
extends RefCounted
## BaseLevel — clase base de los niveles. Ver ADR-007.
##
## Cada nivel es un script que sobreescribe fase_combate / fase_psicologica
## (y fase_laberinto en los niveles 3, 7, 9). jugar() orquesta el flujo
## estándar y conduce la GameScreen vía el engine (async).
##
## Equivale a la estructura de cada game/levels/levelN.py.

var nombre: String = ""


## Flujo estándar: combate → fase psicológica. Devuelve "muerte" o "continuar".
## Port de LevelN.jugar() del Python.
func jugar(player: Player, engine) -> String:
	var resultado: String = await fase_combate(player, engine)
	if resultado == "muerte":
		return "muerte"
	await fase_psicologica(player, engine)
	return "continuar"


# ── Fases sobreescribibles (la base no hace nada por defecto) ──
func fase_laberinto(_player: Player, _engine) -> void:
	pass


func fase_combate(_player: Player, _engine) -> String:
	return "vivo"


func fase_psicologica(_player: Player, _engine) -> void:
	pass
