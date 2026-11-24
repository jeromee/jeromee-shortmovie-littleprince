# massif_rosiers.py — le grand massif à l'échelle réelle (2026-11-22, nuit ; remarque de l'auteur : « les roses autour sont énormes »).
# Le modèle Tripo du massif datait d'un massif plus petit : agrandi, ses roses faisaient la taille d'une tête. On ne garde que sa
# bordure de pierres ; l'intérieur devient un lit de terre planté de rosiers de 0,8 m (PROP_rosier : planche production/refs/rosier-sheet.png,
# Tripo v3.1), roses et pêche, répartis au hasard (graine fixe) en laissant libres le passage de dalles et le rond de mousse
# (clairiere_v2.py). La Rose reste un objet à part. Usage : exec(...) ; appliquer()
import bpy, bmesh, math, random
from mathutils import Vector

K = 0.8
CX, CY = 0.0, -173.92                      # centre du massif (monde)
SRC = "GARDEN_rose_bed_master_mesh"        # maillage maître (écrasé à 0,6 en hauteur)
R_BORD = 2.85                              # rayon intérieur de la bordure, unités locales (≈ 2,28 m monde)
SOIL = 0.30                                # terre, local
AZ = math.radians(-70)                     # passage (clairiere_v2.py)
U = (math.cos(AZ), math.sin(AZ))

def _E(): return bpy.data.objects["ECHELLE_MONDE"]

def bordure():
    me = bpy.data.meshes[SRC].copy()
    bm = bmesh.new(); bm.from_mesh(me)
    for v in bm.verts: v.co.z /= 0.6
    bmesh.ops.delete(bm, geom=[v for v in bm.verts if math.hypot(v.co.x, v.co.y) < R_BORD], context="VERTS")
    bm.to_mesh(me); bm.free()
    old = bpy.data.meshes.get("GARDEN_rose_bed_v3_bordure_mesh")
    if old: old.name = old.name + "_old"
    me.name = "GARDEN_rose_bed_v3_bordure_mesh"
    P = bpy.data.objects["P3D_massif"]; prev = P.data; P.data = me
    if old and old.users == 0: bpy.data.meshes.remove(old)
    return prev.name

def _mat_peche():
    src = bpy.data.objects["PROP_rosier"].data.materials[0]
    m = bpy.data.materials.get("PROP_rosier_peche") or src.copy()
    m.name = "PROP_rosier_peche"
    nt = m.node_tree
    if "teinte_peche" not in nt.nodes:
        tex = next(n for n in nt.nodes if n.type == "TEX_IMAGE")
        bsdf = next(n for n in nt.nodes if n.type == "BSDF_PRINCIPLED")
        hs = nt.nodes.new("ShaderNodeHueSaturation"); hs.name = "teinte_peche"
        hs.inputs["Hue"].default_value = 0.545; hs.inputs["Saturation"].default_value = 1.05; hs.inputs["Value"].default_value = 1.06
        nt.links.new(tex.outputs["Color"], hs.inputs["Color"]); nt.links.new(hs.outputs["Color"], bsdf.inputs["Base Color"])
    return m

def rosiers(seed=3, spacing=0.62, r_in=0.85, r_out=2.0, path_clear=0.62):
    coll = bpy.data.collections.get("AUR_21_rosiers") or bpy.data.collections.new("AUR_21_rosiers")
    par = bpy.data.collections["AUR_21_massif_et_reperes"]
    if coll.name not in [c.name for c in par.children]: par.children.link(coll)
    for o in list(coll.objects): bpy.data.objects.remove(o, do_unlink=True)
    src = bpy.data.objects["PROP_rosier"]; peche = _mat_peche()
    me_peche = bpy.data.meshes.get("PROP_rosier_peche_mesh") or src.data.copy()
    me_peche.name = "PROP_rosier_peche_mesh"; me_peche.materials[0] = peche
    rnd = random.Random(seed); pts = []
    for _ in range(6000):                                  # tirage de Poisson : distance minimale entre deux rosiers
        r = math.sqrt(rnd.uniform(r_in ** 2, r_out ** 2)); a = rnd.uniform(0, 2 * math.pi)
        x, y = r * math.cos(a), r * math.sin(a)
        along = x * U[0] + y * U[1]; across = -x * U[1] + y * U[0]
        if along > 0 and abs(across) < path_clear: continue
        if all(math.hypot(x - px, y - py) >= spacing for px, py in pts): pts.append((x, y))
    for i, (x, y) in enumerate(pts):
        o = src.copy(); o.name = f"rosier_{i:02d}"; coll.objects.link(o)
        if rnd.random() < 0.45: o.data = me_peche
        o.hide_render = False; o.hide_viewport = False
        o.parent = _E(); o.matrix_parent_inverse.identity()
        s = rnd.uniform(0.85, 1.12)
        o.location = Vector((CX + x, CY + y, SOIL * K - 0.03)) / K      # rosiers à taille réelle dans le monde
        o.scale = (s / K,) * 3; o.rotation_mode = "XYZ"; o.rotation_euler = (0, 0, rnd.uniform(0, 2 * math.pi))
    return len(pts)

def terre():
    for n in ("massif_v3_terre",):
        o = bpy.data.objects.get(n)
        if o: bpy.data.objects.remove(o, do_unlink=True)
    me = bpy.data.meshes.new("massif_v3_terre"); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=48, radius1=R_BORD + 0.05, radius2=R_BORD + 0.05, depth=0.06)
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new("massif_v3_terre", me); P = bpy.data.objects["P3D_massif"]; P.users_collection[0].objects.link(o)
    m = bpy.data.materials.get("AUR_terre_massif") or bpy.data.materials.new("AUR_terre_massif")
    m.diffuse_color = (0.20, 0.13, 0.08, 1); m.use_nodes = True
    m.node_tree.nodes["Principled BSDF"].inputs["Base Color"].default_value = (0.20, 0.13, 0.08, 1)
    m.node_tree.nodes["Principled BSDF"].inputs["Roughness"].default_value = 0.95
    o.data.materials.append(m)
    o.parent = _E(); o.matrix_parent_inverse.identity(); o.location = (CX / K, CY / K, SOIL - 0.04)
    return o.name

def rose_fixe():
    """ROSE_provisoire (scènes autres que SC03) : le modèle de la Rose endormie à la place de la tige et de la sphère."""
    coll = bpy.data.collections["AUR_21_rose_statique"]
    for o in list(coll.objects): bpy.data.objects.remove(o, do_unlink=True)
    o = bpy.data.objects["PROP_rose_endormie"].copy(); o.name = "ROSE_provisoire"; coll.objects.link(o)
    o.hide_render = False; o.hide_viewport = False; o.parent = _E(); o.matrix_parent_inverse.identity()
    o.location = Vector((CX, CY, SOIL * K - 0.02)) / K; o.scale = (1 / K,) * 3
    return o.name

def appliquer():
    return {"ancien_maillage": bordure(), "terre": terre(), "rosiers": rosiers(), "rose": rose_fixe()}
