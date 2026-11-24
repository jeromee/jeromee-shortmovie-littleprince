import os, json
# build_mise_en_scene_sc03.py — mise en scène continue de SC03 (le grand massif, la Rose). v1 2026-11-22 matin ; v2 2026-11-22 soir ; v3 2026-11-23.
# Même méthode que SC02 (kb/decisions/0010) : toute la scène jouée en continu, 1 s d'animation = 1 s réelle ;
# trajets sans collision (contrôle par check()) ; caméra de vérification vue de dessus ; une caméra par plan (marqueurs).
# Chrono, plans et remarques : production/mise-en-scene/SC03.md.
# v2 (remarques de l'auteur) : plan de situation en plongée au début (Elias au loin, les jardiniers prêts à partir) ;
# plus d'ellipse : les jardiniers s'arrêtent près du banc et soulèvent leur chapeau quand Elias passe l'arche ;
# massif à sa vraie hauteur, passage de pas japonais jusqu'à un rond de mousse au pied de la Rose (clairiere_v2.py) :
# Elias s'y agenouille à 0,6 m d'elle ; végétation au sud (rosiers sur le muret de l'exèdre, arbustes, arbres).
# v3 (2026-11-23, auteur) : Elias arrive EN COURANT (dépité) jusqu'à l'arche, ralentit autour du massif et se laisse tomber sur
# la bordure (≈ 9 s gagnées) ; Rose à fleur de 13 cm (rose_13cm.py) ; dialogue redécoupé : plan à deux en orbite horaire au début
# (SH06), puis champ / contrechamp aux tiers opposés (la Rose sur le tiers gauche, Elias sur le tiers droit), repère d'échelle.
#
# Scènes créées : SC03_MISE_EN_SCENE (décor + personnages + caméras de plan) et SC03_MES_VERIF (surimpressions, vue de dessus).
# Coordonnées en MÈTRES DU MONDE (après la réduction ×0,8). Pivots et caméras rattachés à ECHELLE_MONDE.
# Provisoire : la Rose, les jardiniers, la brouette et le râteau sont des volumes simples ; Elias est le modèle riggé.
# build() écrit aussi production/animatic/mise-en-scene/SC03_chrono.json (plans, répliques, décalages) pour compose_verification_sc03.py.
# Usage (world.blend ouvert) : exec(compile(open(chemin, encoding="utf-8").read(), chemin, "exec")) ; build() ; check()
import bpy, math
from mathutils import Vector, Matrix

K = 0.8
FPS = 24
GZ = 0.08                     # sol du parvis du massif (monde)
MZ = 0.25                     # dessus du rond de mousse (monde) ; dalles : 0,28
DZ = 0.28
SC, VERIF = "SC03_MISE_EN_SCENE", "SC03_MES_VERIF"
JEU, SUR = "SC03_MES_jeu", "SC03_MES_surimpression"
P = "MES3_"
ROSE_XY = (0.0, -173.92)      # centre du massif = la Rose

def fr(t): return 1 + round(t * FPS)
def W(x, y, z=None): return Vector((x, y, GZ if z is None else z)) / K

COLOR = {"ELIAS": (0.10, 0.40, 1.00), "ROSE": (1.0, 0.85, 0.10), "JARDINIER_1": (0.55, 0.35, 0.18),
         "JARDINIER_2": (0.40, 0.45, 0.20), "CAM": (0.0, 0.85, 0.85)}
LABEL = {"ELIAS": "ELIAS", "ROSE": "ROSE", "JARDINIER_1": "J1", "JARDINIER_2": "J2"}

def route(t0, pts, speed, z=None):
    """Clés (t, x, y, z, None) à vitesse constante le long de pts ; pts peut contenir (x, y) ou (x, y, z)."""
    p0 = pts[0]; out, t = [(t0, p0[0], p0[1], p0[2] if len(p0) > 2 else z, None)], t0
    for a, b in zip(pts, pts[1:]):
        t += math.dist(a[:2], b[:2]) / speed; out.append((round(t, 2), b[0], b[1], b[2] if len(b) > 2 else z, None))
    return out

# ---------------------------------------------------------------- repères (monde)
# Massif : centre (0 ; -173,92), bordure r ≈ 2,6 m (dessus à 0,40 m), rosiers 0,7–0,9 m. Passage de dalles à l'azimut -70°
# (sud-sud-est) ; rond de mousse r ≈ 0,52 m. Banc (-2,5 ; -169,9), fontaine murale (5 ; -172), arche (2,05 ; -167,9).
# Allée au nord de l'arche (axe relevé sur allee_sinueuse) : (2,6 ; -165) (1,7 ; -162) (0 ; -158) (-2,8 ; -154) (-6 ; -150).
U = (math.cos(math.radians(-70)), math.sin(math.radians(-70)))          # direction du passage, depuis la Rose
def AZ(d, z=None): return (ROSE_XY[0] + d * U[0], ROSE_XY[1] + d * U[1]) + ((z,) if z is not None else ())
KNEEL = AZ(0.92, DZ)                                                     # à genoux au bord de la mousse, genoux sur la première dalle :
                                                                         # visage à ≈ 0,40 m de la fleur (demande de l'auteur, 2026-11-22 soir ; 0,14 m avant) ; 0,92 m depuis le modèle de la Rose
KNEEL_CAP = -160                                                         # face à la Rose

# Jardiniers : prêts à partir dans l'exèdre (0–5 s, J2 met les dernières feuilles dans la brouette) ; ils partent par l'ouest
# du massif, s'arrêtent près du banc en voyant venir le prince, soulèvent leur chapeau quand il passe l'arche, puis sortent.
G_IN = [(-4.3, -175.8), (-3.4, -172.4), (-1.6, -171.15), (-0.6, -170.6)]
G_OUT = [(-0.6, -170.6), (1.0, -169.7), (2.0, -168.0), (3.0, -165.0), (3.3, -162.3), (2.6, -159.3), (0.8, -157.4),
         (-1.1, -156.0), (-2.8, -154.0)]
G_GO, G_RESUME = 0.4, 9.8           # v3 : départ presque immédiat (Elias arrive en courant), reprise après son passage
J1 = [(0.0, -4.3, -175.8, None, 20)] + route(G_GO, G_IN, 1.1) + route(G_RESUME, G_OUT, 1.0)   # arrêt près du banc
G2_IN = [(-4.71, -177.35)] + G_IN[:-1] + [(-1.98, -171.41)]
J2 = [(0.0, -4.71, -177.35, None, 60)] + route(0.2, G2_IN, 1.15) + route(G_RESUME + 0.6, [(-1.98, -171.41), (-0.6, -170.6)] + G_OUT[1:], 1.0)
HATS = (7.0, 7.5, 8.8, 9.4)              # chapeau soulevé (pendant qu'Elias passe l'arche en courant), puis remis

# Elias (v3) : au loin dans l'allée au début (plan de situation), il arrive EN COURANT (2,9 m/s, vitesse d'enfant de SC02),
# passe l'arche à ≈ 7,5 s, ralentit en contournant le massif par l'est (2,1 puis 1,4, 1,1 et 0,95 m/s : il a couru, il est
# dépité, il donne un coup de pied dans le gravier) et se laisse tomber sur la bordure sud, face au muret de l'exèdre.
def _chain(t0, legs):
    out = []
    for pts, v in legs:
        r = route(t0, pts, v); out += r if not out else r[1:]; t0 = r[-1][0]
    return out
E_WALK = _chain(0.0, [([(-6.0, -150.0), (-4.4, -152.0), (-2.8, -154.0), (-1.1, -156.0), (0.8, -157.4), (2.6, -159.3), (3.3, -162.3),
                        (3.0, -165.0), (2.0, -168.0)], 2.9),
                      ([(2.0, -168.0), (3.45, -172.6)], 2.1), ([(3.45, -172.6), (2.9, -175.9)], 1.4),
                      ([(2.9, -175.9), AZ(3.1)], 1.0)])
# v4 (2026-11-23, soir, auteur) : il s'assied au bord sud-sud-est du massif, à l'entrée du passage de dalles, dos à la Rose ;
# quand il se lève et se retourne vers elle (par l'ouest), les caméras de l'ouest voient son visage.
E_T = {(round(k[1], 2), round(k[2], 2)): k[0] for k in E_WALK}       # heure de passage à chaque point
T_ARR = E_WALK[-1][0]
# Tout ce qui suit l'arrivée garde le minutage validé de la v1 (« temps v1 ») : S1 jusqu'à l'éveil de la Rose ;
# S2 ensuite, qui ajoute le temps de marcher sur les dalles jusqu'à elle (3,9 s).
SHIFT1 = round(T_ARR - 32.84, 2)
SHIFT2 = round(SHIFT1 + 3.9, 2)
# v5 (2026-11-23, nuit, auteur) : la Rose ne tourne plus sur elle-même (elle fait déjà face au passage) ; les 2,8 s où elle
# tournait (temps v1 42,4–45,2) sont supprimées : elle s'éveille dès qu'Elias a fini de chercher qui a parlé.
CUT0, CUT1 = 42.4, 45.2
CUT = round(CUT1 - CUT0, 2)
def S(t):
    if t <= CUT0: return round(t + SHIFT1, 2)
    if t < CUT1: return round(CUT0 + SHIFT1, 2)
    return round(t + (SHIFT1 if t < 47.5 else SHIFT2) - CUT, 2)
T_END = S(107.0)
# marche sur les dalles (temps v1 + S1) : de W0 à W1, puis il s'agenouille (0,8 s) ; sa première réplique tombe à S(49,4)
W0 = round(47.6 + SHIFT1 - CUT, 2)
SEAT = AZ(2.54)                          # assis sur la bordure, à l'entrée du passage
UP = AZ(3.1)                             # debout devant la bordure, à l'entrée du passage
SEAT_CAP, FACE_CAP = 20, 200             # dos à la Rose (vers le sud-sud-est) ; face à elle (nord-nord-ouest)
WALK_IN = route(W0, [UP + (GZ,), AZ(2.95, GZ), AZ(2.22 * K, DZ), AZ(1.62 * K, DZ), KNEEL], 0.75)   # bordure, trois dalles, mousse
W1 = WALK_IN[-1][0]

BLOCKING = {
    "JARDINIER_1": J1,
    "JARDINIER_2": J2,
    "ELIAS": E_WALK + [
        (S(33.39), *UP, None, SEAT_CAP),                                   # se tourne dos au massif
        (S(33.5), *UP, None, SEAT_CAP), (S(34.3), *SEAT, None, SEAT_CAP),  # se laisse tomber (recule sur la bordure)
        (S(39.7), *SEAT, None, SEAT_CAP), (S(40.3), *UP, None, FACE_CAP - 360),   # « Tu boudes ? » : debout d'un bond, se retourne par l'ouest
        (S(41.0), *UP, None, FACE_CAP - 385), (S(41.8), *UP, None, FACE_CAP - 335), (S(42.4), *UP, None, FACE_CAP - 360),   # personne
        (S(47.4), *UP, None, FACE_CAP - 360)]                              # le visage s'est éveillé ; le jardin se tait
        + WALK_IN[1:]
        + [(W1 + 0.3, *KNEEL[:2], DZ, KNEEL_CAP),                          # sur la mousse, face à elle ; il s'agenouille
           (S(93.6), *KNEEL[:2], DZ, KNEEL_CAP), (S(94.2), *KNEEL[:2], DZ, -192),   # lève les yeux vers le ciel (nord-nord-est)
           (S(96.6), *KNEEL[:2], DZ, -192), (S(97.2), *KNEEL[:2], DZ, KNEEL_CAP),   # se relève : « Il faut prévenir Maman. »
           (T_END, *KNEEL[:2], DZ, KNEEL_CAP)],
    # La Rose : au repos tournée vers le nord-nord-ouest ; elle se tourne lentement vers lui par l'ouest, puis le suit jusqu'à la mousse.
    "ROSE": [(0.0, *ROSE_XY, GZ, 20), (T_END, *ROSE_XY, GZ, 20)],      # v5 : immobile, tournée vers l'entrée du passage
}
SHOW = {}
HIDE = {"JARDINIER_1": round(BLOCKING["JARDINIER_1"][-1][0], 2), "JARDINIER_2": round(BLOCKING["JARDINIER_2"][-1][0], 2)}
ELIAS_POSES = [(0.0, "debout"), (S(33.5), "debout"), (S(34.3), "assis"), (S(39.7), "assis"), (S(40.3), "debout"),
               (W1, "debout"), (W1 + 0.8, "genoux"), (S(93.6), "genoux"), (S(94.2), "genoux_ciel"), (S(96.6), "genoux_ciel"),
               (S(97.2), "debout")]
ROSE_GLOW = [(0.0, 0.0), (S(45.2), 0.0), (S(46.6), 8.0), (S(79.0), 8.0), (S(80.4), 2.5), (T_END, 2.5)]
ROSE_FACE = [(0.0, 0.0), (S(46.2), 0.0), (S(47.3), 1.0), (T_END, 1.0)]

# répliques en « temps v1 » (minutage des voix de référence, production/audio/SC03_mise-en-scene/), puis décalées par S()
_D = [
    (37.6, 39.4, "LA ROSE (hors champ)", "Tu boudes, petit prince ?"),
    (40.0, 42.4, "", "(Elias se retourne d'un bond : personne)"),
    (45.2, 47.4, "", "(la rose jaune s'éveille : son cœur s'illumine, un visage apparaît ;\nle jardin se tait)"),
    (47.6, 53.2, "", "(il entre dans le massif par les dalles et s'agenouille devant elle)"),
    (49.4, 51.1, "ELIAS (chuchotant)", "Tu es… vivante ?"), (51.9, 53.6, "LA ROSE", "Bien sûr que je suis vivante."),
    (54.3, 55.3, "ELIAS (surpris)", "Tu sais parler ?!"),
    (55.9, 60.1, "LA ROSE", "Je parle à ceux qui savent écouter.\nIls sont de moins en moins nombreux."),
    (61.0, 62.4, "ELIAS", "Les grands ne t'entendent pas ?"),
    (63.0, 67.4, "LA ROSE", "Les grands n'entendent plus rien.\nIl y a longtemps que je t'attends, Elias."),
    (68.0, 69.1, "ELIAS", "Tu connais mon nom ?"),
    (69.7, 74.4, "LA ROSE", "Je connais celui de tous les enfants de ce palais.\nIls finissent tous par m'oublier."),
    (75.3, 76.0, "ELIAS", "Pas moi."), (76.5, 79.0, "LA ROSE (amusée)", "C'est ce qu'ils disent tous."),
    (79.0, 80.4, "", "(la lueur de son cœur faiblit ; sa voix change)"),
    (80.4, 82.8, "LA ROSE", "Ce soir, les étoiles vont tomber."),
    (82.9, 85.3, "ELIAS", "Je sais. Ils vont regarder le spectacle."),
    (85.7, 93.7, "LA ROSE", "Ce n'est pas un spectacle. Une seule étoile qui touche le sol,\net tout brûle. Le jardin, le palais… Ta planète entière."),
    (93.7, 96.8, "", "(Elias lève les yeux : au-dessus des cyprès,\ndes étoiles pâles en plein jour)"),
    (97.0, 98.3, "ELIAS", "Il faut prévenir Maman."), (99.0, 100.3, "LA ROSE", "Elle ne t'entendra pas."),
    (100.3, 101.9, "", "(un temps)"), (102.2, 104.8, "LA ROSE", "Cette nuit… j'aurai besoin de toi."),
]
DIALOGUE = [(0.0, 4.5, "", "(au loin, Elias arrive en courant ;\nles jardiniers partent, sans un regard pour les fleurs)"),
            (4.5, HATS[0], "", "(ils le voient venir et s'arrêtent près du banc)"),
            (HATS[0], HATS[3], "", "(ils soulèvent leur chapeau ;\nElias passe l'arche en courant, sans les voir)"),
            (HATS[3], S(33.39), "", "(il ralentit en contournant le massif,\ndonne un coup de pied dans le gravier)"),
            (S(33.5), S(37.5), "", "(il se laisse tomber sur la bordure, dos aux roses ; il boude)")]
for a, b, who, line in _D:
    if a == 47.6: DIALOGUE.append((W0, round(W1 + 0.8, 2), who, line)); continue
    DIALOGUE.append((S(a), S(b), who, line))

# ---------------------------------------------------------------- caméras de plan
# Ligne d'action : Elias — la Rose ; d'abord nord-sud (Elias sur la bordure sud), puis le long du passage (sud-sud-est).
# Toutes les caméras restent du côté ouest de cette ligne (côté banc), comme le point de vue de l'image de concept.
L_ = (-0.94, -0.342)                     # « gauche » d'Elias à genoux face à la Rose (côté des caméras)
def off(p, a, b, z):                     # p + a·U + b·L_ (U : de la Rose vers Elias), hauteur z
    return (p[0] + a * U[0] + b * L_[0], p[1] + a * U[1] + b * L_[1], z)
R0 = ROSE_XY; K0 = KNEEL[:2]
EYE = (K0[0], K0[1], DZ + 0.88)           # yeux d'Elias à genoux (mesuré : haut de la tête à MZ + 1,07)
ROSE_F = (R0[0], R0[1], 1.24)             # visage de la Rose (fleur de 13 cm, cœur à ≈ 1,23 m)
# Règles de cadrage du dialogue (v3, 2026-11-23) : caméras toujours du côté ouest de la ligne Elias–Rose (180°) ; vus de ce côté,
# la Rose est à gauche, Elias à droite. Champ : la Rose sur le TIERS GAUCHE (elle regarde vers la droite), l'épaule ou la tête
# d'Elias en amorce au bord droit (repère d'échelle). Contrechamp : Elias sur le TIERS DROIT (il regarde vers la gauche), les
# pétales de la Rose en amorce floue au bord gauche. On resserre à mesure que la scène devient grave.
def thirds(cam, subj, frac, lens):
    """Point de visée qui place subj à la position horizontale frac (−1/3 : tiers gauche ; +1/3 : tiers droit)."""
    dx, dy = subj[0] - cam[0], subj[1] - cam[1]
    a = math.atan(frac * math.tan(math.atan(18 / lens)))      # capteur 36 mm
    c, s_ = math.cos(a), math.sin(a)
    return (cam[0] + c * dx - s_ * dy, cam[1] + s_ * dx + c * dy, subj[2])
def cam_key(t, pos, subj, frac, lens): return (t, pos, thirds(pos, subj, frac, lens), lens)
# plan à deux : orbite horaire autour du milieu des deux visages, du plan large de dos (fin de SH05) au profil
MID = ((K0[0] + R0[0]) / 2, (K0[1] + R0[1]) / 2, 1.17)
WIDE = off(K0, 1.8, 0.9, 1.95)                                          # fin de SH05 : en plongée, de dos, Elias à genoux dans le passage, la Rose au-dessus de sa tête
A_WIDE = math.degrees(math.atan2(WIDE[1] - MID[1], WIDE[0] - MID[0])); R_WIDE = math.dist(WIDE[:2], MID[:2])
A_PROF = math.degrees(math.atan2(L_[1], L_[0]))                        # profil : caméra sur la perpendiculaire, côté ouest
def orbit(t0, t1, a0, a1, r0, r1, z0, z1, l0, l1, n=8):
    keys = []
    for i in range(n + 1):
        u = i / n; e = u * u * (3 - 2 * u)
        a = math.radians(a0 + (a1 - a0) * e); r = r0 + (r1 - r0) * e
        keys.append((round(t0 + (t1 - t0) * u, 2), (MID[0] + r * math.cos(a), MID[1] + r * math.sin(a), z0 + (z1 - z0) * e),
                     MID, round(l0 + (l1 - l0) * e, 1)))
    return keys
C_OTS = off(K0, 0.45, 0.45, 1.32)          # champ moyen, par-dessus l'épaule gauche d'Elias (sa tête coupée par le bord droit)
C_OTS2 = off(K0, 0.40, 0.33, 1.30)         # champ plus serré, sa tête en amorce au bord droit
C_CU = off(R0, 0.50, 0.24, 1.26)           # gros plan de la Rose (les petites roses du massif autour donnent l'échelle)
C_REV = off(R0, -0.40, 0.25, 1.24)         # contrechamp : derrière la Rose, ses pétales en amorce à gauche
SHOTS = [
    # plan de situation en plongée : l'exèdre et le massif au premier plan, la végétation au nord, Elias au loin qui court
    ("SH01", 0.0, 4.5, [(0.0, (-1.0, -188.5, 22.0), (0.5, -166.0, 0.0), 24), (4.5, (-0.85, -187.7, 21.2), (0.5, -166.3, 0.3), 24)]),
    # les jardiniers : la grue part haut, en plongée, et descend vite à hauteur des personnages ; Elias passe l'arche en courant
    ("SH02", 4.5, 10.0, [(4.5, (-2.6, -180.3, 11.0), (-1.5, -171.0, 0.3), 28), (6.5, (-2.45, -180.2, 6.5), (-0.2, -170.6, 0.8), 27),
                         (8.3, (-2.25, -180.1, 3.2), (0.9, -169.9, 1.5), 26), (10.0, (-2.1, -180.1, 2.0), (1.6, -170.0, 1.8), 26)]),
    ("SH03", 10.0, S(34.4), [(10.0, (-3.2, -179.9, 1.2), (3.3, -172.3, 1.2), 35), (E_T[(2.9, -175.9)], (-3.0, -179.85, 1.15), (2.9, -175.9, 1.1), 35),
                             (T_ARR, (-2.7, -179.7, 1.12), (UP[0], UP[1], 1.15), 35),
                             (S(34.4), (-2.5, -179.6, 1.08), (SEAT[0], SEAT[1], 1.05), 35)]),
    # il boude : gros plan de trois quarts face, depuis le sud-sud-ouest ; la Rose endormie au fond à gauche
    ("SH04", S(34.4), S(39.9), [(S(34.4), (SEAT[0] - 0.57, SEAT[1] - 2.13, 1.05), (SEAT[0], SEAT[1], 1.08), 50),
                                (S(39.9), (SEAT[0] - 0.50, SEAT[1] - 1.90, 1.08), (SEAT[0], SEAT[1], 1.10), 50)]),
    # la Rose s'éveille par-dessus son épaule ; il entre dans le massif par les dalles ; la caméra recule et finit en plan large,
    # de dos, Elias à genoux en entier devant la Rose (comme SH05 fin B, retenue par l'auteur)
    # v4 : vu de l'ouest, Elias à droite (il se retourne vers la Rose : on voit son visage), la Rose à gauche dans le massif ;
    # lente poussée sur la Rose qui se tourne et s'éveille ; puis la caméra passe derrière lui, en plongée, quand il entre
    ("SH05", S(39.9), S(49.3), [(S(39.9), off(R0, 0.9, 3.6, 1.75), (R0[0] + 1.6 * U[0], R0[1] + 1.6 * U[1], 1.25), 30),     # de trois quarts face
                                (S(42.4), off(R0, 0.85, 3.45, 1.72), (R0[0] + 1.5 * U[0], R0[1] + 1.5 * U[1], 1.25), 30),
                                (S(47.4), off(R0, 0.6, 2.0, 1.55), (R0[0], R0[1], 1.28), 60),
                                (S(49.3), WIDE, MID, 30)]),
    # plan à deux : la caméra tourne dans le sens horaire jusqu'au profil, les deux visages dans le cadre (demande de l'auteur)
    ("SH06", S(49.3), S(55.7), orbit(S(49.3), S(55.1), A_WIDE, A_PROF, R_WIDE, 1.30, 1.95, 1.28, 30, 40) + [(S(55.7), None, None, None)]),
    ("SH07", S(55.7), S(62.8), [cam_key(S(55.7), C_OTS, ROSE_F, -1 / 3, 45), cam_key(S(62.8), off(K0, 0.43, 0.44, 1.32), ROSE_F, -1 / 3, 48)]),
    ("SH08", S(62.8), S(67.8), [cam_key(S(62.8), C_OTS2, ROSE_F, -1 / 3, 58), cam_key(S(67.8), off(K0, 0.38, 0.32, 1.30), ROSE_F, -1 / 3, 62)]),
    # v5 (auteur) : plan à deux, de profil, comme la fin de SH06, un peu plus serré (« Tu connais mon nom ? » … « Pas moi. »)
    ("SH09", S(67.8), S(76.4), [(S(67.8), (MID[0] + 1.32 * math.cos(math.radians(A_PROF + 3)), MID[1] + 1.32 * math.sin(math.radians(A_PROF + 3)), 1.28), MID, 40),
                                (S(76.4), (MID[0] + 1.26 * math.cos(math.radians(A_PROF)), MID[1] + 1.26 * math.sin(math.radians(A_PROF)), 1.27), MID, 41)]),
    ("SH10", S(76.4), S(82.85), [cam_key(S(76.4), C_CU, ROSE_F, -1 / 3, 60), cam_key(S(82.85), off(R0, 0.47, 0.23, 1.26), ROSE_F, -1 / 3, 66)]),
    # v4 (auteur) : chaque phrase importante cadre celui qui la dit ; « Je sais… » sur Elias (court : généré sur 4 s), puis
    # « Ce n'est pas un spectacle… » sur la Rose, grave, affligée (lente poussée)
    ("SH11", S(82.85), S(85.55), [cam_key(S(82.85), C_REV, EYE, 1 / 3, 55), cam_key(S(85.55), C_REV, EYE, 1 / 3, 57)]),
    ("SH12", S(85.55), S(93.5), [cam_key(S(85.55), off(R0, 0.55, 0.26, 1.26), ROSE_F, -1 / 3, 50), cam_key(S(93.5), off(R0, 0.48, 0.23, 1.26), ROSE_F, -1 / 3, 62)]),
    ("SH13", S(93.5), S(96.8), [(S(93.5), off(K0, -0.25, 0.0, 1.50), (5.5, -163.5, 7.0), 28), (S(96.8), off(K0, -0.25, 0.0, 1.50), (5.8, -163.0, 9.0), 28)]),   # caméra un peu devant sa tête
    ("SH14", S(96.8), T_END, [cam_key(S(96.8), off(K0, 1.9, 1.7, 1.85), ROSE_F, -1 / 3, 35), cam_key(S(100.6), off(K0, 1.8, 1.6, 1.8), ROSE_F, -1 / 3, 35),
                              cam_key(T_END, off(K0, 1.2, 0.75, 1.55), ROSE_F, -1 / 3, 45)]),
]
SHOT_TITLES = {"SH01": "Situation", "SH02": "Les jardiniers", "SH03": "Elias arrive", "SH04": "Il boude", "SH05": "La Rose s'éveille",
               "SH06": "Tu es vivante ?", "SH07": "Ceux qui savent écouter", "SH08": "Je t'attends, Elias", "SH09": "Pas moi",
               "SH10": "Les étoiles vont tomber", "SH11": "Je sais", "SH12": "Pas un spectacle", "SH13": "Le ciel",
               "SH14": "J'aurai besoin de toi"}

# ---------------------------------------------------------------- outils (repris de build_mise_en_scene_sc02.py)
def _fcurves(action):
    if hasattr(action, "fcurves"): return list(action.fcurves)
    out = []
    for layer in action.layers:
        for strip in layer.strips:
            for cb in getattr(strip, "channelbags", []): out += list(cb.fcurves)
    return out

def mat(name, rgb, emit=0.6):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.diffuse_color = (*rgb, 1)
    if m.node_tree is None: m.use_nodes = True
    b = m.node_tree.nodes.get("Principled BSDF")
    if b:
        b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Emission Color"].default_value = (*rgb, 1)
        b.inputs["Emission Strength"].default_value = emit
    return m

def heading(p, q):
    dx, dy = q[0] - p[0], q[1] - p[1]
    return None if math.hypot(dx, dy) < 0.05 else math.degrees(math.atan2(dx, -dy))

def unwrap(prev, a):
    while a - prev > 180: a -= 360
    while a - prev < -180: a += 360
    return a

def animate_pivot(piv, keys):
    """Comme SC02, avec une différence : entre deux clés qui ont toutes deux un cap, le personnage garde ce cap
    (il peut reculer pour s'asseoir, faire un pas de côté) au lieu de se tourner dans le sens du déplacement."""
    for t, x, y, z, cap in keys:
        piv.location = W(x, y, z); piv.keyframe_insert("location", frame=fr(t))
    n = len(keys)
    seg = [None if (keys[i][4] is not None and keys[i + 1][4] is not None) else heading(keys[i][1:3], keys[i + 1][1:3])
           for i in range(n - 1)]
    cur = keys[0][4] if keys[0][4] is not None else next((s for s in seg if s is not None), 0)
    rot = []
    for i, (t, x, y, z, cap) in enumerate(keys):
        cin = seg[i - 1] if i > 0 and seg[i - 1] is not None else cur
        if i < n - 1 and seg[i] is not None: cout = seg[i]
        elif cap is not None: cout = cap
        else: cout = cin
        if i > 0 and seg[i - 1] is None and cap is not None: cin = cap      # tour sur place entre deux caps
        d_in = min(0.3, (t - keys[i - 1][0]) / 2) if i > 0 else 0
        d_out = min(0.3, (keys[i + 1][0] - t) / 2) if i < n - 1 else 0
        if i > 0 and seg[i - 1] is None and keys[i - 1][4] is not None: d_in = 0
        if i < n - 1 and seg[i] is None and cap is not None and keys[i + 1][4] is not None: d_out = 0
        if i < n - 1 and seg[i] is None and cap is not None and keys[i + 1][4] is not None: d_out = 0
        rot += [(t - d_in, cin), (t + d_out, cout)]
        cur = cout
    prev = None
    for t, a in rot:
        a = a if prev is None else unwrap(prev, a); prev = a
        piv.rotation_euler = (0, 0, math.radians(a)); piv.keyframe_insert("rotation_euler", index=2, frame=fr(t))
    for fc in _fcurves(piv.animation_data.action):
        for k in fc.keyframe_points: k.interpolation = "LINEAR"

def key_visible(objs, t_show=None, t_hide=None):
    for o in objs:
        keys = [(1, t_show is not None)]
        if t_show is not None: keys += [(fr(t_show) - 1, True), (fr(t_show), False)]
        if t_hide is not None: keys += [(fr(t_hide) - 1, False), (fr(t_hide), True)]
        for f, hidden in keys:
            o.hide_render = hidden; o.hide_viewport = hidden
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
    o = bpy.data.objects.new(name, cu); o.data.materials.append(mat("MES3_" + name, rgb)); coll.objects.link(o)
    return o

def poly_curve(name, pts, rgb, coll, bevel=0.06, cyclic=False):
    cu = bpy.data.curves.new(name, "CURVE"); cu.dimensions = "3D"; cu.bevel_depth = bevel
    sp = cu.splines.new("POLY"); sp.points.add(len(pts) - 1)
    for p, q in zip(sp.points, pts): p.co = (*q, 1)
    sp.use_cyclic_u = cyclic
    o = bpy.data.objects.new(name, cu); o.data.materials.append(mat("MES3_" + name, rgb)); coll.objects.link(o)
    return o

def prim(kind, name, coll, size, loc, rgb, rot=(0, 0, 0), emit=0.0, mname=None):
    """Volume simple en mètres réels, posé en coordonnées locales de son parent (un pivot d'échelle 1 dans le monde)."""
    import bmesh
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    if kind == "box": bmesh.ops.create_cube(bm, size=1.0)
    elif kind == "sphere": bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=0.5)
    elif kind == "cyl": bmesh.ops.create_cone(bm, cap_ends=True, segments=16, radius1=0.5, radius2=0.5, depth=1.0)
    for v in bm.verts: v.co = Vector((v.co.x * size[0], v.co.y * size[1], v.co.z * size[2]))
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); coll.objects.link(o)
    o.data.materials.append(mat(mname or ("MES3_m_" + name), rgb, emit)); o.location = loc; o.rotation_euler = rot
    return o

# ---------------------------------------------------------------- figurants et Rose provisoires
def make_gardener(key, piv, coll, h, rgb):
    """Jardiniers : modèles Tripo riggés (assets_sc03.py, planches kb/characters/sheets/gardener1|2.png), bras le long du corps.
    J1 pousse la brouette (PROP_brouette, roue devant lui) ; J2 tient un râteau (volumes simples). Le chapeau fait partie du modèle :
    le geste de le soulever (15–17,4 s) est seulement écrit dans les prompts."""
    master = bpy.data.objects["RIG_Jardinier1" if key == "JARDINIER_1" else "RIG_Jardinier2"]
    A, meshes = _copy_rig(master, coll, P + key)
    A.parent = piv; A.matrix_parent_inverse.identity(); A.rotation_mode = master.rotation_mode
    A.location = master.location.copy(); A.rotation_euler = master.rotation_euler.copy(); A.scale = master.scale.copy()
    for o in [A] + meshes: o.hide_render = False; o.hide_viewport = False
    objs = list(meshes)
    if key == "JARDINIER_1":      # brouette devant lui (le personnage regarde vers -Y local) ; les bras arrivent aux mancherons
        br = bpy.data.objects["PROP_brouette"].copy(); br.name = P + "brouette"; coll.objects.link(br)
        br.parent = piv; br.location = (0, -0.88, 0); br.hide_render = False; br.hide_viewport = False
        objs.append(br)
    else:                         # râteau : il ratisse les dernières feuilles (0–5 s), puis le porte sur l'épaule
        rake = bpy.data.objects.new(P + "rateau", None); coll.objects.link(rake); rake.parent = piv; rake.location = (0.22, -0.15, 1.15)
        parts = [prim("cyl", P + "rateau_manche", coll, (0.03, 0.03, 1.6), (0, 0, 0), (0.40, 0.30, 0.20)),
                 prim("box", P + "rateau_peigne", coll, (0.45, 0.05, 0.06), (0, 0, -0.8), (0.25, 0.25, 0.25))]
        for o in parts: o.parent = rake
        for t, ax in ((0.0, 40), (0.3, 55), (0.9, 150)):          # v3 : dernier coup de râteau, puis sur l'épaule
            rake.rotation_euler = (math.radians(ax), 0, 0); rake.keyframe_insert("rotation_euler", index=0, frame=fr(t))
        objs += parts
    return objs

def make_rose(piv, coll):
    """La Rose : modèle Tripo de la Rose endormie (PROP_rose_endormie, planche production/refs/rose-asleep-sheet.png), fleur tournée
    vers -Y local ; cœur doré qui s'illumine et disque sombre du visage (provisoires) posés sur la fleur."""
    body = bpy.data.objects["PROP_rose_endormie"].copy(); body.name = P + "ROSE_modele"; coll.objects.link(body)
    ax_, ay_ = tuple(body.data.get("rose_axe", (0.03, -0.015)))           # haut de la tige (rose_13cm.py) : la fleur au-dessus du pivot
    body.parent = piv; body.location = (-ax_, -ay_, MZ - GZ - 0.02); body.hide_render = False; body.hide_viewport = False
    zb = ROSE_F[2] - GZ
    # fleur réduite (rose_13cm.py, 2026-11-23 ; diamètre lu sur le maillage : 13 puis 20 cm) : visage ≈ 35–40 % du diamètre
    q = body.data.get("rose_diametre", 0.13) / 0.13
    heart = prim("sphere", P + "ROSE_coeur", coll, (0.032 * q,) * 3, (0, -0.028 * q, zb), (1.0, 0.70, 0.10), mname="MES3_ROSE_coeur_lueur")
    face = prim("cyl", P + "ROSE_visage", coll, (0.05 * q, 0.05 * q, 0.006), (0, -0.055 * q, zb - 0.005), (0.30, 0.18, 0.10),
                rot=(math.radians(90 - 20), 0, 0))
    for o in (heart, face): o.parent = piv
    em = heart.data.materials[0].node_tree.nodes["Principled BSDF"].inputs["Emission Strength"]
    for t, v in ROSE_GLOW:
        em.default_value = v; em.keyframe_insert("default_value", frame=fr(t))
    for t, v in ROSE_FACE:
        face.scale = (max(v, 0.001),) * 3; face.keyframe_insert("scale", frame=fr(t))
    return [body, heart, face]

# ---------------------------------------------------------------- poses d'Elias (assis, à genoux)
LEG = {s: ["tripo::1_%s_Limb_%d" % (s, i) for i in range(3)] for s in ("Left", "Right")}
ARM = {s: ["tripo::0_%s_Limb_%d" % (s, i) for i in range(2)] for s in ("Left", "Right")}
# directions dans l'espace de l'armature : x = devant, z = haut, y = côté (gauche = -y). drop : abaissement du bassin (m).
POSES = {
    "assis": dict(drop=0.23, leg=[(1.0, 0.16, 0.30), (0.25, 0.04, -1.0), (1.0, 0.0, -0.35)],     # bordure de 0,40 m
                  arm=[(0.30, 0.14, -1.0), (1.0, -0.45, 0.30)], spine=(0.18, 0, 1), head=(0.38, 0, 1)),
    "genoux": dict(drop=0.29, leg=[(0.12, 0.10, -1.0), (-1.0, 0.04, 0.02), (-1.0, 0.0, -0.15)],
                   arm=[(0.25, 0.12, -1.0), (0.8, -0.30, -0.55)], spine=(0.12, 0, 1), head=(0.15, 0, 1)),   # la Rose est un peu plus bas que ses yeux
    "genoux_ciel": dict(drop=0.29, leg=[(0.12, 0.10, -1.0), (-1.0, 0.04, 0.02), (-1.0, 0.0, -0.15)],
                        arm=[(0.25, 0.12, -1.0), (0.8, -0.30, -0.55)], spine=(0.0, 0, 1), head=(-0.55, 0, 1)),
}

VL = [None]   # couche de vue de la scène où vit l'armature (fixée par build)
def _upd(): (VL[0] or bpy.context.view_layer).update()

def _aim(A, name, d):
    pb = A.pose.bones[name]; _upd()
    M = pb.matrix.copy(); y = M.col[1].xyz.normalized(); h = M.translation.copy()
    R = y.rotation_difference(Vector(d).normalized()).to_matrix().to_4x4()
    pb.matrix = Matrix.Translation(h) @ R @ Matrix.Translation(-h) @ M
    _upd()

def pose_elias(A, z0, states):
    basis = {pb.name: pb.matrix_basis.copy() for pb in A.pose.bones}
    used = set(sum(LEG.values(), []) + sum(ARM.values(), []) + ["tripo::Spine_0", "tripo::Head_0"])
    for t, st in states:
        for pb in A.pose.bones: pb.matrix_basis = basis[pb.name]
        _upd()
        drop = 0.0
        if st in POSES:
            p = POSES[st]; drop = p["drop"]
            _aim(A, "tripo::Spine_0", p["spine"]); _aim(A, "tripo::Head_0", p["head"])
            for s, sg in (("Left", -1), ("Right", 1)):
                for b, d in zip(LEG[s], p["leg"]): _aim(A, b, (d[0], d[1] * sg, d[2]))
                for b, d in zip(ARM[s], p["arm"]): _aim(A, b, (d[0], d[1] * sg, d[2]))
        for name in used:
            pb = A.pose.bones[name]
            pb.keyframe_insert("rotation_euler" if pb.rotation_mode != "QUATERNION" else "rotation_quaternion", frame=fr(t))
            pb.keyframe_insert("location", frame=fr(t))
        A.location.z = z0 - drop; A.keyframe_insert("location", index=2, frame=fr(t))
    for pb in A.pose.bones: pb.matrix_basis = basis[pb.name]

# ---------------------------------------------------------------- construction
def build():
    prefs = bpy.context.preferences.edit
    src = bpy.data.scenes["SC02-SH01"]                     # même décor, même lumière que la scène 2
    E = bpy.data.objects["ECHELLE_MONDE"]
    for n in (SC, VERIF): _remove_scene(n)
    jeu, sur = _clear_collection(JEU), _clear_collection(SUR)
    sc = bpy.data.scenes.new(SC); ve = bpy.data.scenes.new(VERIF)
    for s in (sc, ve):
        for c in src.collection.children:
            if not c.name.endswith("_jeu"): s.collection.children.link(c)
        s.collection.children.link(jeu)
        s.world = src.world; s.render.fps = FPS; s.frame_start = 1; s.frame_end = fr(T_END)
        for o in src.collection.objects:
            if o.name not in s.collection.objects: s.collection.objects.link(o)
    ve.collection.children.link(sur)
    # la Rose fixe (AUR_21_rose_statique, clairiere_v2.py) est remplacée ici par la Rose animée
    for s in (sc, ve):
        s.view_layers[0].update()
        def _excl(lc):
            if lc is None: return
            if lc.name == "AUR_21_rose_statique": lc.exclude = True; return
            for i in range(len(lc.children)): _excl(lc.children[i])
        _excl(s.view_layers[0].layer_collection)
    win = bpy.context.window; keep = win.scene; win.scene = sc; VL[0] = sc.view_layers[0]
    prefs.keyframe_new_interpolation_type = "LINEAR"
    pivots = {}
    for key, keys in BLOCKING.items():
        piv = bpy.data.objects.new(P + key, None); piv.empty_display_size = 0.4; jeu.objects.link(piv)
        piv.parent = E; piv.matrix_parent_inverse.identity(); piv.scale = (1 / K,) * 3
        animate_pivot(piv, keys); pivots[key] = piv
        if key == "ELIAS":
            master = bpy.data.objects["RIG_Elias"]
            A, objs = _copy_rig(master, jeu, P + key)
            A.parent = piv; A.matrix_parent_inverse.identity()
            A.location = (0, 0, master.location.z); A.rotation_euler = master.rotation_euler.copy(); A.scale = master.scale.copy()
        elif key == "ROSE": objs = make_rose(piv, jeu)
        else: objs = make_gardener(key, piv, jeu, 1.75 if key == "JARDINIER_1" else 1.70, COLOR[key])
        me = bpy.data.meshes.new(P + "fleche_" + key)
        sz = 0.55 if key == "ROSE" else 1.0
        me.from_pydata([(0, -1.0 * sz, 0), (-0.55 * sz, 0.4 * sz, 0), (0, 0.05 * sz, 0), (0.55 * sz, 0.4 * sz, 0)], [],
                       [(0, 1, 2), (0, 2, 3)])
        ar = bpy.data.objects.new(P + "fleche_" + key, me); ar.data.materials.append(mat("MES3_c_" + key, COLOR[key]))
        sur.objects.link(ar); ar.parent = piv; ar.location = (0, 0, 2.6)
        lb = text_obj(P + "nom_" + key, LABEL[key], 0.45, COLOR[key], sur)
        cl = lb.constraints.new("COPY_LOCATION"); cl.target = piv; cl.use_offset = True
        lb.location = (0, 0.9, 2.8)
        if key in SHOW or key in HIDE: key_visible(objs + [ar, lb], SHOW.get(key), HIDE.get(key))
    prefs.keyframe_new_interpolation_type = "BEZIER"
    pose_elias(bpy.data.objects[P + "ELIAS_rig"], bpy.data.objects["RIG_Elias"].location.z, ELIAS_POSES)
    for key, piv in pivots.items():
        if key == "ROSE": continue
        fcs = {(fc.data_path, fc.array_index): fc for fc in _fcurves(piv.animation_data.action)}
        t0, t1 = SHOW.get(key, 0.0), HIDE.get(key, T_END)
        pts, t = [], t0
        while t <= t1 + 1e-6:
            p = Vector([fcs[("location", i)].evaluate(fr(t)) for i in range(3)]) * K
            pts.append((p.x, p.y, p.z + 0.04)); t += 0.2
        poly_curve(P + "trajet_" + key, pts, COLOR[key], sur, bevel=0.035 if key != "ELIAS" else 0.05)
    cams = []
    for name, t0, t1, spec in SHOTS:
        cam = bpy.data.objects.new(P + "CAM_" + name, bpy.data.cameras.new(P + "CAM_" + name))
        cam.data.clip_start = 0.05; cam.data.clip_end = 30000; cam.data.sensor_width = 36
        tgt = bpy.data.objects.new(P + "CAM_" + name + "_VISEE", None); tgt.empty_display_size = 0.2
        for o in (cam, tgt): jeu.objects.link(o); o.parent = E; o.matrix_parent_inverse.identity()
        tc = cam.constraints.new("TRACK_TO"); tc.target = tgt; tc.track_axis = "TRACK_NEGATIVE_Z"; tc.up_axis = "UP_Y"
        for t, pos, aim, lens in spec:
            if pos is None: pos, aim, lens = last
            last = (pos, aim, lens)
            cam.location = W(*pos); tgt.location = W(*aim); cam.data.lens = lens
            cam.keyframe_insert("location", frame=fr(t)); tgt.keyframe_insert("location", frame=fr(t))
            cam.data.keyframe_insert("lens", frame=fr(t))
        m = sc.timeline_markers.new(name, frame=fr(t0)); m.camera = cam
        if t0 == 0: sc.camera = cam
        lens_draw = spec[0][3]
        L = 3.2 if name != "SH01" else 9.0; w = L * 18 / lens_draw
        wd = poly_curve(P + "champ_" + name, [(0, 0, 0), (-w, L, 0), (w, L, 0), (0, 0, 0)], COLOR["CAM"], sur, bevel=0.03)
        c1 = wd.constraints.new("COPY_LOCATION"); c1.target = cam; c1.use_z = False
        c2 = wd.constraints.new("LOCKED_TRACK"); c2.target = tgt; c2.track_axis = "TRACK_Y"; c2.lock_axis = "LOCK_Z"
        wd.location.z = GZ + 2.4
        lab = text_obj(P + "nomcam_" + name, name, 0.4, COLOR["CAM"], sur)
        c3 = lab.constraints.new("COPY_LOCATION"); c3.target = cam; c3.use_z = False; c3.use_offset = True
        lab.location = (0, -0.5, GZ + 2.6)
        for o in (wd, lab):
            for f, v in ((1, True), (fr(t0), False), (fr(t1), True)):
                if f == 1 and t0 == 0: v = False
                o.hide_render = v; o.hide_viewport = v
                o.keyframe_insert("hide_render", frame=f); o.keyframe_insert("hide_viewport", frame=f)
        cams.append(cam)
    vc = bpy.data.objects.new(P + "CAM_VERIF", bpy.data.cameras.new(P + "CAM_VERIF"))
    vc.data.type = "ORTHO"; vc.data.ortho_scale = 34; vc.data.clip_end = 400     # de l'allée (Elias au loin) à l'exèdre
    sur.objects.link(vc); vc.parent = E; vc.matrix_parent_inverse.identity(); vc.location = W(0.0, -166.0, 60)
    ve.camera = vc
    for s, eng, rx, ry in ((sc, "BLENDER_EEVEE", 960, 540), (ve, "BLENDER_WORKBENCH", 1080, 1080)):
        s.render.engine = eng; s.render.resolution_x, s.render.resolution_y = rx, ry; s.render.resolution_percentage = 100
    ve.display.shading.light = "STUDIO"; ve.display.shading.color_type = "TEXTURE"; ve.display.shading.show_shadows = False
    ve.view_settings.view_transform = "Standard"; ve.view_settings.exposure = 0.8
    for a in ("view_transform", "look", "exposure"): setattr(sc.view_settings, a, getattr(src.view_settings, a))
    try: sc.eevee.taa_render_samples = 16
    except Exception: pass
    win.scene = keep
    # chrono pour la vidéo de vérification (compose_verification_sc03.py)
    if bpy.data.filepath:
        out = os.path.join(os.path.dirname(os.path.dirname(bpy.data.filepath)), "animatic", "mise-en-scene", "SC03_chrono.json")
        json.dump({"T_END": T_END, "SHIFT1": SHIFT1, "SHIFT2": SHIFT2, "CUT": [CUT0, CUT1], "W0": W0, "W1": W1,
                   "SHOTS": [[a, b, f"{n} — {SHOT_TITLES[n]}"] for n, a, b, _ in SHOTS],
                   "DIALOGUE": DIALOGUE}, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return {"frames": sc.frame_end, "T_END": T_END, "arrivee_elias": T_ARR, "SHIFT1": SHIFT1, "SHIFT2": SHIFT2, "W0": W0, "W1": W1}

# ---------------------------------------------------------------- contrôle des collisions
OBST_POLY = {
    "massif": [(-2.58, -174.36), (-1.78, -175.88), (0.11, -176.56), (1.99, -175.6), (2.57, -173.53), (2.0, -172.29),
               (0.52, -171.37), (-1.15, -171.57), (-2.37, -172.76)],
    "banc": [(-3.52, -170.12), (-3.04, -170.83), (-1.44, -169.83), (-1.87, -169.09)],
    "fontaine": [(4.29, -171.86), (4.76, -172.64), (5.65, -173.23), (5.94, -173.11), (4.86, -170.4), (4.32, -171.52)],
    "muret_ouest": [(-5.26, -170.49), (-4.8, -170.81), (-1.95, -168.54), (-2.15, -168.02), (-4.1, -169.16)],
    "muret_est": [(4.74, -170.72), (5.71, -174.23), (6.28, -174.0), (5.59, -171.06), (5.21, -170.41)],
    "pilier_arche_O": [(-1.06, -167.39), (-0.95, -167.75), (0.25, -168.15), (0.15, -166.7), (-0.49, -166.23)],
    "pilier_arche_E": [(3.75, -169.3), (4.42, -169.47), (5.06, -168.69), (4.62, -167.76), (3.85, -167.9)],
}
OBST_CIRC = {"arbustes_07": ((0.78, -162.75), 2.17), "arbustes_10": ((5.94, -164.42), 1.81)}
WALL = ((0.0, -173.03), 7.85)

def _dist_poly(p, poly):
    def seg(a, b):
        ax, ay = b[0] - a[0], b[1] - a[1]; L2 = ax * ax + ay * ay
        u = max(0, min(1, ((p[0] - a[0]) * ax + (p[1] - a[1]) * ay) / L2)) if L2 else 0
        return math.hypot(p[0] - a[0] - u * ax, p[1] - a[1] - u * ay)
    d = min(seg(poly[i], poly[(i + 1) % len(poly)]) for i in range(len(poly)))
    inside = False
    for i in range(len(poly)):
        a, b = poly[i], poly[(i + 1) % len(poly)]
        if (a[1] > p[1]) != (b[1] > p[1]) and p[0] < a[0] + (p[1] - a[1]) * (b[0] - a[0]) / (b[1] - a[1]): inside = not inside
    return -d if inside else d

def check(step=0.1, body=0.25):
    """Distances aux obstacles et entre personnages ; renvoie les alertes (texte). Elias contre le massif est voulu dès qu'il
    s'assied (bordure, puis dalles et mousse)."""
    def state(key, t):
        piv = bpy.data.objects[P + key]
        fcs = {(fc.data_path, fc.array_index): fc for fc in _fcurves(piv.animation_data.action)}
        x, y = (fcs[("location", i)].evaluate(fr(t)) * K for i in range(2))
        return (x, y), fcs[("rotation_euler", 2)].evaluate(fr(t))
    alive = lambda k, t: SHOW.get(k, -1) <= t < HIDE.get(k, 1e9)
    alerts, t = [], 0.0
    keys = [k for k in BLOCKING if k != "ROSE"]
    while t <= T_END:
        pos = {}
        for k in keys:
            if not alive(k, t): continue
            p, cap = state(k, t); pts = [p]
            if k == "JARDINIER_1": pts.append((p[0] + 1.2 * math.sin(cap), p[1] - 1.2 * math.cos(cap)))   # brouette
            pos[k] = pts
            for q in pts:
                for n, poly in OBST_POLY.items():
                    d = _dist_poly(q, poly)
                    if d < body and not (k == "ELIAS" and n == "massif" and t >= S(33.5)): alerts.append(f"{t:5.1f} s {k} → {n} : {d:.2f} m")
                for n, (c, r) in OBST_CIRC.items():
                    d = math.dist(q, c) - r
                    if d < body: alerts.append(f"{t:5.1f} s {k} → {n} : {d:.2f} m")
                if math.dist(q, WALL[0]) > WALL[1] - body and q[1] < -172.5: alerts.append(f"{t:5.1f} s {k} → muret de l'exèdre")
        ks = list(pos)
        for i in range(len(ks)):
            for j in range(i + 1, len(ks)):
                d = min(math.dist(a, b) for a in pos[ks[i]] for b in pos[ks[j]])
                if d < 2 * body: alerts.append(f"{t:5.1f} s {ks[i]} ↔ {ks[j]} : {d:.2f} m")
        t = round(t + step, 3)
    return alerts
