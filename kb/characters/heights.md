# Tailles et échelle des personnages

Statut : décidé (2026-11-16, auteur) · Origine : [auteur] constat de tailles variables d'une vignette à l'autre ; [claude] tailles proposées

## Pourquoi
Nano Banana redimensionne les personnages à sa guise : leurs rapports de taille
changent d'un plan à l'autre et ils paraissent trop grands par rapport au palais
(la porte du vestibule, par exemple). On fixe donc les tailles une fois pour
toutes, et on les impose de trois façons (voir plus bas).

## Les tailles
| Personnage | Taille (sommet de la tête) | Remarque |
|---|---:|---|
| Le Chambellan | 1,85 m | le plus grand, légèrement voûté |
| Conseiller 1 (grand, lunettes, vert bouteille) | 1,80 m | |
| Le valet de la Reine | 1,78 m | |
| Conseiller 3 (raide, moustache, gris ardoise) | 1,76 m | |
| La Reine Elara | 1,65 m | ≈ 1,78 m avec chignon et diadème |
| Conseiller 2 (petit, rond, noir et bordeaux) | 1,62 m | |
| Elias (10 ans) | 1,38 m | il arrive à l'épaule de sa mère |
| Porte du vestibule (palais officiel) | mesurée dans la maquette le 2026-11-16 | ≈ 4,5 m sous la clé de l'arc (≈ 4 m à la naissance de l'arc), ≈ 3 m de large : 2,5 fois la Reine, 3,3 fois Elias |

## Comment on les impose
1. **Maquette Blender** : mannequins à leur taille réelle ; le rendu de guidage
   (`@img1`) fait foi pour la taille de chaque personnage à l'écran.
2. **Prompts** : des rapports plutôt que des chiffres (« la Reine a une
   demi-tête de moins que ses conseillers », « Elias arrive à l'épaule de sa
   mère », « la porte fait plus de deux fois la hauteur d'un homme ») et la
   consigne « garder exactement la taille de chaque silhouette de @img1 ».
3. **Planche toise** : `kb/characters/sheets/lineup.png`, à joindre à toute
   vignette où paraissent plusieurs personnages ou une porte.

## Liens
[elias.md](elias.md) · [queen-elara.md](queen-elara.md) · [chamberlain.md](chamberlain.md) · [advisers.md](advisers.md) · [footman.md](footman.md)

Toise 3D (2026-11-17) : `kb/characters/sheets/lineup_3d.png`, rendu Blender des sept modèles 3D à leur taille exacte (de gauche à droite : Chambellan, conseiller 1, valet, conseiller 3, Reine, conseiller 2, Elias). Elle fait foi sur `lineup.png` pour les proportions.

> 2026-11-20 : environnement réduit ×0,8 (kb/decisions/0009). La porte du vestibule mesure désormais ≈ 3,6 m sous la clé de l'arc (≈ 3,2 m à la naissance de l'arc), ≈ 2,4 m de large : 2 fois la Reine, 2,6 fois Elias. Les tailles des personnages ne changent pas.
