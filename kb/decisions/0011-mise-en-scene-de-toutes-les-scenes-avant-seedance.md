# 0011 — Mettre en scène toutes les scènes avant de générer les plans dans Seedance

Statut : décidé (2026-11-22, auteur) · Origine : [auteur]

## Décision
SC02 est stable : mise en scène continue validée, images de début et de fin de chaque plan choisies, animatique de
vérification sonorisée avec les voix de référence (`production/animatic/mise-en-scene/SC02_verification.mp4`).
On **ne génère pas encore** ses plans dans Seedance. On passe d'abord aux scènes suivantes (SC03, SC04…), chacune avec
le même déroulé :
1. mise au point de la mise en scène continue dans Blender (positions, trajets, caméras ; vidéo de vérification) ;
2. mise au point des plans et génération des images de début et de fin (maquette Blender → GPT 2.6, prompt et références seuls) ;
3. animatique `production/animatic/mise-en-scene/SCxx_verification.mp4`, avec les dialogues dits par les voix de référence.
Les générations Seedance de toutes les scènes viennent ensuite.

## Pourquoi
En avançant dans les scènes suivantes, il faudra peut-être modifier des éléments de décor visibles dans SC02 (le palais,
la terrasse, le jardin…). Les plans Seedance coûtent cher (environ 3 400 crédits par plan) : mieux vaut ne les générer
qu'une fois le décor stabilisé sur l'ensemble du film. Les images de début et de fin coûtent peu à refaire, les vidéos beaucoup.

## Conséquences
- Toute modification de décor décidée pendant une scène ultérieure se répercute dans la maquette commune (`world.blend`) ;
  les images des scènes déjà traitées où ce décor se voit sont alors refaites (coût modéré), avant toute vidéo.
- Voir aussi [0010-mise-en-scene-continue.md](0010-mise-en-scene-continue.md) pour la méthode.
