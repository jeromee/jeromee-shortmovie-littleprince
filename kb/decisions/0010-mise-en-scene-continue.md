# 0010 — Mise en scène continue avant de verrouiller les plans

Statut : décidé (2026-11-20, auteur), méthode et mise en scène de SC02 · Origine : [auteur] proposition, [claude] mise en œuvre

## Contexte
En regardant l'animatique de SC02, l'auteur se sent « perdu spatialement » alors que la règle des 180° n'est
pas enfreinte : pas de vrai plan de situation de la terrasse ; la Reine, personnage principal du plan, vue de dos
et plus loin que ses conseillers (Hitchcock : la taille d'un objet dans le cadre doit être proportionnelle à son
importance) ; regards des conseillers illisibles ; on ne sait pas ce qu'Elias a derrière lui ; le Chambellan passe
de gauche à droite entre deux plans sans raison ; Elias passe de la Reine à l'allée des velums sans qu'on le voie.
Diagnostic de l'auteur : les fiches de plan en mots ne suffisent pas pour voir un plan ; les problèmes de continuité
n'apparaissent qu'à l'animatique ; les déplacements entre deux plans consécutifs ne sont pas réalistes, parce que
chaque plan avait ses propres personnages, posés à part.

## Décision
Pour toute scène qui garde le même lieu et la même durée (SC02 la terrasse, la porte de la tour, le jardin la nuit…) :
1. **Une scène Blender de mise en scène** par scène du film : toute l'action jouée en continu,
   **1 s d'animation = 1 s réelle**, à partir d'un chrono parlé (répliques à vitesse naturelle).
2. Tous les personnages (figurants compris) et les objets mobiles volumineux ont une position définie au début,
   puis des déplacements réalistes (vitesses de marche et de course), cohérents et **sans collision** (contrôle par script).
3. Une **caméra de vérification** fixe, vue de dessus, avec en surimpression le nom de chaque personnage, la flèche
   de son regard, son trajet, et le champ de la caméra du plan en cours.
4. **Une caméra par plan**, active sur sa fenêtre de temps (marqueurs de la timeline liés aux caméras).
5. Rendu de vérification en écran partagé : vue de dessus + caméra du plan + réplique en cours.
6. On ne verrouille les plans (vignettes, cartes Seedance) qu'une fois la mise en scène générale satisfaisante.

Analogies : la mise en place (blocking) et le plan maître suivi de la couverture au cinéma et au théâtre filmé à
plusieurs caméras ; la prévisualisation et la techvis ; le layout à l'échelle de la séquence en animation ; le
Sequencer d'Unreal (séquence maîtresse + piste de coupes caméra).

## Mise en œuvre (SC02)
`production/blender/build_mise_en_scene_sc02.py` → scènes `SC02_MISE_EN_SCENE` et `SC02_MES_VERIF` ;
chrono et plans : `production/mise-en-scene/SC02.md` ; rendu : `production/animatic/mise-en-scene/`.
Les anciennes scènes `SC02-SH01` à `SC02-SH06` restent dans `world.blend` comme archives.

## Conséquences
- `production/animatic-workflow.md` : nouvelle étape avant les caméras de plan.
- Les personnages glissent (pas de cycle de marche) : suffisant pour vérifier positions et timing ; ces rendus ne
  sont **jamais** envoyés à Seedance comme vidéo de référence (règle de `production/README.md`).
- Première et dernière images de chaque plan tirées de la scène de mise en scène : la position de chacun à chaque
  coupe est juste par construction.
