# compose_verification.py — assemble la vidéo de vérification de mise en scène (écran partagé) avec ffmpeg.
# Entrées : verif/f_####.png (vue de dessus, 1080²) et plans/f_####.png (caméra du plan, 960×540),
# rendues une image sur deux (12 i/s, temps réel). Usage : python3 compose_verification.py
import os, subprocess, glob, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = "/usr/share/fonts/truetype/lato/Lato-Medium.ttf"
FONTB = "/usr/share/fonts/truetype/lato/Lato-Bold.ttf" if os.path.exists("/usr/share/fonts/truetype/lato/Lato-Bold.ttf") else FONT
SHOTS = [(0.0, 6.8, "SH01 — La terrasse"), (6.8, 12.2, "SH02 — Elle sonne"), (12.2, 15.0, "SH03 — Les rires"),
         (15.0, 16.8, "SH04 — Elias"), (16.8, 28.8, "SH05 — Je ne m'en souviens pas"),
         (28.8, 41.6, "SH06a (nouveau) — Elle repart"), (41.6, 48.6, "SH06 — Seul (retenu)"), (48.6, 52.1, "(après SH06)")]
DIALOGUE = [
    (5.0, 5.6, "ELIAS", "Maman !"), (7.0, 8.4, "ELIAS", "Écoute. Elle sonne."), (9.6, 10.8, "LA REINE", "Plus tard, Elias."),
    (12.8, 14.6, "LE CHAMBELLAN", "Son Altesse parle encore aux fleurs ?"), (14.6, 16.1, "", "(petits rires polis)"),
    (16.6, 18.2, "LA REINE", "Ce soir, pluie d'étoiles."), (18.4, 19.6, "LA REINE", "Tu seras à mes côtés."),
    (20.0, 21.0, "LA REINE", "Tiens-toi droit."),
    (21.4, 25.2, "LE CHAMBELLAN", "La dernière, c'était il y a trente ans.\nVotre Majesté était une enfant."),
    (25.2, 26.8, "", "(la Reine marque un temps)"), (26.8, 28.3, "LA REINE", "Je ne m'en souviens pas."),
    (28.6, 34.6, "", "(elle rentre au palais ; la cour la suit)"), (35.4, 41.4, "", "(Elias, seul, va vers l'allée des velums)"),
    (42.6, 43.6, "", "(la clochette tinte, pour lui seul)"), (43.6, 48.6, "", "(il descend vers le jardin)")]
tmp = tempfile.mkdtemp()
def tf(i, s):
    p = os.path.join(tmp, f"t{i}.txt"); open(p, "w", encoding="utf-8").write(s); return p
F = []
F.append("[0:v]setpts=PTS-STARTPTS[a];[1:v]scale=840:-2,setpts=PTS-STARTPTS[b];"
         "color=c=0x1c1c22:s=1920x1080:r=12[bg];[bg][a]overlay=0:0:shortest=1[x];[x][b]overlay=1080:30[y]")
cur = "y"; n = 0
def dt(text_file, x, y, size, color, enable=None, font=FONT, inp=None):
    global cur, n
    n += 1; out = f"d{n}"
    en = f":enable='between(t,{enable[0]},{enable[1]})'" if enable else ""
    F.append(f"[{cur}]drawtext=fontfile={font}:textfile={text_file}:x={x}:y={y}:fontsize={size}:fontcolor={color}:line_spacing=8{en}[{out}]")
    cur = out
for i, (a, b, name) in enumerate(SHOTS):
    dt(tf(f"s{i}", name), 1100, 530, 40, "0x00d8d8", (a, b - 0.001), FONTB)
    dt(tf(f"w{i}", f"fenêtre {a:.1f} – {b:.1f} s".replace(".", ",")), 1100, 585, 26, "0x9aa0a6", (a, b - 0.001))
F.append(f"[{cur}]drawtext=fontfile={FONT}:text='%{{pts\\:hms}}':x=1640:y=585:fontsize=26:fontcolor=white[tc]"); cur = "tc"
for i, (a, b, who, line) in enumerate(DIALOGUE):
    if who: dt(tf(f"q{i}", who), 1100, 660, 28, "0xffcc66", (a, b))
    dt(tf(f"l{i}", line), 1100, 700 if who else 680, 34, "white", (a, b))
legend = ("Vue de dessus, temps réel (1 s = 1 s). Flèche = regard ; trait = trajet complet ;\n"
          "cyan = champ de la caméra du plan en cours. Les personnages glissent (pas de marche) :\n"
          "seuls comptent les positions, les regards et le timing.")
dt(tf("leg", legend), 1100, 960, 20, "0x9aa0a6")
F[-1] = F[-1].rsplit("[", 1)[0] + "[out]"
fs = os.path.join(tmp, "filter.txt"); open(fs, "w").write(";\n".join(F))
out = os.path.join(HERE, "SC02_verification.mp4")
cmd = ["ffmpeg", "-y", "-framerate", "12", "-pattern_type", "glob", "-i", os.path.join(HERE, "verif", "f_*.png"),
       "-framerate", "12", "-pattern_type", "glob", "-i", os.path.join(HERE, "plans", "f_*.png"),
       "-filter_complex_script", fs, "-map", "[out]", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
       "-pix_fmt", "yuv420p", "-r", "12", out]
subprocess.run(cmd, check=True)
print(out)
# Piste son (voix témoins + clochette) : toujours relancer après la vidéo, sinon la vidéo recomposée est muette.
subprocess.run(["python3", os.path.join(HERE, "mix_son_verification.py")], check=True)
