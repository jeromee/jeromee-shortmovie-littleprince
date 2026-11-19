# Scène 2 du film — EXT. TERRASSE - JOUR (découpage option B, 2026-11-15, auteur) : six plans.
# Une scène Blender par plan, qui réutilise le monde maître (collections AUR_*, sans les mannequins
# de AUR_30_personnages), avec ses propres mannequins animés et sa caméra ; puis ANIMATIC enchaîne
# toutes les scènes SC01-* et SC02-*.
# Usage (world.blend ouvert) : exec(compile(open(chemin, encoding="utf-8").read(), chemin, "exec")) ; build_sc02()
# Repère Blender direct : X = est, Y = nord (le jardin est vers -Y), Z = haut. Palais officiel (Tripo,
# place_palace.py) : terrasse x -18.8..18.8, y -26.5..-6.2, dessus à z = 3.59 ; grand escalier de y = -27
# à -33.5 ; façade du corps central y = -6.2. Les blocs gris AUR_10_palais / AUR_11_tour sont exclus.
# Mannequins (animatic-workflow.md) : Elias bleu, Reine rouge, Chambellan vert, conseillers violets,
# valets lavande, fauteuils bruns, télescope cuivre. Jamais de jaune ni d'or.
import bpy, math
from mathutils import Vector

FPS = 24
T = 3.59  # niveau de la terrasse du palais officiel (place_palace.py, 2026-11-15)
COL = {"elias": (0.05, 0.25, 0.85), "queen": (0.85, 0.10, 0.10), "chamberlain": (0.10, 0.65, 0.20),
       "adviser": (0.45, 0.25, 0.60), "footman": (0.78, 0.74, 0.90), "chair": (0.45, 0.25, 0.15),
       "brass": (0.70, 0.38, 0.18), "lantern": (0.15, 0.15, 0.18)}
H = {"elias": 1.38, "queen": 1.70, "chamberlain": 1.85, "adviser": 1.75, "footman": 1.80}

def mat(key):
    name = "SC02_" + key
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*COL[key], 1)
    if m.node_tree is None: m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    if b: b.inputs["Base Color"].default_value = (*COL[key], 1); b.inputs["Roughness"].default_value = 0.8
    return m

def _mesh_obj(name, kind, size, loc, key, coll):
    bpy.ops.object.select_all(action="DESELECT") if bpy.context.mode == "OBJECT" else None
    me = bpy.data.meshes.new(name)
    import bmesh
    bm = bmesh.new()
    if kind == "box": bmesh.ops.create_cube(bm, size=1); bmesh.ops.scale(bm, vec=size, verts=bm.verts)
    elif kind == "ball": bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=size)
    elif kind == "cyl": bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=size[0], radius2=size[0], depth=size[1])
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); o.location = loc; me.materials.append(mat(key)); coll.objects.link(o)
    return o

def figure(coll, name, key, keys, face=None):
    """Mannequin : corps (boîte) + tête (sphère) sous un pivot animé. keys = [(t_s, x, y[, z])] (z = terrasse par défaut), face = [(t_s, cap_deg)]."""
    h = H[key]; piv = bpy.data.objects.new(name, None); piv.empty_display_size = 0.3; coll.objects.link(piv)
    w = 0.42 * h / 1.7
    b = _mesh_obj(name + "_corps", "box", (w, w * 0.6, h * 0.82), (0, 0, h * 0.41), key, coll); b.parent = piv
    hd = _mesh_obj(name + "_tete", "ball", 0.11 * h / 1.7, (0, 0.04, h * 0.93), key, coll); hd.parent = piv
    for k in keys:
        t, x, y = k[:3]; z = k[3] if len(k) > 3 else T
        piv.location = (x, y, z); piv.keyframe_insert("location", frame=1 + round(t * FPS))
    for t, cap in (face or [(0, 0)]):
        piv.rotation_euler = (0, 0, math.radians(cap)); piv.keyframe_insert("rotation_euler", frame=1 + round(t * FPS))
    return piv

# 2026-11-18 : après une reconstruction, lancer place_fauteuils.py, qui remplace les fauteuils provisoires
# par le fauteuil de terrasse 3D (et pose les mêmes rangées dans SC01-SH03).
def props(coll):
    """Fauteuils en deux rangées tournées vers le jardin, de part et d'autre d'une allée centrale
    (le public du « spectacle des étoiles »), télescope près de la balustrade sud, lanternes."""
    i = 0
    for y in (-21.5, -23.5):
        for x in (-10, -8, -6, -4, 4, 6, 8, 10):
            i += 1; _mesh_obj(f"fauteuil_{i}", "box", (0.8, 0.8, 1.0), (x, y, T + 0.5), "chair", coll)
    tube = _mesh_obj("telescope_tube", "cyl", (0.16, 2.0), (6.5, -25.6, T + 1.6), "brass", coll)
    tube.rotation_euler = (math.radians(-55), 0, 0)   # pointe vers le sud, vers le ciel au-dessus du jardin
    _mesh_obj("telescope_pied", "cyl", (0.05, 1.3), (6.5, -25.3, T + 0.65), "brass", coll)
    for i, (x, y) in enumerate([(-17.5, -9), (17.5, -9), (-17.5, -25.5), (17.5, -25.5)]):
        _mesh_obj(f"lanterne_{i+1}", "cyl", (0.06, 2.2), (x, y, T + 1.1), "lantern", coll)

# --- Mise en scène par plan : durée, focale, caméra [(t, pos, visée)], personnages ---
# Cap des mannequins : 0° = de face vers -Y (le jardin), 90° = vers +X (l'est)...
# Chaque t est en secondes depuis le début du plan.
SHOTS = {
    # SH01 (revu 2026-11-15, palais officiel) : depuis le côté ouest de la terrasse, en diagonale vers le
    # nord-est : façade du corps central (porte du vestibule) et aile est à droite, orangers en caisses ;
    # la Reine et sa suite traversent de gauche à droite ; Elias monte le grand escalier (à droite) et court vers elle.
    "SC02-SH01": dict(title="La terrasse", dur=6, lens=28,
        cam=[(0, (-12.5, -22.6, T + 2.2), (8.0, -7.0, T + 5.5)), (6, (-11.9, -21.9, T + 2.2), (8.0, -7.0, T + 5.5))],
        figs=[("REINE", "queen", [(0, -3.0, -13.5), (6, 3.0, -13.5)], [(0, 90)]),
              ("CONSEILLER_1", "adviser", [(0, -4.5, -12.6), (6, 1.5, -12.6)], [(0, 90)]),
              ("CONSEILLER_2", "adviser", [(0, -5.2, -14.2), (6, 0.8, -14.2)], [(0, 90)]),
              ("CONSEILLER_3", "adviser", [(0, -6.0, -13.2), (6, 0.0, -13.2)], [(0, 90)]),
              ("CHAMBELLAN", "chamberlain", [(0, -7.2, -13.9), (6, -1.2, -13.9)], [(0, 90)]),
              ("VALET_1", "footman", [(0, -7.0, -23.5), (6, -6.6, -23.5)], [(0, 0)]),
              ("VALET_2", "footman", [(0, 8.6, -21.2), (6, 8.2, -21.2)], [(0, -90)]),
              ("ELIAS", "elias", [(0, 1.8, -35.5, 0.0), (1.2, 1.7, -33.6, 0.2), (2.6, 1.6, -28.4, 3.0), (3.0, 1.6, -27.0, T), (6, 1.5, -15.5)], [(0, 180), (3.0, 175)])]),
    "SC02-SH02": dict(title="Elle sonne", dur=7, lens=35,
        cam=[(0, (-2.6, -19.8, T + 1.35), (-2.0, -14.5, T + 1.25)), (7, (5.4, -19.8, T + 1.35), (6.0, -14.5, T + 1.25))],
        figs=[("REINE", "queen", [(0, -2.0, -14.2), (7, 6.0, -14.2)], [(0, 90)]),
              ("ELIAS", "elias", [(0, -3.2, -15.5), (7, 5.0, -15.4)], [(0, 70)]),
              ("CONSEILLER_1", "adviser", [(0, -4.6, -13.4), (7, 3.4, -13.4)], [(0, 90)]),
              ("CHAMBELLAN", "chamberlain", [(0, -6.0, -14.6), (7, 2.0, -14.6)], [(0, 90)])]),
    "SC02-SH03": dict(title="Les rires", dur=4, lens=50,
        cam=[(0, (5.2, -18.6, T + 1.6), (2.4, -13.8, T + 1.55)), (4, (5.4, -18.6, T + 1.6), (2.8, -13.8, T + 1.55))],
        figs=[("CHAMBELLAN", "chamberlain", [(0, 2.0, -14.6), (4, 2.6, -14.6)], [(0, 60)]),
              ("CONSEILLER_1", "adviser", [(0, 3.4, -13.4), (4, 3.8, -13.4)], [(0, -49)]),  # revu 2026-11-17 (personnages 3D)
              ("CONSEILLER_2", "adviser", [(0, 1.0, -12.9), (4, 1.4, -12.9)], [(0, 30)]),
              ("CONSEILLER_3", "adviser", [(0, 0.6, -14.9), (4, 1.0, -14.9)], [(0, 80)])]),
    "SC02-SH04": dict(title="Elias", dur=3, lens=75,
        cam=[(0, (6.6, -18.2, T + 1.2), (5.2, -15.4, T + 1.12)), (3, (6.6, -18.1, T + 1.2), (5.2, -15.4, T + 1.12))],
        figs=[("ELIAS", "elias", [(0, 5.2, -15.4), (3, 5.2, -15.4)], [(0, 10)])]),  # revu 2026-11-17 : trois quarts face, il détourne les yeux des adultes
    "SC02-SH05": dict(title="Je ne m'en souviens pas", dur=9, lens=50,
        cam=[(0, (6.05, -17.9, T + 1.22), (7.0, -14.0, T + 1.45)), (9, (5.97, -17.72, T + 1.22), (7.0, -14.0, T + 1.45))],  # revu 2026-11-16 avec les personnages 3D : caméra à hauteur d'épaule d'Elias (1,22 m)
        figs=[("REINE", "queen", [(0, 7.0, -14.0), (9, 7.0, -14.0)], [(0, -30)]),
              ("ELIAS", "elias", [(0, 6.0, -15.6), (9, 6.0, -15.6)], [(0, 150)]),
              ("CHAMBELLAN", "chamberlain", [(0, 9.0, -13.0), (9, 9.0, -13.0)], [(0, -60)])]),
    "SC02-SH06": dict(title="Seul", dur=7, lens=28,
        cam=[(0, (0.0, -12.0, T + 9.0), (0.0, -42.0, 1.0)), (7, (0.0, -12.2, T + 9.2), (0.0, -44.0, 0.0))],
        figs=[("ELIAS", "elias", [(0, 0.5, -22.0), (2.0, 0.5, -22.0), (3.8, 0.3, -26.8)], [(0, 0)]),
              ("VALET_1", "footman", [(0, -12, -26.0), (7, -12, -26.0)], [(0, 0)])]),
}
# SH06 : Elias descend l'escalier (8 marches de 0,5 m) de t = 4 s à t = 7 s ; animé à part (z).

def _world_collections():
    return [c for c in bpy.data.collections if c.name.startswith("AUR_") and c.name not in ("AUR_90_cameras", "AUR_30_personnages", "AUR_31_persos3d", "AUR_32_persos3d_rig", "AUR_10_palais", "AUR_11_tour")]

def _remove_scene(name):
    s = bpy.data.scenes.get(name)
    if s:
        for c in list(s.collection.children):
            if c.name.startswith(name): 
                for o in list(c.objects): bpy.data.objects.remove(o, do_unlink=True)
                bpy.data.collections.remove(c)
        for o in list(s.collection.objects): bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.scenes.remove(s)

def soleil_matin():
    sun = bpy.data.objects.get("SC01_SOLEIL")
    if sun is None:
        data = bpy.data.lights.get("SC01_SOLEIL") or bpy.data.lights.new("SC01_SOLEIL", "SUN")
        sun = bpy.data.objects.new("SC01_SOLEIL", data)
        sun.data.energy = 4.0; sun.data.angle = math.radians(3); sun.data.color = (1.0, 0.93, 0.80)
        to_sun = Vector((0.80, -0.45, 0.40)).normalized()
        sun.rotation_euler = (-to_sun).to_track_quat("-Z", "Y").to_euler()
    return sun

def make_shot(name, spec, src):
    _remove_scene(name)
    sc = bpy.data.scenes.new(name)
    for c in _world_collections(): sc.collection.children.link(c)
    sc.world = src.world
    sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = int(spec["dur"] * FPS)
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.render.engine = "BLENDER_EEVEE"
    coll = bpy.data.collections.new(name + "_jeu"); sc.collection.children.link(coll)
    props(coll)
    for fname, key, keys, face in spec["figs"]:
        figure(coll, name + "_" + fname, key, keys, face)
    if name == "SC02-SH06":   # descente de l'escalier : de la terrasse (z 4) au jardin (z 0)
        e = bpy.data.objects[name + "_ELIAS"]
        for t, y, z in [(3.8, -26.8, T), (5.9, -33.6, 0.0), (6.9, -39.5, 0.0)]:
            e.location = (0.3, y, z); e.keyframe_insert("location", frame=1 + round(t * FPS))
    cam = bpy.data.objects.new(name + "_CAM", bpy.data.cameras.new(name + "_CAM"))
    cam.data.lens = spec["lens"]; cam.data.clip_start = 0.1; cam.data.clip_end = 30000
    tgt = bpy.data.objects.new(name + "_VISEE", None); tgt.empty_display_size = 0.5
    sc.collection.objects.link(cam); sc.collection.objects.link(tgt); sc.camera = cam
    tc = cam.constraints.new("TRACK_TO"); tc.target = tgt; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
    for t, pos, aim in spec["cam"]:
        f = 1 + round(t / spec["dur"] * (sc.frame_end - 1))
        cam.location = pos; cam.keyframe_insert("location", frame=f)
        tgt.location = aim; tgt.keyframe_insert("location", frame=f)
    for ob in (cam, tgt):
        if ob.animation_data and ob.animation_data.action:
            try:
                for fc in ob.animation_data.action.fcurves:
                    for kp in fc.keyframe_points: kp.interpolation = "BEZIER"; kp.easing = "AUTO"
            except Exception: pass
    sc.collection.objects.link(soleil_matin())
    return sc

def make_animatic():
    an = bpy.data.scenes.get("ANIMATIC")
    if an: bpy.data.scenes.remove(an)
    an = bpy.data.scenes.new("ANIMATIC"); an.render.fps = FPS
    an.render.resolution_x, an.render.resolution_y = 1920, 1080
    ed = an.sequence_editor_create()
    strips = ed.strips if hasattr(ed, "strips") else ed.sequences
    f = 1
    for sc in sorted([s for s in bpy.data.scenes if s.name[:2] == "SC" and "-SH" in s.name], key=lambda s: s.name):
        strips.new_scene(name=sc.name, scene=sc, channel=1, frame_start=f)
        f += sc.frame_end - sc.frame_start + 1
    an.frame_start = 1; an.frame_end = f - 1
    return an

def build_sc02():
    src = bpy.data.scenes.get("AURELIA")
    shots = [make_shot(n, s, src) for n, s in SHOTS.items()]
    an = make_animatic()
    return {s.name: s.frame_end for s in shots} | {"ANIMATIC": an.frame_end}
