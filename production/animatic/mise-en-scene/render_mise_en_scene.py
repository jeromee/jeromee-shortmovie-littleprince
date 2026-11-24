# render_mise_en_scene.py — rendus de la vidéo de vérification d'une scène de mise en scène continue (2026-11-22).
# À lancer DANS Blender (world.blend ouvert et enregistré) :
#   exec(compile(open(chemin, encoding="utf-8").read(), chemin, "exec")) ; lancer("SC03")
# Enregistre une copie temporaire du fichier, puis lance deux Blender en arrière-plan (le fichier ouvert n'est pas touché) :
#   <SC>_MISE_EN_SCENE (EEVEE, 960×540) -> <SC>_plans/f_####.png  et  <SC>_MES_VERIF (Workbench, 1080²) -> <SC>_verif/f_####.png,
# une image sur deux (12 i/s, temps réel). Journaux : _render_<sc>_plans.log, _render_<sc>_verif.log ; fin : _render_<sc>_fini.txt.
# Ensuite : python3 compose_verification_<sc>.py (dans le dossier production/animatic/mise-en-scene).
import bpy, os, subprocess, tempfile

def lancer(sc_id, step=2):
    here = os.path.join(os.path.dirname(os.path.dirname(bpy.data.filepath)), "animatic", "mise-en-scene")
    tmp = os.path.join(tempfile.gettempdir(), f"_tmp_render_mes_{sc_id.lower()}.blend")
    bpy.ops.wm.save_as_mainfile(filepath=tmp, copy=True)
    procs = []
    for scene, sub in ((f"{sc_id}_MISE_EN_SCENE", "plans"), (f"{sc_id}_MES_VERIF", "verif")):
        d = os.path.join(here, f"{sc_id}_{sub}"); os.makedirs(d, exist_ok=True)
        for f in os.listdir(d):
            if f.endswith(".png"): os.remove(os.path.join(d, f))
        s = bpy.data.scenes[scene]
        log = open(os.path.join(here, f"_render_{sc_id.lower()}_{sub}.log"), "w")
        cmd = [bpy.app.binary_path, "-b", tmp, "-S", scene, "-o", os.path.join(d, "f_####"), "-F", "PNG",
               "-s", str(s.frame_start), "-e", str(s.frame_end), "-j", str(step), "-a"]
        procs.append(subprocess.Popen(cmd, stdout=log, stderr=subprocess.STDOUT))
    # petit veilleur : écrit _render_<sc>_fini.txt quand les deux rendus sont terminés
    flag = os.path.join(here, f"_render_{sc_id.lower()}_fini.txt")
    if os.path.exists(flag): os.remove(flag)
    pids = " ".join(str(p.pid) for p in procs)
    watcher = ("import time,subprocess,sys\n"
               f"pids={[p.pid for p in procs]}\n"
               "def alive(p):\n"
               "    r=subprocess.run(['tasklist','/FI',f'PID eq {p}'],capture_output=True,text=True)\n"
               "    return str(p) in r.stdout\n"
               "while any(alive(p) for p in pids): time.sleep(10)\n"
               f"open(r'{flag}','w').write('FINI')\n")
    subprocess.Popen([bpy.app.binary_path, "-b", "--factory-startup", "--python-expr", watcher],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return pids
