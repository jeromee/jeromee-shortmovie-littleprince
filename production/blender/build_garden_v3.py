# build_garden_v3.py — jardin v3 (décidé le 2026-11-19, auteur ; kb/decisions/0007, kb/world/site-plan.md).
# Reconstruit SEULEMENT les collections du jardin du monde maître (AUR_20_jardin,
# AUR_21_massif_et_reperes, AUR_22_arbres) ; ne touche ni au palais, ni aux orangers, ni aux
# personnages, ni aux plans. Les collections gardent leur nom et restent liées aux scènes de plans.
# Usage (world.blend ouvert) :
#   exec(compile(open(chemin, encoding="utf-8").read(), chemin, "exec")) ; build_garden()
# Repère du plan : x = est, s = distance au sud de la tour (Blender : y = -s), z = 0 au jardin.
#
# Nord (34 → 140 m) : jardin à la française — quatre parterres de buis en broderies, ifs en cône,
#   allées de gravier droites, fontaine à vasques au centre du parterre sud-ouest.
# Ceinture : deux allées de gravier le long du muret ; à l'est, portillon au pied de l'aile est,
#   haute haie d'ifs, serre à la lisière est (porte sur l'allée).
# Sud (145 m → exèdre) : bosquet touffu, allée sinueuse ; les trois allées se rejoignent avant
#   l'arche de roses, seuil de la clairière du grand massif.
import bpy, bmesh, math, os, random
from mathutils import Vector

HERE = os.path.dirname(bpy.data.filepath)
W = {"__name__": "build_world_helpers"}
_p = os.path.join(HERE, "build_world.py")
exec(compile(open(_p, encoding="utf-8").read(), _p, "exec"), W)
W["COLORS"].update({
    "gravel": (0.86, 0.82, 0.72), "box": (0.20, 0.38, 0.16), "yew": (0.10, 0.26, 0.15),
    "flowers": (0.78, 0.52, 0.66), "lavender": (0.55, 0.50, 0.78), "shrub": (0.24, 0.44, 0.20),
    "grove": (0.22, 0.42, 0.18),
})
box, cyl, ball, prism, wall, arch, ribbon = (W[k] for k in ("box", "cyl", "ball", "prism", "wall", "arch", "ribbon"))

GA, GB, GCs = 95.0, 95.2, 122.2          # ovale du jardin (demi-axes, centre)
# Clairière du grand massif. "v3" : version du 2026-11-19 (exèdre de 17 m, murets à 14 m, arche à 17 m du
# massif). "resserree" : essai du 2026-11-19 (remarque de l'auteur : espace autour du massif devenu trop
# grand, les images d'avant étaient plus intimes) — murets à 8,5 m, arche à 9 m, exèdre de 11 m, couronne
# d'arbres rapprochée, caméra du massif plus près. Une ligne à changer pour revenir en arrière.
CLAIRIERE = "resserree"   # "v3" : clairière du 2026-11-19 (plus vaste, ouverte plein nord)
# 2026-11-20 (auteur) : clairière resserrée ET ouverture tournée de ROT degrés vers l'est, pour que la caméra
# du massif, placée dans l'axe arche-massif, voie le massif au centre, l'arche derrière et le palais en haut à
# gauche (composition de l'image de concept), sans enfilade arche-palais. Massif ramené à 6 m de diamètre.
CL = {"v3":        dict(ex_r=17.0, walls=14.0, gap=(245, 295), parvis=10.0, arch_d=17.4, ring=26.0, free_r=23.0,
                        bed=4.5, rot=0.0, eye=(-7.0, 228.9, 1.5)),
      "resserree": dict(ex_r=10.0, walls=7.5, gap=(232, 308), parvis=6.0, arch_d=8.0, ring=14.0, free_r=12.5,
                        bed=3.0, rot=18.0, cam_d=8.0)}[CLAIRIERE]
MS = 217.4                                 # centre du grand massif
EX_C, EX_R = (0.0, 216.3), CL["ex_r"]      # exèdre
ROT = math.radians(CL["rot"])              # ouverture de la clairière : nord tourné de ROT vers l'est
ARCH_X = CL["arch_d"] * math.sin(ROT)
ARCH_S = MS - CL["arch_d"] * math.cos(ROT) # arche de roses (200 m en v3)
if "eye" not in CL:                        # caméra du massif : dans l'axe arche-massif, au sud du massif
    CL["eye"] = (-CL["cam_d"] * math.sin(ROT), MS + CL["cam_d"] * math.cos(ROT), 1.6)
LATERAUX = True                            # 2026-11-20 (auteur) : jardins latéraux autour des ailes (palace-ref)
SERRE = (62.0, 78.0, 136.0, 146.0)         # x0, x1, s0, s1
FOUNT = (-40.0, 114.0)                     # fontaine à vasques
PORT_S = 40.0                              # portillon (muret est)

def ell_x(s, inset=0.0):
    a, b = GA - inset, GB - inset; v = 1 - ((s - GCs) / b) ** 2
    return a * math.sqrt(v) if v > 0 else 0.0

def clip(pts, inset):
    """Ramène dans l'ovale (rétréci de 'inset') les points qui en sortent."""
    a, b = GA - inset, GB - inset; out = []
    for x, s in pts:
        k = math.sqrt((x / a) ** 2 + ((s - GCs) / b) ** 2)
        out.append((x / k, GCs + (s - GCs) / k) if k > 1 else (x, s))
    return out

def rrect(x0, x1, s0, s1, r, step=1.5):
    """Contour d'un rectangle aux angles arrondis, échantillonné (sens trigo)."""
    pts = []
    for cx, cs, a0 in ((x1 - r, s0 + r, -90), (x1 - r, s1 - r, 0), (x0 + r, s1 - r, 90), (x0 + r, s0 + r, 180)):
        for i in range(7):
            a = math.radians(a0 + 15 * i); pts.append((cx + r * math.cos(a), cs + r * math.sin(a)))
    dense = []
    for (xa, sa), (xb, sb) in zip(pts, pts[1:] + pts[:1]):
        n = max(1, int(math.hypot(xb - xa, sb - sa) / step))
        dense += [(xa + (xb - xa) * i / n, sa + (sb - sa) * i / n) for i in range(n)]
    return dense

def poly_dist(p, poly):
    best = 1e9
    for (xa, sa), (xb, sb) in zip(poly[:-1], poly[1:]):
        dx, ds = xb - xa, sb - sa; L2 = dx * dx + ds * ds or 1e-9
        t = max(0, min(1, ((p[0] - xa) * dx + (p[1] - sa) * ds) / L2))
        best = min(best, math.hypot(p[0] - xa - t * dx, p[1] - sa - t * ds))
    return best

# Percée vers l'horloge (2026-11-19, auteur) : depuis le point de vue des images du massif (garden-day,
# garden-night… : caméra à 7 m à l'ouest de l'axe, au sud du massif, qui vise l'arche), le cadran de la
# tour de l'horloge doit rester visible, à gauche de l'arche. Le long de cette ligne de vue, la végétation
# du bosquet est limitée en hauteur (arbres plus petits, ou arbustes) pour rester sous le cadran.
VISTA_EYE, VISTA_T = CL["eye"], (0.0, 2.0)
VISTA_DEG, VISTA_HALF = 6.9, 9.0          # angle sous le bas du cadran ; demi-largeur de la percée (m)

def vista_max_h(x, s):
    ex, es, ez = VISTA_EYE; tx, ts = VISTA_T
    dx, ds = tx - ex, ts - es; L = math.hypot(dx, ds)
    u = ((x - ex) * dx + (s - es) * ds) / L            # distance le long de la ligne de vue
    lat = abs((x - ex) * ds - (s - es) * dx) / L        # écart latéral
    if lat > VISTA_HALF or u < 0 or s < 138: return None
    return ez + u * math.tan(math.radians(VISTA_DEG)) - 0.8

def empty_collection(name):
    c = bpy.data.collections[name]
    for o in list(c.objects): bpy.data.objects.remove(o, do_unlink=True)
    W["_cur"][0] = c
    return c

def build_garden(seed=7):
    rnd = random.Random(seed)
    W["_mats"].clear()
    # ------------------------------------------------------------------ AUR_20_jardin
    empty_collection("AUR_20_jardin")
    cyl("pelouse", 0, GCs, 1.0, 0, 0.06, "lawn", segs=96, sx=GA, sy=GB)
    cyl("exedre_sol", EX_C[0], EX_C[1], EX_R, 0, 0.055, "lawn", segs=48)
    S_END = 50.0 if LATERAUX else 32.0       # bout nord du muret ovale
    t0, t1 = math.acos(EX_R / GA), -math.asin((GCs - S_END) / GB)
    east = [(GA * math.cos(t), GCs + GB * math.sin(t)) for t in [t0 + (t1 - t0) * i / 80 for i in range(81)]]
    if LATERAUX:
        # Jardins latéraux (2026-11-20, auteur ; d'après palace-ref) : le muret à balustrade se prolonge autour
        # des ailes jusqu'à l'arrière du palais ; le long de chaque façade extérieure, une allée de gravier courbe,
        # une bordure de buis, des cyprès et de grands arbres ronds contre le muret. La nuit, Elias descend de sa
        # fenêtre (aile est) dans le jardin latéral est, suit l'allée latérale puis l'allée de ceinture est.
        key = [(east[-1][0], S_END), (66.0, 36.0), (68.0, 15.0), (66.0, -6.0), (56.0, -16.0), (42.0, -17.0)]
        lat = []
        for (xa, sa), (xb, sb) in zip(key[:-1], key[1:]):
            lat += [(xa + (xb - xa) * i / 8, sa + (sb - sa) * i / 8) for i in range(8)]
        lat.append(key[-1])
        for sg, nm in ((1, "est"), (-1, "ouest")):
            wall(f"muret_{nm}", [(sg * x, s_) for x, s_ in east + lat[1:]], 1.2, 0.6, "wall")
            prism(f"pelouse_laterale_{nm}", [(sg * x, s_) for x, s_ in [(37.0, -17.0)] + lat[::-1] + [(37.0, S_END)]][::sg], 0, 0.05, "lawn")
            ribbon(f"allee_laterale_{nm}", [(sg * x, s_) for x, s_ in [(44, -11), (47, 0), (48.5, 14), (50, 30), (51, 42), (ell_x(S_END, 7), S_END)]], 3.0, "gravel", lift=0.09)
            wall(f"haie_buis_laterale_{nm}", [(sg * 40.6, -12.0), (sg * 40.6, 33.0)], 0.6, 0.5, "box")
            wall(f"plate_bande_laterale_{nm}", [(sg * 41.6, -12.0), (sg * 41.6, 33.0)], 0.5, 1.0, "flowers" if sg > 0 else "lavender", z0=0.05)
    else:
        wall("muret_ouest", [(-x, s_) for x, s_ in east], 1.2, 0.6, "wall")
        e_s = [p for p in east if p[1] > PORT_S + 1.8]; e_n = [p for p in east if p[1] < PORT_S - 1.8]
        wall("muret_est_sud", e_s, 1.2, 0.6, "wall"); wall("muret_est_nord", e_n, 1.2, 0.6, "wall")
        px = ell_x(PORT_S)
        for k, ds in enumerate((-1.9, 1.9)):
            cyl(f"portillon_pilier{k+1}", px, PORT_S + ds, 0.45, 0, 2.0, "wall", segs=8)
        box("portillon_grille", px - 0.1, px + 0.1, PORT_S - 1.5, PORT_S + 1.5, 0.1, 1.9, "door")
    wall("muret_exedre", [(EX_R * math.cos(a), EX_C[1] + EX_R * math.sin(a)) for a in [math.pi * i / 32 for i in range(33)]], 1.6, 0.7, "wall")
    # Murets courbes de la clairière, au nord du massif, de part et d'autre de l'arche (comme sur garden-day :
    # banc devant le muret ouest, fontaine murale dans le muret est) ; ouverture au nord pour l'allée.
    R_W = CL["walls"]
    rr_ = CL["rot"]
    for nm, a0, a1 in (("ouest", 195 + rr_, CL["gap"][0] + rr_), ("est", CL["gap"][1] + rr_, 345 + rr_)):
        wall(f"muret_clairiere_{nm}", [(R_W * math.cos(math.radians(a)), MS + R_W * math.sin(math.radians(a))) for a in [a0 + (a1 - a0) * i / 16 for i in range(17)]], 1.6, 0.7, "wall")
    # Allées de gravier (partie à la française)
    box("allee_centrale", -3.5, 3.5, 33.5, 136, 0.06, 0.11, "gravel")
    cyl("rond_point", 0, 141, 8.0, 0.06, 0.11, "gravel", segs=40)
    L = ell_x(88, 10)
    box("allee_transversale", -L, L, 86.5, 89.5, 0.06, 0.11, "gravel")
    cyl("fontaine_rond", FOUNT[0], FOUNT[1], 7.0, 0.06, 0.2, "gravel", segs=40)
    # Allées de ceinture
    for sg, nm in ((1, "est"), (-1, "ouest")):
        a, b = GA - 7, GB - 7
        ts = [math.asin((s - GCs) / b) for s in ((50.0 if LATERAUX else 38.0), 175.0)]
        ring = [(sg * a * math.cos(t), GCs + b * math.sin(t)) for t in [ts[0] + (ts[1] - ts[0]) * i / 40 for i in range(41)]]
        tail = [(sg * 55, 186), (sg * 30, 193), (sg * 8, 196.5)]
        ribbon(f"allee_ceinture_{nm}", ring + tail, 3.0, "gravel", lift=0.09)
    if not LATERAUX: px = ell_x(PORT_S); ribbon("allee_portillon", [(px - 1.5, PORT_S), (ell_x(PORT_S + 2, 7) + 0.5, PORT_S + 2.5)], 2.5, "gravel", lift=0.09)
    # Allée sinueuse du bosquet, jusqu'au parvis du massif
    WIND = [(0, 146), (9, 154), (13, 162), (6, 170), (-7, 177), (-10, 185), (-4, 192), (0, 197), ((CL["arch_d"] + 4) * math.sin(ROT), MS - (CL["arch_d"] + 4) * math.cos(ROT)), ((CL["parvis"] - 0.5) * math.sin(ROT), MS - (CL["parvis"] - 0.5) * math.cos(ROT))]
    ribbon("allee_sinueuse", WIND, 3.6, "gravel", lift=0.09, step=1.5)
    cyl("parvis_massif", 0, MS, CL["parvis"], 0.06, 0.10, "gravel", segs=48)
    # Parterres de buis en broderies
    quads = {"NO": (-70, -8, 40, 83), "NE": (8, 70, 40, 83), "SO": (-72, -8, 93, 135), "SE": (8, 72, 93, 135)}
    for nm, (x0, x1, s0, s1) in quads.items():
        border = clip(rrect(x0, x1, s0, s1, 6), 13)
        prism(f"parterre_{nm}_fond", border, 0.06, 0.16, "lawn")
        wall(f"parterre_{nm}_bordure", border + border[:1], 0.6, 0.5, "box")
        band = clip(rrect(x0 + 1.6, x1 - 1.6, s0 + 1.6, s1 - 1.6, 5.5), 14.6)   # plate-bande fleurie le long de la bordure
        wall(f"parterre_{nm}_plate_bande", band + band[:1], 0.55, 1.6, "flowers" if nm in ("NO", "SE") else "lavender", z0=0.1)
        inner = clip(rrect(x0 + 4, x1 - 4, s0 + 4, s1 - 4, 5), 17)
        wall(f"parterre_{nm}_broderie1", inner + inner[:1], 0.5, 0.4, "box")
        cx, cs = (x0 + x1) / 2, (s0 + s1) / 2; hw, hs = (x1 - x0) / 2 - 8, (s1 - s0) / 2 - 8
        if nm == "SO":   # la fontaine occupe le centre : une couronne de buis autour de son rond de gravier
            ring = [(FOUNT[0] + 9.5 * math.cos(a), FOUNT[1] + 9.5 * math.sin(a)) for a in [2 * math.pi * i / 40 for i in range(41)]]
            wall(f"parterre_{nm}_broderie2", ring, 0.5, 0.4, "box")
        else:
            for k, ph in enumerate((0.0, math.pi)):
                curve = clip([(cx + hw * u, cs + hs * 0.55 * math.sin(math.pi * 1.5 * u + ph)) for u in [i / 20 * 2 - 1 for i in range(21)]], 18)
                wall(f"parterre_{nm}_broderie{k+2}", curve, 0.5, 0.4, "box")
        for k, (fx, fs) in enumerate([(cx - hw * 0.5, cs - hs * 0.55), (cx + hw * 0.5, cs + hs * 0.55), (cx - hw * 0.5, cs + hs * 0.55), (cx + hw * 0.5, cs - hs * 0.55)]):
            (fx, fs), = clip([(fx, fs)], 18)
            cyl(f"parterre_{nm}_fleurs{k+1}", fx, fs, 3.2, 0.06, 0.5, "flowers" if k % 2 == 0 else "lavender", segs=16, sy=0.6)
        # 2026-11-19 (auteur : jardin « fourni plutôt que dénudé ») : les compartiments de gazon entre les
        # broderies se garnissent de petits massifs de roses et de lavande, sur une trame de 5 m, à l'écart
        # des haies de buis, de la bordure, de la fontaine et des grands massifs.
        curves = [inner + inner[:1]]
        if nm != "SO":
            curves += [clip([(cx + hw * u, cs + hs * 0.55 * math.sin(math.pi * 1.5 * u + ph)) for u in [i / 40 * 2 - 1 for i in range(41)]], 18) for ph in (0.0, math.pi)]
        big = [(cx - hw * 0.5, cs - hs * 0.55), (cx + hw * 0.5, cs + hs * 0.55), (cx - hw * 0.5, cs + hs * 0.55), (cx + hw * 0.5, cs - hs * 0.55)]
        rnd_p = random.Random(sum(map(ord, nm))); kk = 0   # graine stable (hash() change à chaque session)
        gx = x0 + 7.5
        while gx < x1 - 7:
            gs = s0 + 7.5
            while gs < s1 - 7:
                px_, ps_ = gx + rnd_p.uniform(-0.8, 0.8), gs + rnd_p.uniform(-0.8, 0.8)
                ok = all(poly_dist((px_, ps_), c) > 2.7 for c in curves)
                ok = ok and abs(px_) < ell_x(ps_, 20) and all((px_ - bx) ** 2 + (ps_ - bs) ** 2 > 5.5 ** 2 for bx, bs in big)
                if nm == "SO": ok = ok and (px_ - FOUNT[0]) ** 2 + (ps_ - FOUNT[1]) ** 2 > 12.5 ** 2
                if ok:
                    kk += 1
                    cyl(f"parterre_{nm}_massif{kk:02d}", px_, ps_, rnd_p.uniform(1.5, 2.2), 0.06, 0.45,
                        ("flowers", "lavender", "flowers")[kk % 3], segs=14, sy=0.75)
                gs += 5.0
            gx += 5.0
    W["_cur"][0] = bpy.data.collections["AUR_20_jardin"]
    # ------------------------------------------------------------------ AUR_21_massif_et_reperes
    empty_collection("AUR_21_massif_et_reperes")
    cyl("massif_bordure", 0, MS, CL["bed"] + 0.3, 0, 0.45, "wall", segs=32); cyl("massif", 0, MS, CL["bed"], 0.45, 0.75, "massif", segs=32)
    cyl("REPERE_Rose_tige", 0, MS, 0.04, 0.75, 1.35, "hedge", segs=8); ball("REPERE_Rose", 0, MS, 1.45, 0.14, "rose")
    arch("REPERE_arche_roses", ARCH_X, ARCH_S, 8.0, 5.2, 1.4, 0.8, "arch")
    bpy.data.objects["REPERE_arche_roses"]["p3d_rotz"] = -CL["rot"]   # lu par place_garden_props.py
    for sg, nm in ((-1, "ouest"), (1, "est")):
        arch(f"petite_arche_{nm}", sg * ell_x(150, 7), 150, 4.5, 3.4, 1.0, 0.5, "arch_small")
    x0, x1, s0, s1 = SERRE; sc = (s0 + s1) / 2
    box("REPERE_serre", x0, x1, s0, s1, 0, 3, "greenhouse")
    bm = bmesh.new(); N = 12; prof = [(5 * math.cos(math.pi * i / N), 3 + 3 * math.sin(math.pi * i / N)) for i in range(N + 1)]
    a_ = [bm.verts.new((x0, -(sc + u), z)) for u, z in prof]; b_ = [bm.verts.new((x1, -(sc + u), z)) for u, z in prof]
    bm.faces.new(a_); bm.faces.new(b_)
    for i in range(N): bm.faces.new((a_[i], a_[i + 1], b_[i + 1], b_[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); W["obj"]("REPERE_serre_toit", bm, "greenhouse")
    box("REPERE_serre_porte", x1, x1 + 0.2, sc - 1.0, sc + 1.0, 0, 2.4, "door")
    fx, fs = FOUNT
    cyl("fontaine_vasques", fx, fs, 3.5, 0.2, 0.8, "water"); cyl("fontaine_vasques_fut", fx, fs, 0.35, 0.8, 2.2, "water", segs=12)
    cyl("fontaine_vasques_haut", fx, fs, 1.6, 2.2, 2.6, "water", r_top=1.9)
    box("fontaine_murale", 13, 16, MS - 6, MS - 4.5, 0, 1.8, "water"); box("banc", -15, -11, MS - 6, MS - 4.4, 0, 0.5, "bench")
    # ------------------------------------------------------------------ AUR_22_arbres
    empty_collection("AUR_22_arbres")
    # Haute haie d'ifs le long de l'allée est (côté parterres), du portillon à la serre
    a, b = GA - 10.5, GB - 10.5
    hedge = [(a * math.cos(t), GCs + b * math.sin(t)) for t in [math.asin((s - GCs) / b) for s in [44 + (s0 - 46) * i / 30 for i in range(31)]]]
    wall("haie_ifs_est", hedge, 3.0, 1.4, "yew")
    # Ifs en cône : rythme le long de l'allée centrale, et aux coins des parterres
    n = 0
    for s in range(46, 134, 14):
        if 84 <= s <= 92: continue
        for sg in (-1, 1):
            n += 1; cyl(f"if_allee_{n:02d}", sg * 6.5, s, 1.1, 0.06, 3.6, "yew", r_top=0.0, segs=12)
    for nm, (x0q, x1q, s0q, s1q) in quads.items():
        for k, (x, s) in enumerate(clip([(x0q + 3, s0q + 3), (x1q - 3, s0q + 3), (x0q + 3, s1q - 3), (x1q - 3, s1q - 3)], 16)):
            cyl(f"if_{nm}_{k+1}", x, s, 1.0, 0.16, 3.2, "yew", r_top=0.0, segs=12)
        if nm != "SO":
            (x, s), = clip([((x0q + x1q) / 2, (s0q + s1q) / 2)], 18)
            cyl(f"if_{nm}_centre", x, s, 1.3, 0.16, 4.2, "yew", r_top=0.0, segs=12)
    # Quelques grands arbres le long du muret, côté nord (encadrent les parterres)
    for i, (x, s, r) in enumerate([(-78, 72, 7), (78, 72, 7), (-84, 104, 7.5), (84, 104, 6.5)]):
        if not (SERRE[0] - 6 < x < SERRE[1] + 6 and SERRE[2] - 6 < s < SERRE[3] + 6):
            cyl(f"feuillu_bord{i+1}_tronc", x, s, 0.6, 0, r * 0.8, "bench", segs=8); ball(f"feuillu_bord{i+1}", x, s, r * 1.3, r, "tree", sz=0.85)
    # Bosquet : arbres ronds, cyprès, arbustes et fleurs, hors des allées et de la clairière
    paths = [WIND, [(0, 141), (0, 146)]]
    for sg in (1, -1):
        a2, b2 = GA - 7, GB - 7
        ring = [(sg * a2 * math.cos(t), GCs + b2 * math.sin(t)) for t in [math.asin((s - GCs) / b2) for s in [140 + 35 * i / 14 for i in range(15)]]]
        paths.append(ring + [(sg * 55, 186), (sg * 30, 193), (sg * 8, 196.5)])
    def free(x, s, clear_path):
        if (x / (GA - 6)) ** 2 + ((s - GCs) / (GB - 6)) ** 2 > 1: return False
        if math.hypot(x - EX_C[0], s - EX_C[1]) < EX_R + 6: return False
        if math.hypot(x, s - MS) < CL["free_r"] and s > ARCH_S - 2: return False
        if math.hypot(x, s - 141) < 11: return False
        if SERRE[0] - 5 < x < SERRE[1] + 5 and SERRE[2] - 5 < s < SERRE[3] + 5: return False
        return all(poly_dist((x, s), p) > clear_path for p in paths)
    k = 0
    for gs in range(148, 214, 7):
        for gx in range(-90, 91, 7):
            x, s = gx + rnd.uniform(-2.5, 2.5), gs + rnd.uniform(-2.5, 2.5)
            r = rnd.random()
            near_axis = s > 168 and abs(x) < 9          # garde la vue de la clairière vers la flèche de la tour
            vh = vista_max_h(x, s)
            if r < 0.62 and free(x, s, 6.5) and not near_axis:
                k += 1; rr = rnd.uniform(4.0, 6.5)
                if vh is not None and rr * 2.35 > vh: rr = vh / 2.35
                if rr >= 2.8:
                    cyl(f"bosquet_arbre{k:03d}_tronc", x, s, 0.5, 0, rr * 0.9, "bench", segs=8)
                    ball(f"bosquet_arbre{k:03d}", x, s, rr * 1.35, rr, "grove" if k % 3 else "tree", sz=0.9)
                else:
                    ball(f"bosquet_arbuste{k:03d}", x, s, 1.0, min(2.4, max(1.2, (vh or 4) / 2.2)), "shrub", sz=0.7)
            elif r < 0.75 and free(x, s, 4.0) and not near_axis:
                hc = rnd.uniform(10, 13)
                if vh is None or hc <= vh:
                    k += 1; cyl(f"bosquet_cypres{k:03d}", x, s, 1.5, 0, hc, "cypress", r_top=0.0, segs=12)
            if free(x + 3, s + 2, 3.0) and rnd.random() < 0.7:
                k += 1; ball(f"bosquet_arbuste{k:03d}", x + 3, s + 2, 1.0, rnd.uniform(1.4, 2.4), "shrub", sz=0.7)
            if free(x - 2, s + 3, 2.6) and rnd.random() < 0.35:
                k += 1; cyl(f"bosquet_fleurs{k:03d}", x - 2, s + 3, rnd.uniform(1.5, 2.5), 0.06, 0.6, "flowers" if k % 2 else "lavender", segs=12)
    if LATERAUX:   # jardins latéraux : grands arbres ronds contre le muret, cyprès le long de l'allée
        for sg, nm in ((1, "est"), (-1, "ouest")):
            for i, (x, s_) in enumerate(((59, -7), (61.5, 7), (61.5, 21), (59, 34))):
                rr = 4.6
                cyl(f"feuillu_bord_lat_{nm}{i+1}_tronc", sg * x, s_, 0.5, 0, rr * 0.9, "bench", segs=8)
                ball(f"feuillu_bord_lat_{nm}{i+1}", sg * x, s_, rr * 1.35, rr, "grove", sz=0.9)
            for i, s_ in enumerate((-3, 11, 25)):
                cyl(f"cypres_lat_{nm}{i+1}", sg * 54.0, s_, 1.5, 0, 11.0, "cypress", r_top=0.0, segs=12)
    # Couronne d'arbres autour de la clairière (ouverte au nord, sur l'arche)
    # Au nord, de part et d'autre de l'arche, des arbustes seulement : depuis la clairière, la flèche
    # de la tour de l'horloge dépasse des cimes du bosquet, au loin.
    for i in range(16):
        ang = math.radians(200 + CL["rot"] + 140 * i / 15)   # moitié nord de la clairière, sauf l'arche
        off = abs(math.degrees(ang) - 270 - CL["rot"])
        if off < 14: continue
        x, s = CL["ring"] * math.cos(ang), MS + CL["ring"] * math.sin(ang); k += 1
        if off < 40:
            ball(f"clairiere_arbuste{i+1:02d}", x, s, 1.2, rnd.uniform(2.2, 3.0), "shrub", sz=0.8)
            continue
        rr = rnd.uniform(4.5, 6.0); vh = vista_max_h(x, s)
        if vh is not None and rr * 2.35 > vh:
            ball(f"clairiere_arbuste{i+1:02d}", x, s, 1.2, 2.4, "shrub", sz=0.8); continue
        cyl(f"clairiere_arbre{i+1:02d}_tronc", x, s, 0.5, 0, rr * 0.9, "bench", segs=8)
        ball(f"clairiere_arbre{i+1:02d}", x, s, rr * 1.35, rr, "grove", sz=0.9)
    return {c: len(bpy.data.collections[c].objects) for c in ("AUR_20_jardin", "AUR_21_massif_et_reperes", "AUR_22_arbres")}
