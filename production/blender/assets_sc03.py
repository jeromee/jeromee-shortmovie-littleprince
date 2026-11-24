# assets_sc03.py — modèles 3D des assets de la scène 3 (2026-11-22, nuit) : jardiniers, Rose endormie, brouette, rosier.
# Planches (GPT 2.6, grilles de quatre vues) puis Tripo v3.1 multivue ; rig Tripo pour les jardiniers.
#   kb/characters/sheets/gardener1.png, gardener2.png ; production/refs/rose-asleep-sheet.png, wheelbarrow-sheet.png, rosier-sheet.png
#   production/characters3d/gardener1|2_tripo_v1_rig.glb ; production/props3d/rose_asleep|wheelbarrow|rosier_tripo_v1.glb
# Maîtres (cachés, comme les autres) : RIG_Jardinier1, RIG_Jardinier2 (collection AUR_32_persos3d_rig, tournés face à -Y, pieds à z = 0,
# taille réelle : 1,75 et 1,70 m) ; PROP_rose_endormie (1,15 m), PROP_brouette (1,40 m de long), PROP_rosier (0,80 m), dans
# AUR_34_accessoires_maitres. Usage : exec(...) ; importer_tout()
import bpy, os, math
from mathutils import Matrix, Vector

ROOT = os.path.dirname(os.path.dirname(bpy.data.filepath))
CH, PR = os.path.join(ROOT, "characters3d"), os.path.join(ROOT, "props3d")

def _import(path):
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=path)
    new = [o for o in bpy.data.objects if o not in before]
    for o in [o for o in new if o.name.startswith("Icosphere")]:      # objet parasite livré dans les glb Tripo
        new.remove(o); bpy.data.objects.remove(o)
    return new

def _relink(objs, coll):
    for o in objs:
        for c in list(o.users_collection): c.objects.unlink(o)
        coll.objects.link(o); o.hide_render = True; o.hide_viewport = True

def _bbox(objs):
    bpy.context.view_layer.update()
    pts = [o.matrix_world @ v.co for o in objs if o.type == "MESH" for v in o.data.vertices]
    mn = Vector([min(p[i] for p in pts) for i in range(3)]); mx = Vector([max(p[i] for p in pts) for i in range(3)])
    return mn, mx

def import_rig(fn, name, height, rotz):
    old = bpy.data.objects.get(name)
    if old:
        for c in list(old.children): bpy.data.objects.remove(c, do_unlink=True)
        bpy.data.objects.remove(old, do_unlink=True)
    new = _import(os.path.join(CH, fn))
    A = next(o for o in new if o.type == "ARMATURE"); A.name = name
    for o in new:
        if o.type == "MESH": o.name = name + "_corps"
    A.rotation_mode = "XYZ"; A.rotation_euler = (0, 0, rotz); A.location = (0, 0, 0); A.scale = (1, 1, 1)
    mn, mx = _bbox(new); k = height / (mx.z - mn.z)
    A.scale = (k, k, k); mn, mx = _bbox(new)
    A.location = Vector((-(mn.x + mx.x) / 2, -(mn.y + mx.y) / 2, -mn.z))
    _relink(new, bpy.data.collections["AUR_32_persos3d_rig"])
    return A

def import_prop(fn, name, size, axis, rotz):
    old = bpy.data.objects.get(name)
    if old: bpy.data.objects.remove(old, do_unlink=True)
    new = _import(os.path.join(PR, fn))
    M = max([o for o in new if o.type == "MESH"], key=lambda o: len(o.data.polygons))
    for o in new:
        if o is not M: bpy.data.objects.remove(o, do_unlink=True)
    M.name = name; M.parent = None
    me = M.data; me.transform(M.matrix_world); M.matrix_world = Matrix.Identity(4)
    me.transform(Matrix.Rotation(rotz, 4, "Z"))
    vs = [v.co for v in me.vertices]
    mn = Vector([min(v[i] for v in vs) for i in range(3)]); mx = Vector([max(v[i] for v in vs) for i in range(3)])
    d = mx - mn; k = size / {"x": d.x, "y": d.y, "z": d.z}[axis]
    me.transform(Matrix.Scale(k, 4) @ Matrix.Translation(-Vector(((mn.x + mx.x) / 2, (mn.y + mx.y) / 2, mn.z)))); me.update()
    me.name = name + "_mesh"
    _relink([M], bpy.data.collections["AUR_34_accessoires_maitres"])
    return M

# orientations (rotz) vérifiées sur un rendu de face (caméra au sud, regardant vers +Y) ; voir importer_tout()
ROT = {"J1": -math.pi / 2, "J2": -math.pi / 2, "rose": math.pi / 2, "brouette": math.pi / 2, "rosier": 0.0}

def importer_tout(rosier=True):
    out = {}
    out["J1"] = import_rig("gardener1_tripo_v1_rig.glb", "RIG_Jardinier1", 1.75, ROT["J1"]).name
    out["J2"] = import_rig("gardener2_tripo_v1_rig.glb", "RIG_Jardinier2", 1.70, ROT["J2"]).name
    out["rose"] = import_prop("rose_asleep_tripo_v1.glb", "PROP_rose_endormie", 1.15, "z", ROT["rose"]).name
    out["brouette"] = import_prop("wheelbarrow_tripo_v1.glb", "PROP_brouette", 1.40, "y", ROT["brouette"]).name
    if rosier and os.path.exists(os.path.join(PR, "rosier_tripo_v1.glb")):
        out["rosier"] = import_prop("rosier_tripo_v1.glb", "PROP_rosier", 0.80, "z", ROT["rosier"]).name
    return out
