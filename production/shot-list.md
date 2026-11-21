# Liste des plans

Statut : **en cours** (2026-11-14) — découpage technique (étape 8), scène par scène. Scène 1 découpée ; scènes 2 à 13 à découper. Total découpé : 14 s / objectif ≥ 300 s (film estimé à ≈ 8 min).

Caméras animées, durées et vidéos de référence : `production/blender/world.blend` (une scène Blender par plan, scène ANIMATIC pour l'enchaînement) et `production/animatic/`. Méthode : [animatic-workflow.md](animatic-workflow.md).

## Scène 1 — EXT. ESPACE - AURELIA - JOUR

| # | ID | Titre | Durée | Minutage | Personnages | Caméra | Vignettes | Statut |
|---|---|---|---:|---|---|---|---|---|
| 1 | [SC01-SH01](shots/SC01-SH01.md) | La planète | 4 s | 0:00–0:04 | — | Avancée plongeante depuis l'espace, 35 mm (descente continue avec SH02) | A | généré (v1, 720p + upscale, ancien palais) · vignette A refaite le 2026-11-18 (palais officiel) : vidéo à refaire |
| 2 | [SC01-SH02](shots/SC01-SH02.md) | La plongée | 5 s | 0:04–0:09 | — | Suite de la descente, traversée de nuages, 35 mm | (dernière image de SH01) | généré (v2, 720p, ancien palais) · vignette B refaite le 2026-11-18 (palais officiel) : vidéo à refaire |
| 3 | [SC01-SH03](shots/SC01-SH03.md) | Le survol | 5 s | 0:09–0:14 | (cour au loin) | Vol avant de 25 m à 10 m sur ≈ 180 m, rapide puis de plus en plus lent, 28 mm | A (+ B contrôle) | généré (v1, 720p + upscale, ancien palais) · vignettes A et B refaites le 2026-11-18 (palais officiel) : vidéo à refaire |

## Scène 2 — EXT. PALAIS D'AURELIA - TERRASSE - JOUR

Découpage : option B (6 plans) ← choix de l'auteur, 2026-11-15 ; **mise en scène continue validée le 2026-11-20** (kb/decisions/0010) : toute la scène est jouée en temps réel dans la scène Blender `SC02_MISE_EN_SCENE` (`production/blender/build_mise_en_scene_sc02.py`) ; chaque plan est une fenêtre de temps filmée par sa caméra `MES_CAM_SHxx`. Chrono et détails : [mise-en-scene/SC02.md](mise-en-scene/SC02.md) ; vidéo de vérification `production/animatic/mise-en-scene/SC02_verification.mp4`. Ajout du plan SH06a. Durées = fenêtres avant montage (SH05 et SH06a seront raccourcis au montage).

| # | ID | Titre | Durée | Minutage | Personnages | Caméra | Vignettes | Statut |
|---|---|---|---:|---|---|---|---|---|
| 4 | [SC02-SH01](shots/SC02-SH01.md) | La terrasse | 6,8 s | 0:14–0:21 | Reine, 2 conseillers, Chambellan, 2 valets, Elias | Plan de situation : part haut du coin sud-est, descend vers la Reine, 30 mm ; Elias entre par la gauche | candidates début/fin (`candidates/_mes_SC02/`) | mise en scène validée |
| 5 | [SC02-SH02](shots/SC02-SH02.md) | Elle sonne | 5,4 s | 0:21–0:26 | Reine, Elias, conseillers, Chambellan | Travelling latéral vers l'est à 1,2 m, 35 mm | candidates début/fin (`candidates/_mes_SC02/`) | mise en scène validée |
| 6 | [SC02-SH03](shots/SC02-SH03.md) | Les rires | 2,8 s | 0:26–0:29 | Chambellan, 2 conseillers | Lente poussée à 1,5 m, 45 mm | candidates début/fin (`candidates/_mes_SC02/`) | mise en scène validée |
| 7 | [SC02-SH04](shots/SC02-SH04.md) | Elias | 1,8 s | 0:29–0:31 | Elias (Reine en amorce) | Gros plan par-dessus l'épaule de la Reine, 75 mm | candidates début/fin (`candidates/_mes_SC02/`) | mise en scène validée |
| 8 | [SC02-SH05](shots/SC02-SH05.md) | Je ne m'en souviens pas | 12,0 s | 0:31–0:43 | Reine, Elias (amorce), Chambellan (hors champ) | Par-dessus l'épaule droite d'Elias, 40 mm | candidates début/fin (`candidates/_mes_SC02/`) | mise en scène validée · à raccourcir au montage |
| 9 | [SC02-SH06a](shots/SC02-SH06a.md) | Elle repart | 12,8 s | 0:43–0:56 | Elias, Reine, conseillers, Chambellan | Dans l'allée des velums vers le palais, recule quand Elias approche, 35 mm | candidates début/fin (`candidates/_mes_SC02/`) | mise en scène validée · fiche rédigée · à raccourcir au montage |
| 10 | [SC02-SH06](shots/SC02-SH06.md) | Seul | 7 s | 0:56–1:03 | Elias | Départ bas et serré derrière Elias, grue et zoom arrière vers le jardin | A | **retenu** (image + son) |

Les fiches importées de ChatGPT (SC01-SH01 à SH05, octobre 2026) sont archivées dans `shots/_obsolete/`.
