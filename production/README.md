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

## Vignettes de storyboard
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
