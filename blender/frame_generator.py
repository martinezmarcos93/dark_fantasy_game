"""
Descenso al Umbral — UI Frame Generator v2
==========================================
Blender 5.x compatible.

USO:
    blender --background --python blender/frame_generator.py

SALIDA:
    godot/assets/images/ui_frame.png  (1000×600 px, RGBA)

AJUSTE RÁPIDO:
    Modificar la sección CONFIG. RENDER_SAMPLES=32 para iteraciones rápidas.
"""

import bpy
import bmesh
import math
import os

# ═══════════════════════════════════════════════════════════════
# CONFIG
# ═══════════════════════════════════════════════════════════════

OUTPUT_FILE = "ui_frame.png"
try:
    _dir = os.path.dirname(os.path.realpath(__file__))
    OUTPUT_PATH = os.path.normpath(
        os.path.join(_dir, "..", "godot", "assets", "images", OUTPUT_FILE)
    )
except NameError:
    OUTPUT_PATH = bpy.path.abspath("//godot/assets/images/" + OUTPUT_FILE)

RENDER_W       = 1000
RENDER_H       = 600
RENDER_SAMPLES = 256   # 256 para render final; bajar a 32 para iterar rápido

# Canvas: 1 unidad = 100 px → 10 × 6 unidades
W = 10.0
H = 6.0

# Borde exterior
B = 0.42

# Panel izquierdo
LP_W  = 2.80   # ancho imagen
HUD_H = 0.90   # altura HUD strip
HUD_SEP = 0.06 # separador imagen/HUD

# Columna central
COL_W = 0.68

# Panel derecho
OPT_H  = 1.25  # altura área opciones
DIV_H  = 0.22  # altura divisor derecho

# Material bronce — más oscuro y con más contraste
MAT_BASE  = (0.20, 0.10, 0.02, 1.0)
MAT_METAL = 0.95
MAT_ROUGH = 0.38

# Material cuencas oculares
MAT_VOID  = (0.008, 0.003, 0.003, 1.0)

# Altura Z de cada elemento (jerarquía visual más pronunciada)
Z_FRAME   = 0.16
Z_RIDGE   = 0.07   # cresta sobre el marco
Z_DIV     = 0.12   # divisor panel derecho
Z_SKULL   = 0.09
Z_PENT    = 0.18
Z_BOSS    = 0.06   # medallón circular bajo cada calavera

# Geometría cráneos — cuencas grandes = lectura instantánea de "calavera"
SK_R      = 0.230
SK_EYE_R  = 0.090
SK_EYE_DX = 0.100
SK_EYE_DY = 0.018
SK_EYE_DZ = 0.54

# Geometría pentáculo — más grande
PE_R_EXT  = 0.28
PE_R_INT  = 0.10

# ═══════════════════════════════════════════════════════════════
# COORDENADAS DERIVADAS
# ═══════════════════════════════════════════════════════════════
LP_X1 = B
LP_X2 = B + LP_W
COL_X1 = LP_X2
COL_X2 = LP_X2 + COL_W
COL_CX = (COL_X1 + COL_X2) / 2.0
RP_X1 = COL_X2
RP_X2 = W - B

BOT = B
TOP = H - B

HUD_Y1    = BOT
HUD_Y2    = BOT + HUD_H
HUDSEP_Y1 = HUD_Y2
HUDSEP_Y2 = HUD_Y2 + HUD_SEP
IMG_Y1    = HUDSEP_Y2
IMG_Y2    = TOP

OPT_Y1   = BOT
OPT_Y2   = BOT + OPT_H
DIV_Y1   = OPT_Y2
DIV_Y2   = OPT_Y2 + DIV_H
TXT_Y1   = DIV_Y2
TXT_Y2   = TOP

PENT_CY = TOP - 0.38

# Posiciones de las 5 calaveras
# Insetadas hacia adentro (B*0.82) para que el medallón entre completo
# en el canvas y no se clipee (defecto de LA ELEGIDA).
_ins = B * 0.82
SKULL_POS = [
    (_ins,        _ins),       # bottom-left
    (W - _ins,    _ins),       # bottom-right
    (_ins,        H - _ins),   # top-left
    (W - _ins,    H - _ins),   # top-right
    (COL_CX,      _ins),       # center-bottom (en la columna)
]


# ═══════════════════════════════════════════════════════════════
# UTILIDADES
# ═══════════════════════════════════════════════════════════════

def limpiar_escena():
    bpy.ops.wm.read_factory_settings(use_empty=True)


def suavizar_mesh(mesh):
    """Shade smooth directamente en el mesh — sin operadores de contexto."""
    for poly in mesh.polygons:
        poly.use_smooth = True
    mesh.update()


def caja(name, x1, y1, x2, y2, z_alto, z_bajo=0.0):
    """
    Crea un prisma rectangular extruido.
    Normal de la cara superior apunta en +Z (visible desde la cámara).
    """
    mesh = bpy.data.meshes.new(name)
    bm = bmesh.new()

    # Vértices en sentido antihorario visto desde arriba → normal +Z
    v0 = bm.verts.new((x1, y1, z_bajo))
    v1 = bm.verts.new((x1, y2, z_bajo))
    v2 = bm.verts.new((x2, y2, z_bajo))
    v3 = bm.verts.new((x2, y1, z_bajo))
    bm.faces.new([v0, v1, v2, v3])

    # Extruir en +Z
    res = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
    top = [v for v in res['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=top, vec=(0.0, 0.0, z_alto))

    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(mesh)
    bm.free()

    suavizar_mesh(mesh)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.collection.objects.link(obj)
    return obj


def mat_bronce():
    m = bpy.data.materials.new("Bronce")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()

    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = MAT_BASE
    bsdf.inputs["Metallic"].default_value   = MAT_METAL
    bsdf.inputs["Roughness"].default_value  = MAT_ROUGH
    for k in ("Specular IOR Level", "Specular"):
        if k in bsdf.inputs:
            bsdf.inputs[k].default_value = 0.75
            break

    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m


def mat_void():
    m = bpy.data.materials.new("Void")
    m.use_nodes = True
    nt = m.node_tree
    nt.nodes.clear()

    bsdf = nt.nodes.new("ShaderNodeBsdfPrincipled")
    bsdf.inputs["Base Color"].default_value = MAT_VOID
    bsdf.inputs["Metallic"].default_value   = 0.0
    bsdf.inputs["Roughness"].default_value  = 0.95

    out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(bsdf.outputs["BSDF"], out.inputs["Surface"])
    return m


def asignar(obj, mat):
    obj.data.materials.clear()
    obj.data.materials.append(mat)


# ═══════════════════════════════════════════════════════════════
# MARCO
# ═══════════════════════════════════════════════════════════════

def construir_marco(mb):
    """
    7 piezas sólidas del marco. Los paneles = ausencia de geometría = alpha.
    Las 4 crestas interiores dan la ilusión de tallado en capas.
    """
    piezas = [
        # Bordes principales
        caja("Top",    0,     TOP,  W,    H,    Z_FRAME),
        caja("Bot",    0,     0,    W,    BOT,  Z_FRAME),
        caja("Left",   0,     BOT,  B,    TOP,  Z_FRAME),
        caja("Right",  RP_X2, BOT,  W,    TOP,  Z_FRAME),
        # Columna central
        caja("Col",    COL_X1, BOT, COL_X2, TOP, Z_FRAME),
        # Separador imagen/HUD (izquierda)
        caja("HUDSep", LP_X1, HUDSEP_Y1, LP_X2, HUDSEP_Y2, Z_FRAME + 0.04),
        # Divisor panel derecho (prominente, más alto → más iluminado)
        caja("Div",    RP_X1, DIV_Y1, RP_X2, DIV_Y2, Z_FRAME + Z_DIV),
    ]

    # Crestas interiores decorativas (simulan tallado en capas)
    def cresta(name, x1, y1, x2, y2, margin_factor=0.20):
        mx = min(x2 - x1, y2 - y1) * margin_factor
        return caja(name, x1 + mx, y1 + mx, x2 - mx, y2 - mx, Z_RIDGE, z_bajo=Z_FRAME)

    piezas += [
        cresta("CTop",   0,     TOP,  W,    H),
        cresta("CBot",   0,     0,    W,    BOT),
        cresta("CLeft",  0,     BOT,  B,    TOP),
        cresta("CRight", RP_X2, BOT,  W,    TOP),
    ]

    for p in piezas:
        asignar(p, mb)
    return piezas


# ═══════════════════════════════════════════════════════════════
# CALAVERAS
# ═══════════════════════════════════════════════════════════════

def medallon(cx, cy, mb):
    """Disco circular de bronce bajo cada calavera. Base ornamental."""
    bpy.ops.mesh.primitive_cylinder_add(
        radius=SK_R * 1.32, depth=Z_BOSS,
        location=(cx, cy, Z_FRAME + Z_BOSS * 0.5),
        vertices=44
    )
    m = bpy.context.active_object
    m.name = "Medallon"
    asignar(m, mb)
    return m


def calavera(cx, cy, mb, mv, tag, z_base=Z_FRAME):
    """
    Cráneo en bajorrelieve, cara hacia la cámara (+Z).
    Visto desde arriba se lee como una calavera frontal:
      +Y = corona del cráneo, -Y = mandíbula.
    Componentes:
      - Bóveda craneal (domo)
      - Mandíbula
      - 2 cuencas oculares (oscuras, hundidas)
      - Cavidad nasal (oscura, triángulo invertido)
      - Hilera de dientes (nubs de bronce sobre franja oscura)
    """
    objs = []
    zb = z_base
    # Altura de la superficie donde se incrustan los rasgos oscuros
    z_surf = zb + SK_R * 0.42

    # ── Bóveda craneal: domo aplastado, más alto que ancho ────
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=SK_R,
        location=(cx, cy + SK_R * 0.10, zb + SK_R * 0.22),
        segments=32, ring_count=20
    )
    cr = bpy.context.active_object
    cr.name = f"Skull_{tag}_Boveda"
    cr.scale = (0.90, 1.05, 0.48)   # ancho<alto, domo bajo
    bpy.ops.object.transform_apply(scale=True)
    suavizar_mesh(cr.data)
    asignar(cr, mb)
    objs.append(cr)

    # ── Mandíbula: esfera menor desplazada hacia -Y ───────────
    bpy.ops.mesh.primitive_uv_sphere_add(
        radius=SK_R * 0.62,
        location=(cx, cy - SK_R * 0.62, zb + SK_R * 0.18),
        segments=24, ring_count=14
    )
    jaw = bpy.context.active_object
    jaw.name = f"Skull_{tag}_Mand"
    jaw.scale = (0.80, 0.78, 0.42)
    bpy.ops.object.transform_apply(scale=True)
    suavizar_mesh(jaw.data)
    asignar(jaw, mb)
    objs.append(jaw)

    # ── Cuencas oculares: oscuras, hundidas, simétricas ───────
    for lado, dx in [("L", -SK_EYE_DX), ("R", SK_EYE_DX)]:
        bpy.ops.mesh.primitive_uv_sphere_add(
            radius=SK_EYE_R,
            location=(cx + dx, cy + SK_R * 0.22, z_surf),
            segments=16, ring_count=10
        )
        oj = bpy.context.active_object
        oj.name = f"Skull_{tag}_Cuenca{lado}"
        oj.scale = (1.15, 0.95, 0.85)
        bpy.ops.object.transform_apply(scale=True)
        suavizar_mesh(oj.data)
        asignar(oj, mv)
        objs.append(oj)

    # ── Cavidad nasal: triángulo invertido oscuro ─────────────
    nasal = bpy.data.meshes.new(f"Skull_{tag}_Nasal")
    bm = bmesh.new()
    nw = SK_EYE_R * 0.62      # medio ancho arriba
    nh = SK_EYE_R * 1.05      # alto
    ny = cy - SK_R * 0.04     # centro vertical de la nariz
    zt = z_surf + SK_R * 0.10 # sobresale un poco para verse
    v_top_l = bm.verts.new((cx - nw, ny + nh * 0.5, zt))
    v_top_r = bm.verts.new((cx + nw, ny + nh * 0.5, zt))
    v_bot   = bm.verts.new((cx,      ny - nh * 0.5, zt))
    bm.faces.new([v_top_l, v_top_r, v_bot])
    res = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
    topv = [v for v in res['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=topv, vec=(0, 0, SK_R * 0.10))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(nasal)
    bm.free()
    suavizar_mesh(nasal)
    no = bpy.data.objects.new(f"Skull_{tag}_Nasal", nasal)
    bpy.context.collection.objects.link(no)
    asignar(no, mv)
    objs.append(no)

    # ── Dientes: franja oscura + nubs de bronce ───────────────
    teeth_y = cy - SK_R * 0.52
    teeth_w = SK_R * 0.70
    # Franja oscura (la boca)
    boca = caja(f"Skull_{tag}_Boca",
                cx - teeth_w * 0.5, teeth_y - SK_R * 0.10,
                cx + teeth_w * 0.5, teeth_y + SK_R * 0.10,
                SK_R * 0.12, z_bajo=zb)
    asignar(boca, mv)
    objs.append(boca)
    # Dientes individuales (5 nubs de bronce sobre la boca)
    n_dientes = 5
    dw = teeth_w / (n_dientes + 1)
    for i in range(n_dientes):
        dx = cx - teeth_w * 0.5 + dw * (i + 0.5) + dw * 0.5
        d = caja(f"Skull_{tag}_Diente{i}",
                 dx - dw * 0.30, teeth_y - SK_R * 0.085,
                 dx + dw * 0.30, teeth_y + SK_R * 0.085,
                 SK_R * 0.22, z_bajo=zb)
        asignar(d, mb)
        objs.append(d)

    return objs


def construir_calaveras(mb, mv):
    nombres = ["BL", "BR", "TL", "TR", "CB"]
    all_objs = []
    for nm, (cx, cy) in zip(nombres, SKULL_POS):
        all_objs.append(medallon(cx, cy, mb))
        all_objs.extend(calavera(cx, cy, mb, mv, nm, z_base=Z_FRAME + Z_BOSS))
    return all_objs


# ═══════════════════════════════════════════════════════════════
# PENTÁCULO
# ═══════════════════════════════════════════════════════════════

def construir_pentagrama(mb):
    """Estrella de 5 puntas + anillo ornamental."""
    cx, cy = COL_CX, PENT_CY
    z = Z_FRAME

    # Estrella
    pts = []
    for i in range(10):
        r = PE_R_EXT if i % 2 == 0 else PE_R_INT
        a = math.pi / 2.0 + i * math.pi / 5.0
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))

    mesh = bpy.data.meshes.new("Pent")
    bm = bmesh.new()
    vc = bm.verts.new((cx, cy, z))
    vs = [bm.verts.new((p[0], p[1], z)) for p in pts]
    for i in range(10):
        bm.faces.new([vc, vs[i], vs[(i + 1) % 10]])

    res = bmesh.ops.extrude_face_region(bm, geom=bm.faces[:])
    top = [v for v in res['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm, verts=top, vec=(0, 0, Z_PENT))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces[:])
    bm.to_mesh(mesh)
    bm.free()
    suavizar_mesh(mesh)

    pent_obj = bpy.data.objects.new("Pentagrama", mesh)
    bpy.context.collection.objects.link(pent_obj)
    asignar(pent_obj, mb)

    # Anillo alrededor del pentáculo
    r_ext = PE_R_EXT * 1.44
    r_int = PE_R_EXT * 1.20
    segs  = 48
    z_ring = Z_PENT * 0.55

    ring_mesh = bpy.data.meshes.new("PentAnillo")
    bm2 = bmesh.new()
    inn, out = [], []
    for i in range(segs):
        a = 2 * math.pi * i / segs
        ca, sa = math.cos(a), math.sin(a)
        inn.append(bm2.verts.new((cx + r_int * ca, cy + r_int * sa, z)))
        out.append(bm2.verts.new((cx + r_ext * ca, cy + r_ext * sa, z)))
    bm2.verts.ensure_lookup_table()
    for i in range(segs):
        j = (i + 1) % segs
        bm2.faces.new([out[i], out[j], inn[j], inn[i]])

    res2 = bmesh.ops.extrude_face_region(bm2, geom=bm2.faces[:])
    top2 = [v for v in res2['geom'] if isinstance(v, bmesh.types.BMVert)]
    bmesh.ops.translate(bm2, verts=top2, vec=(0, 0, z_ring))
    bmesh.ops.recalc_face_normals(bm2, faces=bm2.faces[:])
    bm2.to_mesh(ring_mesh)
    bm2.free()
    suavizar_mesh(ring_mesh)

    ring_obj = bpy.data.objects.new("PentAnillo", ring_mesh)
    bpy.context.collection.objects.link(ring_obj)
    asignar(ring_obj, mb)

    return [pent_obj, ring_obj]


# ═══════════════════════════════════════════════════════════════
# ILUMINACIÓN
# ═══════════════════════════════════════════════════════════════

def setup_luz():
    # Key (upper-left, fuerte para highlights metálicos)
    bpy.ops.object.light_add(type='AREA', location=(W * 0.10, H * 1.6, 10.0))
    k = bpy.context.active_object
    k.name = "Key"
    k.data.energy = 1400.0
    k.data.size   = 3.5
    k.rotation_euler = (math.radians(-40), 0, math.radians(-22))

    # Fill (derecha, suave)
    bpy.ops.object.light_add(type='AREA', location=(W * 0.92, H * 0.5, 7.5))
    f = bpy.context.active_object
    f.name = "Fill"
    f.data.energy = 380.0
    f.data.size   = 8.0

    # Rim (desde abajo, resalta aristas inferiores)
    bpy.ops.object.light_add(type='AREA', location=(W * 0.5, -2.0, 4.5))
    r = bpy.context.active_object
    r.name = "Rim"
    r.data.energy = 200.0
    r.data.size   = 4.0
    r.rotation_euler = (math.radians(42), 0, 0)

    # Spot extra sobre la columna central (ilumina pentáculo y cráneo CB)
    bpy.ops.object.light_add(type='SPOT', location=(COL_CX, H * 0.5, 8.0))
    sp = bpy.context.active_object
    sp.name = "ColSpot"
    sp.data.energy     = 600.0
    sp.data.spot_size  = math.radians(30)
    sp.data.spot_blend = 0.4
    sp.rotation_euler  = (0.0, 0.0, 0.0)

    # World ambient mínimo
    world = bpy.context.scene.world
    if world is None:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world
    world.use_nodes = True
    bg = world.node_tree.nodes.get("Background")
    if bg:
        bg.inputs["Color"].default_value    = (0.03, 0.018, 0.008, 1.0)
        bg.inputs["Strength"].default_value = 0.40


# ═══════════════════════════════════════════════════════════════
# CÁMARA — fix crítico respecto a v1
# ═══════════════════════════════════════════════════════════════

def setup_camara():
    """
    Cámara ortográfica mirando hacia abajo (-Z).

    FIX vs v1: ortho_scale = W (no H).
    En Blender con sensor_fit='HORIZONTAL', ortho_scale controla el ancho.
    Para 1000×600 (aspect 5:3):
      - Ancho visible = ortho_scale = W = 10 unidades  → [0, 10] ✓
      - Alto visible  = W × (600/1000) = 6 unidades    → [0, 6]  ✓
    Centrada en (W/2, H/2) = (5, 3) cubre exactamente el canvas del frame.
    """
    cam_data = bpy.data.cameras.new("Cam")
    cam_data.type        = 'ORTHO'
    cam_data.ortho_scale = W              # FIX: W no H
    cam_data.sensor_fit  = 'HORIZONTAL'  # FIX: explícito

    cam_obj = bpy.data.objects.new("Cam", cam_data)
    bpy.context.collection.objects.link(cam_obj)
    cam_obj.location       = (W / 2.0, H / 2.0, 20.0)
    cam_obj.rotation_euler = (0.0, 0.0, 0.0)  # mira en -Z (recto hacia abajo)
    bpy.context.scene.camera = cam_obj
    return cam_obj


# ═══════════════════════════════════════════════════════════════
# RENDER
# ═══════════════════════════════════════════════════════════════

def setup_render():
    sc = bpy.context.scene
    sc.render.engine               = 'CYCLES'
    sc.render.resolution_x         = RENDER_W
    sc.render.resolution_y         = RENDER_H
    sc.render.resolution_percentage = 100
    sc.render.film_transparent     = True   # paneles = alpha, no negro
    sc.render.image_settings.file_format = 'PNG'
    sc.render.image_settings.color_mode  = 'RGBA'
    sc.render.image_settings.compression = 15
    sc.cycles.device      = 'CPU'
    sc.cycles.samples     = RENDER_SAMPLES
    sc.cycles.use_denoising = True
    sc.render.filepath    = OUTPUT_PATH


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    print("\n[frame_generator v2] Iniciando...")

    limpiar_escena()

    mb = mat_bronce()
    mv = mat_void()

    construir_marco(mb)
    construir_calaveras(mb, mv)
    construir_pentagrama(mb)

    setup_luz()
    setup_camara()
    setup_render()

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    print(f"[frame_generator v2] Renderizando {RENDER_W}×{RENDER_H} @ {RENDER_SAMPLES} samples")
    print(f"  Salida: {OUTPUT_PATH}")
    bpy.ops.render.render(write_still=True)
    print("[frame_generator v2] Listo.")


main()
