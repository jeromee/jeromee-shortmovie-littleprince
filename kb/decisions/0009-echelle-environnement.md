# 0009 — Environnement réduit ×0,8, personnages à taille réelle

Statut : décidé (2026-11-20, auteur) · Origine : [auteur] [claude]

## Contexte
La maquette était exacte en mètres, mais les personnages paraissaient trop petits sur la grande terrasse vide du palais (remarque de l'auteur, surtout sur SC02-SH06). Repère : la porte de la tour (4 m à la naissance de l'arc, 4,5 m sous la clé) faisait 2,5 fois la Reine et 3,3 fois Elias.

## Décision
1. **Tout l'environnement est réduit d'un facteur 1,25 (×0,8)** — palais, jardin, terrain, distances, caméras — en gardant **à taille réelle** les personnages et les objets mesurés à la taille d'un corps : fauteuils, banc, fontaine murale, télescope, orangers (2,5 m) et leurs socles. Porte de la tour : ≈ 3,2 m (3,6 m sous la clé) ; terrasse ≈ 30 × 16 m ; marches ≈ 16 cm ; balustrade ≈ 0,9 m ; massif de la Rose Ø ≈ 5,3 m ; distance tour-massif ≈ 174 m.
2. Les vues sans personnage (vue aérienne, clairière jour, nuit, neige d'or, aube) donnent la même image : les références retenues restent valables.
3. **Terrasse garnie** d'éléments utiles à l'histoire (la cour prépare une soirée pour regarder le ciel) : un velum bleu roi au-dessus des fauteuils et une table de rafraîchissements (planches à choisir, puis modèles Tripo).
4. **Caméra** : pour les plans de dialogue sur la terrasse, caméra à hauteur d'œil, personnages plus groupés et cadrés plus serré, orangers et fauteuils au premier plan ; réglé plan par plan en refaisant les vignettes.

## Mise en œuvre
`production/blender/echelle_monde.py` : un Empty `ECHELLE_MONDE` d'échelle 0,8 à l'origine devient le parent de tous les objets ; les objets à taille humaine reçoivent une échelle locale 1,25 autour de leur base. À relancer après tout script qui crée des objets. Copie d'avant : `production/blender/world_avant-echelle-0.8.blend`. Les cotes écrites dans `kb/world/site-plan.md` et dans les scripts restent celles d'avant la réduction (multiplier par 0,8).

## Conséquences
Vignettes à refaire pour les plans avec personnages : SC01-SH03 B, SC02-SH01 à SH06.

## Suite (2026-11-20)
- Planches retenues par l'auteur : velum `terrace-velum_gpt26_nb2`, table `refreshment-table_gpt26_nb1` ; modèles Tripo v3.1 posés par `production/blender/place_terrasse.py` (collection `AUR_14_terrasse_soiree`, liée aux scènes qui ont des fauteuils), rattachés à `ECHELLE_MONDE` et dimensionnés en mètres réels.
- **Deux velums au lieu d'un** [claude] : un velum unique au-dessus de l'allée centrale cachait Elias et le haut de l'escalier dans SC02-SH06 (caméra haute, vers le sud). Deux velums de 3,4 × 4,2 m, 3,2 m de haut, couvrent les paires intérieures de fauteuils de part et d'autre de l'allée ; l'allée reste libre et les velums encadrent Elias. Version à un velum gardée dans `place_terrasse_velum-central.py.txt`. Planche de comparaison : `production/storyboard/candidates/_velum/_planche_SH06_velum.jpg`.
- Table : côté ouest de la terrasse, entre deux orangers, à l'ouest du groupe de la cour ; visible dans SC01-SH03 B seulement.
- Caméras revues : SC02-SH02 (1,2 m, avancée de 0,7 m, un mât du velum coupait le cadre), SC02-SH03 (1,5 m), SC02-SH04 (1,18 m, hauteur des yeux d'Elias). La réduction avait abaissé les caméras avec le décor alors que les personnages gardaient leur taille. SC02-SH01, SH05, SH06 et SC01-SH03 inchangées.
