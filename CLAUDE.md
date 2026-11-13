# Le Prince et la Rose — Guide du projet

> À lire en premier. C'est le contrat commun aux **deux** plugins d'écriture
> (`screenwriting`, skills sw-*, et `creative-writing-skills`) et à tout agent
> qui travaille dans ce dossier.

## Présentation du projet

Un court métrage d'animation de style Pixar, de **5 minutes ou plus**, réalisé
en grande partie avec l'IA générative. Public : cercle privé, sans prétention
de diffusion. Objectifs, exigences et outils détaillés dans
[kb/decisions/0004-production-goals-and-tools.md](kb/decisions/0004-production-goals-and-tools.md)
(source : `Import/Little Prince - clarification 01.md`).

**Niveau d'exigence.**
- **Image : non négociable.** Le film DOIT être visuellement très joli et
  solide sur le plan cinématographique (cadrage, éclairage, montage…).
- **Histoire et scénario : au moins « passable ».** On accepte des faiblesses
  d'originalité, de rythme ou de gestion de la tension. Ne pas sur-investir
  l'écriture au détriment de l'avancement.

**Chaîne d'outils.**
| Outil | Rôle |
|---|---|
| Claude Desktop (ce projet) | Tous les textes : logline, synopsis, bible des personnages, bible du monde, scénario (writer's draft) formaté avec dialogues, scénario de tournage (shooting script), descriptions de plans à copier-coller dans CapCut |
| Freepik / Magnific | Toutes les images : concepts, fiches de personnages, first frame / last frame — modèles Nano Banana, GPT-Image, Seedream… |
| CapCut Video Studio (Director Mode) | Dialogue avec l'agent « CapCut AI », import des assets, génération vidéo de chaque plan (**Seedance 2.5**), voix des dialogues et bruitages intégrés |
| CapCut « classique » | Musique libre de droits (bibliothèque CapCut) et montage final |

**Histoire.** À construire librement à partir d'éléments du *Petit Prince* de
Saint-Exupéry, **empruntés et assumés** : aujourd'hui un petit prince, une
petite planète, une rose qui parle ; d'autres éléments de l'œuvre restent
disponibles (voir [work/brainstorm/borrowable-elements.md](work/brainstorm/borrowable-elements.md)).

## Langue

- Langue de travail, des documents et du scénario : **français**. L'auteur
  s'exprime en français ; tout fichier édité ou généré est en français.
- Les skills sw-* sont rédigés en chinois : la production reste en français ;
  les termes techniques gardent leur original anglais entre parenthèses quand
  c'est utile (logline, beat, midpoint…), selon `sw-workflow/terms.md`.
- **Blocs à coller dans CapCut ou dans un modèle d'image** : chaque bloc existe
  en deux versions — **FR (référence)**, qui fait foi, et **EN (à coller)**,
  traduction fidèle tenue synchronisée. Toute modification se fait d'abord en
  FR, puis est reportée en EN.
- **Voix du film (dialogues parlés générés par CapCut) : français** (décidé le 2026-11-02).
  Dans les prompts EN, les répliques sont citées **en français**, entre guillemets.
- Les prompts importés de ChatGPT (v0) restent en anglais, mot pour mot.
- Les noms de fichiers et de dossiers restent en anglais (liens stables).
- L'auteur utilise volontiers des mots anglais pour le jargon technique
  (first frame, shooting script, writer's draft…) : les garder tels quels.

## Comment les deux plugins se partagent le dossier

| Besoin | Propriétaire | Emplacement |
|---|---|---|
| État de session, étape, éléments décidés, journal des décisions | screenwriting (`sw-workflow`) | `story-bible.md` |
| Wiki de référence par concept (personnages, lieux, règles) | creative-writing (`kb-management`) | `kb/` |
| Faits établis (une fois une scène verrouillée) | creative-writing (`story-memory`) | `kb/canon/` |
| Noms et termes canoniques | creative-writing (`shared-dao`) | `kb/vocab.md` |
| Justification détaillée des décisions | creative-writing | `kb/decisions/` |
| Problèmes transversaux / continuité | creative-writing | `kb/issues/` |
| Plan, séquencier, tableau des beats | les deux (`sw-story-structure`, `sw-scene-craft`, `story-planning`) | `work/outline/` |
| Brouillons du scénario (Fountain) | screenwriting (`sw-format-adaptation`) | `work/drafts/` |
| Brainstorms, options | creative-writing (`brainstormer`) | `work/brainstorm/` |
| Critiques et rapports de diagnostic | les deux (`critic`, `editor`, diagnostics sw) | `work/critique-reports/` |
| Livraison CapCut : liste des plans + prompts par plan | ce projet | `production/` |
| Matériaux bruts (intouchables) | — | `Import/` |

**Règle de source unique.** `story-bible.md` ne contient que des *conclusions
et l'état d'avancement* (≤ ~15 000 mots) ; il renvoie vers les pages `kb/` au
lieu de les répéter. L'apparence, la voix et les verrous visuels des
personnages vivent **uniquement** dans `kb/characters/*` ; les fiches de plan
y renvoient, sans jamais les redéfinir.

## Arborescence

```text
CLAUDE.md                 ce guide
story-bible.md            centre sw-workflow : étape, décisions, journal, « Prochaine étape »
Import/                   matériaux bruts — ne jamais modifier
kb/
  AGENTS.md               intention et règles de la KB
  index.md                catalogue des pages
  vocab.md                termes canoniques
  characters/             une fiche par personnage (avec verrou visuel pour les prompts)
  world/                  planète, lieux, style visuel, règles du monde
  canon/                  faits verrouillés par scène (vide tant qu'aucune scène n'est verrouillée)
  styles/                 références de voix et de ton (dialogues)
  decisions/              fiches de décision (NNNN-slug.md)
  issues/                 problèmes suivis (continuité, conflits ouverts)
work/
  outline/                séquencier, tableau des beats
  drafts/                 brouillons du scénario : screenplay-vN.fountain
  brainstorm/             listes d'options, explorations
  critique-reports/       retours de critique / diagnostic
production/
  README.md               conventions de travail CapCut
  shot-list.md            tableau maître des plans (durées, identifiants, statut)
  shots/                  une fiche par plan : SCxx-SHyy.md
```

## Conventions

- **Statut** en tête de chaque page kb/work/production :
  `provisoire` (importé ou proposé, non validé) → `décidé` (validé par
  l'auteur) → `canon` (verrouillé dans une scène ou un plan terminé).
  Tout le matériau importé de ChatGPT démarre en `provisoire`.
- **Origine** des idées : `[import]` fichier ChatGPT, `[auteur]`, `[claude]`,
  `[image]` image de concept.
- **Identifiants** : scènes `SC01`, plans `SC01-SH01`. Fiches de plan nommées
  par identifiant. Durées en secondes ; minutage du film en `m:ss`.
- **Format du scénario** : Fountain (`.fountain`) ; 1 page ≈ 1 min.
- **Modifier un élément décidé** → ajouter une ligne au journal des décisions
  de `story-bible.md` (date, quoi, pourquoi) ; justification longue →
  `kb/decisions/`.
- Les images de concept sont référencées par leur chemin dans `Import/` (ou un
  futur `production/refs/`), jamais copiées dans les pages kb.
- Les modifications directes de l'auteur font toujours foi ; relire les
  fichiers avant de les modifier.

## Protocole de session (les deux plugins)

1. Ouvrir `story-bible.md` → lire *Étape en cours*, *Décidé*, *Journal des décisions*.
2. Travailler l'étape en cours, dans l'ordre : 0 Intention → 1 Logline → 2 Personnages
   → 3 Monde (boucle 1–3) → 4 Synopsis → 5 Séquencier → 6 Writer's draft →
   7 Shooting script → 8 Découpage technique. **Aucun travail visuel avant la fin
   de l'étape 7** (kb/decisions/0005).
3. Reporter les conclusions dans la bible ; le savoir détaillé dans `kb/`.
4. Terminer en mettant à jour la ligne **Prochaine étape** de la bible.

## Gestion de versions (Git)

- Le dossier est un dépôt Git, versionné par l'auteur.
- Claude ne fait jamais de commit, de push ni de réécriture d'historique sans
  demande de l'auteur.
- Les agents creative-writing (critic, editor, continuity-checker) peuvent lire
  `git diff` / `git log` pour voir ce qui a changé depuis le dernier commit.
- Rythme conseillé : un commit par étape validée (décision prise, plan prêt
  pour CapCut, nouveau brouillon du scénario).
