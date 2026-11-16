# Palais officiel (décidé 2026-11-15, auteur) : modèle 3D Tripo généré par l'auteur depuis
# production/refs/palace-ref-cleaned.png (palace-ref.png nettoyé), copié de
# Import/palace-tripo-test/palace-tripo-test-v2.glb vers assets/palace_official.glb.
# Il remplace, dans les scènes de plans, les blocs gris des collections AUR_10_palais et AUR_11_tour
# (gardées pour mémoire). Usage (world.blend ouvert) :
#   exec(compile(open(chemin, encoding="utf-8").read(), chemin, "exec")) ; place_palace()
# Repère Blender : X = est, Y = nord, Z = haut. Le modèle regarde déjà le sud (-Y), sol à z = 0.
import bpy
from mathutils import Vector

WIDTH = 82.8                 # largeur totale, tourelles comprises (m) — même largeur que la maquette
STAIRS_FOOT_Y = -34.0        # pied du grand escalier, inchangé (fin de SC01-SH03)
LOCAL_WIDTH, LOCAL_STAIRS_Y = 0.982, -0.2827   # mesures dans le fichier GLB (unités du fichier)
# Mesures relevées sur le modèle placé (2026-11-15, lancers de rayons) :
TERRACE_Z = 3.59             # niveau de la terrasse (cour)
FACADE_Y = -6.2              # façade sud du corps central
TERRACE_Y0 = -26.5           # bord sud de la terrasse ; l'escalier descend jusqu'à y ≈ -33.5
WING_INNER_X = 18.8          # faces intérieures des ailes (cour large de 37,6 m)
WING_OUTER_X = 36.7          # faces extérieures des ailes
WING_FRONT_Y = -26.0         # bout sud des ailes (≈ -25 à -27)
NORTH_Y = 9.5                # façade nord (tourelles arrière jusqu'à 14,5)
TOWER_HALF = 4.3             # demi-largeur de la tour ; face sud à y ≈ -6.3, centre y ≈ -2
TOP_Z = 51.3                 # sommet de la flèche

def place_palace(path="//assets/palace_official.glb"):
    coll = bpy.data.collections.get("AUR_12_palais_tripo") or bpy.data.collections.new("AUR_12_palais_tripo")
    au = bpy.data.scenes["AURELIA"]
    if coll.name not in [c.name for c in au.collection.children]: au.collection.children.link(coll)
    o = bpy.data.objects.get("PALAIS_officiel")
    if o is None:
        before = set(bpy.data.objects.keys())
        win = bpy.context.window; prev = win.scene; win.scene = au
        lc = [l for l in bpy.context.view_layer.layer_collection.children if l.name == coll.name][0]
        bpy.context.view_layer.active_layer_collection = lc
        bpy.ops.import_scene.gltf(filepath=bpy.path.abspath(path))
        win.scene = prev
        o = [bpy.data.objects[n] for n in set(bpy.data.objects.keys()) - before if bpy.data.objects[n].type == "MESH"][0]
        o.name = "PALAIS_officiel"
    s = WIDTH / LOCAL_WIDTH
    o.rotation_mode = "XYZ"; o.rotation_euler = (0, 0, 0); o.scale = (s, s, s)
    o.location = (0, STAIRS_FOOT_Y - LOCAL_STAIRS_Y * s, 0)
    return o
