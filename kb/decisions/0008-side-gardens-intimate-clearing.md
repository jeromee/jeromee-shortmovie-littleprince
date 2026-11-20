# 0008 — Jardins latéraux et clairière resserrée

Statut : décidé (2026-11-20, auteur) · Origine : [auteur] [claude]

## Contexte
- Le muret du jardin v3 s'arrêtait au bout des ailes du palais : de sa fenêtre (aile est), Elias se retrouvait hors de l'enceinte et devait rentrer par un portillon. Les côtés du palais s'étaient aussi éloignés de `production/refs/palace-ref.png`, qui montre des allées latérales naturelles le long des ailes (remarque de l'auteur).
- La clairière du massif paraissait trop vaste (exèdre de 17 m, murets à 14 m, arche à 17 m du massif), loin de l'intimité de l'image de concept (remarque de l'auteur).

## Décision
1. **Jardins latéraux** : le muret à balustrade se prolonge autour des deux ailes jusqu'à l'arrière du palais. Le long de chaque façade extérieure : une allée de gravier courbe, une bordure de buis et une plate-bande, des cyprès, de grands arbres ronds contre le muret. Chaque allée latérale rejoint l'allée de ceinture de son côté. Le portillon disparaît.
2. **Chemin d'Elias la nuit** : il descend le long du lierre dans le jardin latéral est, suit l'allée latérale, puis l'allée de ceinture est (derrière la haie d'ifs) jusqu'à la serre et le bosquet. De sa fenêtre, il voit toujours le verger et les champs par-dessus le muret. Shooting script : « En bas, le jardin de l'aile, désert ; au-delà du muret, le verger. »
3. **Clairière resserrée et tournée** : massif de 6 m de diamètre ; murets à 7,5 m de son centre ; arche à 8 m ; exèdre de 10 m ; arbres rapprochés. L'ouverture de la clairière (l'arche) est tournée de 18° vers l'est : la caméra du massif, placée dans l'axe arche-massif, voit le massif au centre, l'arche derrière et la tour de l'horloge en haut à gauche, comme l'image de concept, sans enfilade arche-palais.
4. Banc retourné face au massif (il était posé à l'envers).

## Mise en œuvre
`production/blender/build_garden_v3.py` (`CLAIRIERE = "resserree"`, `LATERAUX = True`) et `place_garden_props.py` ; versions précédentes des deux scripts gardées en `*_avant-lateraux.py.txt`. Rendus de contrôle : `production/storyboard/candidates/_jardin_v3/v4_*.png`.

## Conséquences
Vue aérienne, quatre références du massif (jour, nuit, neige d'or, aube) et SC01-SH03 A à refaire, en génération directe.
