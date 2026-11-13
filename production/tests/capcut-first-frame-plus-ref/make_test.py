# Génère le kit de test CapCut : first frame + vidéo de référence caméra (5 s, 24 i/s).
# Mouvement : départ cadré sur le château (gauche), pan droite + tilt bas + avancée
# vers la Rose jaune, avec accélération et décélération douces.
import math, os, subprocess, sys, tempfile
from PIL import Image
SRC = sys.argv[1]
im = Image.open(SRC).convert('RGB')          # 2560 x 1440
FPS, DUR = 24, 5
N = FPS * DUR
start = (0, 0, 1600)                          # x, y, largeur (16:9)
end = (730, 690, 1100)
ease = lambda t: 0.5 - 0.5 * math.cos(math.pi * t)
def crop(t, size):
    e = ease(t)
    x, y, w = (a + (b - a) * e for a, b in zip(start, end))
    h = w * 9 / 16
    return im.resize(size, Image.LANCZOS, box=(x, y, x + w, y + h))
crop(0, (1920, 1080)).save('SC00-TEST_A_first-frame.png')
crop(1, (1920, 1080)).save('SC00-TEST_B_last-frame.png')
tmp = tempfile.mkdtemp()
for i in range(N):
    crop(i / (N - 1), (1280, 720)).save(os.path.join(tmp, f'{i:04d}.png'))
subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i',
                os.path.join(tmp, '%04d.png'), '-c:v', 'libx264', '-pix_fmt', 'yuv420p',
                '-crf', '18', '-movflags', '+faststart', 'SC00-TEST_camera-ref.mp4'], check=True)
