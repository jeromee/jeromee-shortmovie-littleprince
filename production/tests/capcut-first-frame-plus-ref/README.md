# Test CapCut — first frame + vidéo de référence caméra

Statut : fait (2026-11-13) · Origine : [claude]

Question : CapCut (Seedance 2.5) accepte-t-il, dans une même génération, une
image de départ imposée **et** une vidéo de référence pour le mouvement de
caméra ? Le mode A de `../../animatic-workflow.md` en dépend.

## Fichiers
- `SC00-TEST_A_first-frame.png` — image de départ (1920×1080), tirée de
  `Import/Garden with Rose 01.png`, cadrée sur le château.
- `SC00-TEST_camera-ref.mp4` — vidéo de référence, 5 s, 24 i/s, 1280×720 :
  pan vers la droite + descente + avancée jusqu'à la Rose jaune.
- `SC00-TEST_B_last-frame.png` — image d'arrivée de la référence (pour comparer).
- `make_test.py` — script qui génère ces fichiers.

## Réglages
Seedance 2.5 · 16:9 · **5 s** (même durée que la référence). Mode « Omni reference » si l'interface ne permet pas de combiner une case first frame et une vidéo de référence.

## Prompt
**FR (référence)**
> @Image1 comme première image. Reprendre uniquement le mouvement de caméra de
> @Video1 : même trajectoire, même vitesse, même rythme. Un jardin de roses
> royal ensoleillé, animation 3D façon Pixar ; la caméra part du château doré,
> glisse vers la droite et descend vers une rose jaune endormie au centre d'un
> massif rond. Personne dans le jardin. Brise légère, quelques pétales qui
> volent. La rose reste endormie.

**EN (à coller)**
> @Image1 as the first frame. Take only the camera movement from @Video1: the
> same path, speed and timing. A sunlit royal rose garden, Pixar-style 3D
> animation; the camera starts on the golden castle, glides to the right and
> descends toward a sleeping yellow rose in the center of a round flower bed.
> No people in the garden. Gentle breeze, a few drifting petals. The rose stays
> asleep.

## Résultat — `result-01.mp4.mp4` (2026-11-13)
Seedance 2.5, 720p, 5 s, prompt EN ci-dessus. Coût : 330 crédits.

- **Interface** : génération acceptée avec l'image A et la vidéo de référence
  ensemble (préciser le mode utilisé : … ).
- **Image 0** : même composition que A, mais régénérée et non copiée au pixel
  près (un peu plus douce, cadre décalé d'environ 1 %, 1,5 % plus large).
  Suffisant pour un premier plan ; à surveiller pour un raccord image à image.
- **Mouvement** : trajectoire mesurée par recalage SIFT de chaque image sur
  l'image source. Le résultat suit la référence à environ 1 % près sur tout le
  plan (décalage constant d'environ +12 px en x et +18 px en y sur l'image de
  2560 px), avec le même rythme (accélération et décélération) ; l'arrivée
  correspond à B.
- **Contenu** : pétales qui volent (demandés), Rose qui reste endormie, visage
  conservé ; légère perte de détail (720p).
- **À corriger** : CapCut a ajouté une **musique** (non demandée) et un
  filigrane **« CapCut AI »** en haut à gauche (il se retire avec le plan Pro).
- **Conclusion pour le mode A** : validé. Limite : la référence venait de la
  même image ; le transfert d'un mouvement sur un contenu différent (mode B,
  boîtes grises) reste à tester.

Fichiers d'analyse : `_sheet.jpg` (en haut la référence, en bas le résultat, à
0, 1,25, 2,5, 3,75 et 5 s), `_frame0.jpg` (détail de A à gauche, image 0 du
résultat à droite), `_lastframe.jpg` (fin de la référence à gauche, fin du
résultat à droite).
