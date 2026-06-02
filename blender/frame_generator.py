"""
Descenso al Umbral — UI Frame Generator
========================================
Genera el marco ornamental de la interfaz en Blender 4.x.
Resuelve todos los defectos de "LA ELEGIDA" (imagen AI de referencia):
  - Alpha real en los paneles (no negro sólido)
  - 4 calaveras simétricas y completas
  - Divisor del panel derecho prominente
  - HUD strip con altura suficiente
  - Resolución exacta 1000×600
  - Decoración de bordes consistente

USO:
    blender --background --python blender/frame_generator.py
    O: abrir en Blender Text Editor → Alt+P (Run Script)

SALIDA:
    godot/assets/images/ui_frame.png  (1000×600 px, RGBA, fondo transparente)
    El archivo se sobreescribe cada vez que se ejecuta.

AJUSTE RÁPIDO:
    Modificar la sección CONFIG y re-ejecutar.
    Bajar RENDER_SAMPLES a 32 para iteraciones rápidas.
"""

import bpy
import bmesh
import math
import os

# ═══════════════════════════════════════════════════════════════
# CONFIG — todos los parámetros en un solo lugar
# ═══════════════════════════════════════════════════════════════

# ── Salida ────────────────────────────────────────────────────
OUTPUT_FILE = "ui_frame.png"
try:
    _dir = os.path.dirname(os.path.realpath(__file__))
    OUTPUT_PATH = os.path.normpath(
        os.path.join(_dir, "..", "godot", "assets", "images", OUTPUT_FILE)
    )
except NameError:
    # Ejecutando desde Text Editor de Blender
    OUTPUT_PATH = bpy.path.abspath("//godot/assets/images/" + OUTPUT_FILE)

# ── Render ────────────────────────────────────────────────────
RENDER_W       = 1000
RENDER_H       = 600
RENDER_SAMPLES = 128   # bajar a 32-64 para test rápido

# ── Canvas ────────────────────────────────────────────────────
# 1 unidad Blender = 100 px → canvas = 10.0 × 6.0 unidades
W = 10.0
H = 6.0

# ── Borde exterior ────────────────────────────────────────────
B = 0.42       # grosor del borde en todos los lados (42px)

# ── Panel izquierdo ───────────────────────────────────────────
# Imagen del nivel/enemigo/NPC
LP_W = 2.80    # ancho (280px — ~28% del total)

# Strip HUD debajo del panel imagen
# Arregla el defecto de LA ELEGIDA: strip demasiado angosto
HUD_H = 0.90   # altura (90px — suficiente para 2 barras + nombre + clase)
HUD_SEP = 0.06 # línea separadora entre imagen y HUD (6px, visible)

# ── Columna central (entre paneles) ───────────────────────────
# Contiene el pentáculo arriba y un cráneo abajo
COL_W = 0.68   # ancho (68px — suficiente para el pentáculo)

# ── Panel derecho ─────────────────────────────────────────────
# Arriba: texto narrativo   Abajo: opciones/botones
# Arregla el defecto: divisor más prominente y altura de opciones adecuada
OPT_H   = 1.25  # altura del área de opciones (125px — más generosa)
DIV_H   = 0.22  # altura del divisor prominente (22px — visible y con relieve)

# ── Material: bronce antiguo ──────────────────────────────────
# Paleta: dorado oscuro con pátina marrón, muy metálico, rugosidad media
MAT_BASE_COLOR  = (0.26, 0.14, 0.03, 1.0)  # bronce oscuro
MAT_METALLIC    = 0.92
MAT_ROUGHNESS   = 0.44

# Material para cuencas oculares de las calaveras
MAT_VOID_COLOR  = (0.010, 0.005, 0.005, 1.0)  # casi negro
MAT_VOID_ROUGH  = 0.95

# ── Alturas Z (jerarquía visual) ─────────────────────────────
# Los elementos más altos reciben más luz → más destaque
Z_FRAME    = 0.12   # bordes del marco (base)
Z_RIDGE    = 0.04   # cresta decorativa sobre los bordes (+Z_FRAME = 0.16)
Z_DIVIDER  = 0.08   # el divisor del panel derecho (más alto que el marco base)
Z_SKULL    = 0.10   # cuerpo de las calaveras
Z_PENT     = 0.14   # pentagrama (lo más prominente)

# ── Geometría calaveras ───────────────────────────────────────
SKULL_R      = 0.195  # radio del cráneo
SKULL_EYE_R  = 0.058  # radio de las cuencas oculares
SKULL_EYE_DX = 0.082  # distancia horizontal entre ojos y centro
SKULL_EYE_DY = 0.025  # posición vertical de los ojos respecto al centro del cráneo
SKULL_EYE_DZ = 0.55   # cuánto sobresalen los ojos del cráneo (relativo a SKULL_R)

# ── Geometría pentagrama ──────────────────────────────────────
PENT_R_EXT = 0.24  # radio exterior (puntas)
PENT_R_INT = 0.09  # radio interior (entrantes)

# ═══════════════════════════════════════════════════════════════
# COORDENADAS DERIVADAS — no editar
# ═══════════════════════════════════════════════════════════════
LP_X1 = B
LP_X2 = B + LP_W                 # ~3.22

COL_X1 = LP_X2
COL_X2 = LP_X2 + COL_W          # ~3.90
COL_CX = (COL_X1 + COL_X2) / 2  # centro columna

RP_X1 = COL_X2
RP_X2 = W - B                    # ~9.58

BOT = B
TOP = H - B                      # ~5.58

HUD_Y1    = BOT
HUD_Y2    = BOT + HUD_H          # ~1.32
HUDSEP_Y1 = HUD_Y2
HUDSEP_Y2 = HUD_Y2 + HUD_SEP    # ~1.38
IMG_Y1    = HUDSEP_Y2
IMG_Y2    = TOP

OPT_Y1    = BOT
OPT_Y2    = BOT + OPT_H         # ~1.67
DIV_Y1    = OPT_Y2
DIV_Y2    = OPT_Y2 + DIV_H      # ~1.89
TXT_Y1    = DIV_Y2
TXT_Y2    = TOP

# Centro del cráneo del pentáculo (parte alta de la columna)
PENT_CY = TOP - 0.36             # ~5.22

# Posiciones de las 5 calaveras
# 4 esquinas + 1 centro-inferior en la columna
# Las de esquina se centran en la zona del borde
HALF_B = B * 0.55
SKULL_POSITIONS = [
    (LP_X1 - HALF_B + B * 0.5, BOT - HALF_B + B * 0.5),  # bottom-left
    (RP_X2 + HALF_B - B * 0.5, BOT - HALF_B + B * 0.5),  # bottom-right
    (LP_X1 - HALF_B + B * 0.5, TOP + HALF_B - B * 0.5),  # top-left
    (RP_X2 + HALF_B - B * 0.5, TOP + HALF_B - B * 0.5),  # top-right
    (COL_CX, BOT - HALF_B + B * 0.5),                     # center-bottom
]


# ═══════════════════════════════════════════════════════════════
# FUNCIONES AUXILIARES
# ═══════════════════════════════════════════════════════════════

def limpiar_escena():
    """Borra todos los objetos y datos huérfanos."""
    bpy.ops.object.select_all(action='SELECT')
    bpy.ops.object.delete()
    for blk in [bpy.data.meshes, bpy.data.cameras,
                bpy.data.lights, bpy.data.materials]:
        for item in blk:
            blk.remove(item)


def rect_mesh(name, x1, y1, x2, y2, z_height, z_base=0.0):
    """
    Crea un rectángulo extruido como objeto 3D.
    z_base: nivel Z del piso del objeto
    z_height: cuánto se extruye hacia arriba
    Retorna el objeto creado y linkeado a la escena activa.
    """
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()

    # Cara inferior
    v0 = bm.verts.new((x1, y1, z_base))
    v1 = bm.verts.new((x2, y1, z_base))
    v2 = bm.verts.new((x2, y2, z_base))
    v3 = bm.verts.new((x1, y2, z_base))
    face = bm.faces.new([v0, v1, v2, v3])

    # Extruir en Z
    res = bmesh.ops.extrude_face_region(bm, geom=[face])
    top_verts = [v for v in res['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=top_verts, vec=(0, 0, z_height))

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def cresta_borde(name, x1, y1, x2, y2, grosor=0.05):
    """
    Crea una cresta decorativa delgada sobre un borde.
    Va centrada en el borde, ligeramente elevada.
    Simula el relieve interior/exterior de un marco tallado.
    """
    # Inset horizontal: la cresta ocupa el centro del borde
    margen = min((x2 - x1), (y2 - y1)) * 0.15
    return rect_mesh(
        name,
        x1 + margen, y1 + margen,
        x2 - margen, y2 - margen,
        Z_RIDGE,
        z_base=Z_FRAME
    )


def crear_material_bronce():
    mat = bpy.data.materials.new("Bronce_Umbral")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    # Nodo Principled BSDF (compatible Blender 3.x y 4.x)
    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.location = (0, 0)
    bsdf.inputs["Base Color"].default_value = MAT_BASE_COLOR
    bsdf.inputs["Metallic"].default_value   = MAT_METALLIC
    bsdf.inputs["Roughness"].default_value  = MAT_ROUGHNESS
    # "Specular" en Blender 3.x se llama "Specular IOR Level" en Blender 4.x
    for key in ("Specular IOR Level", "Specular"):
        if key in bsdf.inputs:
            bsdf.inputs[key].default_value = 0.75
            break

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (300, 0)
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def crear_material_oscuro():
    mat = bpy.data.materials.new("Cuenca_Ocular")
    mat.use_nodes = True
    nodes = mat.node_tree.nodes
    links = mat.node_tree.links
    nodes.clear()

    bsdf = nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = MAT_VOID_COLOR
    bsdf.inputs["Metallic"].default_value   = 0.0
    bsdf.inputs["Roughness"].default_value  = MAT_VOID_ROUGH

    out = nodes.new("ShaderNodeOutputMaterial")
    out.location = (300, 0)
    links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return mat


def asignar_mat(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


def suavizar(obj):
    """Shade smooth en el objeto."""
    bpy.context.view_layer.objects.active = obj
    bpy.ops.object.shade_smooth()


# ═══════════════════════════════════════════════════════════════
# CONSTRUCCIÓN DEL MARCO
# ═══════════════════════════════════════════════════════════════

def construir_marco(mat_bronce):
    """
    Crea las 7 piezas sólidas del marco.
    Los paneles son AUSENCIA de geometría → transparentes en el render.

    Jerarquía visual (de menos a más prominente):
      Bordes exterior → Cresta de borde → Divisor → Calaveras → Pentáculo
    """
    piezas = []

    # ── Bordes principales (los 4 lados) ──────────────────────
    # Full width/height para que las esquinas sean completas y simétricas
    piezas += [
        rect_mesh("Borde_Top",    0,    TOP, W, H,    Z_FRAME),
        rect_mesh("Borde_Bot",    0,    0,   W, BOT,  Z_FRAME),
        rect_mesh("Borde_Left",   0,    BOT, B, TOP,  Z_FRAME),
        rect_mesh("Borde_Right",  RP_X2, BOT, W, TOP, Z_FRAME),
    ]

    # ── Columna central (entre paneles) ───────────────────────
    piezas.append(rect_mesh("Col_Central", COL_X1, BOT, COL_X2, TOP, Z_FRAME))

    # ── Separador imagen/HUD (izquierda) ──────────────────────
    # Delgado pero visible; corrige el defecto de LA ELEGIDA
    piezas.append(rect_mesh("HUD_Sep", LP_X1, HUDSEP_Y1, LP_X2, HUDSEP_Y2, Z_FRAME + 0.04))

    # ── Divisor del panel derecho (prominente) ────────────────
    # Z más alto que el marco base = más iluminado = más visible
    # Corrige el defecto: divisor de 2px invisible → ahora 22px con relieve
    piezas.append(rect_mesh("Div_Derecho", RP_X1, DIV_Y1, RP_X2, DIV_Y2, Z_FRAME + Z_DIVIDER))

    # ── Crestas decorativas (bordes) ─────────────────────────
    # Simulan el tallado interior típico de marcos barrocos/góticos
    for nombre, x1, y1, x2, y2 in [
        ("Cresta_Top",   0, TOP, W, H),
        ("Cresta_Bot",   0, 0,   W, BOT),
        ("Cresta_Left",  0, BOT, B, TOP),
        ("Cresta_Right", RP_X2, BOT, W, TOP),
    ]:
        piezas.append(cresta_borde(nombre, x1, y1, x2, y2))

    # Asignar material a todas las piezas
    for p in piezas:
        asignar_mat(p, mat_bronce)
        suavizar(p)

    return piezas


# ═══════════════════════════════════════════════════════════════
# CALAVERAS
# ═══════════════════════════════════════════════════════════════

def crear_calavera(cx, cy, mat_bronce, mat_void, nombre_base="Skull"):
    """
    Calavera simplificada:
    - Esfera principal (cráneo), ligeramente aplastada
    - Dos esferas de cuenca ocular (material oscuro, ligeramente hundidas)
    Posicionada en (cx, cy, Z_FRAME) sobre el marco.
    """
    objetos = []
    z = Z_FRAME  # base sobre la que se apoya la calavera

    # ── Cráneo ────────────────────────────────────────────────
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=SKULL_R,
        location=(cx, cy, z + SKULL_R * 0.85),
        segments=24,
        ring_count=16
    )
    craneo = bpy.context.active_object
    craneo.name = f"{nombre_base}_Craneo"
    # Ligeramente achatado verticalmente (cráneo real ~0.85 en Y, 0.92 en Z)
    craneo.scale = (1.0, 0.82, 0.90)
    bpy.ops.object.transform_apply(scale=True)
    asignar_mat(craneo, mat_bronce)
    suavizar(craneo)
    objetos.append(craneo)

    # ── Cuencas oculares ──────────────────────────────────────
    # Posicionadas hacia el frente (Y positivo en la esfera)
    # y ligeramente hacia arriba del centro del cráneo
    eye_z = z + SKULL_R * (0.85 + SKULL_EYE_DY)
    eye_y_offset = SKULL_R * SKULL_EYE_DZ   # cuánto sobresalen hacia la cámara

    for lado, dx in [("L", -SKULL_EYE_DX), ("R", SKULL_EYE_DX)]:
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=SKULL_EYE_R,
            location=(cx + dx, cy + eye_y_offset, eye_z),
            segments=12,
            ring_count=8
        )
        ojo = bpy.context.active_object
        ojo.name = f"{nombre_base}_Ojo_{lado}"
        # Ligeramente achatada como una cuenca oval
        ojo.scale = (1.0, 0.7, 0.85)
        bpy.ops.object.transform_apply(scale=True)
        asignar_mat(ojo, mat_void)
        suavizar(ojo)
        objetos.append(ojo)

    return objetos


def crear_todas_las_calaveras(mat_bronce, mat_void):
    """
    5 calaveras: 4 esquinas simétricas + 1 en centro-inferior de la columna.
    Corrige el defecto de LA ELEGIDA: bottom-right cortada, bottom-left ausente.
    """
    all_objs = []
    nombres = ["BL", "BR", "TL", "TR", "CB"]

    for i, (cx, cy) in enumerate(SKULL_POSITIONS):
        objs = crear_calavera(cx, cy, mat_bronce, mat_void, f"Skull_{nombres[i]}")
        all_objs.extend(objs)

    return all_objs


# ═══════════════════════════════════════════════════════════════
# PENTÁCULO
# ═══════════════════════════════════════════════════════════════

def crear_pentagrama(mat_bronce):
    """
    Pentagrama de 5 puntas en la parte superior de la columna central.
    Creado a partir de 10 vértices (alternando exterior/interior) + centro.
    Extruido en Z para dar relieve.
    """
    cx = COL_CX
    cy = PENT_CY
    z  = Z_FRAME

    # 10 vértices: 5 puntas externas + 5 entrantes
    # Empieza desde arriba (ángulo π/2) y gira en sentido antihorario
    verts_2d = []
    for i in range(10):
        r = PENT_R_EXT if i % 2 == 0 else PENT_R_INT
        ang = math.pi / 2.0 + i * (math.pi / 5.0)
        verts_2d.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))

    mesh = bpy.data.meshes.new("Pentagrama")
    bm = bmesh.new()

    # Vértice central (para triangulación)
    vc = bm.verts.new((cx, cy, z))
    verts = [bm.verts.new((p[0], p[1], z)) for p in verts_2d]

    # Triángulos en abanico desde el centro
    for i in range(10):
        j = (i + 1) % 10
        bm.faces.new([vc, verts[i], verts[j]])

    # Extruir en Z
    res = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
    top_v = [v for v in res['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=top_v, vec=(0, 0, Z_PENT))

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    obj = bpy.data.objects.new("Pentagrama", mesh)
    bpy.context.collection.objects.link(obj)
    asignar_mat(obj, mat_bronce)
    suavizar(obj)

    # Círculo ornamental alrededor del pentáculo
    _crear_anillo_pentagrama(cx, cy, z, mat_bronce)

    return obj


def _crear_anillo_pentagrama(cx, cy, z, mat_bronce):
    """Anillo circular alrededor del pentáculo — detalle ornamental."""
    r_ext = PENT_R_EXT * 1.45
    r_int = PENT_R_EXT * 1.20
    segmentos = 32
    grosor_z = Z_PENT * 0.5

    mesh = bpy.data.meshes.new("Pentagrama_Anillo")
    bm = bmesh.new()

    verts_bot = []
    verts_top = []
    for i in range(segmentos):
        ang = 2 * math.pi * i / segmentos
        for r, collection in [(r_ext, verts_bot), (r_int, verts_bot)]:
            pass  # se reemplaza abajo

    # Anillo: lista de vértices en aro
    inner, outer = [], []
    for i in range(segmentos):
        ang = 2 * math.pi * i / segmentos
        cos_a, sin_a = math.cos(ang), math.sin(ang)
        inner.append(bm.verts.new((cx + r_int * cos_a, cy + r_int * sin_a, z)))
        outer.append(bm.verts.new((cx + r_ext * cos_a, cy + r_ext * sin_a, z)))

    bm.verts.ensure_lookup_table()

    # Caras del anillo
    for i in range(segmentos):
        j = (i + 1) % segmentos
        bm.faces.new([outer[i], outer[j], inner[j], inner[i]])

    # Extruir
    res = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
    top_v = [v for v in res['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=top_v, vec=(0, 0, grosor_z))

    bm.to_mesh(mesh)
    bm.free()
    mesh.update()

    obj = bpy.data.objects.new("Pentagrama_Anillo", mesh)
    bpy.context.collection.objects.link(obj)
    asignar_mat(obj, mat_bronce)
    suavizar(obj)
    return obj


# ═══════════════════════════════════════════════════════════════
# ILUMINACIÓN
# ═══════════════════════════════════════════════════════════════

def setup_iluminacion():
    """
    3-point lighting para realzar el bronce:
    - Key (luz principal, upper-left, fuerte)
    - Fill (relleno suave desde la derecha)
    - World (ambient muy oscuro, calidez)
    """
    # Key light
    bpy.ops.object.light_add(type='AREA', location=(W * 0.15, H * 1.6, 9.0))
    key = bpy.context.active_object
    key.name = "Key"
    key.data.energy = 900.0
    key.data.size   = 4.0
    key.rotation_euler = (math.radians(-38), 0, math.radians(-18))

    # Fill light
    bpy.ops.object.light_add(type='AREA', location=(W * 0.92, H * 0.5, 7.0))
    fill = bpy.context.active_object
    fill.name = "Fill"
    fill.data.energy = 280.0
    fill.data.size   = 7.0

    # Rim light (desde abajo, resalta los bordes inferiores)
    bpy.ops.object.light_add(type='AREA', location=(W * 0.5, -1.5, 5.0))
    rim = bpy.context.active_object
    rim.name = "Rim"
    rim.data.energy = 140.0
    rim.data.size   = 5.0
    rim.rotation_euler = (math.radians(35), 0, 0)

    # World: ambient oscuro y cálido (no negro puro para evitar sombras duras)
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value    = (0.04, 0.025, 0.012, 1.0)
        bg.inputs["Strength"].default_value = 0.6


# ═══════════════════════════════════════════════════════════════
# CÁMARA ORTOGRÁFICA
# ═══════════════════════════════════════════════════════════════

def setup_camara():
    """
    Cámara ortográfica mirando hacia abajo (-Z).
    ortho_scale = H = 6.0 → la cámara ve exactamente 6 unidades en vertical.
    Con aspect 1000/600 = 5/3, en horizontal ve 10 unidades. Coincide con W.
    El frame queda exactamente dentro del canvas sin recorte.
    """
    cam_data = bpy.data.cameras.new("Camara_Frame")
    cam_data.type       = 'ORTHO'
    cam_data.ortho_scale = H   # 6.0 → vertical = H, horizontal = W automáticamente

    cam_obj = bpy.data.objects.new("Camara_Frame", cam_data)
    bpy.context.collection.objects.link(cam_obj)

    # Posición: centrada sobre el canvas, elevada en Z
    cam_obj.location       = (W / 2.0, H / 2.0, 20.0)
    # Rotación (0,0,0): la cámara local mira en -Z → apunta al canvas en z=0
    cam_obj.rotation_euler = (0.0, 0.0, 0.0)

    bpy.context.scene.camera = cam_obj
    return cam_obj


# ═══════════════════════════════════════════════════════════════
# RENDER
# ═══════════════════════════════════════════════════════════════

def setup_render():
    scene = bpy.context.scene
    scene.render.engine = 'CYCLES'

    # Resolución exacta
    scene.render.resolution_x          = RENDER_W
    scene.render.resolution_y          = RENDER_H
    scene.render.resolution_percentage = 100

    # Fondo transparente — LOS PANELES SERÁN ALPHA, no negro sólido
    # Esto resuelve el defecto crítico de LA ELEGIDA
    scene.render.film_transparent = True

    # Formato de salida: PNG con canal alpha
    scene.render.image_settings.file_format  = 'PNG'
    scene.render.image_settings.color_mode   = 'RGBA'
    scene.render.image_settings.compression  = 15

    # Cycles: CPU (compatible con headless sin GPU)
    scene.cycles.device         = 'CPU'
    scene.cycles.samples        = RENDER_SAMPLES
    scene.cycles.use_denoising = True

    scene.render.filepath = OUTPUT_PATH


def renderizar():
    print(f"\n[frame_generator] Renderizando → {OUTPUT_PATH}")
    print(f"  Resolución: {RENDER_W}×{RENDER_H} px | Samples: {RENDER_SAMPLES}")

    # Asegurar que existe el directorio de salida
    out_dir = os.path.dirname(OUTPUT_PATH)
    os.makedirs(out_dir, exist_ok=True)

    bpy.ops.render.render(write_still=True)
    print(f"[frame_generator] Listo. Archivo: {OUTPUT_PATH}")


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("\n[frame_generator] Iniciando generación del marco...")

    limpiar_escena()

    # Materiales
    mat_bronce = crear_material_bronce()
    mat_void   = crear_material_oscuro()

    # Geometría
    construir_marco(mat_bronce)
    crear_todas_las_calaveras(mat_bronce, mat_void)
    crear_pentagrama(mat_bronce)

    # Escena
    setup_iluminacion()
    setup_camara()
    setup_render()

    # Render
    renderizar()

    print("""
[frame_generator] Resultado:
  ✓ Alpha real en paneles (no negro sólido como LA ELEGIDA)
  ✓ 4 calaveras simétricas y completas en las esquinas
  ✓ 1 calavera en el centro-inferior de la columna
  ✓ Pentáculo con anillo ornamental en la columna superior
  ✓ Divisor del panel derecho prominente (22px, con relieve)
  ✓ HUD strip 90px — suficiente para nombre + clase + 2 barras
  ✓ Resolución exacta 1000×600 px
  ✓ Material bronce PBR (metallic=0.92, roughness=0.44)
""")


if __name__ == "__main__":
    main()
