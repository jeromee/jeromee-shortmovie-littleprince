# place_orangers.py — remplace les huit orangers en pot fondus dans le mesh du palais officiel
# par un oranger 3D (Tripo) posé à leur place exacte.
# À exécuter dans world.blend, après place_palace.py. Idempotent.
#
# 1. Copie le mesh de PALAIS_officiel en PALAIS_officiel_sans_orangers et y supprime les faces
#    des orangers (cylindre de 1,75 m de rayon autour de chaque arbre, au-dessus du sol de la
#    terrasse). L'original reste dans le fichier, masqué : rien n'est perdu.
# 2. Importe production/characters3d/../props3d/orange_tree_tripo_v1.glb une fois (objet maître
#    ORANGER_maitre, masqué) et en pose huit copies liées (même maillage) dans la collection
#    AUR_13_orangers, à TREE_H de haut (bac compris), chacune sur un socle rond de pierre.
# 2026-11-19 (remarque de l'auteur : orangers « gigantesques », pot aussi haut qu'un fauteuil) :
#    hauteur ramenée de 4,18 m (arbres d'origine du palais) à 2,50 m : bac ≈ 0,72 m, couronne ≈ Ø 1,3 m.
#    Socle Ø 1,4 m. Les taches vertes laissées sur le dallage par les anciens bacs sont masquées par une
#    pièce de dallage (disque Ø 2,4 m, texture du palais prise sur le dallage propre voisin).
# Positions mesurées le 2026-11-17 sur le mesh officiel (centre des couronnes).
import bpy, bmesh, os, math
from mathutils.bvhtree import BVHTree
from mathutils import Vector

T = 3.59                      # niveau de la terrasse
TREE_H = 2.50                 # hauteur des orangers, bac compris (4,18 m avant le 2026-11-19)
COVER_R = 1.20                # pièce de dallage qui masque les taches vertes des anciens bacs
PLINTH_R, PLINTH_H = 0.70, 0.06   # socle Ø 1,4 m (Ø 1,9 m avant, réduit à la demande de l'auteur le 2026-11-19)
CENTERS = [(8.13, -23.66), (-8.15, -23.66), (4.98, -8.86), (-4.96, -8.81),
           (-15.97, -9.06), (15.97, -9.05), (-15.97, -23.67), (15.95, -23.69)]
CUT_R = 1.75
HERE = os.path.dirname(bpy.data.filepath)
GLB = os.path.join(HERE, "..", "props3d", "orange_tree_tripo_v1.glb")

def palace_without_trees():
    P = bpy.data.objects["PALAIS_officiel"]
    Q = bpy.data.objects.get("PALAIS_officiel_sans_orangers")
    if Q is None:
        me = P.data.copy(); me.name = "PALAIS_officiel_sans_orangers_mesh"
        Q = bpy.data.objects.new("PALAIS_officiel_sans_orangers", me)
        Q.matrix_world = P.matrix_world.copy()
        for c in P.users_collection: c.objects.link(Q)
        bm = bmesh.new(); bm.from_mesh(me); Mw = Q.matrix_world; dele = []
        for f in bm.faces:
            ws = [Mw @ v.co for v in f.verts]
            if min(w.z for w in ws) < T + 0.04 or max(w.z for w in ws) > T + 4.5: continue
            c = sum(ws, Vector()) / len(ws)
            if c.y > -7.15: continue          # ne pas toucher à la façade
            if any((c.x - x) ** 2 + (c.y - y) ** 2 < CUT_R ** 2 for x, y in CENTERS): dele.append(f)
        bmesh.ops.delete(bm, geom=dele, context="FACES"); bm.to_mesh(me); bm.free()
    P.hide_render = True; P.hide_viewport = True
    return Q

def master_tree():
    M = bpy.data.objects.get("ORANGER_maitre")
    if M:   # maître masqué hors de la scène active : matrix_world n'est pas à jour, on part de matrix_basis
        zs = [(M.matrix_basis @ Vector(c)).z for c in M.bound_box]
        M.scale = M.scale * (TREE_H / (max(zs) - min(zs)))
        zs = [(M.matrix_basis @ Vector(c)).z for c in M.bound_box]; M.location.z -= min(zs)
        return M
    before = set(bpy.data.objects)
    bpy.ops.import_scene.gltf(filepath=GLB)
    new = [o for o in bpy.data.objects if o not in before]
    M = [o for o in new if o.type == "MESH"][0]; M.name = "ORANGER_maitre"
    for o in new:
        if o is not M: bpy.data.objects.remove(o, do_unlink=True)
    M.parent = None; M.rotation_mode = "XYZ"; M.location = (0, 0, 0)
    bpy.context.view_layer.update()
    zs = [(M.matrix_world @ Vector(c)).z for c in M.bound_box]
    k = TREE_H / (max(zs) - min(zs)); M.scale = M.scale * k
    bpy.context.view_layer.update()
    zs = [(M.matrix_world @ Vector(c)).z for c in M.bound_box]
    M.location.z -= min(zs)
    for c in list(M.users_collection): c.objects.unlink(M)
    store = bpy.data.collections.get("AUR_32_persos3d_rig")  # collection des maîtres, exclue des plans
    store.objects.link(M); M.hide_render = True; M.hide_viewport = True
    return M

def floor_uv(Q, bvh, bm, x, y):
    """UV du dallage propre à 1,9 m de l'arbre (côté +x, sinon -x) sur le mesh du palais."""
    inv = Q.matrix_world.inverted(); d = (inv.to_3x3() @ Vector((0, 0, -1))).normalized()
    uvl = bm.loops.layers.uv.active
    for dx in (1.9, -1.9):
        hit = bvh.ray_cast(inv @ Vector((x + dx, y, T + 0.5)), d)
        if hit[0] is not None:
            f = bm.faces[hit[2]]
            return sum((l[uvl].uv for l in f.loops), Vector((0, 0))) / len(f.loops)
    return None

def cover_disc(name, x, y, uv, mat, col):
    """Disque très fin, texture du palais en un seul point de dallage propre : masque les taches vertes."""
    me = bpy.data.meshes.new(name + "_mesh"); bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, segments=48, radius=COVER_R)
    for v in bm.verts: v.co.z = 0.003
    uvl = bm.loops.layers.uv.new("UVMap")
    for f in bm.faces:
        for l in f.loops: l[uvl].uv = uv
    bm.to_mesh(me); bm.free(); me.materials.append(mat)
    o = bpy.data.objects.new(name, me); o.location = (x, y, T); col.objects.link(o)
    return o

def plinth_material():
    m = bpy.data.materials.get("pierre_socle_oranger")
    if m is None:
        m = bpy.data.materials.new("pierre_socle_oranger"); m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (0.78, 0.66, 0.50, 1); b.inputs["Roughness"].default_value = 0.8
    return m

def place_trees():
    M = master_tree()
    col = bpy.data.collections.get("AUR_13_orangers") or bpy.data.collections.new("AUR_13_orangers")
    for o in list(col.objects): bpy.data.objects.remove(o, do_unlink=True)
    Q = bpy.data.objects["PALAIS_officiel_sans_orangers"]
    bmq = bmesh.new(); bmq.from_mesh(Q.data); bmq.faces.ensure_lookup_table(); bvh = BVHTree.FromBMesh(bmq)
    for i, (x, y) in enumerate(CENTERS):
        uv = floor_uv(Q, bvh, bmq, x, y)
        if uv is not None: cover_disc(f"oranger_dallage_{i+1:02d}", x, y, uv, Q.data.materials[0], col)
        o = bpy.data.objects.new(f"oranger_{i+1:02d}", M.data)
        o.scale = M.scale; o.location = (x, y, T + M.location.z)
        o.rotation_euler = (M.rotation_euler.x, M.rotation_euler.y, math.radians(37 * i))  # variété
        col.objects.link(o)
        o.location.z += PLINTH_H
        bpy.ops.mesh.primitive_cylinder_add(vertices=48, radius=PLINTH_R, depth=PLINTH_H, location=(x, y, T + PLINTH_H / 2))
        s = bpy.context.active_object; s.name = f"oranger_socle_{i+1:02d}"
        for c in list(s.users_collection): c.objects.unlink(s)
        col.objects.link(s); s.data.materials.append(plinth_material())
    bmq.free()
    for sc in bpy.data.scenes:
        names = [c.name for c in sc.collection.children]
        if "AUR_12_palais_tripo" in names and col.name not in names:
            sc.collection.children.link(col)
    return col

if __name__ == "__main__":
    palace_without_trees(); place_trees()
