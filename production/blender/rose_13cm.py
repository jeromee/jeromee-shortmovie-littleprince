"""Rose à fleur de 13 cm (demande de l'auteur, 2026-11-23).

Le modèle Tripo PROP_rose_endormie (1,15 m) avait une fleur de ~0,50 m de diamètre et un feuillage de ~0,60 m d'envergure.
On déforme le maillage (partagé par PROP_rose_endormie, ROSE_provisoire et la Rose de SC03) :
  - fleur (îlots aux couleurs des pétales, sépales) : mise à l'échelle uniforme K = 0,13 / diamètre mesuré, centre de la fleur remonté à Z_CENTRE (≈ hauteur
    de ROSE_F, inchangée) ;
  - feuilles et tige au-dessus de Z_TIGE : écart horizontal à l'axe × H_FEUILLES, puis décalées vers le haut ;
  - tige nue sous Z_TIGE : allongée pour combler.
Rejouable une seule fois sur un maillage d'origine : la propriété "rose_13cm" marque le maillage déjà traité.
Copie d'avant : production/blender/world_avant-rose-13cm.blend.
"""
import bpy

ZB = 0.74          # bas de la fleur (sépales compris au-dessus), en z local du modèle
Z_TIGE = 0.26      # au-dessous : tige nue
DIAM = 0.13        # diamètre visé de la fleur
Z_CENTRE = 1.00    # centre de la fleur visé (z local) ; + 0,23 au-dessus du sol = 1,23 m ≈ ROSE_F
H_FEUILLES = 0.50  # resserrement horizontal du feuillage et de la tige


def _ilots(me):
    """Îlots du maillage avec leur teinte moyenne (texture) : pétales h ≈ 0,11, feuilles et tige h ≈ 0,30."""
    import bmesh, colorsys
    bm = bmesh.new(); bm.from_mesh(me); bm.verts.ensure_lookup_table()
    uvl = bm.loops.layers.uv.active
    img = [n.image for n in me.materials[0].node_tree.nodes if n.type == "TEX_IMAGE"][0]
    W, H = img.size; px = img.pixels[:]
    seen = set(); out = []
    for v in bm.verts:
        if v.index in seen: continue
        st = [v]; comp = []; seen.add(v.index)
        while st:
            x = st.pop(); comp.append(x.index)
            for e in x.link_edges:
                o = e.other_vert(x)
                if o.index not in seen: seen.add(o.index); st.append(o)
        hs = []
        for i in comp[::max(1, len(comp) // 50)]:
            l = bm.verts[i].link_loops
            if l:
                u, w = l[0][uvl].uv; k = (int(w % 1 * H) * W + int(u % 1 * W)) * 4
                hs.append(colorsys.rgb_to_hsv(*px[k:k + 3])[0])
        out.append((comp, sum(hs) / len(hs) if hs else 0.3))
    bm.free()
    return out


def appliquer(name="PROP_rose_endormie"):
    me = bpy.data.objects[name].data
    if me.get("rose_13cm"):
        print("déjà fait"); return me
    vs = me.vertices
    fleur = set()
    for comp, h in _ilots(me):
        zs = [vs[i].co.z for i in comp]
        if 0.05 < h < 0.20 or min(zs) >= 0.66:          # pétales, ou sépales collés à la fleur
            fleur.update(comp)
        else:                                              # tige : sa partie haute, cachée dans la fleur, suit la fleur
            fleur.update(i for i in comp if vs[i].co.z >= ZB)
    pts = [vs[i].co for i in fleur]
    xs = [c.x for c in pts]; ys = [c.y for c in pts]; zs = [c.z for c in pts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    diam = max(max(xs) - min(xs), max(ys) - min(ys))
    k = DIAM / diam
    zb = min(zs); z_mid = (zb + max(zs)) / 2
    st = [v.co for v in vs if v.co.z < Z_TIGE]
    ax, ay = sum(c.x for c in st) / len(st), sum(c.y for c in st) / len(st)
    new_zb = Z_CENTRE - (z_mid - zb) * k
    dz = new_zb - zb
    for v in vs:
        c = v.co
        if v.index in fleur:
            c.x = ax + (c.x - cx) * k
            c.y = ay + (c.y - cy) * k
            c.z = new_zb + (c.z - zb) * k
        elif c.z >= Z_TIGE:
            c.x = ax + (c.x - ax) * H_FEUILLES
            c.y = ay + (c.y - ay) * H_FEUILLES
            c.z = c.z + dz
        else:
            c.x = ax + (c.x - ax) * H_FEUILLES
            c.y = ay + (c.y - ay) * H_FEUILLES
            c.z = c.z * (Z_TIGE + dz) / Z_TIGE
    me.update()
    me["rose_13cm"] = 1
    me["rose_axe"] = (ax, ay)
    print("fleur : %d sommets, diamètre d'origine %.3f, k %.3f, axe (%.3f, %.3f), fleur %.3f–%.3f, décalage %.3f"
          % (len(fleur), diam, k, ax, ay, new_zb, new_zb + (max(zs) - zb) * k, dz))
    return me


def epines_discretes(name="PROP_rose_endormie", sat=0.35, val=0.85):
    """Épines moins rouges : dans la texture, les pixels rouge-brun saturés perdent de la saturation (vers le vert-brun de la tige)."""
    import colorsys
    me = bpy.data.objects[name].data
    img = [n.image for n in me.materials[0].node_tree.nodes if n.type == "TEX_IMAGE"][0]
    if img.get("epines_discretes"):
        print("déjà fait"); return
    px = list(img.pixels); n = 0
    for i in range(0, len(px), 4):
        r, g, b = px[i:i + 3]
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        if (h < 0.04 or h > 0.93) and s > 0.45 and v < 0.75:     # rouge / bordeaux
            r, g, b = colorsys.hsv_to_rgb(0.22, s * sat, v * val)  # brun-vert éteint
            px[i:i + 3] = (r, g, b); n += 1
    img.pixels[:] = px; img["epines_discretes"] = 1
    img.pack()
    print("pixels modifiés", n, "sur", len(px) // 4)


# ---------------------------------------------------------------------------------------------------------------------------
# v2 (2026-11-23, soir) : diamètre réglable (test à 20 cm demandé par l'auteur) et feuilles réparties sur la tige, y compris
# sur son tiers du milieu. On repart toujours du maillage d'origine (world_avant-rose-13cm.blend).
#   - fleur : échelle uniforme DIAM / diamètre d'origine, centre à Z_CENTRE ;
#   - tige : allongée linéairement de [0, bas de la fleur] vers [0, nouveau bas de la fleur], amincie (× TIGE) ;
#   - feuilles : chaque groupe de feuilles (îlots voisins) est déplacé d'un bloc le long de la tige (son point d'attache suit
#     l'allongement) et réduit uniformément (× FEUILLE) autour de son point d'attache : elles gardent leur forme.
import os, math
from mathutils import Vector
BACKUP = os.path.join(os.path.dirname(os.path.abspath(__file__)) if "__file__" in globals() else "", "world_avant-rose-13cm.blend")


def _original_coords(path):
    with bpy.data.libraries.load(path) as (src, dst):
        dst.meshes = ["PROP_rose_endormie_mesh.002"]
    m = dst.meshes[0]
    co = [v.co.copy() for v in m.vertices]
    return m, co


def appliquer_v2(diam=0.20, z_centre=1.00, tige=0.6, feuille=0.55, r_tige=0.035, path=None, name="PROP_rose_endormie"):
    me = bpy.data.objects[name].data
    orig, co = _original_coords(path or BACKUP)
    ilots = _ilots(orig)
    bpy.data.meshes.remove(orig)
    st = [c for c in co if c.z < Z_TIGE]
    ax, ay = sum(c.x for c in st) / len(st), sum(c.y for c in st) / len(st)
    # ligne médiane de la tige (elle se courbe vers le haut) : centre, bande de 2 cm par bande, des longs îlots fins verticaux
    info = []
    for comp, h in ilots:
        P = [co[i] for i in comp]
        zs = [c.z for c in P]
        dx = max(c.x for c in P) - min(c.x for c in P); dy = max(c.y for c in P) - min(c.y for c in P)
        info.append((comp, h, P, min(zs), max(zs), dx, dy))
    B = 0.02; bands = {}
    for comp, h, P, z0, z1, dx, dy in info:
        if not (0.05 < h < 0.20) and z1 - z0 > 0.10 and max(dx, dy) < 0.10:
            for c in P: bands.setdefault(int(c.z / B), []).append(c)
    keys = sorted(bands)
    def _med(v): v = sorted(v); return v[len(v) // 2]
    cen_b = {k_: (_med([c.x for c in bands[k_]]), _med([c.y for c in bands[k_]])) for k_ in keys}   # médiane : robuste
    def axe(z):
        q = z / B - 0.5
        lo = max([k_ for k_ in keys if k_ <= q], default=keys[0]); hi = min([k_ for k_ in keys if k_ >= q], default=keys[-1])
        if hi == lo: return cen_b[lo]
        u = (q - lo) / (hi - lo); return (cen_b[lo][0] * (1 - u) + cen_b[hi][0] * u, cen_b[lo][1] * (1 - u) + cen_b[hi][1] * u)
    def r(c):
        a_ = axe(c.z); return math.hypot(c.x - a_[0], c.y - a_[1])
    fleur, feuilles, verts_hauts = set(), [], []
    for comp, h, P, z0, z1, dx, dy in info:
        if 0.05 < h < 0.20: fleur.update(comp)
        elif z0 >= 0.66: verts_hauts.append(comp)                        # sépales… ou pétiole d'une feuille haute
        elif sum(1 for c in P if r(c) < 0.03) > 0.5 * len(P): pass       # tige (autour de sa ligne médiane)
        else: feuilles.append(comp)                                       # limbes, pétioles, épines : groupés, réduits sans déformation
    # un îlot vert sous la fleur qui touche une feuille appartient à cette feuille (pétiole) ; sinon c'est un sépale
    from mathutils import kdtree as _kd
    fv = [i for comp in feuilles for i in comp]
    kdf = _kd.KDTree(len(fv))
    for i in fv: kdf.insert(co[i], i)
    kdf.balance()
    for comp in verts_hauts:
        if any(kdf.find_range(co[i], 0.004) for i in comp): feuilles.append(comp)
        else: fleur.update(comp)
    pts = [co[i] for i in fleur]
    xs = [c.x for c in pts]; ys = [c.y for c in pts]; zs = [c.z for c in pts]
    cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
    k = diam / max(max(xs) - min(xs), max(ys) - min(ys))
    zb = min(zs); z_mid = (zb + max(zs)) / 2
    new_zb = z_centre - (z_mid - zb) * k
    f = lambda z: z * new_zb / zb                      # allongement de la tige
    # regrouper les îlots d'une même feuille (limbe, pétiole, folioles) : îlots dont des sommets se touchent (< 4 mm)
    from mathutils import kdtree
    owner = {}
    for n, comp in enumerate(feuilles):
        for i in comp: owner[i] = n
    kd = kdtree.KDTree(len(owner))
    for i in owner: kd.insert(co[i], i)
    kd.balance()
    par = list(range(len(feuilles)))
    def find(i):
        while par[i] != i: par[i] = par[par[i]]; i = par[i]
        return i
    for i, n in owner.items():
        for _, j, _ in kd.find_range(co[i], 0.004):
            m = owner[j]
            if m != n: par[find(n)] = find(m)
    groupes = {}
    for i, comp in enumerate(feuilles): groupes.setdefault(find(i), []).extend(comp)
    new = [c.copy() for c in co]
    top = axe(zb)
    for i, c in enumerate(co):                         # tige (et tout ce qui n'est ni fleur ni feuille)
        if i in fleur:                                 # fleur centrée sur le haut de la tige
            new[i].x = top[0] + (c.x - cx) * k; new[i].y = top[1] + (c.y - cy) * k; new[i].z = new_zb + (c.z - zb) * k
        else:                                          # tige amincie autour de sa ligne médiane
            a_ = axe(min(c.z, zb))
            new[i].x = a_[0] + (c.x - a_[0]) * tige; new[i].y = a_[1] + (c.y - a_[1]) * tige
            new[i].z = f(c.z) if c.z < zb else new_zb + (c.z - zb) * k
    # chaque groupe de feuilles suit le point qu'il touche (tige ou autre feuille déjà placée) : rien ne se détache
    from mathutils import kdtree
    gid = {}
    for g, comp in groupes.items():
        for i in comp: gid[i] = g
    ancre = {}
    for g, comp in groupes.items():
        others = [j for j in range(len(co)) if gid.get(j) != g and j not in fleur]   # jamais la fleur (elle est réduite à part)
        kd_o = kdtree.KDTree(len(others))
        for j in others: kd_o.insert(co[j], j)
        kd_o.balance()
        best = None
        for i in comp:
            c_, j, d = kd_o.find(co[i])
            if best is None or d < best[2]: best = (i, j, d)
        ancre[g] = best
    place = set(i for i in range(len(co)) if i not in gid)
    reste = dict(groupes)
    while reste:
        prog = False
        for g, comp in list(reste.items()):
            i, j, d = ancre[g]
            if j not in place: continue
            gi = co[i]; oj = co[j]
            ni = new[j] + (gi - oj) * feuille
            for q in comp: new[q] = ni + (co[q] - gi) * feuille
            place.update(comp); del reste[g]; prog = True
        if not prog:                                   # cycle : on rattache le reste à la tige
            for g, comp in reste.items():
                att = min((co[q] for q in comp), key=r); a_ = axe(att.z); tgt = Vector((a_[0] + (att.x - a_[0]) * tige, a_[1] + (att.y - a_[1]) * tige, f(att.z)))
                for q in comp: new[q] = tgt + (co[q] - att) * feuille
            break
    # dernière vérification : une feuille qui ne touche plus rien (écart > 3 mm) est rapprochée de ce qu'elle touchait
    for g, comp in groupes.items():
        if any(i in fleur for i in comp): continue
        cs = set(comp)
        others = [j for j in range(len(new)) if j not in cs and j not in fleur]
        kd_n = kdtree.KDTree(len(others))
        for j in others: kd_n.insert(new[j], j)
        kd_n.balance()
        best = None
        for i in comp:
            c_, j, d = kd_n.find(new[i])
            if best is None or d < best[2]: best = (i, j, d)
        i, j, d = best
        if d > 0.003:
            mv = (new[j] - new[i]) * (1 - 0.0015 / d)
            for q in comp: new[q] = new[q] + mv
            print("feuille rapprochée de %.1f cm" % (d * 100))
    for v, c in zip(me.vertices, new): v.co = c
    me.update()
    me["rose_13cm"] = 1; me["rose_diametre"] = diam; me["rose_axe"] = tuple(top)
    print("fleur %.2f m (k %.3f), centre %.2f, bas %.3f ; %d groupes de feuilles" % (diam, k, z_centre, new_zb, len(groupes)))
    return me
