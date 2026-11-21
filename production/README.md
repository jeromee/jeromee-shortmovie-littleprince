# Production — livraison CapCut

Tout ce qui se trouve ici est destiné à être collé ou importé dans CapCut Video
Studio (Director Mode / Seedance) ou dans Freepik / Magnific (images : Nano
Banana, GPT-Image, Seedream…).

Chaîne : images (concepts, fiches, first / last frames) dans Freepik / Magnific
→ import dans CapCut Director Mode → génération vidéo de chaque plan, avec voix
et bruitages intégrés → musique libre de droits et montage dans CapCut
« classique ».

- `shot-list.md` — tableau maître : ordre, identifiant, durée, personnages, statut.
- `shots/SCxx-SHyy.md` — une fiche par plan : intention, action, dialogues,
  caméra, prompt, et images de référence à joindre.
- `animatic-workflow.md` — storyboard et animatique dans Blender : modes de
  plan, organisation, ce qui fait foi où, références caméra pour CapCut.

## Règles
- **Langue** : chaque bloc à coller existe en **FR (référence)**, qui fait foi,
  et en **EN (à coller)**, traduction fidèle. On modifie d'abord le FR, puis on
  reporte en EN. Seul le bloc EN est collé dans CapCut ou le modèle d'image.
- Le champ de prompt vidéo de CapCut accepte les horodatages : chaque prompt
  vidéo s'écrit en timeline (`[0s] … [3s] … [6s] …`) terminée par une ligne
  `Style:`. Pas de version en paragraphe unique.
- Les prompts reprennent mot pour mot les **verrous visuels EN** de
  `kb/characters/*` et `kb/world/*` — modifier le verrou là-bas, puis rafraîchir
  les prompts.
- Un plan = une génération Seedance. Les répliques doivent tenir dans la durée
  (~2,5 mots/s).
- **Exigence visuelle maximale** : cadrage, lumière et raccords soignés plan
  par plan ; c'est le critère non négociable du projet.
- Statut par plan : `provisoire` → `décidé` → `généré` → `approuvé`.
- Les prompts importés sont conservés mot pour mot, en anglais, sous
  « Prompt importé (v0) » pour référence ; c'est la section « Prompt actuel »
  ou les blocs CapCut qu'il faut utiliser.

- **Vidéo (Seedance) : pas d'animatique en @Video1 quand des personnages y bougent** (2026-11-20, essai 1 de SC02-SH06). Les personnages de la maquette sont des modèles rigides déplacés sans cycle de marche : Seedance recopie ce glissement, même quand le prompt dit de ne reprendre que la caméra, et la référence muette a donné une piste son quasi silencieuse. Caméra fixe : `keyframes.start` = vignette + `cameraMotion` « static ». Caméra mobile : décrire le mouvement dans le prompt (ou `cameraMotion`), et ne joindre l'animatique qu'en version sans personnages.

- **Voix des dialogues : Seedance puis changeur de voix** (2026-11-20, choix de l'auteur). Seedance génère le plan avec les répliques entre guillemets dans le prompt, pour que les lèvres soient synchronisées ; chaque réplique est ensuite passée au changeur de voix de Magnific (`audio_voice_change`) avec **une voix de référence fixe par personnage**, pour que chacun garde la même voix d'un plan à l'autre. Piste `*_dialogues_*.wav` séparée, dans `production/audio/<plan>/`. Voix de référence à établir (Elias, la Reine, le Chambellan, les conseillers) et à noter dans les fiches de personnages.

- **Son : trois familles de pistes séparées** (2026-11-20) — dialogues, bruitages et ambiances, musique — gardées à part jusqu'au mixage final dans CapCut. Une piste par plan et par famille dans `production/audio/<plan>/` (WAV 48 kHz) : `*_dialogues_*.wav`, `*_bruitage_*.wav`, `*_musique_*.wav`. Le son natif de Seedance (très faible via Magnific) sert de repère de timing ; les bruitages viennent de Mirelo SFX 2.0 (`video_soundfx`), qui ne fait pas de voix ; les dialogues viennent de Seedance (répliques entre guillemets), du doublage Magnific ou des voix CapCut ; la musique d'un service dédié.

## Vignettes de storyboard

**Échelle de la maquette** (2026-11-20) : environnement réduit ×0,8, personnages et objets à taille humaine à taille réelle (`production/blender/echelle_monde.py`, à relancer après tout script qui crée des objets ; kb/decisions/0009).

**Vignettes retenues : prompt + références seulement** (2026-11-20, auteur). Une vignette qui part dans CapCut doit sortir d'une génération directe, avec son prompt et ses références, pas d'une retouche d'une autre image : on préfère dépenser quelques crédits de plus et savoir que le prompt seul donne le bon résultat. Une retouche peut servir à explorer, mais le prompt doit ensuite être corrigé et la vignette régénérée.

**Gros plans de personnages** (2026-11-19) : ne pas demander de « garder le personnage de la maquette et seulement l'affiner » — l'IA recopie alors le visage simplifié du modèle 3D. Dire que la maquette ne donne que le cadrage, la place, la taille et la pose ; faire redessiner le visage d'après la planche, traits décrits ; joindre une bonne vignette antérieure comme cible de finition ; décrire l'ombrage (peau, yeux, cheveux) et l'expression ; décrire le décor et ce qui n'y est pas.
Les vignettes sont générées (Freepik / Magnific) puis montées en animatique
dans Blender ; chaque plan en sort aussi en MP4, utilisé dans CapCut comme
vidéo de référence pour le mouvement de caméra.

- **Emplacement** : `production/storyboard/`. À côté de chaque vignette, le rendu de maquette qui sert de référence de cadrage : `SCxx-SHyy_A_graybox.png` (scène Blender du plan, image de départ ou d'arrivée). Images de référence tirées d'`Import/` : `production/refs/`. Les essais non retenus vont dans `production/storyboard/candidates/SCxx-SHyy/`, un sous-dossier par plan.
- **Une vignette par composition qui compte**, pas forcément une par plan.
- **Nommage** : `SCxx-SHyy_A.png`, `SCxx-SHyy_B.png`… La première vignette
  d'un plan est **toujours la frame de départ** (= first frame Seedance) ; la
  dernière est **toujours la frame d'arrivée** (= last frame, si on l'impose).
- Selon le type de plan :

| Type de plan | Vignettes |
|---|---|
| Fixe, action simple | A = départ ; + B = moment fort s'il arrive plus tard |
| Fixe, action qui transforme l'image | A = départ, B = arrivée (+ moment clé éventuel) |
| Pan / tilt | une image élargie contenant les deux cadrages ; Blender en tire départ et arrivée |
| Zoom / travelling avant | A = départ large, B = arrivée serrée (générée à part, pour la netteté) |

- **Références d'images dans les prompts Magnific (Nano Banana)** — (2026-11-16, remarque de l'auteur) : toujours les désigner par la convention de Magnific, `@img1`, `@img2`… (dans l'ordre des références jointes), et non par « Image 1 » en toutes lettres. Pour Seedance, garder `@Image1` / `@Video1`, validés par les essais.
- **Cohérence maquette ↔ prompt** : ne décrire dans le prompt que les mannequins réellement visibles dans le rendu joint (vérifier la première image avant d'écrire le prompt).
- **Personnages 3D dans les rendus de référence** — (2026-11-16, test) : un personnage déjà présent en 3D dans le rendu Blender joint (`@img1`) est redessiné par Nano Banana à sa taille et à sa place ; un mannequin de couleur ne l'est pas de façon fiable. Dire dans le prompt quels personnages sont déjà en 3D (« garder exactement leur taille et leur place ») et quels blocs sont des emplacements. Ne jamais donner de taille relative en mots (« une tête de plus ») qui contredise la perspective du rendu.
- **Références d'objets récurrents** — (2026-11-17, idée de l'auteur) : Nano Banana 2.1 garde jusqu'à 10 objets en plus de 4 personnages, et Magnific accepte 12 références par génération. Joindre la planche d'un objet récurrent (oranger en pot, pendentif, télescope…) dès qu'il est visible, et le désigner dans le prompt par son `@imgN`.
