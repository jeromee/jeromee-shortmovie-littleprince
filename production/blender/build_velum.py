# build_velum.py — velum de la terrasse modélisé dans Blender (2026-11-21), à la place du modèle Tripo :
# la planche GPT (et donc Tripo) donnait un faîtage en plaque dorée, une boule de milieu manquante et une double frange.
# Géométrie exacte et cohérente sous tous les angles ; l'aspect (toile bleu roi étoilée, frange d'or, mâts brun foncé,
# boules de bronze) suit production/refs/terrace-velum-sheet.png.
# make_velum(poles=6|4) -> objet maître (mètres réels, axe long = Y, pied au sol en z = 0, centré).
import bpy, bmesh, math
from mathutils import Vector

L, WD = 4.2, 3.4          # longueur (y), largeur (x)
HE, HR = 2.55, 3.10       # égout, faîtage
RIDGE = 0.70              # demi-longueur du faîtage (toit en croupe)
VAL = 0.30                # hauteur de la bande festonnée
SCAL = 0.35               # largeur d'un feston

def _mat(name, rgb, metal=0.0, rough=0.6):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True; b = m.node_tree.nodes.get("Principled BSDF")
    b.inputs["Base Color"].default_value = (*rgb, 1); b.inputs["Metallic"].default_value = metal
    b.inputs["Roughness"].default_value = rough; m.diffuse_color = (*rgb, 1)
    return m

def _cyl(bm, p0, p1, r, seg=16, mi=0):
    p0, p1 = Vector(p0), Vector(p1); d = p1 - p0; q = d.to_track_quat("Z", "Y")
    ret = bmesh.ops.create_cone(bm, cap_ends=True, segments=seg, radius1=r, radius2=r, depth=d.length)
    for v in ret["verts"]: v.co = q @ v.co + (p0 + p1) / 2
    for f in {f for v in ret["verts"] for f in v.link_faces}: f.material_index = mi

def _ball(bm, c, r, mi):
    ret = bmesh.ops.create_uvsphere(bm, u_segments=16, v_segments=10, radius=r)
    for v in ret["verts"]: v.co += Vector(c)
    for f in {f for v in ret["verts"] for f in v.link_faces}: f.material_index = mi

def _face(bm, pts, mi):
    f = bm.faces.new([bm.verts.new(p) for p in pts]); f.material_index = mi; return f

def _star(bm, c, u, v, n, r1, r2, mi):
    pts = []
    for i in range(16):
        a = math.pi * i / 8; r = r1 if i % 2 == 0 else r2
        pts.append(Vector(c) + n * 0.006 + u * (r * math.cos(a)) + v * (r * math.sin(a)))
    _face(bm, pts, mi)

def make_velum(poles=6, name=None):
    name = name or f"VELUM_{poles}mats_master"
    mats = [_mat("VELUM_toile_bleue", (0.035, 0.085, 0.42), rough=0.8), _mat("VELUM_or", (0.85, 0.58, 0.18), 0.8, 0.35),
            _mat("VELUM_mat_brun", (0.07, 0.04, 0.025), rough=0.45), _mat("VELUM_bronze", (0.22, 0.13, 0.06), 0.7, 0.45)]
    BLUE, GOLD, BROWN, BRONZE = range(4)
    bm = bmesh.new(); hx, hy = WD / 2, L / 2
    # toit en croupe
    A, B, C, D = (-hx, -hy, HE), (hx, -hy, HE), (hx, hy, HE), (-hx, hy, HE)
    R0, R1 = (0, -RIDGE, HR), (0, RIDGE, HR)
    _face(bm, [A, B, R0], BLUE); _face(bm, [C, D, R1], BLUE)          # croupes (petits côtés)
    _face(bm, [B, C, R1, R0], BLUE); _face(bm, [D, A, R0, R1], BLUE)  # longs pans
    # passepoil doré fin : faîtage, arêtiers, égout
    for p, q in [(R0, R1), (A, R0), (B, R0), (C, R1), (D, R1), (A, B), (B, C), (C, D), (D, A)]:
        _cyl(bm, p, q, 0.018, 8, GOLD)
    # étoiles d'or sur la toile
    def pan(p, q, r, s, ts):
        for t, w in ts:
            base = Vector(p).lerp(Vector(q), t); top = Vector(s).lerp(Vector(r), t)
            c = base.lerp(top, w); u = (Vector(q) - Vector(p)).normalized(); v = (top - base).normalized()
            n = u.cross(v).normalized()
            if n.z < 0: n = -n
            _star(bm, c, u, v, n, 0.16 if t == 0.5 else 0.11, 0.05, GOLD)
    pan(B, C, R1, R0, [(0.22, 0.45), (0.5, 0.5), (0.78, 0.45)]); pan(D, A, R0, R1, [(0.22, 0.45), (0.5, 0.5), (0.78, 0.45)])
    pan(A, B, R0, R0, [(0.5, 0.4)]); pan(C, D, R1, R1, [(0.5, 0.4)])
    # bande festonnée (une seule frange)
    for p, q in [(A, B), (B, C), (C, D), (D, A)]:
        p, q = Vector(p), Vector(q); n = max(2, round((q - p).length / SCAL)); out = Vector((p.x + q.x, p.y + q.y, 0)).normalized() * 0.004
        for i in range(n):
            a, b = p.lerp(q, i / n), p.lerp(q, (i + 1) / n)
            top = [a, b]; bot = []
            for k in range(9):
                t = k / 8; x = a.lerp(b, t); dz = VAL * (0.55 + 0.45 * math.sin(math.pi * t))
                bot.append(x - Vector((0, 0, dz)))
            _face(bm, [b, a] + bot, BLUE)
            fr = [x + out for x in bot] + [x + out - Vector((0, 0, 0.07)) for x in bot[::-1]]
            _face(bm, fr, GOLD)
        _face(bm, [p + out, q + out, q + out - Vector((0, 0, 0.05)), p + out - Vector((0, 0, 0.05))], GOLD)  # galon du haut
    # mâts
    px, py = hx - 0.06, hy - 0.06
    spots = [(sx * px, sy * py) for sx in (-1, 1) for sy in (-1, 1)] + ([(-px, 0), (px, 0)] if poles == 6 else [])
    for x, y in spots:
        _cyl(bm, (x, y, 0), (x, y, HE + 0.12), 0.035, 16, BROWN)
        _cyl(bm, (x, y, 0), (x, y, 0.07), 0.07, 16, BROWN)
        _ball(bm, (x, y, HE + 0.19), 0.065, BRONZE)
    bmesh.ops.recalc_face_normals(bm, faces=bm.faces)
    me = bpy.data.meshes.get(name) or bpy.data.meshes.new(name)
    me.materials.clear()                       # avant to_mesh : vider les matériaux remet les indices à 0
    for m in mats: me.materials.append(m)
    bm.to_mesh(me); bm.free()
    for f in me.polygons: f.use_smooth = False
    o = bpy.data.objects.get(name) or bpy.data.objects.new(name, me); o.data = me
    coll = bpy.data.collections.get("AUR_34_accessoires_maitres")
    if coll and o.name not in coll.objects: coll.objects.link(o)
    return o
