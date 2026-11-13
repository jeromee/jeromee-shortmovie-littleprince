# 0001 — Une seule structure de dossier pour deux plugins d'écriture

Statut : décidé · Date : 2026-10-01

**Choix.** Fusionner les deux conventions :
- `story-bible.md` (screenwriting `sw-workflow`) = état de session, étape,
  éléments décidés, journal des décisions. Conclusions uniquement.
- `kb/` + `work/` (creative-writing-skills) = wiki par concept et brouillons.
- `production/` = livraison CapCut (aucun des deux plugins ne la couvre).
- `CLAUDE.md` = contrat commun lu par les deux plugins.

**Pourquoi.** sw-workflow a besoin d'un fichier court pour reprendre d'une
session à l'autre ; les agents creative-writing (muse, critic,
continuity-checker…) cherchent `kb/` et `work/`. Relier la bible aux pages kb
garantit une source unique.

**Écarté.** Deux structures parallèles (elles divergeraient) ; tout dans la
bible (dépasse sa taille limite, casse les agents qui s'appuient sur la kb).
