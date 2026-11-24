# La Rose

Statut : décidé (couleur 2026-10-04 ; rôle et secret 2026-11-01 ; visage 2026-11-02) · Sources : [import] §2, [image] `Import/Rose - Character Sheet.png`

## Rôle
Alliée et catalyseur. Elle en sait plus sur Aurelia qu'elle ne le laisse
d'abord paraître. Elle « attend Elias depuis très longtemps ». [import]

## Désir, secret, prix — décidé (2026-11-01, auteur)
- **Désir** : protéger Aurelia, comme elle l'a toujours fait.
- **Secret** : à chaque grande pluie d'étoiles, la Rose protège la planète
  avec sa lumière. **Seuls les enfants l'entendent.** La reine Elara
  l'entendait, enfant, puis a cessé en devenant reine. Les armoiries à la rose
  couronnée (broche d'Elias, rosettes de la robe de la Reine) en gardent la trace.
- **Pourquoi elle attendait Elias** : cette fois, sa lumière ne suffira pas
  seule ; il lui faut l'aide d'un enfant (action précise à fixer au séquencier).
- **Sa maxime** (décidé 2026-11-02, auteur) : « Petite reine, la vraie noblesse, c'est de savoir admirer une rose. »
  Elle l'a confiée à Elara enfant, qu'elle appelait « petite reine » — comme
  elle appelle Elias « petit prince ». C'est le sens oublié des armoiries à la
  rose couronnée.
- **Prix** : elle donne toute sa lumière et redevient une rose ordinaire, muette.
- **Ce qui reste d'elle** : sa lumière vit désormais dans le regard d'Elias,
  sous la forme d'un éclat d'or (voir [elias.md](elias.md)). Elle continue
  d'exister en lui — comme le petit prince dans la couleur des blés pour le renard.

## Trois dimensions
| Dimension | Contenu |
|---|---|
| Physique | Une rose unique, enracinée au centre du grand massif, au cœur du jardin, au bord d'un petit rond de mousse auquel mène un passage de pas japonais (2026-11-22, `kb/decisions/0012`) ; ≈ 1,15 m, plus haute que les autres roses (0,7–0,9 m) ; elle bouge sans qu'il y ait de vent ; son cœur s'illumine quand elle parle. |
| Social | Origine inconnue ; lien avec Aurelia et la famille royale non défini (les armoiries de la broche d'Elias sont une rose couronnée — piste possible). |
| Psychologique | Sage, mystérieuse, joueuse, un brin taquine. Douce et ancienne, jamais effrayante. |

## Voix
Douce, chaude, presque chuchotée, avec une légère résonance magique ; « voix
féminine ancienne ». Jamais caricaturale.
**Réglage (2026-11-15, auteur, après l'essai Seedance E2)** : la voix obtenue est un peu grave, plus celle d'une dame que d'une jeune fille ; la viser **plus claire et plus jeune**, tout en gardant sa sagesse. Formulation EN pour les prompts : `a soft, clear, youthful female voice, light and warm, with a gentle wise tone`. Voir [../styles/dialogue-voice.md](../styles/dialogue-voice.md).

## Couleur — décidée (2026-10-04, auteur)
La Rose est **jaune** (pétales jaune pâle veloutés, cœur doré), comme sur
l'image de concept. Le « cramoisi » de l'import ChatGPT est abandonné.

Expressions de la planche : douce/sage, joueuse/taquine (clin d'œil),
mystérieuse/grave, parlant (lueur), émerveillée, souriante.

## Visage — décidé (2026-11-02, auteur)
- **Au repos**, c'est une rose ordinaire, sans visage : rien ne la distingue
  dans le grand massif.
- Son visage (celui de la planche) **apparaît seulement quand elle s'éveille**
  pour s'adresser à un enfant, et s'efface quand elle se tait.
- À la fin, son visage s'efface pour toujours : elle redevient une rose comme
  les autres.
- **Prompts** : préciser à chaque plan « rose sans visage » ou « visage éveillé ».

## Verrou visuel (pour les prompts)

**FR (référence)**
> Une rose unique, grande, aux pétales jaune pâle veloutés, au cœur doré
> doucement lumineux qui brille d'une lueur de clair de lune quand elle parle,
> avec un visage stylisé et doux au centre (yeux chaleureux, petite bouche),
> des feuilles vert émeraude, une tige fine vert foncé avec des épines,
> enracinée dans une terre de jardin parsemée de petits cailloux.

**EN (à coller)**
```text
A single large rose with light-yellow, velvety petals, a softly luminous golden centre that glows with a moonlight-like light when she speaks, a gentle stylized face within the centre (warm eyes, small mouth), emerald-green leaves, a slender dark-green stem with thorns, rooted in garden soil with small stones.
```

## Liens
[elias.md](elias.md) · [../world/royal-garden.md](../world/royal-garden.md)

## Voix de référence (2026-11-22, auteur)
Clone ElevenLabs « La Rose — Le Prince et la Rose » (Magnific, My Voices) : **voiceId 215424, source `mine`**. Voix française jeune, claire, douce et tendre, jamais condescendante (l'auteur a écarté les voix qui « font entendre un sentiment de supériorité sur le prince »), créée avec Seed Audio 1.0 puis clonée. Usage : changeur de voix sur chaque réplique générée par Seedance. Détail : `production/audio/voix-reference/README.md`.

## Dimensions (décidé le 2026-11-23, auteur)
- **Fleur : 13 cm de diamètre.** Tige fine d'environ 1 m : le cœur de la fleur est à ≈ 1,23 m du sol du jardin, un peu au-dessus
  des rosiers du massif (0,80 m), à hauteur du visage d'Elias à genoux. De loin, elle se distingue à peine des autres roses :
  c'est voulu, elle « entre en scène » quand Elias s'approche.
- **Visage** : au cœur de la fleur, entre un tiers et 40 % du diamètre (≈ 4,5 à 5 cm), **toujours le même rapport**. Le dessin du visage de la planche est gardé.
- **Épines** : petites et discrètes, brun-vert, pas rouges.
- Blender : `production/blender/rose_13cm.py` (déforme le modèle Tripo : fleur réduite, feuillage resserré, tige allongée ;
  épines désaturées dans la texture). Copie d'avant : `world_avant-rose-13cm.blend`.
- Planches à 13 cm proposées le 2026-11-23, **à choisir par l'auteur** (`production/refs/candidates/rose-13cm/`) :
  `rose-asleep-sheet_13cm_A|B_gpt26.png` (quatre vues, mesures, Elias à genoux pour l'échelle) et
  `rose-face-sheet_13cm_A|B_gpt26.png` (la plante entière et six expressions). Dans ces planches, le visage fait plutôt **40 %** du
  diamètre de la fleur (GPT ne descend pas en dessous), mais le rapport est le même dans tous les panneaux ; c'est cette constance
  qui compte. Les anciennes planches (`production/refs/rose-asleep-sheet.png`, planche du visage) ont la fleur trop large et des
  épines rouges : ne plus les utiliser comme référence de taille.

### Mise à jour du 2026-11-23, soir (auteur)
- **Planche du visage retenue : `production/refs/candidates/rose-13cm/rose-face-sheet_13cm_B_gpt26.png`** (Magnific `4RHC4EK9Aa`).
- 13 cm s'est révélé trop petit à l'image : **test en cours à 20 cm** (`rose_13cm.appliquer_v2(diam=0.20)`), visage ≈ 40 % du
  diamètre, centre de la fleur toujours à ≈ 1,23 m. Des **feuilles aussi sur le tiers du milieu de la tige** (demande de l'auteur) :
  les groupes de feuilles sont répartis le long de la tige allongée et réduits sans être déformés.
- Rendu d'essai : `production/storyboard/candidates/_mes_SC03/gpt_v3/` (fin de SH06). La taille définitive (13, 20 cm ou autre)
  reste à décider ; le titre « Dimensions » ci-dessus décrit l'état à 13 cm.

### Décision du 2026-11-23, soir (auteur) : **fleur de 20 cm**
- Le rendu `production/storyboard/candidates/_mes_SC03/gpt_v3/SH06_last_rose20_a.png` est jugé « parfait (dimensions, expressions) » :
  **la fleur fait 20 cm de diamètre**, le visage ≈ 40 % du diamètre (planche du visage B), centre de la fleur à ≈ 1,23 m, à environ
  40 cm du visage d'Elias à genoux. Cela remplace les 13 cm de la section « Dimensions » ci-dessus (épines et tige inchangées).
- Blender : `rose_13cm.appliquer_v2(diam=0.20)` ; les feuilles (limbe et pétiole ensemble) sont réparties le long de la tige et
  restent attachées (correction des trous signalés par l'auteur le même soir). Vues : `production/refs/candidates/rose-13cm/rose20_blender_*.png`.
- Planche de la Rose endormie à 20 cm, **à choisir** : `rose-asleep-sheet_20cm_A|B_gpt26.png` (même dossier).

### Planches retenues (2026-11-23, soir, auteur)
- Rose endormie à 20 cm : **`production/refs/rose-asleep-sheet.png`** (= `candidates/rose-13cm/rose-asleep-sheet_20cm_B_gpt26.png`, Magnific `LwIBSBVswO`) ;
  l'ancienne (fleur de 52 cm, épines rouges) : `candidates/rose-13cm/rose-asleep-sheet_ancienne-52cm.png`.
- Visage : **`production/refs/rose-face-sheet.png`** (= `rose-face-sheet_13cm_B_gpt26.png`, Magnific `4RHC4EK9Aa`) ; dessinée pour
  13 cm, mais le rendu à 20 cm qui s'en sert est validé (`SH06_last_rose20_a`).
- Tige du modèle Blender réparée (le 2026-11-23 au soir) : la ligne médiane de la tige, qui se courbe vers le haut, est suivie ;
  la fleur est posée sur le haut de la tige.
