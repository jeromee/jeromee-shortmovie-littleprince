# Test — modèles d'image et respect des échelles (2026-11-17)

Statut : provisoire · Origine : [auteur] (demande) + [claude] (essais)

Question de l'auteur : Nano Banana 2.1 est très bon, mais ne respecte pas toujours
les échelles du rendu Blender (`@img1`). Les deux autres modèles font-ils mieux ?

## Protocole
- Trois vignettes A de la scène 2 où Nano Banana 2.1 avait du mal :
  SC02-SH01 (cinq petits personnages devant le palais), SC02-SH05 (trois personnages
  à garder à leur taille), SC02-SH06 (Elias minuscule, serre lointaine).
- **Même prompt, mêmes références** (rendu Blender avec personnages et orangers 3D,
  fiches de personnages, planche de l'oranger, pendentif) que les candidates
  `*_3d_or_*` de Nano Banana 2.1 ; 2K, 16:9, deux variantes par modèle.
- Modèles : GPT 2.6 (`gpt-2-6`, réglages par défaut) et Seedream 5.5 (`seedream-5-5`).
- Fichiers : `storyboard/candidates/SC02-SH0x/SC02-SH0x_A_gpt26_nb1|nb2.png` et
  `…_sd55_nb1|nb2.png` ; planche `storyboard/candidates/_cmp_modeles_SC02_SH01-05-06.jpg`,
  détail `_cmp_modeles_zoom.jpg`.

## Résultats (lecture de Claude, à confirmer par l'auteur)
| Plan | Nano Banana 2.1 | GPT 2.6 | Seedream 5.5 |
|---|---|---|---|
| SH01 | personnages nettement agrandis | tailles et places justes (2/2), action jouée (marche, carnets), fauteuils en rangées | tailles justes (2/2), mais personnages plutôt figés ; gros fauteuils au premier plan |
| SH05 | Elias et la Reine un peu agrandis | très proche du rendu (2/2), pendentif visible | nb1 : la Reine nettement agrandie ; nb2 : juste |
| SH06 | serre énorme au premier plan | serre petite au fond, Elias minuscule (2/2) | nb1 : Elias grossi et déplacé ; nb2 : juste |

- **Échelles** : GPT 2.6 6/6, Seedream 5.5 4/6, Nano Banana 2.1 en difficulté sur les trois.
- **Fidélité aux personnages** : bonne pour les deux ; GPT 2.6 un peu plus net et plus vivant.
- **Rendu** : Seedream 5.5 plus doux et plus voilé ; GPT 2.6 plus contrasté, lumière rasante marquée.
- **Coût par image (2K)** : Nano Banana 2.1 = 65 crédits ; GPT 2.6 = 135 ; Seedream 5.5 = 70 à 100
  selon le nombre de références. Durée : ~45 s pour GPT 2.6, ~35 s pour Seedream 5.5.

## Piste
Pour les vignettes A tirées d'un rendu Blender (mode B), essayer GPT 2.6 en premier
choix, Nano Banana 2.1 restant le modèle des planches et des retouches.

## Suite — GPT 2.6 sur le reste du storyboard (2026-11-17)
Demande de l'auteur : rejouer avec GPT 2.6 les autres vignettes, avec le dernier prompt et les
dernières références de chacune (retrouvés dans l'historique Magnific), 2K, deux variantes.
Fichiers `storyboard/candidates/SCxx-SHyy/SCxx-SHyy_A|B_gpt26_nb1|nb2.png` ; planche
`storyboard/candidates/_cmp_gpt26_storyboard.jpg` (maquette ou rendu 3D | Nano Banana 2.1 | GPT 2.6 ×2).

| Vignette | Ce qui a été rejoué | Lecture de Claude (à confirmer) |
|---|---|---|
| SC01-SH01 A | la retouche v2 (vignette v1 + vue aérienne de l'époque) | quasi identique à Nano Banana ; palais minuscule respecté |
| SC01-SH02 B | maquette v2 + vue aérienne v4 | très fidèle à la vue aérienne, comme Nano Banana |
| SC01-SH03 A | maquette v3 + palace-ref + vue aérienne v4 | angle plus bas, plus proche de la maquette ; fontaine à gauche, serre à droite ; jardin moins « ovale » |
| SC01-SH03 B | génération de base seulement (maquette v2 + palace-ref) | les deux retouches Nano Banana du télescope (orientation, taille) ne sont pas rejouées ; maquette antérieure au palais Tripo officiel |
| SC02-SH02 A | rendu 3D + fiches + oranger | tailles justes, Elias tend la clochette, marche jouée |
| SC02-SH03 A | rendu 3D + fiches + oranger | tailles justes, rires « main devant la bouche » joués |
| SC02-SH04 A | rendu 3D + fiche + oranger | cadrage et taille d'Elias fidèles au rendu (Nano Banana le grossissait) |

SC02-SH06 n'a pas été rejoué une seconde fois : ses deux variantes GPT 2.6 existent déjà (essai précédent).
Coût : 14 images × 135 = 1 890 crédits.

## Suite — GPT 2.6 sur les références de décor et d'accessoires (2026-11-17)
Demande de l'auteur : rejouer avec GPT 2.6 les onze références de `production/refs/`, avec le
dernier prompt et les dernières références de chacune (retrouvés par la lignée Magnific), 2K,
deux variantes. Fichiers `refs/candidates/<nom>_gpt26_nb1|nb2.png` ; planches
`refs/candidates/_cmp_gpt26_refs_1.jpg` et `_cmp_gpt26_refs_2.jpg` (référence actuelle | GPT 2.6 ×2).

Limite du test : huit références s'appuient sur des images Nano Banana (chaînes de retouches dont on
ne rejoue que la dernière étape, avec ses références d'origine). Pour celles-là, GPT 2.6
retouche une image Nano Banana au lieu de tout refaire. Cela compte surtout pour garden-night,
garden-night-golden-snow, tower-door, elias-room et key-pendant-sheet.

| Référence | Ce qui a été rejoué | Lecture de Claude (à confirmer) |
|---|---|---|
| palace-aerial | maquette v3 + vue aérienne précédente + palace-ref | proportions plus proches de la maquette (jardin ovale profond, palais plus petit) ; parterres de buis plus simples que chez Nano Banana |
| garden-day | Garden with Rose 01 + palace-ref + palace-aerial | presque identique ; palais un peu plus lointain, échelle plus juste |
| garden-night | retouche « palais officiel » (jardin de nuit NB + garden-day + palace-ref) | palais en pierre dorée au clair de lune plus lisible, horloge éclairée |
| garden-night-golden-snow | retouche « palais officiel » (image NB + garden-day + palace-ref) | très proche ; serre détruite et fumée conservées, palais plus net |
| garden-dawn | garden-day + image d'ambiance (lumière de l'aube) | brume et lumière rose bien rendues ; palais et serre détruite justes |
| queen-study | palace-ref seul | plus riche et plus doré ; ajoute des roses jaunes sur le bureau ; portrait plus grand que « petit » |
| tower-interior | palace-ref seul | nettement plus spectaculaire : engrenages, balancier, escalier en spirale, cadran vu de dos |
| tower-door | retouche « porte à l'intérieur » (porte v2 NB) | porte conservée ; sol miroitant et ombres de fenêtres au clair de lune |
| elias-room | retouche « paysage de nuit » (chambre v4 NB) | quasi identique à Nano Banana |
| key-pendant-sheet | correction du panneau 3 (planche NB) | panneau 3 juste : l'étui reste sur le collier, la clé sort à moitié |
| petal-sheet | fiche de la Rose + fiche d'Elias | dôme de pétales plus lisible au panneau 3 ; cadres arrondis autour des panneaux |

Coût : 22 images × 135 = 2 970 crédits.

## Suite — scène 1 refaite avec le palais officiel (2026-11-18)
Les maquettes SC01 ont été refaites avec le palais Tripo officiel (voir le journal de la bible).
Vignettes régénérées avec GPT 2.6 depuis ces maquettes v4, 2K, deux variantes :
`storyboard/candidates/SC01-SHxx/*_v4_gpt26_nb1|nb2.png`, planche
`storyboard/candidates/_cmp_SC01_v4_palais-officiel.jpg` (maquette | vignette actuelle | GPT 2.6 ×2).

| Vignette | Prompt et références | Lecture de Claude (à confirmer) |
|---|---|---|
| SC01-SH01 A | prompt EN de la fiche du plan, plus une phrase sur @img3 ; maquette v4 + tiny-kingdom_t0s + palace-aerial | palais et jardin minuscules, à la taille de la maquette (Nano Banana les grossissait) ; plus de nuages |
| SC01-SH02 B | dernier prompt GPT 2.6 ; maquette v4 + palace-aerial | très fidèle à la vue aérienne |
| SC01-SH03 A | dernier prompt GPT 2.6 ; maquette v4 + palace-ref + palace-aerial | palais lointain et petit comme dans la maquette ; jardin moins touffu que la vignette actuelle |
| SC01-SH03 B | dernier prompt GPT 2.6 ; maquette v4 + palace-ref | façade entière, escalier, télescope, dame en rose et conseillers sur la terrasse |

Coût : 8 images × 135 = 1 080 crédits.
