# Voix de référence des personnages

Statut : décidé (voix retenues le 2026-11-22) · Origine : [claude] · 2026-11-21

Règle (production/README.md, choix de l'auteur du 2026-11-20) : Seedance génère chaque plan avec les répliques en français ; chaque
réplique passe ensuite dans le changeur de voix de Magnific (`audio_voice_change`, ElevenLabs speech-to-speech) avec **une voix de
référence fixe par personnage**. Le changeur garde le jeu (rythme, émotion, synchronisation des lèvres) et remplace le timbre.

Personnages qui parlent (shooting script) : Elias (23 répliques), la Rose (19), la Reine (13), le Chambellan (3).
Les conseillers n'ont aucune réplique : leurs petits rires sont des bruitages, pas de voix de référence.

## Candidates (`candidates/`)
Textes : vraies répliques du film. Voix du catalogue : ElevenLabs v4. Elias : le catalogue n'a aucune voix d'enfant ; voix inventée
par Seed Audio 1.0 (description d'un garçon de 10 ans, avec ou sans la planche d'Elias en référence), à cloner ensuite.

| Personnage | Fichier | Voix (id Magnific) | Création |
|---|---|---|---|
| Reine | `reine_485-emma-simon.mp3` | Emma Simon (485) — voix témoin de la vérification | `jU8syZXLD0` |
| Reine | `reine_219-louise-bernard.mp3` | Louise Bernard (219) | `Syvw6YPUb8` |
| Reine | `reine_147-claire-laval.mp3` | Claire Laval (147) | `79COR0hJAL` |
| Chambellan | `chambellan_486-maxime-giraud.mp3` | Maxime Giraud (486) — voix témoin | `nVlWdfBYQD` |
| Chambellan | `chambellan_148-antoine-lefevre.mp3` | Antoine Lefèvre (148) | `p8Pdv56ehw` |
| Chambellan | `chambellan_1096-cedric-marchand.mp3` | Cédric Marchand (1096) | `eI4XakKdqL` |
| Rose | `rose_150-elise-durand.mp3` | Elise Durand (150) | `WDS0BuzcXe` |
| Rose | `rose_497-louise-martin.mp3` | Louise Martin (497) | `KLe1URVkqp` |
| Rose | `rose_676-melodie-nuit.mp3` | Mélodie Nuit (676) | `EbWQryauuO` |
| Elias | `elias_seed-audio_avec-planche(_normalise).wav` | Seed Audio, planche d'Elias jointe | `Doyehkupcl` |
| Elias | `elias_seed-audio_description(_normalise).wav` | Seed Audio, description seule | `gOhUN0mSXO` |

## Ensuite
1. L'auteur choisit une voix par personnage (ou en demande d'autres).
2. Elias : produire environ une minute de parole avec la voix choisie, puis la cloner dans « My Voices » (`audio_voice_clone`) :
   le clone devient sa voix de référence.
3. Test : passer une réplique Seedance existante au changeur de voix pour chaque personnage.
4. Noter la voix retenue (nom, id) dans `kb/characters/<personnage>.md`, section « Voix ».

## Choix de l'auteur (2026-11-21, soir)
- **Elias : `elias_seed-audio_avec-planche`** — retenu. Deux suites de 25 s faites avec la même voix (Seed Audio, `@Audio1` = l'échantillon
  retenu ; `elias-clonage/`, créations `MBOp56JDCm`, `bxDKi895Y2`), puis **clone ElevenLabs « Elias — Le Prince et la Rose » : voiceId 215420,
  source `mine`** (sources : `Doyehkupcl`, `MBOp56JDCm`, `bxDKi895Y2`).
  Tests (`tests/`) : `elias_clone_tts-v4.mp3` (le clone lit des répliques) ; `elias_clone_changeur_depuis-temoin-adulte.mp3` (une voix
  d'homme passée au changeur de voix vers le clone : timbre d'enfant, mais l'intonation reste un peu basse, environ 250 Hz contre 330 Hz ;
  avec la voix d'enfant que Seedance donne déjà à Elias, l'écart sera plus faible).
- **La Reine : Emma Simon (485)** — retenue. Louise Bernard (219) : « très bien aussi », en réserve.
- **Le Chambellan** : Maxime Giraud (486) « bien, peut-être une voix plus grave, sans avoir trop d'autorité » ; Cédric Marchand (1096)
  « pas mal » ; Antoine Lefèvre (148) « trop de présence pour un personnage secondaire ». Nouvelles candidates plus graves :
  Corentin Beaulieu (1191, `UPa7TuSwny`), Thibault Vasseur (1230, `u5cFPDJQLD`), Adrien Moreau (230, `xSoLGvLjfW`).
- **La Rose** : Louise Martin (497) « bien, mais il faudrait une voix un peu plus jeune » ; Elise Durand « trop mijaurée », Mélodie Nuit non.
  Le catalogue ElevenLabs n'a pas de voix française plus jeune. Nouvelles candidates (à cloner si l'une est retenue, comme Elias) :
  Gemini Achernar (694, `P3F9dqC42C`), Gemini Leda (711, `huAaUnjvqL`), Seed Audio « Louise Martin rajeunie » (`yiQ4eq7PW9`),
  Seed Audio sur description (`rgBjAtMxtc`). Fichiers `*_normalise.wav` pour l'écoute.

## Choix de l'auteur (2026-11-22)
- **Elias** : clone 215420 validé (« OK » sur `tests/elias_clone_tts-v4.mp3`).
- **Le Chambellan : Adrien Moreau (230)** — « OK, passable ».
- **La Rose : `rose_seed-audio_description`** — « OK, mais le son est très faible ». Les trois autres candidates (Louise Martin rajeunie, Gemini Leda,
  Gemini Achernar) refusées : « elles font entendre un sentiment de supériorité sur le prince ». Échantillon remis à niveau, deux suites de 25 s
  dans la même voix, jouées « tendre, proche de lui, jamais condescendante » (`rose-clonage/`), puis **clone ElevenLabs « La Rose — Le Prince
  et la Rose » : voiceId 215424, source `mine`** (sources : `5jpkzM4Kxe`, `Syvwd68Ub8`, `O6uPI2Kynm`). Test : `tests/rose_clone_tts-v4.mp3`.

## Voix de référence retenues
| Personnage | Voix | voiceId | source |
|---|---|---|---|
| Elias | clone « Elias — Le Prince et la Rose » | 215420 | mine |
| La Rose | clone « La Rose — Le Prince et la Rose » (validé le 2026-11-22) | 215424 | mine |
| La Reine | Emma Simon | 485 | catalog |
| Le Chambellan | Adrien Moreau | 230 | catalog |
