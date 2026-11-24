# clairiere_v2.py — clairière du grand massif, version 2 (2026-11-22, demandes de l'auteur après la mise en scène de SC03).
#  1. Massif à sa vraie hauteur : place_garden_props.py l'écrasait à 60 % (ZSCALE rose_bed 0.6) parce que la fleur jaune
#     centrale du modèle Tripo montait à 2,15 m ; les rosiers ne faisaient plus que 0,3–0,5 m et la bordure 0,22 m.
#     On repart du maillage d'origine (hauteur ÷ 0,6) et on retire la fleur centrale : la Rose est désormais un objet à part
#     (provisoire : ROSE_provisoire ; plus tard son modèle 3D), animable dans les scènes 3, 8, 12, 13.
#  2. Accès à la Rose : un passage de pas japonais traverse le massif depuis la bordure sud-sud-est (azimut -70°) jusqu'à
#     un petit rond de mousse au pied de la Rose (choix de l'auteur, 2026-11-22). Elias s'y agenouille à 0,6 m d'elle.
#  3. Fond sud : rosiers grimpants sur le muret de l'exèdre, grands arbustes fleuris derrière lui, grands arbres au-delà
#     (choix de l'auteur : végétation le long du muret), pour les contrechamps sur Elias.
# Usage (world.blend ouvert) : exec(compile(open(chemin, encoding="utf-8").read(), chemin, "exec")) ; appliquer()
# Rejouable : chaque fonction supprime ce qu'elle a créé avant de le refaire.
import bpy, bmesh, math, random
from mathutils import Vector

K = 0.8                                    # échelle de l'environnement (kb/decisions/0009)
MASSIF = (0.0, -217.4)                     # centre du massif, coordonnées locales d'ECHELLE_MONDE (= monde / 0,8)
SOIL = 0.30                                # terre du massif, local (≈ 0,24 m monde)
MOSS_R = 0.65                              # rond de mousse, rayon local (≈ 0,52 m monde : la place d'un enfant à genoux)
PATH_AZ = math.radians(-70)                # azimut du passage (depuis +X, sens trigo) : sud-sud-est
PATH_HALF = 0.36                           # demi-largeur du passage, local (≈ 0,58 m monde)
EXEDRE = (0.0, -216.29)                    # centre du muret de l'exèdre, local
WALL_R = 10.1                              # rayon du muret, local
SRC_MESH = "GARDEN_rose_bed_master_mesh"   # maillage d'origine (écrasé à 0,6 en hauteur, partagé avec le maître)
NEW_MESH = "GARDEN_rose_bed_v2_mesh"

def _E(): return bpy.data.objects["ECHELLE_MONDE"]

def _mat(name, rgb):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1)
    if m.node_tree is None: m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    if b: b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = 0.8
    return m

def _prim(kind, name, coll, size, loc, mat, rot=(0, 0, 0)):
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    if kind == "sphere": bmesh.ops.create_uvsphere(bm, u_segments=20, v_segments=12, radius=0.5)
    elif kind == "box": bmesh.ops.create_cube(bm, size=1.0)
    else: bmesh.ops.create_cone(bm, cap_ends=True, segments=24, radius1=0.5, radius2=0.5, depth=1.0)
    for v in bm.verts: v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); coll.objects.link(o); o.data.materials.append(mat)
    o.parent = _E(); o.matrix_parent_inverse.identity(); o.location = loc; o.rotation_euler = rot
    return o

def _purge(prefix):
    for o in [o for o in bpy.data.objects if o.name.startswith(prefix)]:
        me = o.data if o.type == "MESH" else None
        bpy.data.objects.remove(o, do_unlink=True)
        if me is not None and me.users == 0: bpy.data.meshes.remove(me)

# ---------------------------------------------------------------- 1 + 2. massif
def massif_v2():
    src = bpy.data.meshes[SRC_MESH]
    old = bpy.data.meshes.get(NEW_MESH)
    me = src.copy()
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts: v.co.z /= 0.6                     # hauteur d'origine
    ux, uy = math.cos(PATH_AZ), math.sin(PATH_AZ)
    kill = []
    for v in bm.verts:
        x, y, z = v.co; r = math.hypot(x, y)
        along, across = x * ux + y * uy, -x * uy + y * ux
        in_moss = r < MOSS_R and z > SOIL + 0.03
        in_path = 0.6 < along < 2.85 and abs(across) < PATH_HALF and z > SOIL + 0.03
        central_rose = r < 1.0 and z > 1.4
        if in_moss or in_path or central_rose: kill.append(v)
    bmesh.ops.delete(bm, geom=kill, context="VERTS")
    bm.to_mesh(me); bm.free()
    if old: old.name = NEW_MESH + "_old"
    me.name = NEW_MESH
    P = bpy.data.objects["P3D_massif"]; P.data = me
    if old and old.users == 0: bpy.data.meshes.remove(old)
    # mousse, terre du passage, pas japonais (dans la même collection que le massif)
    coll = P.users_collection[0]
    _purge("massif_v2_")
    cx, cy = MASSIF
    _prim("cyl", "massif_v2_mousse", coll, (2 * MOSS_R, 2 * MOSS_R, 0.04), (cx, cy, SOIL + 0.01), _mat("AUR_mousse", (0.22, 0.38, 0.12)))
    L = 2.4; mid = 0.6 + L / 2
    # passage rectiligne : une bande de terre droite, de la mousse à la bordure (2026-11-22, soir : demande de l'auteur)
    _prim("box", "massif_v2_terre_passage", coll, (L, 2 * PATH_HALF, 0.03), (cx + mid * ux, cy + mid * uy, SOIL), _mat("AUR_terre", (0.30, 0.20, 0.12)),
          rot=(0, 0, PATH_AZ))
    # pas japonais carrés ou rectangulaires, alignés sur le passage (à peine décalés, comme posés à la main)
    random.seed(7)
    for i, (d, lg, la) in enumerate(((1.05, 0.42, 0.42), (1.62, 0.36, 0.48), (2.22, 0.42, 0.42))):
        _prim("box", f"massif_v2_dalle_{i + 1}", coll, (lg, la, 0.06), (cx + d * ux, cy + d * uy, SOIL + 0.02),
              _mat("AUR_dalle", (0.72, 0.66, 0.55)), rot=(0, 0, PATH_AZ + math.radians(random.uniform(-4, 4))))
    return len(kill)

# ---------------------------------------------------------------- la Rose provisoire (toutes les scènes sauf SC03, qui a la sienne, animée)
def rose_statique():
    par = bpy.data.collections["AUR_21_massif_et_reperes"]
    coll = bpy.data.collections.get("AUR_21_rose_statique") or bpy.data.collections.new("AUR_21_rose_statique")
    if coll.name not in [c.name for c in par.children]: par.children.link(coll)
    _purge("ROSE_provisoire")
    cx, cy = MASSIF
    top = 1.15 / K                                       # fleur à ≈ 1,15 m (les autres roses : 0,7–0,9 m)
    _prim("cyl", "ROSE_provisoire_tige", coll, (0.02 / K, 0.02 / K, top - SOIL), (cx, cy, (top + SOIL) / 2), _mat("AUR_rose_tige", (0.08, 0.30, 0.10)))
    _prim("sphere", "ROSE_provisoire_fleur", coll, (0.20 / K, 0.20 / K, 0.14 / K), (cx, cy, top), _mat("AUR_rose_jaune", (1.0, 0.88, 0.35)))
    return coll.name

# ---------------------------------------------------------------- 3. végétation de l'exèdre
def vegetation_exedre():
    coll = bpy.data.collections["AUR_22_arbres"]
    _purge("exedre_")
    random.seed(11)
    ex, ey = EXEDRE
    shrub, flowers, roses = bpy.data.materials["AUR_shrub"], bpy.data.materials["AUR_flowers"], _mat("AUR_rosiers_grimpants", (0.80, 0.45, 0.58))
    lilas = _mat("AUR_arbustes_fleuris", (0.86, 0.84, 0.92))
    n = 0
    # rosiers grimpants posés sur le muret (le muret fait 1,28 m monde = 1,6 local)
    a = -176.0
    while a < -4:
        t = math.radians(a); L = random.uniform(2.2, 3.2)
        _prim("sphere", f"exedre_rosier_{n:02d}", coll, (L, 0.9, random.uniform(0.9, 1.3)),
              (ex + WALL_R * math.cos(t), ey + WALL_R * math.sin(t), 1.55 + random.uniform(-0.1, 0.15)), roses, rot=(0, 0, t + math.pi / 2))
        n += 1; a += random.uniform(12, 17)
    # grands arbustes fleuris juste derrière le muret (≈ 2,4–3,2 m monde)
    a, i = -170.0, 0
    while a < -8:
        t = math.radians(a); h = random.uniform(3.0, 4.0)
        _prim("sphere", f"exedre_arbuste_{i:02d}", coll, (random.uniform(3.2, 4.2), random.uniform(2.6, 3.2), h),
              (ex + (WALL_R + 1.7) * math.cos(t), ey + (WALL_R + 1.7) * math.sin(t), h / 2 - 0.1),
              lilas if i % 3 == 1 else (flowers if i % 3 == 2 else shrub), rot=(0, 0, t + math.pi / 2))
        i += 1; a += random.uniform(13, 17)
    # grands arbres au-delà (tilleuls et cyprès des modèles Tripo)
    lind = next(o for o in bpy.data.objects if o.name.startswith("P3D_arbre") and not o.hide_render)
    cyp = next(o for o in bpy.data.objects if o.name.startswith("P3D_cypres") and not o.hide_render)
    trees = [("tilleul", -158, 15.5, 12.5), ("cypres", -138, 13.0, 12.0), ("tilleul", -118, 16.5, 13.5), ("tilleul", -88, 15.0, 12.0),
             ("cypres", -64, 13.0, 12.5), ("tilleul", -44, 16.0, 13.0), ("tilleul", -18, 15.0, 12.0)]
    for j, (kind, adeg, r, h) in enumerate(trees):
        src = lind if kind == "tilleul" else cyp
        o = src.copy(); o.name = f"exedre_{kind}_{j}"; coll.objects.link(o)
        t = math.radians(adeg); o.parent = _E(); o.matrix_parent_inverse.identity()
        o.location = (ex + r * math.cos(t), ey + r * math.sin(t), 0)
        o.scale = (h * src.scale.x / src.dimensions.z * K,) * 3 if src.parent is None else (h * src.scale.x / (src.dimensions.z / K),) * 3
        o.rotation_euler = (0, 0, random.uniform(0, 6.28))
    return n, i, len(trees)

def appliquer():
    out = {"massif_sommets_retires": massif_v2(), "rose": rose_statique(), "vegetation": vegetation_exedre()}
    # la copie de SC03 faite le matin (massif sans rose centrale) n'a plus lieu d'être
    o = bpy.data.objects.get("MES3_massif_sans_rose_centrale")
    if o: bpy.data.objects.remove(o, do_unlink=True)
    c = bpy.data.collections.get("AUR_35_SC03_massif")
    if c: bpy.data.collections.remove(c)
    return out
