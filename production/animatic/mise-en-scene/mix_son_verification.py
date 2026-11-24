# mix_son_verification.py — piste son provisoire de SC02_verification.mp4 (voix témoins + sons clés), placée sur le chrono.
# Voix : ElevenLabs Turbo 2.5 via Magnific (modèle économique), qualité d'animatique.
# 2026-11-22 : voix de référence du film (production/audio/voix-reference/README.md). La Reine était déjà Emma Simon (485) ;
# Elias et le Chambellan sont passés au changeur de voix (Elias -> clone 215420, Chambellan -> Adrien Moreau 230) : fichiers *_voixref.wav.
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.normpath(os.path.join(HERE, "..", "..", "audio", "SC02_mise-en-scene"))
BELL = os.path.normpath(os.path.join(HERE, "..", "..", "audio", "SC02-SH06", "SC02-SH06_bruitage_clochette_v1.wav"))
CUES = [  # (début en s, fichier, gain)
    (0.8, "00_reine_dictee.wav", 0.35),          # dictée (texte provisoire, non écrit dans le scénario)
    (5.0, "01_elias_maman_voixref.wav", 1.0),
    (7.0, "02_elias_ecoute_voixref.wav", 1.0),
    (9.6, "03_reine_plus-tard.wav", 1.0),
    (12.8, "04_chambellan_fleurs_voixref.wav", 0.8),     # à mi-voix, en aparté
    (14.6, "05_rires.wav", 0.5),               # petits rires polis, en fond
    (16.6, "06_reine_ce-soir.wav", 1.0),
    (18.4, "07_reine_cotes.wav", 1.0),
    (20.0, "08_reine_droit.wav", 1.0),
    (21.4, "09_chambellan_trente-ans_voixref.wav", 1.0),
    (26.8, "10_reine_souviens.wav", 0.9),
    (42.5, BELL, 0.7),                           # = SC02-SH06 retenu, clochette à 0,9 s
]
# 2026-11-22 : chaque réplique est d'abord ramenée au même niveau sonore (sonie intégrée, en LUFS), puis multipliée par
# son gain de jeu (dictée à bas niveau, aparté du Chambellan). Les voix sortaient du changeur de voix à des niveaux très différents.
TARGET_LUFS = -20.0
import re
def lufs(path):
    # lu 4 fois de suite : la mesure EBU R128 demande au moins 0,4 s, et « Maman ! » en dure 0,37
    r = subprocess.run(["ffmpeg", "-hide_banner", "-nostats", "-stream_loop", "3", "-i", path, "-af", "ebur128", "-f", "null", "-"],
                       capture_output=True, text=True)
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)
    return float(m[-1]) if m else None
inputs, parts = [], []
for i, (t, f, g) in enumerate(CUES):
    path = f if os.path.isabs(f) else os.path.join(A, f)
    inputs += ["-i", path]
    if path != BELL:
        L = lufs(path)
        if L is not None and L > -70: g = g * 10 ** ((TARGET_LUFS - L) / 20)
        print(f"{os.path.basename(path):40s} {L} LUFS -> gain {g:.2f}")
    parts.append(f"[{i}]aresample=48000,aformat=channel_layouts=mono,volume={g:.4f},adelay={int(t*1000)}:all=1[a{i}]")
n = len(CUES)
fc = ";".join(parts) + ";" + "".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,alimiter=limit=0.89,apad=whole_dur=52.1,atrim=0:52.1[mix]"
wav = os.path.join(A, "SC02_mise-en-scene_voix-temoins.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[mix]", "-ar", "48000", wav], check=True)
src = os.path.join(HERE, "SC02_verification.mp4"); tmp = os.path.join(HERE, "_tmp_son.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "160k", "-shortest", tmp], check=True)
os.replace(tmp, src); print(src)
