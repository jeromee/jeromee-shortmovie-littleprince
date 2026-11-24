# Liste des plans

Statut : **en cours** (2026-11-14) — découpage technique (étape 8), scène par scène. Scènes 1 et 2 découpées ; scène 3 proposée (2026-11-22) ; scènes 4 à 13 à découper. Total découpé : 14 s / objectif ≥ 300 s (film estimé à ≈ 8 min).

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

## Scène 3 — EXT. JARDIN ROYAL - GRAND MASSIF - JOUR

Mise en scène continue, **v5 du 2026-11-23 (nuit), à valider par l'auteur** : scène Blender `SC03_MISE_EN_SCENE` (`production/blender/build_mise_en_scene_sc03.py`), caméras `MES3_CAM_SHxx` ; décor de la clairière : `clairiere_v2.py` (kb/decisions/0012). Chrono, décisions et points ouverts : [mise-en-scene/SC03.md](mise-en-scene/SC03.md) ; vidéo `production/animatic/mise-en-scene/SC03_verification.mp4`. v3 : Elias arrive en courant, plan à deux en orbite (SH06), champ / contrechamp aux tiers opposés. v4 : il s'assied à l'entrée du passage, Rose de 20 cm, nouveau SH11 (« Je sais… ») et « Ce n'est pas un spectacle… » sur la Rose (SH12) ; v5 : la Rose ne tourne plus, SH09 en plan à deux ; 89,5 s. Durées = fenêtres avant montage ; fiches de plan à rédiger après validation.

| # | ID | Titre | Durée | Minutage | Personnages | Caméra | Vignettes | Statut |
|---|---|---|---:|---|---|---|---|---|
| 11 | SC03-SH01 | Situation | 4,5 s | 1:03–1:08 | 2 jardiniers, Elias (au loin, qui court), la Rose | plongée de 22 m au-dessus de l'exèdre, 24 mm, légère descente | — | mise en scène proposée (v5) |
| 12 | SC03-SH02 | Les jardiniers | 5,5 s | 1:08–1:13 | 2 jardiniers, Elias (au fond, par l'arche, en courant) | grue rapide : part haut en plongée (11 m, 28 mm) et descend à hauteur des personnages (2 m, 26 mm) | — | mise en scène proposée (v5) |
| 13 | SC03-SH03 | Elias arrive | 5,8 s | 1:13–1:19 | Elias | 35 mm, au sud-ouest, panoramique qui le suit | — | mise en scène proposée (v5) |
| 14 | SC03-SH04 | Il boude | 5,5 s | 1:19–1:24 | Elias (la Rose hors champ) | 50 mm, trois quarts face depuis le sud-sud-ouest, lente poussée | — | mise en scène proposée (v5) |
| 15 | SC03-SH05 | La Rose s'éveille | 10,5 s | 1:24–1:35 | Elias, la Rose | Vu de l'ouest, trois quarts face, poussée sur la Rose qui s'éveille (sans tourner), puis derrière lui en plongée, 30 → 60 → 30 mm | — | mise en scène proposée (v5) |
| 16 | SC03-SH06 | Tu es vivante ? | 6,4 s | 1:35–1:41 | Elias, la Rose (plan à deux) | orbite horaire de la plongée de dos au profil (30 → 40 mm) | — | mise en scène proposée (v5) |
| 17 | SC03-SH07 | Ceux qui savent écouter | 7,1 s | 1:41–1:48 | la Rose, Elias (amorce) | champ par-dessus l'épaule gauche d'Elias, 45 → 48 mm ; la Rose sur le tiers gauche | — | mise en scène proposée (v5) |
| 18 | SC03-SH08 | Je t'attends, Elias | 5,0 s | 1:48–1:53 | la Rose, Elias (amorce) | champ plus serré, 58 → 62 mm | — | mise en scène proposée (v5) |
| 19 | SC03-SH09 | Pas moi | 8,6 s | 1:53–2:02 | Elias, la Rose (plan à deux) | Plan à deux de profil, comme la fin de SH06, 40 → 41 mm | — | mise en scène proposée (v5) |
| 20 | SC03-SH10 | Les étoiles vont tomber | 6,5 s | 2:02–2:08 | la Rose | gros plan de la Rose, 60 → 66 mm, tiers gauche | — | mise en scène proposée (v5) |
| 21 | SC03-SH11 | Je sais | 2,7 s | 2:08–2:11 | Elias, la Rose (amorce) | contrechamp, 55 mm, Elias sur le tiers droit | — | mise en scène proposée (v5) · à générer sur 4 s |
| 22 | SC03-SH12 | Pas un spectacle | 7,9 s | 2:11–2:19 | la Rose | gros plan de la Rose, lente poussée 50 → 62 mm, tiers gauche | — | mise en scène proposée (v5) |
| 23 | SC03-SH13 | Le ciel | 3,3 s | 2:19–2:22 | — | 28 mm, à sa place, vers le nord-nord-est | — | mise en scène proposée (v5) · à générer sur 4 s |
| 24 | SC03-SH14 | J'aurai besoin de toi | 10,2 s | 2:22–2:32 | Elias (de dos), la Rose | 35 → 45 mm, derrière lui à l'ouest, poussée vers la Rose (tiers gauche) | — | mise en scène proposée (v5) |

Les fiches importées de ChatGPT (SC01-SH01 à SH05, octobre 2026) sont archivées dans `shots/_obsolete/`.
