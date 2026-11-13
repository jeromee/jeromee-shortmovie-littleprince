# Storyboard et animatique dans Blender

Statut : décidé (2026-11-12) · Origine : [auteur] + [claude]

Méthode de travail pour passer des fiches de plan (`shots/SCxx-SHyy.md`) aux
vignettes, à l'animatique et aux références caméra envoyées à CapCut.
Le nommage des vignettes est défini dans `README.md` (section « Vignettes de
storyboard »).

## Principe
1. L'auteur choisit le cadrage de chaque plan et génère les vignettes
   (Freepik / Magnific : Nano Banana, GPT-Image, Seedream) à partir des fiches
   de personnages et de décors.
2. Blender anime la caméra sur ces vignettes et rend l'animatique.
3. Chaque plan est aussi rendu en MP4 : CapCut s'en sert comme **vidéo de
   référence pour le mouvement de caméra** (Seedance), avec la vignette A en
   first frame.
4. Claude pilote le Blender 5.3 de l'auteur (RTX 3090 Ti, OptiX) par le
   connecteur « MCP for Blender » (paquet `mcp-for-blender`, installé le
   2026-11-13 ; télémétrie désactivée), et par des scripts générateurs
   versionnés dans le dépôt. Fichier de travail prévu :
   `production/blender/world.blend`.

## Deux modes de plan
| | Mode A — vignette sur plan (2,5D) | Mode B — blocking en boîtes grises (3D) |
|---|---|---|
| Quand | plans fixes, pan, tilt, zoom / travelling avant, petit travelling latéral | caméra qui tourne autour d'un personnage, déplacements dans l'espace, placement précis de plusieurs personnages |
| Contenu de la scène Blender | caméra + plan(s) texturé(s) avec les vignettes, débordant du cadre sur tout le trajet | caméra + décor en volumes gris + un mannequin simple par personnage |
| Ordre de travail | vignettes → Blender | Blender → rendu de la 1re image → Nano Banana la redessine dans le style du film = vignette A |
| Parallaxe | aucune, sauf personnage détouré sur un second plan (facultatif) | naturelle |

**Mannequins (mode B).** Boîte pour le corps, sphère pour la tête, une couleur
par personnage, nommée dans le prompt : Elias = bleu, la Reine = rouge, le
Chambellan = vert ; décor gris. Jamais de jaune ni d'or (réservés à la Rose).
L'action des personnages (s'asseoir, se lever…) est écrite dans le prompt ; la
référence vidéo porte d'abord la caméra. Si la caméra doit accompagner une
action, deux poses suffisent (ex. bloc debout → bloc assis). Mannequin
articulé seulement si nécessaire (Mixamo, gratuit, import FBX).

## Organisation du fichier Blender
- Un seul fichier `.blend` pour le film.
- **Une scène Blender par plan** (nommée `SCxx-SHyy`), pas par vignette. Les
  vignettes A, B… sont des objets dans la scène du plan.
- Une **scène maîtresse** `ANIMATIC` : le monteur vidéo (VSE) enchaîne les
  scènes des plans, avec voix témoins et musique provisoire.
- Fonctions natives de Blender (5.0 et plus, l'auteur utilise 5.3) ; aucun
  add-on de storyboard. `ANIMATIC` est la **Sequencer Scene** du VSE,
  indépendante de la scène active ; avec **Sync Scene Time**, la scène active
  (et donc le viewport 3D) suit le clip de scène sous la tête de lecture.
  Point de départ possible : le modèle « Storyboarding » de Blender.
- 24 images/s.

## Ce qui est défini où
| Donnée | Où elle fait foi |
|---|---|
| Durée d'un plan | `shot-list.md` jusqu'au début de l'animatique ; ensuite **Blender** (plage d'images de la scène), recopiée par Claude dans `shot-list.md` |
| Mouvement de caméra — intention, en mots | fiche de plan, champ Caméra (sert aussi au prompt) |
| Mouvement de caméra — exécution exacte | images clés de la caméra Blender (position, rotation, focale) |
| Annotations, flèches, croquis | Grease Pencil |

Les mots de la fiche et la caméra Blender doivent rester d'accord : en cas de
désaccord, Seedance suit la vidéo de référence, pas le texte.

## Sorties
- `animatic/SCxx-SHyy.mp4` — un MP4 par plan, référence caméra pour CapCut.
- `animatic/animatic.mp4` — l'animatique complète (rendu de la scène `ANIMATIC`).
- Planche de storyboard PDF « pour information » : par plan, vignettes,
  identifiant, durée, action, dialogue, caméra ; sur les pans, cadres de
  départ et d'arrivée dessinés sur l'image élargie.

## Dans CapCut
- Modèle : **Seedance 2.5**. Durée de génération : nombre entier de secondes,
  de 4 à 30 s ; jusqu'à 30 images, 10 vidéos et 10 audios de référence.
- Dans le modèle, « first frame » et « références » sont deux modes distincts
  et exclusifs. Pour combiner vignette A et référence caméra, on passe en mode
  référence et on écrit « @Image1 as the first frame » (voir test ci-dessous).
- La vidéo de référence a **la même durée** que la génération demandée. Le
  clip est coupé au montage final.
- Le prompt commence par demander de ne reprendre que le mouvement de caméra
  de la référence, puis décrit la scène.
- Le son est précisé dans le prompt (ambiance, dialogues) ; sinon CapCut peut
  ajouter une musique. La musique du film est posée au montage final.

## Points à vérifier
- [x] First frame imposé + vidéo de référence dans une même génération :
  **validé** avec Seedance 2.5 (2026-11-13). Trajectoire suivie à environ 1 %
  près, même rythme ; image 0 régénérée mais fidèle. Détails :
  `tests/capcut-first-frame-plus-ref/README.md`.
- [x] Mode B : **validé pour le mouvement** (2026-11-13) — orbite suivie en
  sens, amplitude et rythme ; Elias stable. La caméra de la référence impose
  aussi le cadrage de l'image 0 : la vignette A doit coller au cadrage de la
  maquette. Détails : `tests/capcut-mode-b-graybox/README.md`.
- [x] Netteté : **générer en 720p puis upscaler avec Magnific Precision**
  (plus net que le 1080p natif, pour un coût comparable). Le 1080p natif, la
  référence plus nette et « sharp focus » n'apportent presque rien
  (2026-11-13, `tests/capcut-mode-b-graybox/README.md`).
- [ ] Décors dévoilés par une orbite (mode B) : Seedance invente des éléments
  (arche dédoublée, puis galerie d'arches). Ni la description dans le prompt
  ni la couleur dans la maquette ne règlent le problème. Pistes : une
  vignette où chaque repère a exactement la taille et la profondeur de la
  maquette ; une vignette de fin (dernière image) ; ou limiter les orbites
  aux décors simples.
  Essais B6 à B8 (2026-11-13) : aucune combinaison ne donne à la fois trajet,
  cadrage et décor justes (tableau dans `tests/capcut-mode-b-graybox/README.md`).
- [x] Musique : l'option « no music » de Seedance 2.5 dans Magnific la
  supprime.
- [ ] Coût : 330 crédits pour 5 s en 720p avec référence vidéo. Comparer avec
  le même plan sans vidéo de référence (first frame + mouvement en mots).
- [ ] Empêcher la musique ajoutée automatiquement : « no music » dans le
  prompt ne suffit pas (tests A et B). Chercher un réglage audio dans CapCut,
  sinon couper ou isoler les voix au montage.
- [x] Filigrane « CapCut AI » : se retire avec le plan Pro (CapCut le propose).
- [x] Storypencil : abandonné. L'add-on ne fonctionne plus depuis Blender 5.0
  et ses fonctions sont devenues natives (voir « Organisation du fichier
  Blender ») ; la structure est construite par script (2026-11-12).
