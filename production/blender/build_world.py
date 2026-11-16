# Blockout d'Aurelia — construit le monde maître d'après kb/world/site-plan.md (v2).
# Usage dans Blender : exec(compile(open(chemin, encoding="utf-8").read(), chemin, "exec")) ; build()
# Idempotent : supprime et reconstruit les collections « AUR_* ». Ne touche à rien d'autre.
# Repère : X = est, Y = nord, Z = haut. Coordonnées du plan (x, y_sud) -> Blender (x, -y_sud).
# Origine : centre de la tour de l'horloge, au niveau du jardin (z = 0).
import bpy, bmesh, math
from mathutils import Vector, Matrix

ALENTOURS = {"riviere": [[-248.1, -60.7], [-213.1, -33.1], [-188.1, -12.6], [-165.0, 21.6], [-153.5, 56.8], [-147.9, 85.6], [-135.7, 111.0], [-117.1, 131.1], [-96.3, 147.6], [-80.4, 162.6], [-65.7, 176.9], [-53.9, 188.0]], "pont_nord": [[-207.7, -31.8]], "pont_sud": [[-98.8, 144.3]], "chemin_ouest": [[-113.9, -97.7], [-144.5, -82.1], [-184.3, -61.2], [-206.1, -27.8], [-221.1, 1.3]], "chemin_sud_ouest": [[-86.0, 151.7], [-106.2, 160.1], [-126.2, 170.1], [-139.9, 178.7]], "chemin_village": [[112.3, -162.0], [105.4, -232.2], [108.2, -295.9], [142.7, -402.2]], "chemin_est": [[133.6, -79.9], [167.1, -25.5], [181.9, 40.7], [178.4, 85.1], [152.5, 112.2], [117.1, 136.0], [89.5, 155.9], [74.7, 180.3]], "verger": [[130.6, 47.8], [177.5, 41.4], [156.2, 94.2], [115.5, 98.2]], "haies": [[177.2, -180.6], [340.8, -241.8], [153.3, -76.1], [229.5, -16.4], [234.8, -219.9], [145.1, 0.3]]}
GARDEN_DEPTH = 1.4         # jardin allongé de 40 % du nord au sud (2026-11-15, auteur)
def Y(y):
    """Coordonnée nord-sud du plan après allongement du jardin : inchangée côté palais (y <= 32)."""
    return y if y <= 32 else 32 + (y - 32) * GARDEN_DEPTH
R_PLANET = 2000.0          # rayon de la planète (diamètre 4 km) — à ajuster
TERRACE_Z = 4.0            # la terrasse domine le jardin de 4 m
COLORS = {                 # code couleur des repères (voir kb/world/site-plan.md)
    "planet": (0.33, 0.50, 0.26), "plateau": (0.33, 0.50, 0.26),   # plateau = prairie (2026-11-15 : en gris, il passait pour un second muret)
    "lawn": (0.45, 0.62, 0.33),
    "path": (0.80, 0.74, 0.60), "hedge": (0.25, 0.42, 0.22), "wall": (0.55, 0.52, 0.46),
    "palace": (0.85, 0.72, 0.42), "tower": (0.72, 0.55, 0.22), "roof": (0.30, 0.33, 0.45),
    "terrace": (0.90, 0.84, 0.68), "clock": (0.95, 0.95, 0.92),
    "massif": (0.90, 0.50, 0.60), "rose": (0.95, 0.80, 0.15), "arch": (0.78, 0.40, 0.48),
    "arch_small": (0.70, 0.55, 0.58), "greenhouse": (0.35, 0.80, 0.85), "water": (0.45, 0.60, 0.80),
    "bench": (0.50, 0.33, 0.18), "cypress": (0.10, 0.28, 0.16), "tree": (0.30, 0.50, 0.22),
    "village": (0.75, 0.45, 0.35), "forest": (0.16, 0.34, 0.18), "river": (0.35, 0.55, 0.75), "orchard": (0.40, 0.55, 0.25),
    "door": (0.40, 0.15, 0.08), "elias": (0.05, 0.25, 0.85), "queen": (0.85, 0.10, 0.10),
    "chamberlain": (0.10, 0.65, 0.20),
}
_mats = {}
def M(key):
    if key not in _mats:
        name = "AUR_" + key
        m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
        rgb = COLORS[key]; m.diffuse_color = (*rgb, 1)
        try:
            if m.node_tree is None: m.use_nodes = True
            b = m.node_tree.nodes.get("Principled BSDF")
            if b: b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Roughness"].default_value = 0.8
        except Exception: pass
        _mats[key] = m
    return _mats[key]

_cur = [None]
def coll(name):
    c = bpy.data.collections.new("AUR_" + name); bpy.context.scene.collection.children.link(c); _cur[0] = c; return c
def obj(name, bm, mat, smooth=False):
    me = bpy.data.meshes.new(name); bm.normal_update(); bm.to_mesh(me); bm.free()
    if smooth:
        for p in me.polygons: p.use_smooth = True
    o = bpy.data.objects.new(name, me); me.materials.append(M(mat)); _cur[0].objects.link(o); return o
def box(name, x0, x1, ys0, ys1, z0, z1, mat):
    bm = bmesh.new(); bmesh.ops.create_cube(bm, size=1)
    sx, sy, sz = abs(x1 - x0), abs(ys1 - ys0), abs(z1 - z0)
    bmesh.ops.scale(bm, vec=(sx, sy, sz), verts=bm.verts)
    bmesh.ops.translate(bm, vec=((x0 + x1) / 2, -(ys0 + ys1) / 2, (z0 + z1) / 2), verts=bm.verts)
    return obj(name, bm, mat)
def cyl(name, x, ys, r, z0, z1, mat, r_top=None, segs=32, sx=1.0, sy=1.0, rot=0.0):
    bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=segs, radius1=r, radius2=r if r_top is None else r_top, depth=z1 - z0)
    if rot: bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(rot, 3, "Z"), verts=bm.verts)
    bmesh.ops.scale(bm, vec=(sx, sy, 1), verts=bm.verts)
    bmesh.ops.translate(bm, vec=(x, -ys, (z0 + z1) / 2), verts=bm.verts)
    return obj(name, bm, mat, smooth=segs > 8)
def ball(name, x, ys, z, r, mat, sz=1.0):
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=r)
    bmesh.ops.scale(bm, vec=(1, 1, sz), verts=bm.verts); bmesh.ops.translate(bm, vec=(x, -ys, z), verts=bm.verts)
    return obj(name, bm, mat, smooth=True)
def prism(name, pts, z0, z1, mat):
    """Prisme vertical de base polygonale pts = [(x, y_sud), ...]."""
    bm = bmesh.new()
    lo = [bm.verts.new((x, -y, z0)) for x, y in pts]; hi = [bm.verts.new((x, -y, z1)) for x, y in pts]
    n = len(pts); bm.faces.new(lo); bm.faces.new(hi)
    for i in range(n): bm.faces.new((lo[i], lo[(i + 1) % n], hi[(i + 1) % n], hi[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); return obj(name, bm, mat)
def wall(name, pts, h, thick, mat, z0=0.0):
    """Muret le long d'une ligne brisée pts = [(x, y_sud), ...]."""
    bm = bmesh.new()
    for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
        a, b = Vector((xa, -ya, 0)), Vector((xb, -yb, 0)); d = b - a
        if d.length < 1e-6: continue
        nrm = Vector((-d.y, d.x, 0)).normalized() * thick / 2
        q = [a - nrm, b - nrm, b + nrm, a + nrm]
        lo = [bm.verts.new((v.x, v.y, z0)) for v in q]; hi = [bm.verts.new((v.x, v.y, z0 + h)) for v in q]
        bm.faces.new(lo); bm.faces.new(hi)
        for i in range(4): bm.faces.new((lo[i], lo[(i + 1) % 4], hi[(i + 1) % 4], hi[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); return obj(name, bm, mat)
def arch(name, x, ys, width, height, depth, thick, mat, along_x=True):
    """Arche : deux piliers + demi-cercle. along_x=True : l'ouverture enjambe une allée nord-sud."""
    r_out = width / 2; r_in = r_out - thick; zc = height - r_out
    bm = bmesh.new(); N = 12
    def add(quad):  # quad : 4 points (u, z) dans le plan de l'arche
        fr = [bm.verts.new((u, -depth / 2, z)) for u, z in quad]; bk = [bm.verts.new((u, depth / 2, z)) for u, z in quad]
        bm.faces.new(fr); bm.faces.new(bk)
        for i in range(4): bm.faces.new((fr[i], fr[(i + 1) % 4], bk[(i + 1) % 4], bk[i]))
    for s in (-1, 1): add([(s * r_in, 0), (s * r_out, 0), (s * r_out, zc), (s * r_in, zc)])
    for i in range(N):
        a0, a1 = math.pi * i / N, math.pi * (i + 1) / N
        add([(r_in * math.cos(a0), zc + r_in * math.sin(a0)), (r_out * math.cos(a0), zc + r_out * math.sin(a0)),
             (r_out * math.cos(a1), zc + r_out * math.sin(a1)), (r_in * math.cos(a1), zc + r_in * math.sin(a1))])
    if not along_x: bmesh.ops.rotate(bm, cent=(0, 0, 0), matrix=Matrix.Rotation(math.pi / 2, 3, "Z"), verts=bm.verts)
    bmesh.ops.translate(bm, vec=(x, -ys, 0), verts=bm.verts)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); return obj(name, bm, mat)
def hip(name, x0, x1, ys0, ys1, z0, h, mat):
    """Toit à quatre pans (croupes) sur le rectangle [x0,x1] x [ys0,ys1], faîtage dans le sens long."""
    bm = bmesh.new(); xa, xb = sorted((x0, x1)); ya, yb = sorted((-ys0, -ys1))
    w, d = xb - xa, yb - ya; zt = z0 + h
    base = [bm.verts.new(v) for v in ((xa, ya, z0), (xb, ya, z0), (xb, yb, z0), (xa, yb, z0))]
    if w >= d:
        r1 = bm.verts.new((xa + d / 2, (ya + yb) / 2, zt)); r2 = bm.verts.new((xb - d / 2, (ya + yb) / 2, zt))
        faces = [(base[0], base[1], r2, r1), (base[1], base[2], r2), (base[2], base[3], r1, r2), (base[3], base[0], r1)]
    else:
        r1 = bm.verts.new(((xa + xb) / 2, ya + w / 2, zt)); r2 = bm.verts.new(((xa + xb) / 2, yb - w / 2, zt))
        faces = [(base[0], base[1], r1), (base[1], base[2], r2, r1), (base[2], base[3], r2), (base[3], base[0], r1, r2)]
    for f in faces: bm.faces.new(f)
    bm.faces.new(base[::-1]); bmesh.ops.recalc_face_normals(bm, faces=bm.faces); return obj(name, bm, mat)
def ground_z(x, ys, PC=(0.0, 105.0)):
    """Altitude du sol au point du plan (x, y_sud) : plateau plat (z = 0) puis surface de la planète."""
    dx, dy = x - PC[0], ys - PC[1]
    if (dx / 115) ** 2 + (dy / 140) ** 2 <= 1: return 0.0
    r2 = dx * dx + dy * dy
    return math.sqrt(max(R_PLANET ** 2 - r2, 0)) - R_PLANET
def ribbon(name, pts, width, mat, lift=0.08, step=4.0):
    """Ruban posé sur le sol (rivière, chemin) le long d'une ligne pts = [(x, y_sud), ...]."""
    dense = []
    for (xa, ya), (xb, yb) in zip(pts[:-1], pts[1:]):
        n = max(1, int(math.hypot(xb - xa, yb - ya) / step))
        dense += [(xa + (xb - xa) * i / n, ya + (yb - ya) * i / n) for i in range(n)]
    dense.append(pts[-1])
    bm = bmesh.new(); prev = None
    for i, (x, y) in enumerate(dense):
        j0, j1 = max(i - 1, 0), min(i + 1, len(dense) - 1)
        tx, ty = dense[j1][0] - dense[j0][0], dense[j1][1] - dense[j0][1]; L = math.hypot(tx, ty) or 1
        nx, ny = -ty / L * width / 2, tx / L * width / 2
        a = bm.verts.new((x - nx, -(y - ny), ground_z(x - nx, y - ny) + lift)); b = bm.verts.new((x + nx, -(y + ny), ground_z(x + nx, y + ny) + lift))
        if prev: bm.faces.new((prev[0], prev[1], b, a))
        prev = (a, b)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); return obj(name, bm, mat)
def dummy(name, x, ys, z, height, mat):
    """Mannequin : corps (boîte) + tête (sphère)."""
    hr = height * 0.13
    box(name + "_corps", x - height * 0.13, x + height * 0.13, ys - height * 0.08, ys + height * 0.08, z, z + height - 2 * hr, mat)
    ball(name + "_tete", x, ys, z + height - hr, hr, mat)
def on_planet(dist, azimuth_deg, center):
    """Point et matrice d'orientation à 'dist' m du sommet (le long de la surface), azimut 0 = est, 90 = nord."""
    th = dist / R_PLANET; ph = math.radians(azimuth_deg)
    n = Vector((math.sin(th) * math.cos(ph), math.sin(th) * math.sin(ph), math.cos(th)))
    return center + n * R_PLANET, n.to_track_quat("Z", "Y").to_matrix().to_4x4()

def clear():
    for c in [c for c in bpy.data.collections if c.name.startswith("AUR_")]:
        for o in list(c.objects): bpy.data.objects.remove(o, do_unlink=True)
        bpy.data.collections.remove(c)
    for blk in (bpy.data.meshes, bpy.data.cameras, bpy.data.lights):
        for d in [d for d in blk if d.users == 0]: blk.remove(d)

def build():
    clear(); _mats.clear()
    PC = (0.0, 105.0)                                  # centre du plateau (plan) — 80 avant l'allongement du jardin
    center = Vector((PC[0], -PC[1], -R_PLANET))        # centre de la planète
    # ---------- Planète, plateau, forêts, villages ----------
    coll("00_planete")
    bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=128, v_segments=64, radius=R_PLANET)
    bmesh.ops.translate(bm, vec=center, verts=bm.verts); obj("planete", bm, "planet", smooth=True)
    cyl("plateau", PC[0], PC[1], 1.0, -14, 0, "plateau", segs=96, sx=115, sy=140)
    for i, (d, az) in enumerate([(430, 205), (620, 325), (720, 75)]):       # trois villages
        p, mat4 = on_planet(d, az, center)
        for k in range(14):
            a = k * 2.399; rr = 8 + 6 * math.sqrt(k)
            o = box(f"village{i+1}_maison{k:02d}", -4, 4, -3, 3, 0, 5 + (k % 3), "village")
            o.matrix_world = Matrix.Translation(p) @ mat4 @ Matrix.Translation((rr * math.cos(a), rr * math.sin(a), 0)) @ Matrix.Rotation(a, 4, "Z")
    for i, (d, az, n) in enumerate([(330, 140, 26), (380, 20, 22), (560, 255, 30), (520, 110, 24), (800, 180, 30), (820, 300, 26), (900, 30, 26)]):
        p, mat4 = on_planet(d, az, center)
        for k in range(n):
            a = k * 2.399; rr = 14 * math.sqrt(k)
            o = ball(f"foret{i+1}_{k:02d}", 0, 0, 7, 9, "forest", sz=0.9)
            o.matrix_world = Matrix.Translation(p) @ mat4 @ Matrix.Translation((rr * math.cos(a), rr * math.sin(a), 0))
    # ---------- Palais (en U, au nord) ----------
    coll("10_palais")
    T = TERRACE_Z
    CW, SW, YW = 17.0, 7.0, 35.0                       # demi-largeur de la cour et du grand escalier, bout des ailes (recalés sur palace-ref.png)
    box("corps_central", -36, 36, -14, 6, 0, 22, "palace")
    box("aile_ouest", -36, -CW, 6, YW, 0, 19, "palace")
    box("aile_est", CW, 36, 6, YW, 0, 19, "palace")
    # Toits d'ardoise à croupes, pentus, comme sur la référence production/refs/palace-ref.png (2026-11-14)
    hip("toit_corps", -36.5, 36.5, -14.5, 6.5, 22, 8, "roof")
    hip("toit_aile_ouest", -36.5, -CW + 0.5, -4, YW + 0.5, 19, 8, "roof"); hip("toit_aile_est", CW - 0.5, 36.5, -4, YW + 0.5, 19, 8, "roof")
    # Tourelles : grosses tours d'angle extérieures, tourelles plus fines aux angles de la cour, deux à l'arrière
    for i, (x, y, r, zr, zt) in enumerate([(-36, -14, 3.5, 24, 33), (36, -14, 3.5, 24, 33),
                                           (-36, YW, 4.8, 24, 37), (36, YW, 4.8, 24, 37),
                                           (-CW - 2.8, YW, 3.0, 22, 34), (CW + 2.8, YW, 3.0, 22, 34)]):
        cyl(f"tourelle{i+1}", x, y, r, 0, zr, "palace", segs=16); cyl(f"tourelle{i+1}_toit", x, y, r + 0.6, zr, zt, "roof", r_top=0.0, segs=16)
    box("terrasse", -CW, CW, 6, 30, 0, T, "terrace")
    wall("terrasse_balustrade", [(-CW, 30), (-SW, 30)], 1.0, 0.4, "wall", z0=T); wall("terrasse_balustrade2", [(SW, 30), (CW, 30)], 1.0, 0.4, "wall", z0=T)
    for k in range(8):                                 # grand escalier : 8 marches de 0,5 m
        box(f"escalier_marche{k+1}", -SW, SW, 30 + k * 1.25, 30 + (k + 1) * 1.25, 0, T - k * 0.5, "terrace")
    coll("11_tour")
    TY = 5.0                                           # décalage de la tour vers le jardin (avant-corps sur la façade)
    TW = 7.0                                           # demi-largeur de la tour (recalée sur palace-ref.png)
    HG = 40.0                                          # hauteur de la galerie du beffroi (recalée sur palace-ref.png)
    box("tour", -TW, TW, -10 + TY, 2 + TY, 0, HG, "tower")
    box("tour_cadran", -4, 4, 2.0 + TY, 2.3 + TY, HG - 10.5, HG - 2.5, "clock")
    # Sommet en beffroi (décidé 2026-11-14) : galerie à balustrade en encorbellement (1,4 m) au-dessus
    # du cadran, étage des cloches ouvert à arcades (piliers d'angle et médians), flèche d'ardoise.
    G = 1.6
    y0, y1 = -10 + TY, 2 + TY
    box("tour_galerie", -TW - G, TW + G, y0 - G, y1 + G, HG - 0.4, HG + 0.2, "wall")
    wall("tour_galerie_balustrade", [(-TW - G, y0 - G), (TW + G, y0 - G), (TW + G, y1 + G), (-TW - G, y1 + G), (-TW - G, y0 - G)], 1.1, 0.3, "wall", z0=HG + 0.2)
    for px in (-TW + 0.6, 0.0, TW - 0.6):
        for py in (y0 + 0.6, (y0 + y1) / 2, y1 - 0.6):
            if (px, py) != (0.0, (y0 + y1) / 2): box(f"tour_beffroi_pilier_{px:+.0f}_{py:+.0f}", px - 0.6, px + 0.6, py - 0.6, py + 0.6, HG + 0.2, HG + 7.5, "tower")
    box("tour_beffroi_entablement", -TW, TW, y0, y1, HG + 7.5, HG + 8.7, "tower")
    cyl("tour_beffroi_cloche", 0, (y0 + y1) / 2, 1.6, HG + 2.3, HG + 5.3, "clock", r_top=0.8, segs=16)
    cyl("tour_fleche", 0, (y0 + y1) / 2, (TW + 0.2) * math.sqrt(2), HG + 8.7, HG + 22, "roof", r_top=0.0, segs=4, rot=math.pi / 4)
    # Porte de la tour (2026-11-15) : intérieure, sur la face est de la tour, au fond du grand vestibule
    # du corps central (on y entre depuis la terrasse par les portes-fenêtres) ; scène 10.
    box("REPERE_porte_tour", TW, TW + 0.3, -1.2, 1.2, T, T + 3.2, "door")
    # Chambre d'Elias (2026-11-15) : 2e étage de l'aile est, fenêtre sur la façade extérieure (est) :
    # verger, champs, ciel du sud-est ; évasion discrète par le lierre (scènes 5-6).
    box("REPERE_fenetre_Elias", 36.0, 36.4, 20, 24, 12, 15, "elias")
    box("REPERE_cabinet_Reine", -36.4, -36.0, 12, 20, 7, 10, "queen")
    # ---------- Jardin (ovale, murets courbes, au sud) ----------
    coll("20_jardin")
    GA, GB = 95.0, 68.0 * GARDEN_DEPTH                 # demi-axes de l'ovale (profondeur allongée)
    GC = (0.0, 27.0 + GB)                              # centre : le bout nord reste à 27 m
    EX_C, EX_R = (0.0, GC[1] + GB - 1.1), 17.0         # exèdre du grand massif
    M = EX_C[1] + 1.1                                  # centre du grand massif (≈ 217 m ; 163 avant)
    cyl("pelouse", GC[0], GC[1], 1.0, 0, 0.06, "lawn", segs=96, sx=GA, sy=GB)
    cyl("exedre_sol", EX_C[0], EX_C[1], EX_R, 0, 0.055, "lawn", segs=48)
    t0, t1 = math.acos(EX_R / GA), -math.asin((GC[1] - 32) / GB)
    east = [(GA * math.cos(t), GC[1] + GB * math.sin(t)) for t in [t0 + (t1 - t0) * i / 60 for i in range(61)]]
    wall("muret_est", east, 1.2, 0.6, "wall"); wall("muret_ouest", [(-x, y) for x, y in east], 1.2, 0.6, "wall")
    wall("muret_exedre", [(EX_R * math.cos(a), EX_C[1] + EX_R * math.sin(a)) for a in [math.pi * i / 32 for i in range(33)]], 1.6, 0.7, "wall")
    box("allee_centrale", -3, 3, 40, M - 11, 0.06, 0.10, "path")
    outer = [(62 * math.cos(a), Y(112) + 9 * GARDEN_DEPTH * math.sin(a)) for a in [2 * math.pi * i / 64 for i in range(65)]]
    wall("allee_transversale", outer, 0.04, 3.0, "path", z0=0.06)
    cyl("parvis_massif", 0, M, 10, 0.06, 0.10, "path", segs=48)
    for s, nm in ((-1, "ouest"), (1, "est")):          # parterres de buis (courbes)
        P0, P1, P2 = (s * 7, Y(48)), (s * 42, Y(52)), (s * 52, Y(98))
        curve = [((1 - u) ** 2 * P0[0] + 2 * u * (1 - u) * P1[0] + u * u * P2[0], (1 - u) ** 2 * P0[1] + 2 * u * (1 - u) * P1[1] + u * u * P2[1]) for u in [i / 16 for i in range(17)]]
        prism(f"parterre_{nm}", curve + [(s * 7, Y(99))], 0.06, 0.7, "hedge")
        Q0, Q1, Q2 = (s * 7, Y(128)), (s * 35, Y(130)), (s * 58, Y(142))
        wall(f"haie_{nm}", [((1 - u) ** 2 * Q0[0] + 2 * u * (1 - u) * Q1[0] + u * u * Q2[0], (1 - u) ** 2 * Q0[1] + 2 * u * (1 - u) * Q1[1] + u * u * Q2[1]) for u in [i / 12 for i in range(13)]], 0.8, 1.2, "hedge")
    coll("21_massif_et_reperes")
    cyl("massif_bordure", 0, M, 4.8, 0, 0.45, "wall", segs=32); cyl("massif", 0, M, 4.5, 0.45, 0.75, "massif", segs=32)
    cyl("REPERE_Rose_tige", 0, M, 0.04, 0.75, 1.35, "hedge", segs=8); ball("REPERE_Rose", 0, M, 1.45, 0.14, "rose")
    arch("REPERE_arche_roses", 0, M - 17, 8.0, 5.2, 1.4, 0.8, "arch")
    arch("petite_arche_ouest", -28, Y(120), 4.5, 3.4, 1.0, 0.5, "arch_small"); arch("petite_arche_est", 28, Y(120), 4.5, 3.4, 1.0, 0.5, "arch_small")
    SY = Y(101)                                        # centre nord-sud de la serre (taille inchangée)
    box("REPERE_serre", 37, 53, SY - 5, SY + 5, 0, 3, "greenhouse")   # 16 x 10 m
    bm = bmesh.new(); N = 12; prof = [(5 * math.cos(math.pi * i / N), 3 + 3 * math.sin(math.pi * i / N)) for i in range(N + 1)]
    a_ = [bm.verts.new((37, -(SY + u), z)) for u, z in prof]; b_ = [bm.verts.new((53, -(SY + u), z)) for u, z in prof]
    bm.faces.new(a_); bm.faces.new(b_)
    for i in range(N): bm.faces.new((a_[i], a_[i + 1], b_[i + 1], b_[i]))
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces); obj("REPERE_serre_toit", bm, "greenhouse")
    # Fontaine à vasques : un seul ouvrage (bassin, fût, vasque haute) — 2026-11-15
    cyl("fontaine_vasques", -42, Y(98), 3.5, 0, 0.6, "water"); cyl("fontaine_vasques_fut", -42, Y(98), 0.35, 0.6, 2.0, "water", segs=12)
    cyl("fontaine_vasques_haut", -42, Y(98), 1.6, 2.0, 2.4, "water", r_top=1.9)
    box("fontaine_murale", 13, 16, M - 6, M - 4.5, 0, 1.8, "water"); box("banc", -15, -11, M - 6, M - 4.4, 0, 0.5, "bench")
    coll("22_arbres")
    for i, (x, y) in enumerate([(-12, 58), (12, 58), (-14, 88), (14, 88), (-9, 136), (9, 136), (-46, 76), (46, 76), (-62, 126), (64, 124), (-24, 150), (26, 150), (70, 92), (-70, 96)]):
        cyl(f"cypres{i+1:02d}", x, Y(y), 1.6, 0, 11 + (i % 3), "cypress", r_top=0.0, segs=12)
    for i, (x, y, r) in enumerate([(-80, 72, 8), (-86, 104, 9), (-74, 130, 8), (80, 72, 8), (86, 104, 9), (74, 130, 8), (-56, 42, 7), (58, 44, 7)]):
        cyl(f"feuillu{i+1}_tronc", x, Y(y), 0.6, 0, r * 0.8, "bench", segs=8); ball(f"feuillu{i+1}", x, Y(y), r * 1.3, r, "tree", sz=0.85)
    # ---------- Alentours (2026-11-15, d'après la référence aérienne production/refs/palace-aerial.png) ----------
    # Points relevés sur l'image et projetés sur le sol par la caméra CAM_aerien_ref (refs/match/pick_ground.py).
    coll("23_alentours")
    A = {k: [[x, Y(y)] for x, y in v] for k, v in ALENTOURS.items()}   # suit l'allongement du jardin
    ribbon("riviere", [tuple(p) for p in A["riviere"]], 7.0, "river", lift=0.05)
    for nm in ("pont_nord", "pont_sud"):
        x, y = A[nm][0]; z = ground_z(x, y)
        o = box(nm, x - 5, x + 5, y - 2.2, y + 2.2, z, z + 1.6, "wall"); o.rotation_euler.z = math.radians(-35)
    for nm in ("chemin_ouest", "chemin_sud_ouest", "chemin_village", "chemin_est"):
        ribbon(nm, [tuple(p) for p in A[nm]], 3.0, "path", lift=0.1)
    vx = [p[0] for p in A["verger"]]; vy = [p[1] for p in A["verger"]]
    k = 0
    for gx in range(int(min(vx)) + 4, int(max(vx)) - 3, 9):
        for gy in range(int(min(vy)) + 4, int(max(vy)) - 3, 9):
            ball(f"verger_{k:02d}", gx, gy, ground_z(gx, gy) + 2.5, 2.2, "orchard"); k += 1
    H_ = A["haies"]
    for i in range(0, len(H_) - 1, 2):
        (xa, ya), (xb, yb) = H_[i], H_[i + 1]
        wall(f"haie_champ_{i // 2 + 1}", [(xa, ya), (xb, yb)], 1.8, 1.4, "hedge", z0=min(ground_z(xa, ya), ground_z(xb, yb)))
    # ---------- Mannequins (échelle) ----------
    coll("30_personnages")
    dummy("ELIAS", 0, M - 11, 0.1, 1.35, "elias")
    dummy("REINE", -3, 22, TERRACE_Z, 1.70, "queen"); dummy("CHAMBELLAN", 3, 24, TERRACE_Z, 1.85, "chamberlain")
    # ---------- Caméras de contrôle et lumière ----------
    coll("90_cameras")
    def cam(name, pos, target, lens):
        c = bpy.data.objects.new(name, bpy.data.cameras.new(name)); _cur[0].objects.link(c)
        c.data.lens = lens; c.data.clip_start = 0.1; c.data.clip_end = 30000
        p = Vector((pos[0], -pos[1], pos[2])); t = Vector((target[0], -target[1], target[2]))
        c.location = p; c.rotation_euler = (t - p).to_track_quat("-Z", "Y").to_euler(); return c
    cam("CAM_concept", (0, M + 11.5, 1.5), (0, 60, 9), 24)            # point de vue de l'image de concept
    cam("CAM_plongee", (0, 420, 260), (0, 70, 0), 35)             # vue aérienne du plateau
    cam("CAM_aerien_ref", (0, 430, 215), (0, 80, 8), 35)          # référence : palais et jardin vus de haut, depuis le sud
    cam("CAM_espace", (0, 5200, 3600), (0, 80, -1400), 35)        # la planète entière
    cam("CAM_terrasse", (0, 14, TERRACE_Z + 1.6), (0, 160, 0), 28)  # depuis la terrasse, vers le jardin
    cam("CAM_sommet_tour", (0, 7.8, 41.6), (0, 600, -60), 20)      # de la galerie du beffroi, vers le jardin
    cam("CAM_palais_ref", (-31.3, 98.8, 43.2), (4.0, 8.9, 16.8), 20.8)         # référence du palais : trois-quarts sud-ouest, légère plongée
    cam("CAM_serre_haut", (-10, Y(60), 38), (45, Y(101), 3), 32)        # vue élevée sur la serre (scène 8)
    bpy.context.scene.camera = bpy.data.objects["CAM_concept"]
    sun = bpy.data.objects.new("SOLEIL_matin", bpy.data.lights.new("SOLEIL_matin", "SUN")); _cur[0].objects.link(sun)
    sun.data.energy = 3.0; sun.rotation_euler = (math.radians(55), 0, math.radians(110))   # lumière venant de l'est
    sc = bpy.context.scene; sc.render.resolution_x, sc.render.resolution_y, sc.render.fps = 1920, 1080, 24
    if sc.world is None: sc.world = bpy.data.worlds.new("AUR_ciel")
    try:
        if sc.world.node_tree is None: sc.world.use_nodes = True
        sc.world.node_tree.nodes["Background"].inputs["Color"].default_value = (0.55, 0.70, 0.90, 1)
    except Exception: pass
    return {c.name: len(c.objects) for c in bpy.data.collections if c.name.startswith("AUR_")}
