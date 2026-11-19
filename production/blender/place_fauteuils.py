# place_fauteuils.py — remplace les fauteuils provisoires (boîtes brunes fauteuil_1..16 de chaque plan
# SC02-SHxx, créées par build_shots_sc02.py) par le fauteuil de terrasse 3D (Tripo v3.1, planche
# production/refs/terrace-armchair-sheet.png, choisie par l'auteur le 2026-11-18).
# À exécuter dans world.blend, APRÈS build_shots_sc01.py, build_shots_sc02.py et persos3d.py. Idempotent.
#
# Objet maître : FAUTEUIL_terrasse_master (0,98 m de haut, face avant vers -Y = le jardin, base à z = 0),
# rangé dans la collection des maîtres AUR_32_persos3d_rig (exclue des plans), masqué.
# Si absent, il est importé de production/props3d/terrace_armchair_tripo_v1_light.glb.
# Dans chaque plan : une copie liée (même maillage) par boîte, posée au sol de la terrasse à la place
# de la boîte, même orientation (vers le jardin) ; la boîte est masquée, pas supprimée.
# 2026-11-19 : les colonnes à x = ±8 tombaient dans les bacs des orangers (±8,1 ; -23,66). Les fauteuils
# sont regroupés par paires de part et d'autre des orangers : x = ±4 → ±3, ±6 → ±5, ±8 → ±10, ±10 → ±12
# (X_REMAP, appliqué aux boîtes des plans de la scène 2 comme aux rangées de SC01-SH03).
import bpy, os, math
from mathutils import Vector

T = 3.59   # niveau de la terrasse
X_REMAP = {4: 3, 6: 5, 8: 10, 10: 12}
def remap_x(x):
    k = round(abs(x))
    return math.copysign(X_REMAP[k], x) if k in X_REMAP and abs(abs(x) - k) < 0.01 else x
HERE = os.path.dirname(bpy.data.filepath)
GLB = os.path.join(HERE, "..", "props3d", "terrace_armchair_tripo_v1_light.glb")

def master_chair():
    M = bpy.data.objects.get("FAUTEUIL_terrasse_master")
    if M is None:
        before = set(bpy.data.objects)
        bpy.ops.import_scene.gltf(filepath=GLB)
        new = [o for o in bpy.data.objects if o not in before]
        M = [o for o in new if o.type == "MESH"][0]; M.name = "FAUTEUIL_terrasse_master"
        for o in new:
            if o is not M: bpy.data.objects.remove(o, do_unlink=True)
        M.parent = None; M.location = (0, 0, 0); M.rotation_euler = (0, 0, 0)
    store = bpy.data.collections["AUR_32_persos3d_rig"]
    for c in list(M.users_collection):
        if c is not store: c.objects.unlink(M)
    if M.name not in store.objects: store.objects.link(M)
    M.hide_render = True; M.hide_viewport = True
    return M

def place_in_shot(scname, M):
    coll = bpy.data.collections[scname + "_jeu"]
    boxes = sorted([o for o in coll.objects if o.name.split(".")[0].startswith("fauteuil_")], key=lambda o: o.name)
    for o in [o for o in coll.objects if o.name.startswith(scname + "_FAUTEUIL_")]:
        bpy.data.objects.remove(o, do_unlink=True)
    n = 0
    for b in boxes:
        c = b.matrix_world.translation
        F = M.copy(); F.name = f"{scname}_FAUTEUIL_{n+1:02d}"; F.data = M.data
        F.location = (remap_x(c.x), c.y, T); F.rotation_euler = (0, 0, 0)
        F.hide_render = False; F.hide_viewport = False
        coll.objects.link(F); n += 1
        b.hide_render = True; b.hide_viewport = True
    return n

# Scène 1 : la fin du survol (SC01-SH03) voit la terrasse ; on y pose les mêmes rangées que dans la
# scène 2 (positions de build_shots_sc02.props), dans une collection SC01-SH03_jeu créée au besoin.
ROWS_Y = (-21.5, -23.5)
ROWS_X = (-10, -8, -6, -4, 4, 6, 8, 10)
SC01_SHOTS = ("SC01-SH03",)

def place_in_sc01(scname, M):
    sc = bpy.data.scenes[scname]
    coll = bpy.data.collections.get(scname + "_jeu") or bpy.data.collections.new(scname + "_jeu")
    if coll.name not in [c.name for c in sc.collection.children]: sc.collection.children.link(coll)
    for o in [o for o in coll.objects if o.name.startswith(scname + "_FAUTEUIL_")]:
        bpy.data.objects.remove(o, do_unlink=True)
    n = 0
    for y in ROWS_Y:
        for x in ROWS_X:
            n += 1
            F = M.copy(); F.name = f"{scname}_FAUTEUIL_{n:02d}"; F.data = M.data
            F.location = (remap_x(x), y, T); F.rotation_euler = (0, 0, 0)
            F.hide_render = False; F.hide_viewport = False
            coll.objects.link(F)
    return n

def place_all():
    M = master_chair()
    out = {s.name: place_in_shot(s.name, M) for s in bpy.data.scenes
           if s.name.startswith("SC02-SH") and (s.name + "_jeu") in bpy.data.collections}
    for n in SC01_SHOTS:
        if n in bpy.data.scenes: out[n] = place_in_sc01(n, M)
    return out

if __name__ == "__main__":
    print(place_all())
