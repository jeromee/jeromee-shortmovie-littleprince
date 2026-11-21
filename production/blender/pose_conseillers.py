"""Conseillers de SC02 : posture naturelle et carnet + crayon en main (2026-11-21, demande de l'auteur).

Les mannequins Tripo des conseillers avaient les bras le long du corps et les mains vides ; GPT recopiait
la maquette et les dessinait sans carnet, alors que leur fiche (kb/characters/advisers.md) dit qu'ils tiennent
toujours un petit carnet de cuir et un crayon. Ce module plie les bras (avant-bras vers l'avant, à hauteur
de taille), incline un peu la tête vers le carnet, et attache un carnet ouvert (main gauche) et un crayon
(main droite) aux os des mains. Pose fixe pour toute la scène.

Appelé à la fin de build() dans build_mise_en_scene_sc02.py ; peut aussi être lancé seul : apply().
"""
import bpy
from mathutils import Vector, Matrix

# os par conseiller : (bras, avant-bras, main) gauche et droite ; tête ; signe latéral lu sur le squelette
RIGS = {
    "MES_CONSEILLER_1_rig": dict(
        L=("tripo::0_Left_Limb_1", ["tripo::0_Left_Limb_2"], "tripo::0_Left_Limb_3"),
        R=("tripo::0_Right_Limb_1", ["tripo::0_Right_Limb_2"], "tripo::0_Right_Limb_3"),
        head="tripo::Head_0"),
    "MES_CONSEILLER_3_rig": dict(
        L=("bone_13", ["bone_14"], "tripo::0_Left_Limb_0"),
        R=None,   # bras droit laissé au repos : la main droite de ce mannequin est soudée à l'habit
        head="tripo::Head_0"),
}
# groupes de la main (jamais rendus au torse, même loin de l'axe du bras)
PROTECT = {
    "MES_CONSEILLER_1_rig": {"L": ["tripo::0_Left_Limb_%d" % i for i in range(3, 7)],
                             "R": ["tripo::0_Right_Limb_%d" % i for i in range(3, 7)]},
    "MES_CONSEILLER_3_rig": {"L": ["tripo::0_Left_Limb_0", "tripo::0_Left_Limb_1", "tripo::0_Left_Limb_2",
                                   "bone_18", "bone_19", "bone_20"],
                             "R": ["bone_31"]},
}
# directions dans l'espace de l'armature (x = devant, z = haut, y = côté ; s = côté du bras)
UPPER = lambda s: Vector((0.35, 0.22 * s, -1.0))
FORE_BOOK = lambda s: Vector((1.0, -0.55 * s, 0.30))     # main qui tient le carnet, ramenée devant la taille
FORE_PEN = lambda s: Vector((1.0, -0.75 * s, 0.38))      # main qui tient le crayon, au-dessus du carnet
HEAD = Vector((0.28, 0.0, 1.0))                          # tête un peu penchée vers le carnet

BOOK = (0.095, 0.135, 0.016)   # carnet (largeur, hauteur, épaisseur), mètres monde
PEN = (0.004, 0.13)            # crayon (rayon, longueur)


def _mat(name, rgb):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    bsdf = m.node_tree.nodes.get("Principled BSDF")
    if bsdf:
        bsdf.inputs["Base Color"].default_value = (*rgb, 1); bsdf.inputs["Roughness"].default_value = 0.6
    m.diffuse_color = (*rgb, 1)
    return m


def _aim(rig, name, d):
    pb = rig.pose.bones[name]
    bpy.context.view_layer.update()
    M = pb.matrix.copy(); y = M.col[1].xyz.normalized(); h = M.translation.copy()
    R = y.rotation_difference(d.normalized()).to_matrix().to_4x4()
    pb.matrix = Matrix.Translation(h) @ R @ Matrix.Translation(-h) @ M
    bpy.context.view_layer.update()


def _side(rig, bone):
    return 1.0 if rig.data.bones[bone].head_local.y > 0 else -1.0


def _box(name, dims, mats, coll):
    import bmesh
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cube(bm, size=1.0)
    for v in bm.verts: v.co = Vector((v.co.x * dims[0], v.co.y * dims[1], v.co.z * dims[2]))
    for m in mats: me.materials.append(m)
    bm.faces.ensure_lookup_table()
    for f in bm.faces: f.material_index = 1 if (len(mats) > 1 and f.normal.z > 0.9) else 0
    bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); coll.objects.link(o); return o


def _pencil(name, mat, coll):
    import bmesh
    me = bpy.data.meshes.new(name); bm = bmesh.new()
    bmesh.ops.create_cone(bm, cap_ends=True, segments=6, radius1=PEN[0], radius2=PEN[0], depth=PEN[1])
    me.materials.append(mat); bm.to_mesh(me); bm.free()
    o = bpy.data.objects.new(name, me); coll.objects.link(o); return o


def _attach(o, rig, bone, world):
    o.parent = rig; o.parent_type = "BONE"; o.parent_bone = bone
    bpy.context.view_layer.update(); o.matrix_world = world


# --- Réparation du squelette Tripo du conseiller (3) et nettoyage des étirements ---------------------------------
# Défauts des mannequins Tripo : la main droite du conseiller (3) (os bone_31) est rattachée à la racine et ne suit
# pas l'avant-bras (corrigé une fois dans le squelette partagé ; sauvegarde « …_avant-pose-2026-11-21 ») ; et le
# maillage est d'un seul tenant : là où la main pendante touchait l'habit, des faces s'étirent en éventail quand on
# plie le bras. On les supprime dans une copie du maillage propre à la mise en scène (« …_MES_pose ») ; le maître et
# les scènes d'archive gardent le maillage d'origine.
STRETCH = 1.8     # une face est supprimée si l'une de ses arêtes est plus de 1,8 fois plus longue qu'au repos


def fix_rig_conseiller3():
    rig = bpy.data.objects.get("MES_CONSEILLER_3_rig")
    if not rig or rig.data.get("main_droite_rattachee"):
        return "déjà fait"
    if not bpy.data.armatures.get(rig.data.name + "_avant-pose-2026-11-21"):
        c = rig.data.copy(); c.name = rig.data.name + "_avant-pose-2026-11-21"; c.use_fake_user = True
    vl = bpy.context.view_layer
    for o in vl.objects: o.select_set(False)
    vl.objects.active = rig; rig.select_set(True)
    bpy.ops.object.mode_set(mode="EDIT")
    eb = rig.data.edit_bones; eb["bone_31"].use_connect = False; eb["bone_31"].parent = eb["tripo::0_Right_Limb_0"]
    bpy.ops.object.mode_set(mode="OBJECT")
    rig.data["main_droite_rattachee"] = True
    return "fait"


ARM_R = 0.05      # rayon autour de l'axe du bras, unités de l'armature (≈ 9 cm)
HAND_EXT = 0.12  # longueur ajoutée au bout du bras (main), unités de l'armature
ARM_R_REST = 0.045  # au repos, un point plus loin que cela de l'axe du bras appartient à l'habit
MOVED = 0.012     # déplacement au-delà duquel un point est « emporté » par le bras


def _seg_dist(p, a, b):
    ab = b - a; t = max(0.0, min(1.0, (p - a).dot(ab) / max(ab.length_squared, 1e-9)))
    return (a + ab * t - p).length


def _posed(body):
    bpy.context.view_layer.update()
    dg = bpy.context.evaluated_depsgraph_get(); ev = body.evaluated_get(dg); em = ev.to_mesh()
    out = [v.co.copy() for v in em.vertices]; ev.to_mesh_clear(); return out


def _cut_stretched(body, rig, spec):
    """Sur une copie du maillage propre à la mise en scène : 1) les points de l'habit pondérés (même en partie)
    sur un bras et emportés loin de ce bras sont rendus au torse ; 2) les faces encore étirées sont supprimées."""
    import bmesh
    if not body.data.name.startswith(body.name + "_MES_pose"):
        me = body.data.copy(); me.name = body.name + "_MES_pose"; body.data = me
    me = body.data; vg = body.vertex_groups
    rest = [v.co.copy() for v in me.vertices]; posed = _posed(body)
    n_strip = 0
    for side in ("L", "R"):
        if not spec[side]: continue
        up, fores, hand = spec[side]
        bone = rig.data.bones[up]; arm = {bone.name} | {c.name for c in bone.children_recursive}
        idx = {vg[n].index for n in arm if n in vg}
        keep = {vg[n].index for n in PROTECT.get(rig.name, {}).get(side, []) if n in vg}
        anc = bone.parent
        while anc and (anc.name not in vg or anc.name in arm): anc = anc.parent
        torso = vg[anc.name] if anc else None
        pb = rig.pose.bones
        def chain(h, t):
            q = [h(up), t(up), t(fores[0]), t(hand)]
            d = q[-1] - q[1]                       # prolonger l'axe au-delà du poignet : la main et le carnet
            q.append(q[-1] + d.normalized() * HAND_EXT if d.length > 1e-6 else q[-1]); return q
        pts = chain(lambda b: pb[b].head.copy(), lambda b: pb[b].tail.copy())
        bones = rig.data.bones
        pts0 = chain(lambda b: bones[b].head_local.copy(), lambda b: bones[b].tail_local.copy())
        for v in me.vertices:
            gs = [(g.group, g.weight) for g in v.groups if g.group in idx and g.weight > 0]
            if not gs or (posed[v.index] - rest[v.index]).length < MOVED: continue
            if any(g.group in keep and g.weight > 0.3 for g in v.groups): continue
            near_now = min(_seg_dist(posed[v.index], pts[i], pts[i + 1]) for i in range(len(pts) - 1)) <= ARM_R
            near_rest = min(_seg_dist(rest[v.index], pts0[i], pts0[i + 1]) for i in range(len(pts0) - 1)) <= ARM_R_REST
            if near_now and near_rest: continue     # vraie manche ou vraie main : elle suit le bras
            w = sum(x[1] for x in gs)
            for gi, _ in gs: vg[gi].remove([v.index])
            if torso: torso.add([v.index], w, "ADD")
            n_strip += 1
    posed = _posed(body); bad = set()
    for poly in me.polygons:
        vs = list(poly.vertices)
        for i in range(len(vs)):
            a, b = vs[i], vs[(i + 1) % len(vs)]
            lr = (rest[a] - rest[b]).length
            if lr > 1e-6 and (posed[a] - posed[b]).length > STRETCH * lr + 0.004:
                bad.add(poly.index); break
    n_frag = 0
    if bad:
        bm = bmesh.new(); bm.from_mesh(me); bm.faces.ensure_lookup_table()
        lay = bm.faces.layers.int.new("ilot0")
        size0 = _islands(bm, lay)                       # taille de l'îlot d'origine de chaque face
        bmesh.ops.delete(bm, geom=[bm.faces[i] for i in bad], context="FACES_ONLY")
        bm.faces.index_update(); bm.faces.ensure_lookup_table()
        # lambeaux : morceaux détachés par la coupe, bien plus petits que l'îlot dont ils viennent
        frag = []
        for comp in _components(bm):
            orig = max(size0[f[lay]] for f in comp)
            if len(comp) < FRAG_MAX and len(comp) < FRAG_RATIO * orig: frag.extend(comp)
        if frag:
            bmesh.ops.delete(bm, geom=frag, context="FACES_ONLY"); n_frag = len(frag)
        bm.to_mesh(me); bm.free()
    return n_strip, len(bad), n_frag


FRAG_MAX = 4000     # un lambeau compte moins de faces que cela…
FRAG_RATIO = 0.6    # … et moins du quart de l'îlot dont il a été détaché


def _components(bm):
    seen = set(); out = []
    for f in bm.faces:
        if f.index in seen: continue
        stack = [f]; seen.add(f.index); comp = []
        while stack:
            g = stack.pop(); comp.append(g)
            for e in g.edges:
                for h in e.link_faces:
                    if h.index not in seen: seen.add(h.index); stack.append(h)
        out.append(comp)
    return out


def _islands(bm, lay):
    sizes = {}
    for k, comp in enumerate(_components(bm)):
        sizes[k] = len(comp)
        for f in comp: f[lay] = k
    return sizes


def apply(scene_name="SC02_MISE_EN_SCENE"):
    sc = bpy.data.scenes[scene_name]
    win = bpy.context.window; prev = win.scene if win else None
    if win: win.scene = sc           # l'évaluation (pose, déformation) se fait dans la couche de vue active
    try:
        return _apply(sc)
    finally:
        if win and prev: win.scene = prev


def _apply(sc):
    fix_rig_conseiller3()
    coll = bpy.data.collections.get("SC02_MES_jeu") or sc.collection
    cuir = _mat("CARNET_cuir", (0.20, 0.09, 0.04)); papier = _mat("CARNET_papier", (0.92, 0.88, 0.76))
    bois = _mat("CRAYON_bois", (0.85, 0.62, 0.25))
    for o in [o for o in bpy.data.objects if o.name.startswith(("MES_carnet_", "MES_crayon_"))]:
        bpy.data.objects.remove(o, do_unlink=True)
    done = []
    for rn, spec in RIGS.items():
        rig = bpy.data.objects.get(rn)
        if not rig: continue
        for pb in rig.pose.bones: pb.matrix_basis = Matrix()
        bpy.context.view_layer.update()
        for side, fore_dir in (("L", FORE_BOOK), ("R", FORE_PEN)):
            if not spec[side]: continue
            up, fores, hand = spec[side]; s = _side(rig, up)
            _aim(rig, up, UPPER(s))
            for f in fores: _aim(rig, f, fore_dir(s))
        _aim(rig, spec["head"], HEAD)
        body = next((c for c in rig.children if c.type == "MESH"), None)
        if body: done.append((body.name, [_cut_stretched(body, rig, spec) for _ in range(2)]))
        mw = rig.matrix_world; rot = mw.to_quaternion()
        fwd = (rot @ Vector((1, 0, 0))).normalized(); upv = Vector((0, 0, 1))
        # carnet : au bout de la main gauche, couché à plat et incliné de 35° vers le conseiller
        pbL = rig.pose.bones[spec["L"][2]]; tipL = mw @ pbL.tail
        side_w = fwd.cross(upv).normalized()
        tilt = Matrix.Rotation(0.6, 4, side_w)
        basis = Matrix((side_w, fwd, upv)).transposed().to_4x4()
        book = _box(f"MES_carnet_{rn[4:-4]}", BOOK, [cuir, papier], coll)
        _attach(book, rig, spec["L"][2], Matrix.Translation(tipL + upv * 0.01) @ tilt @ basis)
        # crayon : dans la main droite, pointé vers le carnet
        if spec["R"]:
            pen = _pencil(f"MES_crayon_{rn[4:-4]}", bois, coll)
            pbR = rig.pose.bones[spec["R"][2]]; tipR = mw @ pbR.tail
            d = (tipL + upv * 0.03 - tipR); d = d.normalized() if d.length > 1e-4 else fwd
            q = Vector((0, 0, 1)).rotation_difference(d)
            _attach(pen, rig, spec["R"][2], Matrix.Translation(tipR + d * PEN[1] * 0.3) @ q.to_matrix().to_4x4())
        # sans main droite (conseiller 3) : pas de crayon visible, il est glissé dans le carnet
        done.append(rn)
    return done
