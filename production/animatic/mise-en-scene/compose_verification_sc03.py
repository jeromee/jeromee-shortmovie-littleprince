# compose_verification_sc03.py — vidéo de vérification de la mise en scène de SC03 (écran partagé) + piste son. 2026-11-22 (v2 le soir) ; v3 2026-11-23.
# Entrées : SC03_verif/f_####.png (vue de dessus, 1080²) et SC03_plans/f_####.png (caméra du plan, 960×540), une image sur deux
# (12 i/s, temps réel), rendues par render_mise_en_scene.py ; sons : production/audio/SC03_mise-en-scene/.
# Usage (dans ce dossier) : python3 compose_verification_sc03.py
import os, re, json, subprocess, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.normpath(os.path.join(HERE, "..", "..", "audio", "SC03_mise-en-scene"))
FONT = "/usr/share/fonts/truetype/lato/Lato-Medium.ttf"
FONTB = "/usr/share/fonts/truetype/lato/Lato-Bold.ttf" if os.path.exists("/usr/share/fonts/truetype/lato/Lato-Bold.ttf") else FONT
# Plans, répliques et décalages : SC03_chrono.json, écrit par build_mise_en_scene_sc03.py (build()).
CH = json.load(open(os.path.join(HERE, "SC03_chrono.json"), encoding="utf-8"))
T_END, SHIFT1, SHIFT2 = CH["T_END"], CH["SHIFT1"], CH["SHIFT2"]
SHOTS = [tuple(x) for x in CH["SHOTS"]]
DIALOGUE = [tuple(x) for x in CH["DIALOGUE"]]
CUT0, CUT1 = CH.get("CUT", [99, 99])
def S(t):                                                       # « temps v1 » -> chrono actuel (même règle que build())
    if t <= CUT0: return t + SHIFT1
    if t < CUT1: return CUT0 + SHIFT1
    return t + (SHIFT1 if t < 47.5 else SHIFT2) - (CUT1 - CUT0)
# (début du fichier en s, fichier, cible de sonie LUFS, gain de jeu, découpe du fichier (début, fin) ou None, fondu de sortie en s)
# 2026-11-22 (soir) : « Tu sais parler ? » surpris à voix normale, « Les grands… » à voix normale (_v2) ; seul « Tu es… vivante ? » est chuchoté.
# Répliques : temps v1, le début du fichier avancé de son silence initial ; mesurés sur les voix de référence.
CUES = [
    # v3 (2026-11-23) : Elias arrive en courant ; les jardiniers partent à 0,4 s, s'arrêtent près du banc (6,6 s), repartent à 9,8 s
    (0.4, "21_brouette.mp3", -30, 1.0, (0.0, 6.2), 0.6),
    (9.8, "21_brouette.mp3", -30, 1.0, (7.6, 13.0), 2.0),
    (0.0, "23_course.mp3", -27, 1.0, (0.0, 15.6), 0.8),           # course sur le gravier, ralentit, coup de pied, s'arrête (ElevenLabs SFX)
] + [(S(t), f, -20, g, None, 0) for t, f, g in [
    (37.6, "00_rose_tu-boudes.mp3", 0.9), (49.19, "01_elias_vivante.mp3", 0.8), (51.73, "02_rose_bien-sur.mp3", 1.0),
    (54.115, "03_elias_parler_v2.mp3", 1.0), (55.9, "04_rose_ecouter.mp3", 1.0), (60.71, "05_elias_les-grands_v2.mp3", 1.0),
    (62.77, "06_rose_je-t-attends.mp3", 1.0), (68.0, "07_elias_mon-nom.mp3", 1.0), (69.7, "08_rose_oublier.mp3", 1.0),
    (75.1, "09_elias_pas-moi.mp3", 1.0), (76.5, "10_rose_disent-tous.mp3", 1.0), (80.2, "11_rose_ce-soir.mp3", 1.0),
    (82.71, "12_elias_spectacle.mp3", 1.0), (85.7, "13_rose_pas-un-spectacle.mp3", 1.0), (97.0, "14_elias_prevenir.mp3", 1.0),
    (98.78, "15_rose_entendra-pas.mp3", 1.0), (101.96, "16_rose_besoin-de-toi.mp3", 1.0)]] + [
    (S(45.0), "22_eveil.mp3", -26, 1.0, None, 0)]
BIRDS = ("20_oiseaux.mp3", -32, S(45.6), S(47.3))   # chant d'oiseaux en boucle, fondu : « le jardin se tait »

tmp = tempfile.mkdtemp()
def tf(i, s):
    p = os.path.join(tmp, f"t{i}.txt"); open(p, "w", encoding="utf-8").write(s); return p

def video():
    F = ["[0:v]setpts=PTS-STARTPTS[a];[1:v]scale=840:-2,setpts=PTS-STARTPTS[b];"
         "color=c=0x1c1c22:s=1920x1080:r=12[bg];[bg][a]overlay=0:0:shortest=1[x];[x][b]overlay=1080:30[y]"]
    st = {"cur": "y", "n": 0}
    def dt(text_file, x, y, size, color, enable=None, font=FONT):
        st["n"] += 1; out = f"d{st['n']}"
        en = f":enable='between(t,{enable[0]},{enable[1]})'" if enable else ""
        F.append(f"[{st['cur']}]drawtext=fontfile={font}:textfile={text_file}:x={x}:y={y}:fontsize={size}:fontcolor={color}:line_spacing=8{en}[{out}]")
        st["cur"] = out
    for i, (a, b, name) in enumerate(SHOTS):
        dt(tf(f"s{i}", name), 1100, 530, 38, "0x00d8d8", (a, b - 0.001), FONTB)
        dt(tf(f"w{i}", f"fenêtre {a:.1f} – {min(b, T_END):.1f} s".replace(".", ",")), 1100, 583, 26, "0x9aa0a6", (a, b - 0.001))
    F.append(f"[{st['cur']}]drawtext=fontfile={FONT}:text='%{{pts\\:hms}}':x=1640:y=583:fontsize=26:fontcolor=white[tc]"); st["cur"] = "tc"
    for i, (a, b, who, line) in enumerate(DIALOGUE):
        if who: dt(tf(f"q{i}", who), 1100, 650, 28, "0xffcc66", (a, b))
        dt(tf(f"l{i}", line), 1100, 690 if who else 670, 30, "white", (a, b))
    legend = ("Vue de dessus, temps réel (1 s = 1 s). Flèche = regard ; trait = trajet ;\n"
              "cyan = champ de la caméra du plan en cours. Les personnages glissent (pas de marche).\n"
              "Modèles Tripo (jardiniers, brouette, rosiers, Rose) ; le visage de la Rose est un simple disque.")
    dt(tf("leg", legend), 1100, 960, 20, "0x9aa0a6")
    F[-1] = F[-1].rsplit("[", 1)[0] + "[out]"
    fs = os.path.join(tmp, "filter.txt"); open(fs, "w").write(";\n".join(F))
    out = os.path.join(HERE, "SC03_verification.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-framerate", "12", "-pattern_type", "glob", "-i", os.path.join(HERE, "SC03_verif", "f_*.png"),
                    "-framerate", "12", "-pattern_type", "glob", "-i", os.path.join(HERE, "SC03_plans", "f_*.png"),
                    "-filter_complex_script", fs, "-map", "[out]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-r", "12", out], check=True)
    return out

def lufs(path):
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-stream_loop", "3", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else None

def son(video_path):
    inputs, parts = [], []
    for i, (t, f, target, g, cut, fade) in enumerate(CUES):
        path = os.path.join(A, f); inputs += ["-i", path]
        L = lufs(path); gain = g * (10 ** ((target - L) / 20) if L is not None and L > -70 else 1)
        pre = ""
        if cut: pre = f"atrim={cut[0]}:{cut[1]},asetpts=PTS-STARTPTS,"
        if fade and cut: pre += f"afade=t=out:st={max(0, cut[1] - cut[0] - fade)}:d={fade},"
        parts.append(f"[{i}]aresample=48000,aformat=channel_layouts=mono,{pre}volume={gain:.4f},adelay={int(t * 1000)}:all=1[a{i}]")
    n = len(CUES); f, target, f0, f1 = BIRDS
    path = os.path.join(A, f); L = lufs(path); gain = 10 ** ((target - L) / 20)
    inputs += ["-stream_loop", "-1", "-i", path]
    parts.append(f"[{n}]aresample=48000,aformat=channel_layouts=mono,atrim=0:{f1},volume={gain:.4f},"
                 f"afade=t=in:st=0:d=1.5,afade=t=out:st={f0}:d={f1 - f0}[a{n}]")
    fc = ";".join(parts) + ";" + "".join(f"[a{i}]" for i in range(n + 1)) + \
         f"amix=inputs={n + 1}:normalize=0,alimiter=limit=0.89,apad=whole_dur={T_END + 0.1},atrim=0:{T_END + 0.1}[mix]"
    wav = os.path.join(A, "SC03_mise-en-scene_voix.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[mix]", "-ar", "48000", wav], check=True)
    tmpv = os.path.join(HERE, "_tmp_son_sc03.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", video_path, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-shortest", tmpv], check=True)
    os.replace(tmpv, video_path)

if __name__ == "__main__":
    v = video(); son(v); print(v)
