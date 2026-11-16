# Scène 1 du film (découpage, option B) : trois scènes Blender, une par plan,
# qui réutilisent le monde maître (collections AUR_*) et ont chacune leur caméra animée,
# plus une scène ANIMATIC qui les enchaîne dans le monteur vidéo.
# Usage dans Blender (world.blend ouvert) :
#   exec(compile(open(chemin, encoding="utf-8").read(), chemin, "exec")) ; build_sc01()
# Idempotent : supprime et recrée les scènes SC01-SH01..03 et ANIMATIC.
# Repère : X = est, Y = nord (le jardin est vers -Y), Z = haut ; coordonnées Blender directes.
import bpy, math
from mathutils import Vector

FPS = 24
# Chaque plan : durée (s), focale (mm), clés [(temps_relatif 0..1, position caméra, point visé)]
SHOTS = {
    # SH01 et SH02 forment UNE descente continue (même trajectoire, vitesse sans à-coup à la coupe) :
    # la coupe tombe au milieu du mouvement ; SH02 reprend exactement là où SH01 s'arrête.
    "SC01-SH01": dict(title="La planète", dur=4, lens=35, path=("descente", 0)),
    "SC01-SH02": dict(title="La plongée", dur=5, lens=35, path=("descente", 96)),
    "SC01-SH03": dict(title="Le survol", dur=5, lens=28, path=("survol", 0)),
}

# Descente continue SH01+SH02 : distance au point visé interpolée en logarithme
# (vitesse perçue constante en approchant), légère accélération au départ, pas d'arrêt à la coupe.
# Départ recalé le 2026-11-14 sur la vignette retenue SC01-SH01_A (planète plus proche, vue plus plongeante).
DESCENTE = dict(frames=216, aim0=(0, -148, -104), aim1=(0, -70, 0), d0=2934.0, d1=407.0, el0=33.9, el1=27.8)

def descente_pose(g):
    P = DESCENTE; u = (g - 1) / (P["frames"] - 1)
    s = 0.5 * u + 0.5 * u * u * (3 - 2 * u)
    d = P["d0"] * (P["d1"] / P["d0"]) ** s
    el = math.radians(P["el0"] + (P["el1"] - P["el0"]) * s)
    aim = Vector(P["aim0"]).lerp(Vector(P["aim1"]), s)
    return aim + Vector((0, -d * math.cos(el), d * math.sin(el))), aim

# Survol SH03 : départ à 25 m au-dessus de l'exèdre, vol rapide qui ralentit jusqu'à l'arrêt
# devant le grand escalier (décélération continue). Trajet = courbe de Bézier quadratique.
# 2026-11-15 : jardin allongé de 40 % → départ plus au sud (au-dessus de l'exèdre déplacée), plan de 5 s.
SURVOL = dict(frames=120, p0=(0, -246, 25), p1=(0, -152, 13), p2=(0, -66, 10.5),
              aim0=(0, -127, 14), aim1=(0, -16, 9), ease=2.6)

def survol_pose(g):
    P = SURVOL; u = (g - 1) / (P["frames"] - 1)
    s = 1 - (1 - u) ** P["ease"]
    p0, p1, p2 = (Vector(P[k]) for k in ("p0", "p1", "p2"))
    pos = (1 - s) ** 2 * p0 + 2 * (1 - s) * s * p1 + s * s * p2
    return pos, Vector(P["aim0"]).lerp(Vector(P["aim1"]), s)

PATHS = {"descente": descente_pose, "survol": survol_pose}

def _world_collections():
    return [c for c in bpy.data.collections if c.name.startswith("AUR_") and c.name != "AUR_90_cameras"]

def _remove_scene(name):
    s = bpy.data.scenes.get(name)
    if s:
        for o in list(s.collection.objects): bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.scenes.remove(s)

def make_shot(name, spec, src):
    _remove_scene(name)
    sc = bpy.data.scenes.new(name)
    for c in _world_collections(): sc.collection.children.link(c)
    sc.world = src.world
    sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = int(spec["dur"] * FPS)
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.render.engine = "BLENDER_EEVEE"
    cam = bpy.data.objects.new(name + "_CAM", bpy.data.cameras.new(name + "_CAM"))
    cam.data.lens = spec["lens"]; cam.data.clip_start = 0.1; cam.data.clip_end = 30000
    tgt = bpy.data.objects.new(name + "_VISEE", None); tgt.empty_display_size = 2
    sc.collection.objects.link(cam); sc.collection.objects.link(tgt); sc.camera = cam
    tc = cam.constraints.new("TRACK_TO"); tc.target = tgt; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
    if "path" in spec:
        fn, off = PATHS[spec["path"][0]], spec["path"][1]
        for f in range(1, sc.frame_end + 1):
            pos, aim = fn(off + f)
            cam.location = pos; cam.keyframe_insert("location", frame=f)
            tgt.location = aim; tgt.keyframe_insert("location", frame=f)
    for t, pos, aim in spec.get("keys", []):
        f = 1 + round(t * (sc.frame_end - 1))
        cam.location = pos; cam.keyframe_insert("location", frame=f)
        tgt.location = aim; tgt.keyframe_insert("location", frame=f)
    sc.collection.objects.link(soleil_matin())
    return sc

def soleil_matin():
    # Soleil du matin, bas, venant de l'est-sud-est : éclaire la façade sud du palais
    # et place la serre (côté est) à contre-jour léger, comme sur l'image de concept.
    sun = bpy.data.objects.get("SC01_SOLEIL")
    if sun is None:
        data = bpy.data.lights.get("SC01_SOLEIL") or bpy.data.lights.new("SC01_SOLEIL", "SUN")
        sun = bpy.data.objects.new("SC01_SOLEIL", data)
    sun.data.energy = 4.0; sun.data.angle = math.radians(3); sun.data.color = (1.0, 0.93, 0.80)
    to_sun = Vector((0.80, -0.45, 0.40)).normalized()
    sun.rotation_euler = (-to_sun).to_track_quat("-Z", "Y").to_euler()
    return sun

def make_animatic(shots):
    _remove_scene("ANIMATIC")
    an = bpy.data.scenes.new("ANIMATIC"); an.render.fps = FPS
    an.render.resolution_x, an.render.resolution_y = 1920, 1080
    ed = an.sequence_editor_create()
    strips = ed.strips if hasattr(ed, "strips") else ed.sequences
    f = 1
    for sc in shots:
        st = strips.new_scene(name=sc.name, scene=sc, channel=1, frame_start=f)
        f += sc.frame_end - sc.frame_start + 1
    an.frame_start = 1; an.frame_end = f - 1
    return an

def build_sc01():
    src = bpy.data.scenes.get("AURELIA") or bpy.context.scene
    shots = [make_shot(n, s, src) for n, s in SHOTS.items()]
    an = make_animatic(shots)
    return {s.name: (s.frame_end, s.camera.data.lens) for s in shots} | {"ANIMATIC": an.frame_end}
