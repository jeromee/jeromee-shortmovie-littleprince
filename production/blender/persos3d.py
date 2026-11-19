# persos3d.py — personnages 3D (Tripo multivue + rig Tripo) dans les plans Blender.
# À exécuter dans world.blend, APRÈS build_shots_sc02.py (qui recrée les mannequins).
#
# Les modèles maîtres vivent dans la collection AUR_32_persos3d_rig (scène TEST_PERSOS3D),
# exclue des plans. Ils sont déjà mis à l'échelle (Reine 1,78 m avec chignon, Elias 1,38 m, Chambellan 1,85 m,
# conseillers 1,80 / 1,62 / 1,76 m, valet 1,78 m),
# tournés face à -Y (cap 0° des mannequins) et les bras détendus (pose sur le rig).
# Pour chaque plan, dress_shot() crée une copie liée (même maillage, même pose) de chaque
# personnage, l'accroche au pivot animé du mannequin et masque le mannequin.
# Source des modèles : production/characters3d/*_tripo_v1_rig.glb (Magnific, Tripo v3.1).
import bpy

MASTERS = {  # clé du mannequin -> armature maîtresse
    "REINE": "RIG_Reine",
    "ELIAS": "RIG_Elias",
    "CHAMBELLAN": "RIG_Chambellan",
    "CONSEILLER_1": "RIG_Conseiller1",
    "CONSEILLER_2": "RIG_Conseiller2",
    "CONSEILLER_3": "RIG_Conseiller3",
    "VALET_1": "RIG_Valet",
    "VALET_2": "RIG_Valet",
}

def _copy_rig(master, coll, name):
    A = master.copy(); A.name = name + "_rig"; A.animation_data_clear(); coll.objects.link(A)
    for m in [c for c in master.children if c.type == "MESH"]:
        M = m.copy(); M.name = name + "_3d"; coll.objects.link(M)
        M.parent = A; M.matrix_parent_inverse = m.matrix_parent_inverse.copy()
        for mod in M.modifiers:
            if mod.type == "ARMATURE": mod.object = A
    return A

def dress_shot(scname, cast=None):
    """Remplace dans le plan `scname` les mannequins listés par les personnages 3D."""
    cast = cast or MASTERS
    coll = bpy.data.collections[scname + "_jeu"]
    for key, rig in cast.items():
        piv = bpy.data.objects.get(f"{scname}_{key}")
        master = bpy.data.objects.get(rig)
        if piv is None or master is None: continue
        for o in [o for o in coll.objects if o.name.startswith(f"{scname}_{key}_") and o.name.endswith(("_rig", "_3d"))]:
            bpy.data.objects.remove(o, do_unlink=True)
        A = _copy_rig(master, coll, f"{scname}_{key}")
        A.parent = piv; A.matrix_parent_inverse.identity()
        A.location = (0, 0, master.location.z)          # pieds au niveau du pivot (sol)
        A.rotation_euler = master.rotation_euler.copy()  # -90° : face au cap du pivot
        A.scale = master.scale.copy()
        for part in ("_corps", "_tete"):
            o = bpy.data.objects.get(f"{scname}_{key}{part}")
            if o: o.hide_render = True; o.hide_viewport = True

if __name__ == "__main__":
    for n in [s.name for s in bpy.data.scenes if s.name.startswith("SC02-SH")]:
        dress_shot(n)
