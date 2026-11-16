# Projette des points mesurés sur palace-aerial.png (1000 x 562) sur le sol de la maquette
# (sphère de la planète), à travers la caméra CAM_aerien_ref. Sortie : coordonnées du plan (x, y_sud).
import numpy as np, json
W, H, SW, F = 1000.0, 562.5, 36.0, 35.0
C = np.array([0, -380, 190.0]); T = np.array([0, -55, 8.0])
fwd = (T - C) / np.linalg.norm(T - C); right = np.cross(fwd, [0, 0, 1]); right /= np.linalg.norm(right); up = np.cross(right, fwd)
PC = np.array([0, -80, -2000.0]); R = 2000.0
def ground(u, v):
    x = (u - W / 2) / (F / SW * W); y = (H / 2 - v) / (F / SW * W)
    d = fwd + x * right + y * up; d /= np.linalg.norm(d)
    oc = C - PC; b = oc @ d; c = oc @ oc - R * R; disc = b * b - c
    if disc < 0: return None
    t = -b - np.sqrt(disc); p = C + t * d
    return [round(float(p[0]), 1), round(float(-p[1]), 1)]
SETS = {
 "riviere": [(5,218),(50,232),(85,245),(108,275),(105,315),(92,355),(100,395),(135,430),(185,462),(225,495),(265,530),(300,560)],
 "pont_nord": [(60,232)], "pont_sud": [(180,455)],
 "chemin_ouest": [(285,172),(220,185),(130,205),(60,235),(0,265)],
 "chemin_sud_ouest": [(215,470),(140,492),(60,520),(0,545)],
 "chemin_village": [(690,140),(660,115),(650,100),(672,88)],
 "chemin_est": [(760,185),(860,230),(950,300),(990,360),(950,400),(870,440),(800,480),(770,540)],
 "verger": [(830,300),(940,300),(940,370),(830,370)],
 "haies": [(790,140),(1000,150),(800,190),(1000,250),(860,135),(830,250)],
 "controle_massif": [(500,480)], "controle_tour": [(500,250)],
}
out = {k: [ground(u, v) for u, v in pts] for k, pts in SETS.items()}
for k, v in out.items(): print(k, v)
json.dump(out, open("ground_points.json", "w"), indent=1)
