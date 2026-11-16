# Ajuste une caméra (position, cap, plongée, focale) pour que des points de la maquette
# tombent sur leurs positions mesurées dans l'image de référence (1000 x 562).
import numpy as np, json, sys
W, H, SW = 1000.0, 562.5, 36.0
PTS = [  # (nom, point monde Blender, pixel mesuré)
 ("fleche_pointe", (0, -1, 62), (465, 22)),
 ("galerie_av_g", (-7.4, -8.4, 40.2), (410, 145)),
 ("galerie_av_d", (7.4, -8.4, 40.2), (522, 147)),
 ("cadran", (0, -7.3, 33.5), (482, 197)),
 ("porte_bas", (0, -7.3, 4), (485, 345)),
 ("tour_O_ext_pointe", (-36, -32, 37), (228, 185)),
 ("tour_O_int_pointe", (-19.8, -32, 34), (392, 225)),
 ("tour_E_int_pointe", (19.8, -32, 34), (690, 205)),
 ("tour_E_ext_pointe", (36, -32, 37), (765, 150)),
 ("tour_O_ext_pied", (-36, -32, 0), (240, 515)),
 ("tour_O_int_pied", (-19.8, -32, 0), (393, 470)),
]
P = np.array([p[1] for p in PTS], float); UV = np.array([p[2] for p in PTS], float)
def proj(x):
    cx, cy, cz, yaw, pitch, f = x
    fwd = np.array([np.sin(yaw) * np.cos(pitch), np.cos(yaw) * np.cos(pitch), np.sin(pitch)])
    right = np.array([np.cos(yaw), -np.sin(yaw), 0.0]); up = np.cross(right, fwd)
    d = P - np.array([cx, cy, cz]); z = d @ fwd
    u = W / 2 + (f / SW) * W * (d @ right) / z; v = H / 2 - (f / SW) * W * (d @ up) / z
    return np.stack([u, v], 1)
def cost(x): return float(np.sum((proj(x) - UV) ** 2))
def nm(f, x0, steps, iters=6000):
    n = len(x0); S = [np.array(x0, float)] + [np.array(x0, float) + np.eye(n)[i] * steps[i] for i in range(n)]
    F = [f(s) for s in S]
    for _ in range(iters):
        o = np.argsort(F); S = [S[i] for i in o]; F = [F[i] for i in o]
        c = np.mean(S[:-1], 0); r = c + (c - S[-1]); fr = f(r)
        if fr < F[0]:
            e = c + 2 * (c - S[-1]); fe = f(e)
            S[-1], F[-1] = (e, fe) if fe < fr else (r, fr)
        elif fr < F[-2]: S[-1], F[-1] = r, fr
        else:
            k = c + 0.5 * (S[-1] - c); fk = f(k)
            if fk < F[-1]: S[-1], F[-1] = k, fk
            else:
                S = [S[0]] + [S[0] + 0.5 * (s - S[0]) for s in S[1:]]; F = [f(s) for s in S]
    i = int(np.argmin(F)); return S[i], F[i]
best = None
for yaw0 in (0.1, 0.25, 0.4, 0.6):
    for d0 in (120, 200, 300):
        x0 = [-d0 * np.sin(yaw0) * 0.9, -d0 * np.cos(yaw0) * 0.9, d0 * 0.45, yaw0, -0.42, 40]
        x, c = nm(cost, x0, [20, 20, 20, 0.1, 0.1, 10])
        if best is None or c < best[1]: best = (x, c)
x, c = best
res = proj(x) - UV
print("camera", np.round(x[:3], 1).tolist(), "cap", round(np.degrees(x[3]), 1), "plongee", round(np.degrees(x[4]), 1), "focale", round(x[5], 1), "rms px", round(np.sqrt(c / len(P)), 1))
for (n, _, uv), r in zip(PTS, res): print(f"  {n:20s} ecart {r[0]:+6.1f} {r[1]:+6.1f}")
json.dump({"loc": x[:3].tolist(), "yaw": x[3], "pitch": x[4], "lens": x[5]}, open(sys.argv[1], "w"))
