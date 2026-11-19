# Accessoires et effets

Statut : décidé (2026-11-13, auteur) · Date : 2026-11-02 · Origine : [claude] shooting script

## Accessoires

### La clochette bleue (scènes 2, 3)
Une campanule d'un bleu cobalt lumineux, à clochettes en grappe, cueillie dans
le jardin. Quand elle « sonne » pour Elias, ses clochettes frémissent et un
minuscule scintillement argenté s'en échappe — que personne d'autre ne remarque.

**EN (à coller)**
```text
a small sprig of bright cobalt-blue bellflowers (campanula) held in a child's cupped hands; when it rings, the tiny bells tremble and release a faint silver shimmer
```

### Le pendentif-clé (scènes 2, 4, 9)
Le petit pendentif du collier de perles roses de la Reine (déjà sur sa planche).
**Décidé (2026-11-13, auteur)** : c'est une minuscule clé d'or dont l'anneau a
la forme d'une **rose couronnée** — les armoiries, encore. Fermée contre la
gorge, on la prend pour un simple bijou. Elle n'ouvre pas la grande serrure de
la tour, mais la serrure secrète cachée au cœur d'une des dizaines de petites
roses couronnées sculptées sur la porte ; son anneau a la même forme que ces
motifs (voir [palace-sets.md](palace-sets.md)).

**Le pendentif-étui** — décidé (2026-11-15, auteur) : on ne voit jamais le
panneton. La rose couronnée (l'anneau de la clé) est posée dans un **calice**
d'or à cinq sépales, au sommet d'un fin **étui** d'or ciselé et fuselé qui se
termine par une petite perle rose. Les deux sépales latéraux finissent en
anneaux où passe le fil de perles : l'étui est enfilé sur le collier, la rose
n'y est que posée. Pour donner la clé, la Reine **tire la rose vers le haut** :
la tige et le panneton sortent de l'étui, qui reste au collier (scène 9).
Planche : `production/refs/key-pendant-sheet.png` (candidate
« pendant-etui-calice_v2_nb1 ») — 1 porté, 2 seul, 3 la clé qu'on tire,
4 la clé dans la paume d'Elias.

**La serrure secrète** — planche `production/refs/key-lock-sheet.png`
(candidate « nb2 ») : seules ses images 3 et 4 font foi (une rose de la porte au
repos, sans serrure visible ; la même rose révélée par la lumière dorée, la
clé qui entre). Ses images 1 et 2 montrent l'ancien pendentif, remplacé par
l'étui. L'anneau est une rose compacte couronnée, sans tige ni feuilles.

**Design visuel** (demande de l'auteur, faite) : planche dédiée de la
clé et de la serrure secrète avant le découpage de la scène 10 — la clé doit
être lisible en gros plan, rester crédible comme bijou, et « répondre » aux
roses sculptées de la porte.

**EN (à coller)**
```text
a slender chased-gold pendant strung on a pink pearl necklace: a small crowned gold rose sitting in a gold calyx whose two side sepals end in rings the pearl strand passes through, above a tapered gold sheath ending in a tiny pink pearl drop; the rose is the bow of a tiny gold key hidden inside the sheath, and pulling the rose upward draws the key out while the sheath stays on the necklace
```

### Le pétale de lumière (scènes 8, 9, 11)
Un pétale de la Rose, jaune pâle et velouté, grand comme une paume d'enfant ; il
brille de l'intérieur d'une lumière d'or chaude, avec de fines particules
dorées qui s'en échappent. Elias le tient serré contre sa poitrine, les mains
croisées dessus : sa lumière filtre entre ses doigts.
**Planche de référence** — décidé (2026-11-15, auteur) : `production/refs/petal-sheet.png`
(candidate « nb2 ») — 1 dans ses mains (scène 8), 2 contre sa poitrine
(scènes 9-10), 3 levé à deux mains, il s'embrase et la bulle s'ouvre
(scène 11), 4 éteint, un fil d'or s'élève (fin de la scène 11).

**EN (à coller)**
```text
a single pale-yellow velvety rose petal the size of a child's palm, glowing from within with warm golden light, fine golden particles drifting off it; light leaking between the fingers when hidden in a hand
```

### Orangers en pot (terrasse)
Statut : décidé pour la planche (2026-11-17, auteur : « proche de nb2, grosses oranges mieux réparties ») ; modèle 3D en test · Origine : [auteur] [image]
- Orangers taillés en boule dense sur tige, petites feuilles vert sombre, grosses oranges mûres réparties sur toute la couronne, quelques fleurs blanches, dans de grands bacs ronds en terre cuite.
- **Planche de référence** : `production/refs/orange-tree-sheet.png` (v2 nb1). Candidates précédentes dans `production/refs/candidates/orange-tree_*.png`. À joindre en référence à toute vignette où un oranger est visible, et à désigner dans le prompt (« exactement comme l'arbre de @imgN »). Test sur SC02-SH03 avec la planche nb2 : arbre gardé à sa place et à sa taille (`production/characters3d/renders/oranger_test_SH03.jpg`).
- **Modèle 3D** : `production/props3d/orange_tree_tripo_v1.glb` (Tripo v3.1, une seule vue). Huit copies sur la terrasse, aux places des orangers d'origine, posées par `production/blender/place_orangers.py`. **Hauteur : 2,50 m, bac compris** (bac ≈ 0,72 m, plus bas que le dossier d'un fauteuil ; couronne ≈ Ø 1,3 m), sur un **socle rond de pierre** (Ø 1,4 m, réduit à la demande de l'auteur ; les taches vertes des anciens bacs sur le dallage sont masquées par une pièce de dallage de Ø 2,4 m prise sur la texture voisine) — 2026-11-19, remarque de l'auteur : à 4,18 m (taille des arbres du palais d'origine), les orangers paraissaient gigantesques, le bac aussi haut qu'un fauteuil.
- **Palais sans orangers** : les orangers d'origine faisaient partie du mesh du palais Tripo. Le script en fait une copie, `PALAIS_officiel_sans_orangers`, d'où les arbres sont découpés ; `PALAIS_officiel` reste dans le fichier, masqué. Reste visible : de légères taches vertes sur le dallage autour des bacs (texture d'origine).

### Fauteuils de terrasse
Statut : décidé pour la planche (2026-11-18, auteur : piste B nb1, noyer et velours bleu roi) ; modèle 3D fait et posé dans les plans (2026-11-18) · Origine : [auteur] [image] [claude]
- **Planche de référence** : `production/refs/terrace-armchair-sheet.png` (copie de `candidates/terrace-armchair/terrace-armchair_B-noyer-bleu-roi_gpt26_nb1.png`) : bâti de noyer ciré sculpté, pieds cambrés, manchettes rembourrées ; assise, dossier ovale capitonné et manchettes en velours bleu roi soutenu ; dos du dossier en velours uni. À joindre en référence à toute vignette où un fauteuil est visible.
- **Modèle 3D** (2026-11-18) : Tripo v3.1 multivue (face, côté, dos, et le côté en miroir pour l'autre côté, le fauteuil étant symétrique), vues découpées de la planche dans `production/props3d/terrace-armchair_views/`. Brut : `production/props3d/terrace_armchair_tripo_v1.glb` (1,9 million de faces). Version allégée à 57 000 faces (décimation), 0,98 m de haut, 0,67 × 0,60 m au sol, face avant vers −Y (le jardin), base à z = 0 : `production/props3d/terrace_armchair_tripo_v1_light.glb`, et dans `world.blend` l'objet `FAUTEUIL_terrasse_master` (collection `AUR_14_fauteuils`, scène `TEST_FAUTEUIL`). Vues de contrôle : `terrace-armchair_views/_check_tripo_v1.jpg`. Posé le 2026-11-18 par `production/blender/place_fauteuils.py` : 16 copies liées (deux rangées de huit, y = −21,5 et −23,5 m, tournées vers le jardin ; depuis le 2026-11-19, par paires de part et d'autre des orangers de la terrasse, x = ±3, ±5, ±10 et ±12 m : à ±8 m, deux fauteuils tombaient dans les bacs des orangers) dans chaque plan SC02-SH01 à SH06, à la place des boîtes brunes (masquées), et les mêmes rangées dans SC01-SH03 (collection `SC01-SH03_jeu`). Le maître est rangé, masqué, dans `AUR_32_persos3d_rig`. Visibles à l'image : SC01-SH03 (fin), SC02-SH01 (un fauteuil en bas à droite), SC02-SH02 (en mouvement), SC02-SH06 (quatre fauteuils de dos).
- Rôle : rangées de fauteuils que les valets installent sur la terrasse face au ciel (scènes 1 et 2). Un seul modèle, pour que les fauteuils soient les mêmes d'un plan à l'autre ; une fois la planche retenue, conversion en modèle 3D dans Tripo, comme les orangers.
- Pistes de l'auteur : les fauteuils de `SC01-SH03_B_v4_gpt26_nb1` (bois doré, tissu bleu un peu passé, non uni) et ceux de `SC02-SH06_A_v2_nb1` (bleu soutenu qui ressort sur la pierre chaude). Recadrages joints en référence : `production/refs/candidates/terrace-armchair/_crop_*.png`.
- Planches candidates (GPT 2.6, 2K, deux variantes chacune) : `production/refs/candidates/terrace-armchair/terrace-armchair_<piste>_gpt26_nb1|nb2.png`, planche comparative `_cmp_terrace-armchair.jpg`.

| Piste | Bâti | Tissu | Référence jointe |
|---|---|---|---|
| A | bois doré sculpté, rocaille | bleu passé, damas à grands médaillons | recadrage SC01-SH03_B |
| B | noyer ciré sculpté | velours bleu roi soutenu, dossier capitonné | recadrage SC02-SH06_A |
| C | bois doré sculpté (de A) | velours bleu roi capitonné (de B), galon or | les deux |
| D | bois doré sculpté | velours bleu nuit semé de petites étoiles d'or, rose couronnée brodée en haut du dossier | aucune (proposition de Claude) |
| E | style Louis XVI, laqué ivoire rechampi d'or, pieds droits cannelés, dossier médaillon | soie à larges rayures crème et bleu bleuet | aucune (proposition de Claude) |

Prompt commun, suivi de la ligne propre à chaque piste :

**FR (référence)**
```text
Planche de design d'accessoire pour un long métrage d'animation 3D stylisé, 16:9, fond blanc uni avec de légères ombres de contact, sans texte ni légende. Un seul et même fauteuil de terrasse montré quatre fois, identique dans chaque vue et à la même échelle, toujours en entier : vue de face, vue de trois quarts avant, vue de côté, vue de dos ; caméra à hauteur d'assise, lumière de studio douce et égale. C'est un fauteuil de palais royal français des années 1830 (style cabriolet Louis XV), élégant mais solide, assez léger pour qu'un valet le porte seul, installé sur une terrasse de pierre dorée pour que la cour regarde le ciel ; le dossier est très légèrement incliné. Formes nettes et lisibles, faciles à convertir en modèle 3D. Ni personnage ni autre objet.
A — Le fauteuil : les mêmes fauteuils que les petits fauteuils lointains de l'image 1. Bâti de bois doré sculpté, petite sculpture rocaille en haut du dossier et sur les genoux des pieds cambrés, manchettes rembourrées ; assise, dossier et manchettes garnis d'un tissu bleu un peu passé, délavé par le soleil, non uni : un doux damas bleu-gris à grands médaillons floraux.
B — Le fauteuil : les mêmes fauteuils que ceux de l'image 1. Bâti de noyer ciré, fines sculptures en haut du dossier ovale, pieds cambrés, manchettes rembourrées ; assise, dossier ovale et manchettes garnis d'un velours bleu roi profond et saturé, dossier capitonné.
C — Le fauteuil : un mélange des fauteuils de l'image 1 et de l'image 2. Le bâti de bois doré sculpté de l'image 1 (petite sculpture rocaille en haut du dossier et sur les genoux des pieds cambrés, manchettes rembourrées), garni comme dans l'image 2 d'un velours bleu roi profond et saturé, capitonné sur le dossier ovale, bordé d'un fin galon d'or.
D — Le fauteuil : bâti de bois doré sculpté, pieds cambrés, manchettes rembourrées ; assise, dossier ovale et manchettes garnis d'un velours bleu nuit brodé d'un léger semis de petites étoiles d'or, et d'une petite rose couronnée brodée d'or en haut du dossier.
E — (sans « style cabriolet Louis XV » dans le prompt commun) Le fauteuil : style Louis XVI, dossier en médaillon ovale, pieds droits fuselés et cannelés, manchettes rembourrées ; bâti laqué ivoire, sculptures rechampies d'or ; assise, dossier et manchettes garnis d'une soie à larges rayures crème et bleu bleuet profond.
```
**EN (à coller)**
```text
Prop design sheet for a stylized 3D animated feature film, 16:9, plain white background with soft contact shadows, no text, no labels. One single terrace armchair shown four times, identical in every view and at the same scale, the whole chair always visible: front view, three-quarter front view, side view, back view; camera at seat height, soft even studio light. It is an 1830s French royal palace armchair (Louis XV cabriolet style), elegant but sturdy, light enough for one footman to carry, set out on a golden-stone terrace so the court can watch the sky; the back is very slightly reclined. Clean, readable shapes that can be turned into a 3D model. No people, no other objects.
A — The armchair: the same armchairs as the small distant ones in Image 1. Frame of carved gilded wood, with a small rocaille carving at the top of the back and on the knees of the curved cabriole legs, padded armrests; seat, back and armrest pads upholstered in a slightly faded, sun-washed blue fabric that is not plain: a soft blue-gray damask pattern of large floral medallions.
B — The armchair: the same armchairs as in Image 1. Frame of warm polished walnut with fine carvings along the top of the oval back, curved cabriole legs, padded armrests; seat, oval back and armrest pads upholstered in a deep, saturated royal-blue velvet, button-tufted on the back.
C — The armchair: a blend of the armchairs of Image 1 and Image 2. The carved gilded-wood frame of Image 1 (a small rocaille carving at the top of the back and on the knees of the curved cabriole legs, padded armrests), upholstered like Image 2 in a deep, saturated royal-blue velvet, button-tufted on the oval back, edged with a thin gold braid.
D — The armchair: frame of carved gilded wood, curved cabriole legs, padded armrests; seat, oval back and armrest pads upholstered in midnight-blue velvet embroidered with a light scattering of small golden stars, and one small embroidered golden crowned rose at the top of the back.
E — (without "Louis XV cabriolet style" in the common prompt) The armchair: Louis XVI style, a medallion-shaped (oval) back, straight fluted tapered legs, padded armrests; frame lacquered in ivory white with its carved details picked out in gold; seat, back and armrest pads upholstered in a silk with wide stripes of cream and deep cornflower blue.
```

### Objets du jardin v3 (serre, fontaine à vasques, arche, banc, fontaine murale, if, cyprès, tilleul)
Statut : décidé pour les planches (2026-11-19, auteur) ; modèles 3D posés dans la maquette · Origine : [auteur] [claude]
- **Planches retenues** (copiées dans `production/refs/`) : `bench-sheet.png` (banc nb2), `garden-plants-sheet.png` (if, cyprès, tilleul nb1), `greenhouse-sheet.png` (serre nb2), `lion-wall-fountain-sheet.png` (fontaine murale nb1), `rose-arch-sheet.png` (arche nb1), `tiered-fountain-sheet.png` (fontaine à vasques nb2). À joindre en référence à toute vignette où l'objet est en gros plan.
- **Modèles 3D** (Tripo v3.1 ; multivue face, côté, dos et côté en miroir pour les objets symétriques ; une seule vue pour les végétaux) : `production/props3d/<objet>_tripo_v1.glb` ; vues découpées dans `production/props3d/garden_views/`. Allégés et posés par `production/blender/place_garden_props.py` (maîtres `GARDEN_<clé>_master`, masqués, dans `AUR_32_persos3d_rig`) : serre 16 × 6,7 m, 6 m de haut, porte à l'est ; fontaine Ø 7 m, 4,7 m de haut ; arche 8 m × 5,9 m (petites arches : même modèle à 4,5 m) ; banc 2 m ; fontaine murale 3 m de muret ; ifs, cyprès et tilleuls à la taille de chaque forme provisoire (≈ 130 copies).
- But : figer leur géométrie (planche, puis modèle Tripo posé dans la maquette), pour que le jardin ne change plus d'une vignette à l'autre ([../decisions/0007-garden-v3-formal-then-secret.md](../decisions/0007-garden-v3-formal-then-secret.md)).
- Planches candidates (GPT 2.6, 2K, deux variantes chacune ; référence de style : `production/refs/garden-day.png`) : `production/refs/candidates/garden-props/<objet>_gpt26_nb1|nb2.png` (greenhouse, tiered-fountain, rose-arch, bench, lion-wall-fountain ; garden-plants = if taillé, cyprès d'Italie, tilleul du bosquet) ; planche comparative `_cmp_garden-props.jpg`.
- Mesures demandées : serre 16 × 10 m, 6 m de haut, toit en berceau, porte vitrée au milieu d'un pignon ; fontaine : bassin rond ≈ 7 m, fût, une seule vasque haute ; arche ≈ 8 × 5 m, 1,4 m d'épaisseur ; banc ≈ 2 m ; fontaine murale sur ≈ 3 m de muret ; if ≈ 3,5 m ; cyprès et tilleul ≈ 12 m.
- La serre détruite (squelette de fer, scènes 12-13) sera faite à partir de la serre intacte retenue.

## Effets

### La pluie d'étoiles (scènes 5 à 11)
- Traits **d'argent** fins, à traînée douce, jamais rouges ni « boules de feu » ;
  d'abord rares, puis de plus en plus nombreux et proches, avec un sifflement aigu.
- À l'impact au sol (la serre, scène 8) : éclair blanc-argent, puis vraies
  flammes orange.

**EN (à coller)**
```text
silver shooting stars with soft luminous trails streaking across the night sky, growing in number, a high whistling sound; on impact a white-silver flash followed by orange flames
```

### Le dôme d'or (scène 11)
Forme décidée le 2026-11-15 (auteur) : **une bulle complète**, comme une boule
à neige.
- **Naissance** : au sommet de la tour, un petit dôme de lumière dorée
  translucide s'ouvre autour d'Elias, sur la galerie du beffroi.
- **Croissance** : il gonfle ; son bord lumineux balaie le palais, le jardin,
  les forêts, les villages, passe l'horizon et se referme de l'autre côté de
  la planète.
- **Vu de l'espace** : Aurelia est enfermée dans une bulle d'or, à peine plus
  grande qu'elle. La neige d'or de la scène 12 fait d'elle une boule à neige.
- **Vu du sol** (scène 12) : la bulle est presque invisible, un léger voile
  doré dans le ciel ; on la devine surtout aux impacts.
- Sa surface porte un motif discret de **pétales de rose** qui s'emboîtent.
  Les étoiles qui la frappent se brisent en gerbes d'étincelles dorées.
- Géométrie : la bulle « glisse » en grandissant pour devenir concentrique à
  la planète ; c'est voulu et invisible à l'écran.

**EN (à coller)**
```text
a translucent golden bubble of light born as a small dome around a boy at the top of a clock tower, swelling outward over the palace, the garden, the forests and the villages until it closes around the whole small planet, which seen from space sits inside a golden bubble barely larger than itself, like a snow globe; its surface faintly patterned with interlocking rose petals; silver shooting stars hitting it burst into showers of golden sparks
```

### La neige d'or (scènes 11, 12)
Les étincelles retombent lentement, comme une neige dorée, inoffensive, qui
se pose sur le jardin et fond sans bruit.

**EN (à coller)**
```text
slow golden sparkles drifting down like snow, harmless, settling softly on the garden and fading
```

### L'éclat d'or (scènes 11 à 13)
Le dernier fil de lumière du pétale entre dans les yeux d'Elias ; ensuite, de
fines paillettes d'or autour de ses pupilles. Discret : on doit le remarquer
en gros plan, pas de loin. Voir la variante « après la nuit » de
[../characters/elias.md](../characters/elias.md).

**EN (à coller)**
```text
a thin thread of golden light rising from a fading petal and flowing gently into a boy's green eyes; afterwards, fine gold flecks around his pupils, subtle, visible only in close-up
```

### La serre en feu (scènes 8, 9, 13)
La serre victorienne de l'image de concept : verre qui éclate, flammes orange
derrière les vitres (8) ; lueur orange lointaine vue de la terrasse (9) ;
squelette de fer et de verre brisé, fumée légère à l'aube (13).

## Liens
[star-shower.md](star-shower.md) · [palace-sets.md](palace-sets.md) · [royal-garden.md](royal-garden.md)
