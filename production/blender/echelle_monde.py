# echelle_monde.py — réduit l'environnement d'un facteur K (0,8) en gardant les personnages et les objets
# à taille humaine à leur taille réelle (2026-11-20, décision de l'auteur : les personnages paraissaient
# trop petits sur la grande terrasse ; voir kb/decisions/0009-echelle-environnement.md).
#
# Principe : un Empty ECHELLE_MONDE à l'origine, d'échelle K, devient le parent de tous les objets sans
# parent (palais, jardin, terrain, caméras, personnages, accessoires). Tout le monde se rapproche de
# l'origine d'un facteur K, animations comprises (les clés restent en coordonnées locales). Les objets à
# taille humaine reçoivent une échelle locale 1/K autour de leur base : leur taille réelle ne change pas.
# Les vues sans personnage (vue aérienne, clairière) donnent exactement la même image qu'avant.
#
# Réversible : supprimer ECHELLE_MONDE en gardant les transformations n'est PAS l'inverse ; pour revenir
# en arrière, utiliser la copie production/blender/world_avant-echelle-0.8.blend.
# À relancer après tout script qui crée des objets (build_garden_v3.py, place_*.py, build_shots_*.py) :
# il ne touche qu'aux objets pas encore rattachés. ATTENTION : ces scripts placent leurs objets en
# coordonnées « réelles » d'avant la réduction ; c'est apply() qui les réduit ensuite.
import bpy
from mathutils import Matrix, Vector

K = 0.8
NAME = "ECHELLE_MONDE"
SKIP_COLLECTIONS = {"AUR_32_persos3d_rig"}          # maîtres (modèles 3D de référence), jamais rendus
HUMAN_KEYS = ("FAUTEUIL", "fauteuil_", "telescope", "P3D_banc", "P3D_fontaine_murale",
              "oranger_0", "oranger_socle")         # objets gardés à taille réelle (personnages : voir is_human)

def is_human(o):
    if any(k in o.name for k in HUMAN_KEYS): return True
    # personnages : Empty racine dont un descendant est un rig ou un modèle 3D de personnage
    if o.type == "EMPTY" and any(c.name.endswith(("_rig", "_3d", "_corps")) for c in o.children_recursive):
        return True
    return False

def _fcurves(action):
    if hasattr(action, "fcurves"):                    # anciennes actions
        return list(action.fcurves)
    out = []                                          # actions par calques (Blender 4.4+)
    for layer in action.layers:
        for strip in layer.strips:
            for cb in getattr(strip, "channelbags", []):
                out += list(cb.fcurves)
    return out

def animated(o):
    ad = o.animation_data
    return bool(ad and ad.action and any(fc.data_path in ("location", "rotation_euler", "rotation_quaternion")
                                         for fc in _fcurves(ad.action)))

def empty():
    E = bpy.data.objects.get(NAME)
    if E is None:
        E = bpy.data.objects.new(NAME, None); E.empty_display_size = 5
        E.scale = (K, K, K)
    for sc in bpy.data.scenes:
        if E.name not in sc.collection.objects: sc.collection.objects.link(E)
    return E

def base_point(o):
    # matrix_basis (et non matrix_world, pas à jour pour les objets des scènes inactives) : objet sans parent
    B = o.matrix_basis
    if o.type in ("MESH", "CURVE") and o.data is not None:
        bb = [B @ Vector(c) for c in o.bound_box]
        return Vector(((min(v.x for v in bb) + max(v.x for v in bb)) / 2,
                       (min(v.y for v in bb) + max(v.y for v in bb)) / 2, min(v.z for v in bb)))
    return B.translation.copy()

def apply():
    E = empty(); n = {"env": 0, "human": 0}
    tele_anchor = {o.name[len("telescope_pied"):]: base_point(o) for o in bpy.data.objects
                   if o.name.startswith("telescope_pied") and o.parent is None}
    for o in list(bpy.data.objects):
        if o is E or o.parent is not None: continue
        if any(c.name in SKIP_COLLECTIONS for c in o.users_collection): continue
        W = o.matrix_basis.copy(); hum = is_human(o); anim = animated(o)   # tout lire avant de modifier
        a = base_point(o) if hum and not anim else None
        if o.name.startswith("telescope_tube"):        # le tube grandit autour de la base du pied, pas de la sienne
            a = tele_anchor.get(o.name[len("telescope_tube"):], a)
        o.parent = E; o.matrix_parent_inverse = Matrix.Identity(4)
        if hum and anim:
            o.scale = o.scale / K                      # les clés de position restent en local : ×K en monde
        elif hum:
            o.matrix_basis = Matrix.Translation(a) @ Matrix.Scale(1 / K, 4) @ Matrix.Translation(-a) @ W
        # sinon : rien à faire, la transformation locale reste la même et le parent la réduit
        if o.type == "CAMERA" and o.data.dof.use_dof and o.data.dof.focus_object is None:
            o.data.dof.focus_distance *= K
        n["human" if hum else "env"] += 1
    return n

if __name__ == "__main__":
    print(apply())
