# Plan de masse d'Aurelia

Statut : décidé (2026-11-14, auteur) — v2, d'après `Import/Garden with Rose 01.png` et `Import/shot_01_tiny_kingdom.mp4` ; seul le palais en U vient de la v1.

Référence unique pour la géographie du film : la position des lieux les uns
par rapport aux autres, l'échelle et la lumière. Le blockout Blender
(`production/blender/`) et tous les cadrages en découlent.

## Échelle
- Planète **petite**, aux proportions de la vidéo `Import/shot_01_tiny_kingdom.mp4`
  (voir [aurelia.md](aurelia.md)) .

## Corrections demandées par l'auteur (2026-11-14)
- Vu en regardant le château depuis le jardin (comme sur l'image de concept) :
  **serre à droite**, fontaine murale à droite, banc et fontaine à vasques à
  gauche.
- **L'arche est entre le château et le massif.**
- **Le massif est à 100 m ou plus du château.**
- **Murets en courbes**, comme dans la vidéo, et non rectilignes.
- Palais en U conservé.

## Orientation et lumière
- Repère : le **palais est au nord**, le jardin au sud. L'image de concept est
  prise depuis le bord sud du jardin, en regardant le château (vers le nord) :
  la **serre est à droite (à l'est)**, le banc et la fontaine à vasques à
  gauche (à l'ouest).
- **Le soleil se lève à l'est, derrière la serre** ; il se couche à l'ouest
  (lumière orangée dans le cabinet de la Reine, scène 4).

## Le palais : en U, ouvert sur le jardin (au sud)
- **Corps central** au nord, avec la **tour de l'horloge** en son centre. La
  tour est prise dans le bâtiment (elle s'arrête à 9 m de la façade nord) ;
  sa **porte** est intérieure, sur sa face est, au fond du **grand vestibule**
  où l'on entre depuis la terrasse par les portes-fenêtres (2026-11-15, auteur).
- **Terrasse** entre les deux ailes, surélevée ; un **grand escalier** descend
  vers le jardin (comme dans la vidéo).
- **Aile est** : **chambre d'Elias** au 2e étage, fenêtre sur la **façade
  extérieure, à l'est** (2026-11-15, auteur) : verger, champs bordés de haies,
  ciel du sud-est ; aucun élément du palais n'est visible. Lierre sur cette
  façade (scène 6) : Elias s'évade sans être vu de la terrasse.
- **Aile ouest** : **cabinet de la Reine**, fenêtre sur la façade extérieure,
  au couchant.

## Le jardin : plateau ovale, murets courbes
- Jardin ovale d'environ 190 × 190 m (allongé de 40 % du nord au sud le 2026-11-15, auteur ; 190 × 135 auparavant), bordé d'un **muret courbe** à
  balustrade (comme dans la vidéo).
- Allée centrale du grand escalier jusqu'au massif ; allée transversale en
  ellipse, avec deux **petites arches** de part et d'autre.
- Parterres de buis courbes, cyprès isolés, groupes de grands feuillus sur
  les côtés.
- **Serre** à l'est, à mi-distance ; **fontaine à vasques** à l'ouest.
- **L'arche de roses** est sur l'allée centrale, **entre le château et le
  massif**, juste avant lui.
- **Le grand massif**, avec la Rose, est au **bord sud du jardin, dans une
  exèdre** (niche semi-circulaire du muret), avec le banc à gauche et la
  fontaine murale à droite. Il est à environ **210 m de la façade** (2026-11-15 ; 130 auparavant) du
  palais.

## Palais officiel en 3D — décidé (2026-11-15, auteur)
Le palais de la maquette est désormais un **modèle 3D** généré par l'auteur avec Tripo
(compte personnel) à partir de `production/refs/palace-ref-cleaned.png` (palace-ref
nettoyé : arbre retiré, fond gris, escaliers conservés). Original :
`Import/palace-tripo-test/palace-tripo-test-v2.glb` ; copie de travail :
`production/blender/assets/palace_official.glb` ; mise en place :
`production/blender/place_palace.py` (collection `AUR_12_palais_tripo`, objet
`PALAIS_officiel`). Les blocs gris (`AUR_10_palais`, `AUR_11_tour`) restent pour mémoire
mais sont exclus des plans. L'auteur préfère les proportions de ce modèle : **le reste
s'aligne sur lui** (elles priment sur les mesures proposées plus bas).

Mesures relevées sur le modèle placé (largeur totale calée à 82,8 m, pied du grand
escalier inchangé à 34 m au sud de l'origine) :
| Élément | Mesure |
|---|---|
| Emprise | 82,8 × 49 m ; flèche de la tour à ≈ 51 m |
| Terrasse (cour) | 37,6 m de large (faces intérieures des ailes à ± 18,8 m) × ≈ 20 m de profondeur ; niveau 3,6 m |
| Grand escalier | du bord de la terrasse au jardin, ≈ 6,5 m |
| Corps central | façade sud alignée sur la face sud de la tour ; ≈ 16 m de profondeur |
| Ailes | faces extérieures à ± 36,7 m ; bout sud à ≈ 20 m de la façade |
| Tour | ≈ 8,6 m de large ; galerie et étage des cloches vers 38–42 m |
| Orangers en caisses | sur la terrasse, le long des façades (fournis par le modèle) |

Repères recalés : fenêtre d'Elias sur la face extérieure de l'aile est ; porte de la
tour sur sa face est, au fond du vestibule ; cabinet de la Reine sur la face extérieure
de l'aile ouest.

## Dessin
![Plan de masse v2](site-plan.png)

Mesures proposées : corps central ≈ 72 × 20 m, ailes ≈ 19 × 29 m (jusqu'à 35 m de la façade), terrasse
≈ 34 × 24 m, grand escalier 14 m de large, tour ≈ 14 × 12 m au sol, en avant-corps de 1 m sur la terrasse (recalés le 2026-11-14 sur `production/refs/palace-ref.png`), jardin ≈ 190 × 195 m, exèdre ≈ 34 m de
diamètre, massif ≈ 9 m de diamètre, serre ≈ 16 × 10 m (6 m de haut).

## Blockout Blender (monde maître) — validé par l'auteur, 2026-11-14
- Fichier : `production/blender/world.blend`, reconstruit par
  `production/blender/build_world.py` (idempotent : ne touche qu'aux
  collections `AUR_*`). Repère : X = est, Y = nord, origine au centre de la
  tour, z = 0 au niveau du jardin.
- **Planète** : sphère de **4 km de diamètre** (décidé ; constante `R_PLANET`). Le palais et le jardin sont sur un plateau
  plat au sommet ; trois villages et des forêts sont posés sur la sphère.
- Hauteurs décidées : terrasse à 4 m au-dessus du jardin, corps central 22 m,
  ailes 19 m, toits à croupes (faîtage du corps à 30 m), tour : galerie du beffroi à 40 m, cloches jusqu'à 48 m, flèche jusqu'à 62 m (recalée le 2026-11-14 sur `production/refs/palace-ref.png`), arche de roses 5,2 m. Le dessin `site-plan.svg` n'est pas encore mis à jour de ces mesures.
- Caméras de contrôle : `CAM_concept` (point de vue de l'image de concept),
  `CAM_plongee`, `CAM_espace`, `CAM_terrasse`, `CAM_sommet_tour`,
  `CAM_serre_haut` (scène 8).

### Code couleur des repères (maquettes et prompts)
| Repère | Couleur |
|---|---|
| Elias | bleu |
| La Reine | rouge |
| Le Chambellan | vert vif |
| La Rose | jaune (réservé) |
| Arche de roses | rose soutenu |
| Petites arches | vieux rose |
| Serre | cyan |
| Porte de la tour | brun-rouge |
| Fontaines | bleu-gris |
| Palais / tour / toits | sable / or sombre / ardoise |

## Alentours du palais — décidé (2026-11-15, auteur)
D'après la référence aérienne `production/refs/palace-aerial.png` (vue du sud, ≈ 200 m de haut ; caméra `CAM_aerien_ref`) :
- Hors de l'enceinte, **un seul muret** : au-delà, prairie en pente douce (le plateau n'est pas une terrasse).
- **Une petite rivière** en méandres descend à l'ouest du jardin, du nord-ouest vers le sud, et passe devant l'exèdre ; **deux ponts de pierre en dos d'âne** (au nord-ouest et au sud-ouest).
- **Chemins** de terre : vers la forêt à l'ouest (par le pont nord), vers le village rouge au nord, en grande boucle à l'est, et vers le sud-ouest par le pont sud.
- À l'est : un **petit verger** et des **champs bordés de haies** ; bosquets épars ; fleurs des champs.
- Dans la maquette : collection `AUR_23_alentours` (positions relevées sur l'image et projetées au sol, `production/refs/match/pick_ground.py`).
- Proportions (2026-11-15, auteur) : un grand palais demande un grand jardin. Plutôt que réduire le palais, on a **allongé le jardin de 40 % du nord au sud** (maquette : `GARDEN_DEPTH = 1.4` dans `build_world.py`) ; la référence aérienne a été refaite avec ces proportions (palais ≈ un tiers de la largeur du jardin, au lieu de 0,57 sur l'ancienne version). Le plateau et le centre de la planète ont été décalés de 25 m vers le sud pour porter le jardin allongé.

## Liens
[aurelia.md](aurelia.md) · [royal-garden.md](royal-garden.md) · [palace-sets.md](palace-sets.md)
