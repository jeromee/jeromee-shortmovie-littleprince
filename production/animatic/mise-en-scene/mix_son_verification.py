# mix_son_verification.py — piste son provisoire de SC02_verification.mp4 (voix témoins + sons clés), placée sur le chrono.
# Voix : ElevenLabs Turbo 2.5 via Magnific (modèle économique), voix d'Elias montée de 4 demi-tons ; qualité d'animatique.
import os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
A = os.path.normpath(os.path.join(HERE, "..", "..", "audio", "SC02_mise-en-scene"))
BELL = os.path.normpath(os.path.join(HERE, "..", "..", "audio", "SC02-SH06", "SC02-SH06_bruitage_clochette_v1.wav"))
CUES = [  # (début en s, fichier, gain)
    (0.8, "00_reine_dictee.wav", 0.35),          # dictée (texte provisoire, non écrit dans le scénario)
    (5.0, "01_elias_maman_enfant.wav", 1.0),
    (7.0, "02_elias_ecoute_enfant.wav", 1.0),
    (9.6, "03_reine_plus-tard.wav", 1.0),
    (12.8, "04_chambellan_fleurs.wav", 0.8),     # à mi-voix, en aparté
    (14.6, "05_rires.wav", 0.8),
    (16.6, "06_reine_ce-soir.wav", 1.0),
    (18.4, "07_reine_cotes.wav", 1.0),
    (20.0, "08_reine_droit.wav", 1.0),
    (21.4, "09_chambellan_trente-ans.wav", 1.0),
    (26.8, "10_reine_souviens.wav", 0.9),
    (42.5, BELL, 0.7),                           # = SC02-SH06 retenu, clochette à 0,9 s
]
inputs, parts = [], []
for i, (t, f, g) in enumerate(CUES):
    inputs += ["-i", f if os.path.isabs(f) else os.path.join(A, f)]
    parts.append(f"[{i}]aresample=48000,aformat=channel_layouts=mono,volume={g},adelay={int(t*1000)}:all=1[a{i}]")
n = len(CUES)
fc = ";".join(parts) + ";" + "".join(f"[a{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0,apad=whole_dur=52.1,atrim=0:52.1[mix]"
wav = os.path.join(A, "SC02_mise-en-scene_voix-temoins.wav")
subprocess.run(["ffmpeg", "-v", "error", "-y", *inputs, "-filter_complex", fc, "-map", "[mix]", "-ar", "48000", wav], check=True)
src = os.path.join(HERE, "SC02_verification.mp4"); tmp = os.path.join(HERE, "_tmp_son.mp4")
subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", src, "-i", wav, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                "-c:a", "aac", "-b:a", "160k", "-shortest", tmp], check=True)
os.replace(tmp, src); print(src)
