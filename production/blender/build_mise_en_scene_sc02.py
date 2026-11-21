import os
# build_mise_en_scene_sc02.py — scène de vérification de mise en scène de SC02 (terrasse), 2026-11-20.
# Proposition de l'auteur (« filmer une pièce de théâtre ») : toute la scène 2 jouée en continu, en temps réel
# (1 s d'animation = 1 s réelle), personnages à des positions définies, déplacements réalistes et sans collision ;
# une caméra de vérification fixe, aérienne ; une caméra par plan, active sur sa fenêtre de temps (marqueurs).
# Voir production/animatic-workflow.md (§ Mise en scène continue) et kb/decisions/0010.
#
# Scènes créées :
#   SC02_MISE_EN_SCENE : décor + personnages + caméras de plan (marqueurs liés aux caméras) ;
#   SC02_MES_VERIF     : mêmes objets + surimpressions (noms, flèches de regard, trajets, champs des caméras),
#                        caméra MES_CAM_VERIF orthographique vue de dessus.
# Coordonnées : on écrit en MÈTRES DU MONDE (après la réduction ×0,8) ; les pivots et les caméras sont rattachés
# à ECHELLE_MONDE (échelle 1/K pour les pivots), donc les clés stockées valent monde / K.
# Les surimpressions ne sont pas rattachées à ECHELLE_MONDE (contraintes en coordonnées monde) :
# ne pas relancer echelle_monde.py après ce script sans les exclure.
# Usage (world.blend ouvert) : exec(compile(open(chemin, encoding="utf-8").read(), chemin, "exec")) ; build()
import bpy, math
from mathutils import Vector

K = 0.8
FPS = 24
TZ = 3.59 * K                 # dessus de la terrasse (monde)
SC, VERIF = "SC02_MISE_EN_SCENE", "SC02_MES_VERIF"
JEU, SUR = "SC02_MES_jeu", "SC02_MES_surimpression"
T_END = 52.0

def fr(t): return 1 + round(t * FPS)
def W(x, y, z=None): return Vector((x, y, TZ if z is None else z)) / K   # monde -> local ECHELLE_MONDE

MASTERS = {"REINE": "RIG_Reine", "ELIAS": "RIG_Elias", "CHAMBELLAN": "RIG_Chambellan",
           "CONSEILLER_1": "RIG_Conseiller1", "CONSEILLER_2": "RIG_Conseiller2", "CONSEILLER_3": "RIG_Conseiller3",
           "VALET_1": "RIG_Valet", "VALET_2": "RIG_Valet"}
COLOR = {"REINE": (0.95, 0.10, 0.10), "ELIAS": (0.10, 0.40, 1.00), "CHAMBELLAN": (0.05, 0.75, 0.20),
         "CONSEILLER_1": (0.65, 0.30, 0.85), "CONSEILLER_2": (0.55, 0.20, 0.75), "CONSEILLER_3": (0.75, 0.45, 0.95),
         "VALET_1": (0.55, 0.55, 0.60), "VALET_2": (0.55, 0.55, 0.60), "CAM": (0.0, 0.85, 0.85)}
LABEL = {"REINE": "REINE", "ELIAS": "ELIAS", "CHAMBELLAN": "CHAMB.", "CONSEILLER_1": "C1",
         "CONSEILLER_2": "C2", "CONSEILLER_3": "C3", "VALET_1": "V1", "VALET_2": "V2"}

# ---------------------------------------------------------------- chrono (secondes, temps réel)
# Repères : terrasse x -15..15, y -21.2..-5 (façade, porte du vestibule en x = 0) ; buffet x -12.1..-11.1,
# y -13.5..-10.5 ; velums x ±1.6..±5, y -15.2..-19.4 (allée centrale libre |x| < 1.6) ; fauteuils y -17.2 et -18.8 ;
# orangers (±6.5, -18.9), (±12.8, -18.9), (±4, -7.1), (±12.8, -7.2) ; haut du grand escalier y = -21.6, bas y = -26.9.
DIALOGUE = [  # (début, fin, qui, texte)
    (5.0, 5.6, "ELIAS", "Maman !"),
    (7.0, 8.4, "ELIAS", "Écoute. Elle sonne."),
    (9.6, 10.8, "REINE", "Plus tard, Elias."),
    (12.8, 14.6, "CHAMBELLAN", "Son Altesse parle encore aux fleurs ?"),
    (14.6, 16.1, "", "(petits rires polis)"),
    (16.6, 18.2, "REINE", "Ce soir, pluie d'étoiles."),
    (18.4, 19.6, "REINE", "Tu seras à mes côtés."),
    (20.0, 21.0, "REINE", "Tiens-toi droit."),
    (21.4, 25.2, "CHAMBELLAN", "La dernière, c'était il y a trente ans. Votre Majesté était une enfant."),
    (25.2, 26.8, "", "(la Reine marque un temps)"),
    (26.8, 28.3, "REINE", "Je ne m'en souviens pas."),
    (28.6, 34.6, "", "(elle rentre au palais ; la cour la suit)"),
    (35.4, 41.4, "", "(Elias, seul, va vers l'allée des fauteuils)"),
    (42.6, 43.6, "", "(la clochette tinte, pour lui seul)"),
    (43.6, 48.6, "", "(il descend vers le jardin)"),
]

def Qx(t): return -9.0 + (t - 1.2)          # la Reine longe la façade vers l'est à 1 m/s (1,2 s -> 12,6 s)

# (t, x, y, z|None, cap|None) — cap 0 = face au jardin (-Y), 90 = face à l'est (+X), 180 = face au palais
BLOCKING = {
    "REINE": [
        (0.0, -9.9, -10.9, None, 270), (0.6, -9.9, -10.9, None, None), (1.2, -9.0, -10.3, None, None),
        (12.6, 2.4, -10.3, None, -141),                        # s'arrête un peu après la porte, se tourne vers C1 (dos à Elias)
        (16.0, 2.4, -10.3, None, -141), (16.4, 2.4, -10.3, None, -33),  # se tourne vers Elias
        (19.4, 2.4, -10.3, None, -33), (20.2, 2.0, -10.9, None, -32),   # s'approche : « Tiens-toi droit. »
        (25.2, 2.0, -10.9, None, -32), (25.8, 2.0, -10.9, None, 10),    # marque un temps, regard vers le jardin
        (28.6, 2.0, -10.9, None, 10),
        (28.9, 2.0, -10.9, None, None), (33.1, 0.7, -6.0, None, None), (34.6, 0.4, -4.2, None, None)],  # rentre
    "ELIAS": [
        (0.0, 1.4, -30.5, 0.0, None), (1.0, 1.4, -27.0, 0.0, None), (1.95, 1.2, -24.3, 1.44, None),
        (2.9, 1.0, -21.6, None, None), (5.0, 0.0, -15.0, None, None),            # court dans l'allée des velums
        (6.8, Qx(6.8) - 0.4, -11.4, None, None), (8.0, Qx(8.0) - 0.4, -11.4, None, None),
        (8.4, Qx(8.4) - 0.1, -11.0, None, None), (9.4, Qx(9.4) - 0.1, -11.0, None, None),  # fleur à l'oreille
        (9.8, Qx(9.8) - 0.4, -11.4, None, None), (10.8, Qx(10.8) - 0.4, -11.4, None, None),
        (11.9, 1.5, -11.7, None, 147),                                             # s'arrête, face à sa mère
        (28.8, 1.5, -11.7, None, 147), (29.3, 1.5, -11.7, None, 188),             # la regarde partir
        (34.8, 1.5, -11.7, None, 188),
        (35.4, 1.5, -11.7, None, None), (41.4, 0.4, -17.6, None, 0),             # va vers l'allée (SH06, 1re image)
        (43.6, 0.4, -17.6, None, None), (45.39, 0.24, -21.44, None, None),        # = SC02-SH06 retenu, décalé
        (47.52, 0.24, -26.88, 0.0, None), (48.52, 0.24, -31.6, 0.0, None), (52.0, 0.24, -36.0, 0.0, None)],
    "CONSEILLER_1": [
        (0.0, -10.4, -9.7, None, 200), (1.0, -10.4, -9.7, None, None), (2.4, Qx(2.4) - 1.0, -9.4, None, None),
        (12.0, Qx(12.0) - 1.0, -9.4, None, None), (12.8, 1.6, -9.3, None, 39),   # présente un registre à la Reine
        (28.4, 1.6, -9.3, None, None), (30.6, 0.9, -6.3, None, 180),               # part devant ouvrir la porte,
        (31.6, 0.9, -6.3, None, None), (32.6, 0.6, -4.2, None, None)],             # entre le premier (on la referme de l'intérieur)
        # 2026-11-21 : il ne tient plus la porte du dehors — à (1,6 ; -6,6) il était dans le pilastre à droite de la porte
    "CONSEILLER_3": [
        (0.0, -11.6, -9.8, None, 120), (1.4, -11.6, -9.8, None, None), (2.8, Qx(2.8) - 2.4, -10.0, None, None),
        (12.4, Qx(12.4) - 2.4, -10.0, None, None), (12.8, 0.0, -10.0, None, 90),
        (13.0, 0.0, -10.0, None, -55), (14.6, 0.0, -10.0, None, -55), (14.9, 0.0, -10.0, None, 41),   # écoute C., puis regarde Elias
        (16.2, 0.0, -10.0, None, 41), (16.6, 0.0, -10.0, None, 75),
        (32.0, 0.0, -10.0, None, None), (34.8, 0.2, -6.6, None, None), (36.8, 0.3, -4.2, None, None)],
    # CONSEILLER_2 (le petit rond en brocart noir) supprimé le 2026-11-21 (auteur) : il attirait l'œil au premier plan.
    "CHAMBELLAN": [
        (0.0, -10.6, -12.4, None, 0), (1.6, -10.6, -12.4, None, None), (3.4, Qx(3.4) - 3.4, -10.7, None, None),
        (12.4, Qx(12.4) - 3.4, -10.7, None, None), (13.0, -1.0, -10.7, None, 125),  # se penche vers C3 (C2 supprimé le 2026-11-21)
        (21.2, -1.0, -10.7, None, 75), (21.5, -1.0, -10.7, None, 86),              # s'adresse à la Reine
        (33.2, -1.0, -10.7, None, None), (36.7, -0.5, -6.5, None, None), (38.6, -0.2, -4.2, None, None)],
    "VALET_1": [
        (0.0, -7.2, -20.0, None, 180), (3.0, -7.2, -20.0, None, None), (4.5, -8.8, -20.0, None, 180),
        (9.0, -8.8, -20.0, None, None), (11.0, -9.6, -20.8, None, 0), (52.0, -9.6, -20.8, None, 0)],
    "VALET_2": [
        (0.0, 8.0, -16.3, None, 0), (2.5, 8.0, -16.3, None, None), (3.8, 9.6, -16.3, None, 0),
        (8.0, 9.6, -16.3, None, None), (9.0, 10.8, -16.4, None, None), (11.6, 10.6, -19.8, None, None),
        (13.6, 8.8, -20.0, None, 180), (52.0, 8.8, -20.0, None, 180)],
}
HIDE = {"CONSEILLER_1": 32.6, "REINE": 34.6, "CONSEILLER_3": 36.8, "CHAMBELLAN": 38.6}

# ---------------------------------------------------------------- porte du vestibule (2026-11-21)
# La porte du modèle Tripo est fermée et fait partie du maillage : deux battants et un fond sombre, visibles seulement quand
# elle est ouverte. Ouverture vers la terrasse (les battants se rabattent entre l'encadrement et les pilastres).
# Mesures (lancer de rayons) : surface de la porte y = -5,20, poignées jusqu'à -5,26 (la terrasse est du côté des y plus petits), ouverture x -1,2..1,2, cintre à ≈ 3,3 m.
DOOR = dict(y=-5.56, half=1.2, h_rect=2.15, open_t=(30.6, 31.6), close_t=(39.0, 39.8), angle=100)

# ---------------------------------------------------------------- caméras de plan
# (nom, début, fin, focale, [(t, position, visée)]) — monde ; SH06 = caméra du plan retenu, recopiée image par image
SHOTS = [
    ("SH01", 0.0, 6.8, 30, [(0.0, (13.8, -20.6, TZ + 7.0), (-4.0, -9.8, TZ + 1.0)),
                            (3.4, (8.5, -14.2, TZ + 3.6), (Qx(3.4), -10.2, TZ + 1.2)),      # passe au nord du velum est
                            (6.8, (3.5, -13.6, TZ + 1.8), (Qx(6.8), -10.4, TZ + 1.4))]),
    # SH02 commence quand Elias a rejoint sa mère (6,8 s) : avant, il arrive du sud-est et passerait de gauche à droite de l'écran
    ("SH02", 6.8, 12.2, 35, [(6.8, (Qx(6.8) - 0.2, -14.6, TZ + 1.2), (Qx(6.8) - 0.2, -10.8, TZ + 1.15)),
                             (12.2, (1.8, -14.6, TZ + 1.2), (1.8, -10.8, TZ + 1.15))]),
    ("SH03", 12.2, 15.0, 45, [(12.2, (-0.6, -14.4, TZ + 1.5), (-0.3, -10.5, TZ + 1.5)),
                              (15.0, (-0.45, -14.0, TZ + 1.5), (-0.3, -10.5, TZ + 1.5))]),
    # SH04 et SH05 : champ-contrechamp, les deux caméras à l'est de la ligne Elias-Reine (règle des 180°)
    ("SH04", 15.0, 16.8, 75, [(15.0, (2.9, -10.0, TZ + 1.15), (1.5, -11.7, TZ + 1.15)),   # par-dessus l'épaule de la Reine
                              (16.8, (2.85, -10.1, TZ + 1.15), (1.5, -11.7, TZ + 1.15))]),
    ("SH05", 16.8, 28.8, 40, [(16.8, (2.4, -12.9, TZ + 1.35), (2.05, -10.4, TZ + 1.5)),   # par-dessus l'épaule d'Elias
                              (20.2, (2.38, -12.85, TZ + 1.35), (1.7, -10.6, TZ + 1.5)),   # suit le pas de la Reine
                              (28.8, (2.35, -12.7, TZ + 1.35), (1.7, -10.6, TZ + 1.5))]),
    ("SH06a", 28.8, 41.6, 35, [(28.8, (0.6, -18.6, TZ + 1.3), (1.0, -9.5, TZ + 1.5)),
                               (35.0, (0.6, -18.6, TZ + 1.3), (1.0, -9.5, TZ + 1.5)),
                               (41.4, (0.5, -19.9, TZ + 1.2), (0.45, -17.6, TZ + 1.1))]),
    ("SH06", 41.6, 48.6, None, "SC02-SH06"),
]

# ---------------------------------------------------------------- outils
def _fcurves(action):
    if hasattr(action, "fcurves"): return list(action.fcurves)
    out = []
    for layer in action.layers:
        for strip in layer.strips:
            for cb in getattr(strip, "channelbags", []): out += list(cb.fcurves)
    return out

def mat(name, rgb):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1)
    if m.node_tree is None: m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    if b: b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Emission Color"].default_value = (*rgb, 1); b.inputs["Emission Strength"].default_value = 0.6
    return m

def heading(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    return None if math.hypot(dx, dy) < 0.05 else math.degrees(math.atan2(dx, -dy))

def unwrap(prev, a):
    while a - prev > 180: a -= 360
    while a - prev < -180: a += 360
    return a

def animate_pivot(piv, keys):
    for t, x, y, z, cap in keys:
        piv.location = W(x, y, z); piv.keyframe_insert("location", frame=fr(t))
    n = len(keys); seg = [heading(keys[i][1:3], keys[i + 1][1:3]) for i in range(n - 1)]
    cur = keys[0][4] if keys[0][4] is not None else next((s for s in seg if s is not None), 0)
    rot = []
    for i, (t, x, y, z, cap) in enumerate(keys):
        cin = seg[i - 1] if i > 0 and seg[i - 1] is not None else cur
        if i < n - 1 and seg[i] is not None: cout = seg[i]
        elif cap is not None: cout = cap
        else: cout = cin
        d_in = min(0.3, (t - keys[i - 1][0]) / 2) if i > 0 else 0
        d_out = min(0.3, (keys[i + 1][0] - t) / 2) if i < n - 1 else 0
        rot += [(t - d_in, cin), (t + d_out, cout)]
        cur = cout
    prev = None
    for t, a in rot:
        a = a if prev is None else unwrap(prev, a); prev = a
        piv.rotation_euler = (0, 0, math.radians(a)); piv.keyframe_insert("rotation_euler", index=2, frame=fr(t))
    for fc in _fcurves(piv.animation_data.action):      # vitesse constante entre deux clés
        for k in fc.keyframe_points: k.interpolation = "LINEAR"

def key_hidden(objs, t_hide):
    for o in objs:
        for f, v in ((1, False), (fr(t_hide) - 1, False), (fr(t_hide), True)):
            o.hide_render = v; o.hide_viewport = v
            o.keyframe_insert("hide_render", frame=f); o.keyframe_insert("hide_viewport", frame=f)

def _remove_scene(name):
    s = bpy.data.scenes.get(name)
    if s: bpy.data.scenes.remove(s)

def _clear_collection(name):
    c = bpy.data.collections.get(name)
    if c:
        for o in list(c.all_objects): bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c)
    return bpy.data.collections.new(name)

def _copy_rig(master, coll, name):
    A = master.copy(); A.name = name + "_rig"; A.animation_data_clear(); coll.objects.link(A)
    meshes = []
    for m in [c for c in master.children if c.type == "MESH"]:
        M = m.copy(); M.name = name + "_3d"; coll.objects.link(M)
        M.parent = A; M.matrix_parent_inverse = m.matrix_parent_inverse.copy()
        for mod in M.modifiers:
            if mod.type == "ARMATURE": mod.object = A
        meshes.append(M)
    return A, meshes

def text_obj(name, body, size, rgb, coll):
    cu = bpy.data.curves.new(name, "FONT"); cu.body = body; cu.size = size; cu.align_x = "CENTER"; cu.align_y = "CENTER"
    o = bpy.data.objects.new(name, cu); o.data.materials.append(mat("MES_" + name, rgb)); coll.objects.link(o)
    return o

def poly_curve(name, pts, rgb, coll, bevel=0.06, cyclic=False):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = bevel
    sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts): p.co = (*q, 1)
    sp.use_cyclic_u = cyclic
    o = bpy.data.objects.new(name, cu); o.data.materials.append(mat("MES_" + name, rgb)); coll.objects.link(o)
    return o

# ---------------------------------------------------------------- construction
def build():
    prefs = bpy.context.preferences.edit
    old_interp = prefs.keyframe_new_interpolation_type
    src = bpy.data.scenes["SC02-SH01"]
    E = bpy.data.objects["ECHELLE_MONDE"]
    for n in (SC, VERIF): _remove_scene(n)
    jeu, sur = _clear_collection(JEU), _clear_collection(SUR)
    sc = bpy.data.scenes.new(SC); ve = bpy.data.scenes.new(VERIF)
    for s in (sc, ve):
        for c in src.collection.children:
            if not c.name.endswith("_jeu"): s.collection.children.link(c)
        s.collection.children.link(jeu)
        s.world = src.world; s.render.fps = FPS; s.frame_start = 1; s.frame_end = fr(T_END)
        for o in src.collection.objects:          # ECHELLE_MONDE, soleil...
            if o.name not in s.collection.objects: s.collection.objects.link(o)
    ve.collection.children.link(sur)
    # accessoires de la terrasse (copies liées de SC02-SH01)
    for o in bpy.data.collections["SC02-SH01_jeu"].objects:
        if o.parent == E and o.type == "MESH" and (o.name.startswith("SC02-SH01_FAUTEUIL_") or o.name.startswith("lanterne_")):
            c = o.copy(); c.name = "MES_" + o.name.replace("SC02-SH01_", ""); jeu.objects.link(c)
    # télescope : modèle Tripo (planche telescope-sheet_v3_gpt26_nb2, 2026-11-21), objectif vers le sud (le ciel du jardin)
    tel = bpy.data.objects["TELESCOPE_terrasse"].copy(); tel.name = "MES_telescope"; jeu.objects.link(tel)
    tel.parent = E; tel.matrix_parent_inverse.identity(); tel.scale = (1 / K,) * 3; tel.location = W(5.2, -20.2)
    # personnages
    prefs.keyframe_new_interpolation_type = "LINEAR"
    pivots = {}
    for key, keys in BLOCKING.items():
        piv = bpy.data.objects.new("MES_" + key, None); piv.empty_display_size = 0.4; jeu.objects.link(piv)
        piv.parent = E; piv.matrix_parent_inverse.identity(); piv.scale = (1 / K,) * 3
        animate_pivot(piv, keys); pivots[key] = piv
        master = bpy.data.objects[MASTERS[key]]
        A, meshes = _copy_rig(master, jeu, "MES_" + key)
        A.parent = piv; A.matrix_parent_inverse.identity()
        A.location = (0, 0, master.location.z); A.rotation_euler = master.rotation_euler.copy(); A.scale = master.scale.copy()
        # surimpressions : flèche de regard (enfant du pivot), nom (suit le pivot), trajet complet
        me = bpy.data.meshes.new("MES_fleche_" + key)
        me.from_pydata([(0, -1.0, 0), (-0.55, 0.4, 0), (0, 0.05, 0), (0.55, 0.4, 0)], [], [(0, 1, 2), (0, 2, 3)])
        ar = bpy.data.objects.new("MES_fleche_" + key, me); ar.data.materials.append(mat("MES_c_" + key, COLOR[key]))
        sur.objects.link(ar); ar.parent = piv; ar.location = (0, 0, 2.6)
        lb = text_obj("MES_nom_" + key, LABEL[key], 0.55, COLOR[key], sur)
        cl = lb.constraints.new("COPY_LOCATION"); cl.target = piv; cl.use_offset = True
        lb.location = (0, 1.1, 2.8)
        if key in HIDE: key_hidden(meshes + [ar, lb], HIDE[key])
    prefs.keyframe_new_interpolation_type = "BEZIER"
    # trajets (échantillonnés sur les courbes d'animation)
    for key, piv in pivots.items():
        fcs = {(fc.data_path, fc.array_index): fc for fc in _fcurves(piv.animation_data.action)}
        t_stop = HIDE.get(key, T_END); pts = []
        t = 0.0
        while t <= t_stop + 1e-6:
            f = fr(t); p = Vector([fcs[("location", i)].evaluate(f) for i in range(3)]) * K
            pts.append((p.x, p.y, p.z + 0.04)); t += 0.2
        poly_curve("MES_trajet_" + key, pts, COLOR[key], sur, bevel=0.05 if key != "ELIAS" else 0.08)
    # porte du vestibule : fond sombre cintré + deux battants
    import bmesh
    def _mesh(name, verts, faces, rgb):
        me = bpy.data.meshes.new(name); me.from_pydata(verts, [], faces)
        o = bpy.data.objects.new(name, me); o.data.materials.append(mat("MES_" + name, rgb)); jeu.objects.link(o)
        o.parent = E; o.matrix_parent_inverse.identity(); o.scale = (1 / K,) * 3
        return o
    D = DOOR; hw = D["half"]; hr = D["h_rect"]
    arch = [(hw * math.cos(math.pi * i / 12), 0, hr + hw * math.sin(math.pi * i / 12)) for i in range(13)]
    fond = _mesh("MES_porte_fond", [(-hw, 0, 0), (hw, 0, 0)] + arch, [tuple([0, 1] + list(range(2, 15)))], (0.035, 0.028, 0.022))
    fond.location = W(0, -5.27)                    # juste devant la porte fermée du modèle Tripo
    # battants : modèle Tripo de la porte (planche vestibule-door, 2026-11-21) coupé en deux, pivot sur les gonds
    # (maîtres PORTE_VESTIBULE_battant_ouest|est de AUR_34_accessoires_maitres, en mètres réels, face vers -Y)
    leaves = []
    for side, sgn in (("ouest", 1), ("est", -1)):
        lf = bpy.data.objects["PORTE_VESTIBULE_battant_" + side].copy(); lf.name = "MES_porte_battant_" + side
        jeu.objects.link(lf); lf.parent = E; lf.matrix_parent_inverse.identity(); lf.scale = (1 / K,) * 3
        lf.location = W(-sgn * hw, D["y"]); leaves.append((lf, sgn))
    (o0, o1), (c0, c1) = D["open_t"], D["close_t"]
    for lf, sgn in leaves:
        for t, a in ((o0, 0), (o1, -sgn * D["angle"]), (c0, -sgn * D["angle"]), (c1, 0)):
            lf.rotation_euler = (0, 0, math.radians(a)); lf.keyframe_insert("rotation_euler", index=2, frame=fr(t))
    for o in [fond]:                               # les battants restent toujours visibles (porte fermée = Tripo + battants)
        for f, v in ((1, True), (fr(o0), False), (fr(c1), True)):
            o.hide_render = v; o.hide_viewport = v
            o.keyframe_insert("hide_render", frame=f); o.keyframe_insert("hide_viewport", frame=f)
    # caméras de plan
    cams = []
    for name, t0, t1, lens, spec in SHOTS:
        cam = bpy.data.objects.new("MES_CAM_" + name, bpy.data.cameras.new("MES_CAM_" + name))
        cam.data.clip_start = 0.1; cam.data.clip_end = 30000; cam.data.sensor_width = 36
        tgt = bpy.data.objects.new("MES_CAM_" + name + "_VISEE", None); tgt.empty_display_size = 0.3
        for o in (cam, tgt): jeu.objects.link(o); o.parent = E; o.matrix_parent_inverse.identity()
        tc = cam.constraints.new("TRACK_TO"); tc.target = tgt; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
        if isinstance(spec, str):                          # recopie image par image d'un plan existant
            s6 = bpy.data.scenes[spec]; c6 = bpy.data.objects[spec + "_CAM"]; v6 = bpy.data.objects[spec + "_VISEE"]
            win = bpy.context.window; keep = win.scene; win.scene = s6
            for f in range(s6.frame_start, s6.frame_end + 1):
                s6.frame_set(f); ff = fr(t0) + f - s6.frame_start
                cam.location = c6.location.copy(); tgt.location = v6.location.copy(); cam.data.lens = c6.data.lens
                cam.keyframe_insert("location", frame=ff); tgt.keyframe_insert("location", frame=ff); cam.data.keyframe_insert("lens", frame=ff)
            win.scene = keep; lens_draw = 40
        else:
            cam.data.lens = lens; lens_draw = lens
            for t, pos, aim in spec:
                cam.location = W(*pos); tgt.location = W(*aim)
                cam.keyframe_insert("location", frame=fr(t)); tgt.keyframe_insert("location", frame=fr(t))
        m = sc.timeline_markers.new(name, frame=fr(t0)); m.camera = cam
        if t0 == 0: sc.camera = cam
        # champ de la caméra vu de dessus (visible pendant son plan)
        L = 9.0; w = L * 18 / lens_draw
        wd = poly_curve("MES_champ_" + name, [(0, 0, 0), (-w, L, 0), (w, L, 0), (0, 0, 0)], COLOR["CAM"], sur, bevel=0.07)
        c1 = wd.constraints.new("COPY_LOCATION"); c1.target = cam; c1.use_z = False
        c2 = wd.constraints.new("LOCKED_TRACK"); c2.target = tgt; c2.track_axis = "TRACK_Y"; c2.lock_axis = "LOCK_Z"
        wd.location.z = TZ + 2.4
        lab = text_obj("MES_nomcam_" + name, name, 0.9, COLOR["CAM"], sur)
        c3 = lab.constraints.new("COPY_LOCATION"); c3.target = cam; c3.use_z = False; c3.use_offset = True
        lab.location = (0, -1.0, TZ + 2.6)
        for o in (wd, lab):
            for f, v in ((1, True), (fr(t0), False), (fr(t1), True)):
                if f == 1 and t0 == 0: v = False
                o.hide_render = v; o.hide_viewport = v
                o.keyframe_insert("hide_render", frame=f); o.keyframe_insert("hide_viewport", frame=f)
        cams.append(cam)
    # caméra de vérification : vue de dessus orthographique
    vc = bpy.data.objects.new("MES_CAM_VERIF", bpy.data.cameras.new("MES_CAM_VERIF"))
    vc.data.type = "ORTHO"; vc.data.ortho_scale = 30; vc.data.clip_end = 400   # 30 m de côté (l'échelle du parent n'agit pas)
    sur.objects.link(vc); vc.parent = E; vc.matrix_parent_inverse.identity(); vc.location = W(0, -13.5, 70)
    ve.camera = vc
    # rendu : plans (EEVEE) et vérification (Workbench)
    for s, eng, rx, ry in ((sc, "BLENDER_EEVEE", 960, 540), (ve, "BLENDER_WORKBENCH", 1080, 1080)):
        s.render.engine = eng; s.render.resolution_x, s.render.resolution_y = rx, ry; s.render.resolution_percentage = 100
    ve.display.shading.light = "STUDIO"; ve.display.shading.color_type = "TEXTURE"; ve.display.shading.show_shadows = False
    ve.view_settings.view_transform = "Standard"; ve.view_settings.exposure = 0.8
    for a in ("view_transform", "look", "exposure"): setattr(sc.view_settings, a, getattr(src.view_settings, a))
    try: sc.eevee.taa_render_samples = 16
    except Exception: pass
    # conseillers : posture naturelle, carnet et crayon en main (pose_conseillers.py, 2026-11-21)
    _pc = os.path.join(os.path.dirname(bpy.data.filepath), "pose_conseillers.py") if bpy.data.filepath else None
    if _pc and os.path.exists(_pc):
        _ns = {"__name__": "pose_conseillers"}; exec(compile(open(_pc, encoding="utf-8").read(), _pc, "exec"), _ns)
        _ns["apply"](sc.name)
    return {"frames": sc.frame_end, "cams": [c.name for c in cams]}
