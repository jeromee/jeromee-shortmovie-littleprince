# 0012 — Clairière v2 : massif à sa vraie hauteur, passage jusqu'à la Rose, végétation de l'exèdre

Statut : décidé (2026-11-22, auteur) · Origine : [auteur] remarques sur la mise en scène de SC03 ; [claude] mise en œuvre

## Constat (remarques de l'auteur sur la première mise en scène de SC03)
- Le modèle 3D du massif avait été **écrasé à 60 % en hauteur** (`place_garden_props.py`, `ZSCALE rose_bed 0.6`, 2026-11-20) pour
  ramener la grande fleur jaune centrale du modèle Tripo de 2,15 m à 1,3 m : les rosiers ne faisaient plus que 0,3–0,5 m et la
  bordure 0,22 m.
- La Rose, au centre d'un massif de 5,2 m, était à ≈ 2,9 m d'Elias à genoux sur la bordure : trop loin pour se parler, et pour
  qu'elle lui donne un pétale (scène 8) ou qu'il s'endorme « tout près d'elle » (scène 12).
- Dans les contrechamps sur Elias, il n'y avait derrière lui que le muret de l'exèdre (1,28 m) et le ciel.

## Décision (choix de l'auteur parmi des options proposées)
1. **Massif à sa vraie hauteur** (rosiers 0,7–0,9 m, bordure 0,40 m) ; la grande fleur centrale du modèle Tripo est retirée :
   **la Rose est désormais un objet à part** (provisoire `ROSE_provisoire`, ≈ 1,15 m ; modèle 3D à faire), animable.
2. **Passage de pas japonais** : un passage rectiligne de trois dalles carrées ou rectangulaires (précision de l'auteur, 2026-11-22 soir) depuis la bordure sud-sud-est (azimut -70°) jusqu'à **un petit rond de mousse**
   (≈ 1 m de diamètre) au pied de la Rose. Elias s'y agenouille à ≈ 0,6 m de la fleur ; en scène 12, il s'y endort.
   Vu de loin, depuis l'axe de l'image de concept, le passage et le creux du centre restent un peu visibles (les rosiers les
   cachent en partie) : les images devront les montrer discrets, mousse et dalles entre les rosiers.
3. **Végétation au sud** : rosiers grimpants sur le muret de l'exèdre, grands arbustes fleuris juste derrière lui
   (≈ 2,5–3,2 m), grands arbres au-delà (tilleuls et cyprès). Le muret reste bas.

## Mise en œuvre
`production/blender/clairiere_v2.py` (`appliquer()`, rejouable) ; copie du fichier d'avant : `production/blender/world_avant-clairiere-v2.blend`.
Si `place_garden_props.py` est relancé, relancer ensuite `clairiere_v2.appliquer()`.

## Conséquences
- `kb/world/royal-garden.md` et `kb/characters/rose.md` complétés ; le bloc canonique du jardin mentionne le passage et la mousse.
- Les images de référence du massif (`production/refs/garden-*.png`) ne montrent ni le passage, ni la mousse, ni la végétation
  de l'exèdre : à refaire avant les images de début et de fin des scènes 3, 8, 12 et 13.

## Complément (2026-11-22, soir)
- Dalles carrées ou rectangulaires, passage rectiligne (demande de l'auteur).
- 77 tilleuls et cyprès Tripo du bosquet (entre le massif et le palais), visibles dans la vue 3D mais exclus du rendu sans raison connue,
  sont réactivés au rendu, pour que les animatiques aient la même végétation que Blender (liste : `production/blender/_arbres_rendu_reactives_2026-11-22.txt`).
  Les maquettes de SC01 et SC02 rendues avant cette date n'avaient pas ces arbres : à garder en tête si on refait leurs images.

## Complément (2026-11-22, nuit)
- **Rosiers à l'échelle** (demande de l'auteur : « les roses autour sont énormes ») : le maillage Tripo du massif avait été agrandi
  depuis un massif beaucoup plus petit, d'où des fleurs démesurées. Le massif garde sa bordure de pierre (`GARDEN_rose_bed_v3_bordure_mesh`)
  et une terre neuve ; les fleurs sont désormais 38 rosiers d'un modèle à l'échelle (buisson de 0,80 m, petites roses roses et pêche),
  répartis hors du passage et de la mousse. Script : `production/blender/massif_rosiers.py` ; copie d'avant : `world_avant-massif-rosiers.blend`.
  Planche : `production/refs/rosier-sheet.png`.
- **La Rose au repos** a un vrai modèle (`production/props3d/rose_asleep_tripo_v1.glb`, planche `production/refs/rose-asleep-sheet.png`),
  utilisé par `ROSE_provisoire` et par la Rose animée de SC03.
- Les images de référence du massif à refaire (voir Conséquences) doivent montrer ces rosiers à l'échelle.
