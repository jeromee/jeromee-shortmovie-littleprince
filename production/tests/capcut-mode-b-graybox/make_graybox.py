# Test mode B : maquette en boîtes grises du jardin + mannequin d'Elias (bleu),
# caméra en quart d'orbite autour du massif. Rendu de la vidéo de référence (5 s,
# 24 i/s, 1280x720) et des images de départ / d'arrivée (1920x1080).
# Lancement : python make_graybox.py <dossier_sortie> cycles [--stills | --preview | --frames A B [--hq]]
import bpy, math, sys, os
from mathutils import Vector
OUT = os.path.abspath(sys.argv[1]); ENGINE = sys.argv[2] if len(sys.argv) > 2 else 'workbench'
bpy.ops.wm.read_factory_settings(use_empty=True)
sc = bpy.context.scene
FPS, N = 24, 120
sc.render.fps = FPS; sc.frame_start = 1; sc.frame_end = N

def mat(name, rgb, checker=False):
    m = bpy.data.materials.new(name); m.use_nodes = True
    nt = m.node_tree; bsdf = nt.nodes['Principled BSDF']
    bsdf.inputs['Base Color'].default_value = (*rgb, 1); bsdf.inputs['Roughness'].default_value = 0.8
    if checker:
        c = nt.nodes.new('ShaderNodeTexChecker'); c.inputs['Scale'].default_value = 20
        c.inputs['Color1'].default_value = (0.42, 0.42, 0.42, 1); c.inputs['Color2'].default_value = (0.30, 0.30, 0.30, 1)
        nt.links.new(c.outputs['Color'], bsdf.inputs['Base Color'])
    m.diffuse_color = (*rgb, 1)
    return m
def put(obj, m): obj.data.materials.append(m); return obj
G = mat('ground', (0.36, 0.36, 0.36), checker=True)
GR = mat('gray', (0.55, 0.55, 0.55)); DK = mat('dark', (0.25, 0.25, 0.25))
BLUE = mat('elias_blue', (0.05, 0.25, 0.85)); YEL = mat('rose_yellow', (0.95, 0.8, 0.15))
# --arch-color : l'arche prend une teinte proche de l'arche réelle (pierre rosée)
ARCH = mat('arch_rose_stone', (0.78, 0.52, 0.50)) if '--arch-color' in sys.argv else GR

bpy.ops.mesh.primitive_plane_add(size=30); put(bpy.context.object, G)
# massif rond + Rose (repère jaune)
bpy.ops.mesh.primitive_cylinder_add(radius=1.6, depth=0.45, location=(0, 0, 0.225)); put(bpy.context.object, DK)
bpy.ops.mesh.primitive_cylinder_add(radius=0.03, depth=0.5, location=(0, 0, 0.7)); put(bpy.context.object, GR)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.13, location=(0, 0, 0.98)); put(bpy.context.object, YEL)
# arche derrière le massif, allée, murets, château au loin
bpy.ops.mesh.primitive_torus_add(major_radius=1.3, minor_radius=0.14, location=(0, 4.0, 1.4)); arch = put(bpy.context.object, ARCH)
import bmesh
bm = bmesh.new(); bm.from_mesh(arch.data)
bmesh.ops.delete(bm, geom=[v for v in bm.verts if v.co.y < -0.02], context='VERTS'); bm.to_mesh(arch.data); bm.free()
arch.rotation_euler.x = math.pi/2
for x in (-1.3, 1.3):
    bpy.ops.mesh.primitive_cube_add(size=1, location=(x, 4.0, 0.7), scale=(0.28, 0.28, 1.4)); put(bpy.context.object, ARCH)
bpy.ops.mesh.primitive_cube_add(size=1, location=(-6, 3, 0.5), scale=(0.4, 6, 1.0)); put(bpy.context.object, GR)
bpy.ops.mesh.primitive_cube_add(size=1, location=(6, 3, 0.5), scale=(0.4, 6, 1.0)); put(bpy.context.object, GR)
bpy.ops.mesh.primitive_cube_add(size=1, location=(0, 14, 3), scale=(8, 2, 6)); put(bpy.context.object, GR)
for x in (-4.5, -3, 3, 4.5):
    bpy.ops.mesh.primitive_cone_add(radius1=0.45, depth=4, location=(x, 6.5, 2)); put(bpy.context.object, DK)
# mannequin d'Elias (bleu) : corps + tête, tourné vers la Rose
ex, ey = -1.25, -1.55
bpy.ops.mesh.primitive_cube_add(size=1, location=(ex, ey, 0.5), scale=(0.34, 0.22, 1.0)); body = put(bpy.context.object, BLUE)
bpy.ops.mesh.primitive_uv_sphere_add(radius=0.17, location=(ex, ey, 1.17)); put(bpy.context.object, BLUE)
body.rotation_euler.z = math.atan2(-ey, -ex) - math.pi/2
# lumière
bpy.ops.object.light_add(type='SUN', rotation=(math.radians(50), 0, math.radians(-30))); bpy.context.object.data.energy = 3
w = bpy.data.worlds.new('w'); sc.world = w; w.use_nodes = True
w.node_tree.nodes['Background'].inputs['Color'].default_value = (0.6, 0.65, 0.72, 1)
# caméra : quart d'orbite (de l'avant-gauche vers la droite), hauteur d'enfant
target = Vector((-0.55, -0.7, 0.75))
bpy.ops.object.empty_add(location=target); tgt = bpy.context.object
bpy.ops.object.camera_add(); cam = bpy.context.object; sc.camera = cam
cam.data.lens = 35
tc = cam.constraints.new('TRACK_TO'); tc.target = tgt; tc.track_axis = 'TRACK_NEGATIVE_Z'; tc.up_axis = 'UP_Y'
R, H = 5.2, 1.15
a0, a1 = math.radians(-165), math.radians(-75)
ease = lambda t: 0.5 - 0.5 * math.cos(math.pi * t)
for f in range(1, N + 1):
    a = a0 + (a1 - a0) * ease((f - 1) / (N - 1))
    cam.location = target + Vector((R * math.cos(a), R * math.sin(a), H - target.z))
    cam.keyframe_insert('location', frame=f)
# rendu
if ENGINE == 'cycles':
    sc.render.engine = 'CYCLES'; sc.cycles.samples = 4; sc.cycles.device = 'CPU'; sc.cycles.use_denoising = True; sc.cycles.max_bounces = 2
else:
    sc.render.engine = 'BLENDER_WORKBENCH'
    sh = sc.display.shading; sh.light = 'STUDIO'; sh.color_type = 'MATERIAL'; sh.show_shadows = True; sh.show_cavity = False
sc.render.image_settings.file_format = 'PNG'
# Options : --stills (images de départ/arrivée en 1920x1080) ; --preview (idem
# en 854x480) ; --frames A B (images A à B de la vidéo, 854x480, dans frames/).
args = sys.argv[3:]
if '--stills' in args or '--preview' in args:
    sc.render.resolution_x, sc.render.resolution_y = (854, 480) if '--preview' in args else (1920, 1080)
    for f, name in ((1, 'SC00-TESTB_graybox-first.png'), (N, 'SC00-TESTB_graybox-last.png')):
        sc.frame_set(f); sc.render.filepath = os.path.join(OUT, name)
        bpy.ops.render.render(write_still=True)
if '--frames' in args:
    k = args.index('--frames'); a, b = int(args[k + 1]), int(args[k + 2])
    if '--hq' in args:   # référence plus nette : 1280x720, filtre de pixel serré
        sc.render.resolution_x, sc.render.resolution_y = 1280, 720
        sc.cycles.samples = 2; sc.cycles.filter_width = 0.8
    else:
        sc.render.resolution_x, sc.render.resolution_y = 854, 480
    for f in range(a, b + 1):
        sc.frame_set(f); sc.render.filepath = os.path.join(OUT, 'frames', f'g{f:04d}.png')
        bpy.ops.render.render(write_still=True)
