import numpy as np, json, sys
exec(open('fit_camera.py').read().split('best = None')[0])
# géométrie libre : profondeur des ailes (y des tours d'extrémité), demi-largeur de cour, échelle de hauteur de la tour, demi-largeur de la tour
def geom(g):
    yw, cw, sh, tw = g
    pts = np.array(P, float)
    for i, (n, _, _) in enumerate(PTS):
        if n.startswith("tour_O_int"): pts[i, 0] = -(cw + 2.8)
        if n.startswith("tour_E_int"): pts[i, 0] = cw + 2.8
        if n.startswith("tour_") and not n.startswith("tour_O_ext_pied") or n.startswith("tour_O_ext_pied") or n.startswith("tour_O_int_pied"): pts[i, 1] = yw
        if n in ("fleche_pointe", "galerie_av_g", "galerie_av_d", "cadran"): pts[i, 2] = P[i, 2] * sh
        if n.startswith("galerie"): pts[i, 0] = np.sign(P[i, 0]) * tw
    return pts
P0 = P.copy()
def cost2(z):
    global P
    P = geom(z[6:]); c = cost(z[:6]) + 50 * ((z[8] - 1) ** 2); P = P0; return c
best = None
for yaw0 in (0.2, 0.4):
    for d0 in (120, 200):
        z0 = [-d0 * np.sin(yaw0) * 0.9, -d0 * np.cos(yaw0) * 0.9, d0 * 0.45, yaw0, -0.42, 40, -32, 17, 1.0, 7.4]
        z, c = nm(cost2, z0, [20, 20, 20, 0.1, 0.1, 10, 4, 3, 0.1, 1], iters=12000)
        if best is None or c < best[1]: best = (z, c)
z, c = best; P = geom(z[6:]); res = proj(z[:6]) - UV
print("camera", np.round(z[:3], 1).tolist(), "cap", round(np.degrees(z[3]), 1), "plongee", round(np.degrees(z[4]), 1), "focale", round(z[5], 1), "rms", round(np.sqrt(np.mean(np.sum(res**2,1))), 1))
print("aile_y", round(z[6], 1), "CW", round(z[7], 1), "echelle_tour", round(z[8], 2), "demi_galerie", round(z[9], 1))
for (n, _, uv), r in zip(PTS, res): print(f"  {n:20s} ecart {r[0]:+6.1f} {r[1]:+6.1f}")
json.dump({"loc": z[:3].tolist(), "yaw": z[3], "pitch": z[4], "lens": z[5], "geom": z[6:].tolist()}, open("cam_fit2.json", "w"))
