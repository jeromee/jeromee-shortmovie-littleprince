"""Pose le velum et la table de rafraichissements sur la terrasse (soiree d'observation).
A lancer dans world.blend APRES echelle_monde.py : les objets sont rattaches a ECHELLE_MONDE
et dimensionnes en metres reels du monde final (objets a taille humaine, comme les fauteuils).
Masters importes dans la scene TEST_TRIPO : MASTER_velum_tripo, MASTER_table_tripo.
Les positions VELUMS / TABLE_C sont en coordonnees MONDE (deja x0,8)."""
import bpy, math
from mathutils import Vector, Matrix

# Deux velums de part et d'autre de l'allee centrale, au-dessus des paires interieures de fauteuils :
# l'allee reste libre (SC02-SH06 : Elias doit y rester visible depuis la camera haute).
# Version a un seul velum central : place_terrasse_velum-central.py.txt
VELUMS = [("P3D_velum_terrasse_ouest", (-3.3, -17.3)), ("P3D_velum_terrasse_est", (3.3, -17.3))]
VELUM_DIM = (3.4, 4.2, 3.2)   # largeur (x) x profondeur (y) x hauteur, metres reels
TABLE_C = (-11.6, -12.0)      # cote ouest, entre les orangers 05 et 07, a l'ouest du groupe de la cour
TABLE_LEN = 3.0               # longueur reelle ; le reste suit les proportions du modele
TABLE_W = 1.0
TABLE_ROTZ = 0.0              # modele : grand axe deja selon y (nord-sud)
COLL = "AUR_14_terrasse_soiree"
T_PRE = 3.59                  # niveau de la terrasse, coordonnees pre-echelle

def scenes_with_chairs():
    return [s for s in bpy.data.scenes if not s.name.startswith("TEST") and any("FAUTEUIL" in o.name for o in s.objects)]

def bbox(o):
    pts = [Vector(c) for c in o.bound_box]
    mn = Vector((min(p.x for p in pts), min(p.y for p in pts), min(p.z for p in pts)))
    mx = Vector((max(p.x for p in pts), max(p.y for p in pts), max(p.z for p in pts)))
    return mn, mx

def terrace_z(dg, sc, x, y):
    r = sc.ray_cast(dg, Vector((x, y, 30)), Vector((0, 0, -1)))
    return r[1].z if r[0] else None

def place(master, name, center, scale, rotz, coll, E, sc, dg):
    o = bpy.data.objects.get(name)
    if o is None:
        o = bpy.data.objects.new(name, master.data); coll.objects.link(o)
    mn, mx = bbox(master)
    c_loc = Vector(((mn.x+mx.x)/2, (mn.y+mx.y)/2, mn.z))   # centre du pied, repere modele
    z = (E.matrix_world @ Vector((0, 0, T_PRE))).z   # sol de la terrasse (un rayon toucherait les fauteuils)
    W = (Matrix.Translation((center[0], center[1], z)) @ Matrix.Rotation(math.radians(rotz), 4, 'Z')
         @ Matrix.Diagonal((*scale, 1.0)) @ Matrix.Translation(-c_loc))
    o.rotation_mode = "XYZ"
    o.parent = E; o.matrix_parent_inverse = Matrix.Identity(4)
    o.matrix_basis = E.matrix_world.inverted() @ W
    return o, z

def apply():
    E = bpy.data.objects["ECHELLE_MONDE"]
    coll = bpy.data.collections.get(COLL) or bpy.data.collections.new(COLL)
    targets = scenes_with_chairs()
    for s in targets:
        if coll.name not in s.collection.children: s.collection.children.link(coll)
    sc = bpy.data.scenes["SC02-SH01"]; bpy.context.window.scene = sc
    for o in coll.objects: o.hide_viewport = o.hide_render = True
    dg = bpy.context.evaluated_depsgraph_get()
    vm = bpy.data.objects["MASTER_velum_tripo"]; tm = bpy.data.objects["MASTER_table_tripo"]
    mn, mx = bbox(vm); d = mx - mn
    old = bpy.data.objects.get("P3D_velum_terrasse")
    if old: bpy.data.objects.remove(old)
    vs = [place(vm, nm, c, (VELUM_DIM[0]/d.x, VELUM_DIM[1]/d.y, VELUM_DIM[2]/d.z), 0.0, coll, E, sc, dg) for nm, c in VELUMS]
    zv = vs[0][1]
    mn, mx = bbox(tm); d = mx - mn
    k = TABLE_LEN / d.y
    t, zt = place(tm, "P3D_table_rafraichissements", TABLE_C, (TABLE_W/d.x, k, k), TABLE_ROTZ, coll, E, sc, dg)
    for o in [x[0] for x in vs] + [t]: o.hide_viewport = o.hide_render = False
    return {"scenes": [s.name for s in targets], "z": (round(zv, 3), round(zt, 3)), "table_h": round(d.z*k, 2)}
