# 0006 — Préparer tous les plans avant de générer la moindre vidéo

Statut : décidé · Date : 2026-11-15 · Origine : [auteur], ordre détaillé proposé par [claude]

## Constat
La scène 1 a été générée dans Seedance avant que les références soient fixées. Sur ≈ 13 000 crédits, 5 200 sont partis en deux essais de SC01-SH02, et le vrai défaut (le palais de la vignette SC01-SH01_A, sans rapport avec le palais vu de près) venait d'une image fixe qu'on aurait corrigée pour 65 crédits. Comme au cinéma, le « tournage » (une génération vidéo, ≈ 2 000 à 2 600 crédits, plus ≈ 1 900 d'upscale) coûte cher : on prépare tout avant.

## Choix
Pas de génération Seedance de production avant que tout le film soit préparé, dans cet ordre :

| # | Étape | Livrable | Emplacement |
|---|---|---|---|
| 1 | Images de référence (« bible visuelle ») | palais en vue aérienne, jardin et massif (jour, nuit, aube), intérieurs (cabinet, chambre, tour), accessoires (clé et serrure, pétale, dôme), fiches de personnages | `production/refs/`, `kb/characters/sheets/` |
| 2 | Découpage des scènes 2 à 13 | fiches de plan, validées scène par scène | `production/shots/`, `production/shot-list.md` |
| 3 | Caméras Blender | seulement pour les plans dont la caméra se déplace dans l'espace ; plans fixes et gros plans : vignette + mots | `production/blender/world.blend` |
| 4 | Vignettes | départ (A), et arrivée (B) quand l'image change vraiment ; essais dans `candidates/SCxx-SHyy/` | `production/storyboard/` |
| 5 | Animatique du film entier | vignettes + mouvements Blender au bon minutage ; vérifier la durée (≥ 5 min) et le rythme | `production/animatic/` |
| 6 | Génération Seedance + upscale | plan par plan | `production/generated/` |

## Exceptions
- **Trois essais Seedance, tout de suite**, sur ce qu'on n'a jamais testé et qui conditionne la forme des fiches : (1) dialogue en français avec synchronisation des lèvres, Elias et la Rose en plan à deux ; (2) l'éveil de la Rose en gros plan (visage qui apparaît) et sa voix ; (3) un plan à effets, le dôme d'or (scène 11). Voir `production/tests/seedance-essais/`.
- Les plans déjà générés de la scène 1 restent comme repères ; SC01-SH03 pourra sans doute être gardé, SC01-SH01 et SH02 seront refaits avec la vue aérienne du palais.

## Règles apprises (2026-11-14)
- Une image de référence peut imposer son cadrage : à Nano Banana comme à Seedance. On ne joint une référence d'architecture qu'avec une consigne explicite (« reproduire l'architecture, pas le point de vue »), et pas à Seedance quand une vidéo de référence caméra doit faire foi.
- Toute vignette où un lieu ou un personnage apparaît reçoit sa référence officielle.
