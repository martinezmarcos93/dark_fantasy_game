"""Test suite - Descenso al Umbral. Ejecutar: python test_game.py"""
import sys, os, tempfile, shutil

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

import types
pg = types.ModuleType("pygame")
pg.init = pg.quit = lambda: None
pg.RESIZABLE = pg.SRCALPHA = pg.KEYDOWN = 0
pg.QUIT = 1; pg.VIDEORESIZE = 2; pg.MOUSEBUTTONDOWN = 3
pg.K_ESCAPE=27; pg.K_SPACE=32; pg.K_RETURN=13; pg.K_BACKSPACE=8
pg.K_DOWN=274; pg.K_UP=273
pg.K_1=ord("1"); pg.K_2=ord("2"); pg.K_3=ord("3"); pg.K_4=ord("4")

class _S:
    def __init__(self,*a,**kw): pass
    def fill(self,*a): pass
    def blit(self,*a): pass
    def set_alpha(self,*a): pass
    def set_clip(self,*a): pass
    def copy(self): return _S()
    def get_size(self): return (480,500)
    def get_width(self): return 480
    def convert(self): return self

pg.Surface=_S
pg.Rect=lambda *a:type("R",(),{"collidepoint":lambda s,p:False})()
pg.image=type("i",(),{"load":lambda p:_S(),"set_icon":lambda *a:None})()
pg.transform=type("t",(),{"scale":lambda s,sz:_S()})()
pg.display=type("d",(),{"set_mode":lambda *a,**kw:_S(),"set_caption":lambda *a:None,
    "set_icon":lambda *a:None,"flip":lambda *a:None})()
pg.font=type("f",(),{"init":lambda:None,"Font":lambda *a:type("F",(),{
    "render":lambda s,t,aa,c:_S(),"size":lambda s,t:(10,10)})()})()
pg.mixer=type("m",(),{"init":lambda:None,
    "Sound":lambda p:type("Snd",(),{"set_volume":lambda s,v:None,"play":lambda s:None})(),
    "music":type("mu",(),{"load":lambda p:None,"play":lambda *a:None,"get_busy":lambda:False})()})()
pg.draw=type("dr",(),{"rect":lambda *a,**kw:None,"line":lambda *a,**kw:None})()
pg.time=type("tm",(),{"Clock":lambda:type("C",(),{"tick":lambda s,fps:None})(),"delay":lambda ms:None})()
pg.event=type("ev",(),{"get":lambda:[]})()
pg.mouse=type("mo",(),{"get_pos":lambda:(0,0)})()
sys.modules["pygame"]=pg

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

PASS=0; FAIL=0

def ok(n):
    global PASS; PASS+=1; print(f"  [OK]  {n}")

def fallo(n,d=""):
    global FAIL; FAIL+=1; print(f"  [FAIL] {n}")
    if d: print(f"         -> {d}")

def check(n,c,d=""): ok(n) if c else fallo(n,d)

# ── Player ──────────────────────────────────────────────────────
print("\n== Player ==")
from game.player import Player

p=Player("T","Guerrero")
check("Guerrero fuerza=8 vida=120", p.stats["fuerza"]==8 and p.vida_max==120)
check("Hechicero energia=100",      Player("X","Hechicero").energia_max==100)
check("Ladron energia=70",          Player("X","Ladrón").energia_max==70)

p.modificar_psique({"corrupcion":110})
check("Psique cap 100",             p.psique["corrupcion"]==100)

p2=Player("X","Guerrero"); p2.modificar_psique({"miedo":-5})
check("Psique min 0",               p2.psique["miedo"]==0)

p3=Player("X","Guerrero"); d3=p3.recibir_daño(50)
check("recibir_danio int>0",        isinstance(d3,int) and d3>0)
check("vida baja",                  p3.vida<120)

p4=Player("X","Guerrero"); p4.gastar_energia(9999)
check("energia min 0",              p4.energia==0)

p5=Player("X","Guerrero"); p5.vida=10; p5.recuperar(vida=9999)
check("recuperar cap vida_max",     p5.vida==p5.vida_max)

p6=Player("X","Guerrero"); p6.registrar_decision("test")
check("historial funciona",         len(p6.historial)==1)
check("stats_combate existe",       "daño_infligido" in p6.stats_combate)

# ── Save System ──────────────────────────────────────────────────
print("\n== Save System ==")
from game.save_system import (guardar_partida, cargar_partida, borrar_partida,
                               listar_slots, guardar_ng_plus, cargar_ng_plus,
                               SAVE_DIR, NUM_SLOTS)
import game.save_system as ss

td=tempfile.mkdtemp()
ss.SAVE_DIR=td; ss.NG_PLUS_FILE=os.path.join(td,"ng_plus.json")

ps=Player("SaveTest","Hechicero"); ps.psique["lucidez"]=55; ps.historial=["DecA"]
guardar_partida(ps, 3, slot=0)
check("slot0.json creado",          os.path.exists(os.path.join(td,"slot0.json")))

data=cargar_partida(slot=0)
check("cargar => dict",             isinstance(data,dict))
check("nombre OK",                  data.get("nombre")=="SaveTest")
check("psique OK",                  data.get("psique",{}).get("lucidez")==55)
check("historial OK",               data.get("historial")==["DecA"])
check("nivel OK",                   data.get("nivel_actual")==3)
check("stats_combate OK",           "stats_combate" in data)

slots=listar_slots()
check("listar 3 slots",             len(slots)==NUM_SLOTS)
check("slot0 no vacio",             not slots[0]["vacio"])
check("slot1 vacio",                slots[1]["vacio"])

borrar_partida(slot=0)
check("borrar OK",                  not os.path.exists(os.path.join(td,"slot0.json")))
check("cargar inexistente=>None",   cargar_partida(slot=2) is None)

pndata={"violencia":60,"miedo":10,"culpa":5,"lucidez":80,"corrupcion":30}
guardar_ng_plus(pndata)
check("ng_plus round-trip",         cargar_ng_plus()==pndata)

ss.SAVE_DIR=SAVE_DIR; shutil.rmtree(td)

# ── 14 Finales ───────────────────────────────────────────────────
print("\n== 14 Finales ==")
from game.game_engine import GameEngine

def ending(pd):
    eng=GameEngine.__new__(GameEngine)
    eng.player=Player("T","Guerrero")
    eng.player.psique={"violencia":0,"miedo":0,"culpa":0,"lucidez":0,"corrupcion":0,**pd}
    return eng.determinar_final()

casos=[
    ("Combo miedo+culpa=>Suspension",          {"miedo":60,"culpa":45},                        "suspendido"),
    ("Combo culpa+miedo=>Suspension inv",       {"culpa":60,"miedo":45},                        "suspendido"),
    ("Combo violencia+miedo=>AtkMiedo",         {"violencia":60,"miedo":40},                    "miedo"),
    ("Combo culpa+lucidez=>Complice",           {"culpa":60,"lucidez":40},                      "cómplice"),
    ("Combo lucidez+culpa=>Complice inv",       {"lucidez":60,"culpa":40},                      "cómplice"),
    ("Combo miedo+lucidez=>Sufrimiento",        {"miedo":60,"lucidez":40},                      "Entender"),
    ("Combo violencia+culpa=>Ciclo",            {"violencia":60,"culpa":40},                    "anestesia"),
    ("Combo corrupcion+lucidez=>VPura",         {"corrupcion":60,"lucidez":40},                 "abismo"),
    ("Simple corrupcion=>Entidad",              {"corrupcion":55,"lucidez":20},                 "desciende"),
    ("Simple lucidez co<50=>Integracion",       {"lucidez":65,"corrupcion":20},                 "comprende"),
    ("Simple lucidez co>=50 sin combo",         {"lucidez":80,"violencia":40,"corrupcion":55},  "abismo"),
    ("Simple miedo=>Fragmentacion",             {"miedo":60,"violencia":10},                    "fragmenta"),
    ("Simple violencia=>Ruptura",               {"violencia":60,"miedo":10},                    "ruptura"),
    ("Simple culpa=>Juicio",                    {"culpa":60,"miedo":10},                        "suficiente"),
    ("Default=>Olvido",                         {"violencia":5,"miedo":5,"culpa":5,"lucidez":5,"corrupcion":5},"nunca"),
]

for nom,psq,frag in casos:
    try:
        txt=ending(psq)
        check(nom, frag.lower() in txt.lower(), f"'{frag}' no encontrado")
    except Exception as e:
        fallo(nom, str(e))

# ── Combat System ────────────────────────────────────────────────
print("\n== Combat System ==")
from game.combat_system import (tirar, CombatState, acciones_disponibles,
                                 HECHIZOS, _texto_ataque)

t=tirar(0,3)
check("tirar claves OK",     all(k in t for k in ("exito","critico","tirada","umbral")))
check("umbral=dif*2",        t["umbral"]==6)
check("critico=>exito",      not (t["critico"] and not t["exito"]))
check("stat=20 dif=1=>crit", tirar(20,1)["critico"])

pn1=Player("X","Hechicero")
cs1=CombatState(pn1)
check("Niv1: 3 hechizos",  len(cs1.hechizos_disponibles)==3)
check("Niv1: no nombre",   "nombre" not in cs1.hechizos_disponibles)
check("Niv1: no abismo",   "abismo" not in cs1.hechizos_disponibles)

pn3=Player("X","Hechicero"); pn3.level=3
check("Niv3: nombre OK",   "nombre" in CombatState(pn3).hechizos_disponibles)

pn4=Player("X","Hechicero"); pn4.level=4
check("Niv4: abismo OK",   "abismo" in CombatState(pn4).hechizos_disponibles)

class FE:
    dificultad=4

pg_=Player("X","Guerrero"); pg_.energia=0; pg_.vida=pg_.vida_max
csg=CombatState(pg_); csg.golpe_cargado_disponible=True
ids_g=[a[0] for a in acciones_disponibles(pg_,csg,FE())]
check("Guer sin ST: golpe_directo OK",   "golpe_directo" in ids_g)
check("Guer sin ST: no golpe_cargado",   "golpe_cargado" not in ids_g)

pl_=Player("X","Ladrón"); pl_.energia=0
ids_l=[a[0] for a in acciones_disponibles(pl_,CombatState(pl_),FE())]
check("Ladron sin IN: improvisar",  "improvisar" in ids_l)
check("Ladron sin IN: no observar", "observar" not in ids_l)

ph_=Player("X","Hechicero"); ph_.energia=0
ids_h=[a[0] for a in acciones_disponibles(ph_,CombatState(ph_),FE())]
check("Hech sin MP: daga",          "daga" in ids_h)
check("Hech sin MP: sin hechizos",  not any(h["id"] in ids_h for h in HECHIZOS))

# ── Enemies ──────────────────────────────────────────────────────
print("\n== Enemies ==")
from game.enemies import (crear_guardian, crear_reflejo, crear_sacerdote, crear_sombra,
                           crear_eco, crear_archivista, crear_grieta,
                           crear_testigo, crear_umbral_encarnado)

gua=crear_guardian(); ref=crear_reflejo()
sac=crear_sacerdote(); som=crear_sombra()
eco=crear_eco(); arc=crear_archivista()
gri=crear_grieta(); tes=crear_testigo(); boss=crear_umbral_encarnado()

for clase in ("Guerrero","Hechicero","Ladrón"):
    txt=_texto_ataque(gua.textos_ataque,"default",clase)
    check(f"Guardian default {clase}", isinstance(txt,str) and len(txt)>5)

tg=_texto_ataque(ref.textos_ataque,"default","Guerrero")
th=_texto_ataque(ref.textos_ataque,"default","Hechicero")
check("Reflejo Guer!=Hech",     tg!=th)
check("Sacerdote 5 ataques",    len(sac.textos_ataque)==5)
check("Sombra dif=6",           som.dificultad==6)
check("Sombra vida=110",        som.vida==110)
check("Eco dif=6 rondas=3",     eco.dificultad==6 and eco.rondas_max==3)
check("Archivista dif=6",       arc.dificultad==6)
check("Grieta inmune a nombre", "nombre" in gri.inmunidades)
check("Testigo dif=7",          tes.dificultad==7)
check("Boss rondas_max=5",      boss.rondas_max==5)
check("Boss dificultad=8",      boss.dificultad==8)
check("Boss inmune nombre+paralizar",
      "nombre" in boss.inmunidades and "paralizar" in boss.inmunidades)
check("_ta fallback _",         _texto_ataque({"default":{"_":"fb","Guerrero":"g"}},"default","Raro")=="fb")
check("_ta string plano",       _texto_ataque({"default":"plano"},"default","X")=="plano")
check("_ta accion=>default",    _texto_ataque({"default":"def"},"rara","X")=="def")

# ── Niveles ──────────────────────────────────────────────────────
print("\n== Niveles ==")
from game.levels.level1  import Level1
from game.levels.level2  import Level2
from game.levels.level3  import Level3
from game.levels.level4  import Level4
from game.levels.level5  import Level5
from game.levels.level6  import Level6
from game.levels.level7  import Level7
from game.levels.level8  import Level8
from game.levels.level9  import Level9
from game.levels.level10 import Level10

for Kls,nom in [(Level1,"L1"),(Level2,"L2"),(Level3,"L3"),(Level4,"L4"),
                 (Level5,"L5"),(Level6,"L6"),(Level7,"L7"),(Level8,"L8"),
                 (Level9,"L9"),(Level10,"L10")]:
    lvl=Kls()
    check(f"{nom} instancia OK", hasattr(lvl,"nombre") and hasattr(lvl,"jugar"))

for Kls,nom in [(Level1,"L1"),(Level2,"L2"),(Level3,"L3"),(Level4,"L4"),
                 (Level7,"L7"),(Level8,"L8")]:
    check(f"{nom} fase_combate", hasattr(Kls(),"fase_combate"))

check("L9 fase_combate",        hasattr(Level9(),"fase_combate"))
check("L10 fase_combate_boss",  hasattr(Level10(),"fase_combate_boss"))

for Kls,nom in [(Level5,"L5"),(Level6,"L6"),(Level9,"L9")]:
    check(f"{nom} distorsionar_texto", hasattr(Kls(),"distorsionar_texto"))

pd_=Player("X","Guerrero")
pd_.psique={"miedo":50,"corrupcion":60,"lucidez":60,"violencia":0,"culpa":0}
for Kls,nom in [(Level5,"L5"),(Level6,"L6"),(Level9,"L9")]:
    r=Kls().distorsionar_texto("Texto distorsion prueba",pd_)
    check(f"{nom} distorsion OK", isinstance(r,str) and len(r)>0)

pc_=Player("X","Guerrero")
rc=Level5().distorsionar_texto("Sin distorsion",pc_)
check("L5 psique=0 sin cambio", rc=="Sin distorsion")

# ── Resultado ────────────────────────────────────────────────────
total=PASS+FAIL
print(f"\n{'='*50}")
print(f"  Resultado: {PASS}/{total} tests pasaron", end="")
print(f"  ({FAIL} FALLARON)" if FAIL else "  -- TODO OK")
print(f"{'='*50}\n")
sys.exit(0 if FAIL==0 else 1)
