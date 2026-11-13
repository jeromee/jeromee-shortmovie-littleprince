# Test CapCut — mode B (référence caméra en boîtes grises)

Statut : fait (2026-11-13) · Origine : [claude]

Question : une vidéo de référence **en boîtes grises**, de contenu différent de
la vignette, transmet-elle son mouvement de caméra à Seedance 2.5 ? Ici, un
mouvement impossible en mode A : un **quart d'orbite** autour d'Elias et du
massif, avec parallaxe.

## Fichiers
- `make_graybox.py` — script Blender (bpy 5.0) : maquette grise du jardin
  (massif rond, Rose = sphère jaune, arche, cyprès = cônes, murets), mannequin
  d'Elias en bleu, caméra en quart d'orbite (5 s, 24 i/s, à hauteur d'enfant).
- `SC00-TESTB_graybox-first.png` / `-last.png` — première et dernière image (1920×1080).
- `SC00-TESTB_camera-ref.mp4` — vidéo de référence grise (5 s, 854×480).
- `SC00-TESTB_A_first-frame.png` — **à créer par l'auteur** (étape 1).
- `_ref_sheet.jpg` — la référence à 0 ; 1,25 ; 2,5 ; 3,75 et 5 s.

Rendu Cycles (CPU) avec bpy 5.0, sans ouvrir Blender : environ 10 s par image
en 854×480 ; il faut au moins du 480p pour une vidéo de référence Seedance.

## Étape 1 — vignette A dans Freepik (Nano Banana)
Images jointes, dans cet ordre : 1) `SC00-TESTB_graybox-first.png`,
2) `Import/Elias - Character Sheet.png`, 3) `Import/Garden with Rose 01.png`.
Format 16:9. Enregistrer le résultat ici sous `SC00-TESTB_A_first-frame.png`.

**FR (référence)**
> Redessine l'image 1 en gardant exactement la même caméra, le même cadrage, la
> même perspective et les mêmes positions. Le personnage bleu devient le prince
> Elias de l'image 2, debout, tourné vers la rose. Le bloc rond gris devient le
> massif de roses rond de l'image 3 ; la sphère jaune est la grande rose jaune,
> endormie, au centre du massif. L'arche grise devient l'arche couverte de
> roses, les cônes des cyprès, les murets des murets de pierre couverts de
> lierre, le sol une allée pavée et du gazon. Jardin royal ensoleillé de
> l'image 3, lumière dorée du matin. Rendu de long métrage d'animation 3D
> stylisé, formes arrondies et attachantes. Aucune forme grise ni bleue ne
> reste visible.

**EN (à coller)**
> Redraw image 1 keeping exactly the same camera, framing, perspective and
> positions. The blue figure becomes Prince Elias from image 2, standing,
> facing the rose. The round gray block becomes the round rose bed from
> image 3; the yellow sphere is the large yellow rose, asleep, at the centre of
> the bed. The gray arch becomes the rose-covered arch, the cones become
> cypress trees, the low walls become ivy-covered stone walls, the floor a
> cobbled path and lawn. The sunlit royal garden of image 3, golden morning
> light. Stylized 3D animated feature-film look, rounded appealing shapes. No
> gray or blue shapes remain visible.

## Étape 2 — génération dans CapCut
Seedance 2.5 · mode Omni reference · 16:9 · **5 s** · 720p.
Fichiers joints, dans cet ordre : 1) `SC00-TESTB_A_first-frame.png`,
2) `SC00-TESTB_camera-ref.mp4`, 3) `Import/Elias - Character Sheet.png`.

**FR (référence)**
> @Image1 comme première image. Reprendre uniquement le mouvement de caméra de
> @Video1 : même trajectoire, même vitesse, même rythme ; les formes grises et
> bleues de @Video1 ne sont que des repères et ne doivent pas apparaître. La
> caméra tourne d'un quart de tour vers la droite autour du garçon et du
> massif de roses. Le prince Elias (@Image2) reste immobile et regarde la rose
> jaune endormie au centre du massif. [verrou EN d'Elias]. Son : ambiance de
> jardin douce, chants d'oiseaux ; pas de musique, pas de dialogue.

**EN (à coller)**
> @Image1 as the first frame. Take only the camera movement from @Video1: the
> same path, speed and timing; the gray and blue shapes in @Video1 are only
> placeholders and must not appear. The camera circles a quarter turn to the
> right around the boy and the rose bed. Prince Elias (@Image2) stands still,
> watching the sleeping yellow rose at the centre of the bed. Prince Elias, a
> 10-year-old boy, slender and slightly small for his age, fair skin with light
> freckles, green eyes, medium-blond tousled hair falling across his forehead;
> deep navy-blue velvet 1830s jacket with gold embroidery on collar, cuffs and
> hem, gold buttons, small gold signet pin with a crowned-rose crest on the
> left lapel; cream high-collared shirt; fitted beige trousers; polished brown
> ankle boots. Stylized 3D animated feature-film look. Sound: soft garden
> ambience, birdsong; no music, no dialogue.

Enregistrer le résultat ici sous `result-01.mp4`.

## Ce qu'on vérifie
- Le sens (vers la droite), l'amplitude (un quart de tour) et le rythme de
  l'orbite, comparés à la référence.
- Elias reste identique (visage, costume) pendant qu'on tourne autour de lui.
- Aucune forme grise ni bleue n'apparaît.
- La musique est-elle évitée par la ligne « Sound » ?

## Résultat — `result-01.mp4` (2026-11-13)
Seedance 2.5, 720p, 5 s. Vignette A = `SC00-TESTB_A_first-frame-b.png`
recadrée en 16:9.

- **Orbite : réussie.** Sens, amplitude et rythme suivent la référence grise :
  Elias passe de droite à gauche de la Rose et la masque à mi-plan, la Rose
  passe à droite, l'arche traverse le cadre de gauche à droite, avec la même
  accélération et la même décélération.
- **Image 0 :** la caméra de la référence l'emporte sur la vignette. Le
  contenu de A est repris, mais **recadré comme la maquette** (Elias vers 0,65
  de la largeur au lieu de 0,75). Une vignette A doit donc respecter
  fidèlement le cadrage de la maquette.
- **Elias :** reconnaissable et stable pendant toute l'orbite (cheveux,
  costume) ; on finit sur son profil.
- **Aucune forme grise ni bleue** dans l'image.
- **Netteté : faible.** Variance du laplacien : vignette A 1142 → image 0 371
  → environ 185 pendant l'orbite (≈ 16 % de la vignette). Au test A, on gardait
  environ 45 %. Causes probables : sortie 720p, flou de mouvement d'une orbite
  rapide (90° en 5 s), référence grise rendue douce (854×480, débruitée).
- **Musique :** toujours présente malgré « no music ».
- Petit filigrane « CapCut AI » (retiré à l'export avec le plan Pro).

**Conclusion :** le mode B fonctionne pour le mouvement. À régler : netteté
(1080p, référence plus nette, « sharp focus » dans le prompt, ou upscale
ensuite) et musique.

Fichiers d'analyse : `_sheet.jpg` (en haut la référence, en bas le résultat, à
0 ; 1,25 ; 2,5 ; 3,75 et 5 s), `_detail_f1.jpg` (détail de A à gauche, image 0
du résultat à droite).

---

# Test B2 — netteté (2026-11-13)

Même plan, trois changements pour gagner en netteté :
1. **Référence plus nette** : `SC00-TESTB_camera-ref-720p.mp4` (1280×720,
   filtre de pixel serré ; `make_graybox.py … --frames 1 120 --hq`).
2. **Vignette A2** générée par Claude dans Magnific (Nano Banana 2.1, 2k,
   16:9) en insistant sur le respect du cadrage de la maquette : création
   « The blue figure becomes Prince Elias, standing » (variante retenue),
   dans le projet Magnific « Little Prince ». Rose, massif et arche bien
   placés ; Elias bien placé en largeur mais environ un tiers plus grand que
   le mannequin. À télécharger et enregistrer ici sous
   `SC00-TESTB_A2_first-frame.png`.
3. **Génération en 1080p** et « sharp focus » dans le prompt.

## Génération dans CapCut
Seedance 2.5 · Omni reference · 16:9 · **5 s** · **1080p**.
Fichiers joints, dans cet ordre : 1) `SC00-TESTB_A2_first-frame.png`,
2) `SC00-TESTB_camera-ref-720p.mp4`, 3) `Import/Elias - Character Sheet.png`.
Prompt : celui du test B, en ajoutant avant « Sound » :

**FR (référence)**
> Mise au point nette sur le garçon et la rose, grande profondeur de champ,
> image nette et détaillée.

**EN (à coller)**
> Sharp focus on the boy and the rose, deep depth of field, crisp detailed image.

Enregistrer le résultat ici sous `result-02.mp4`.

## Résultat B2 — `result-02.mp4` (2026-11-13)
CapCut, Seedance 2.5, 1080p, 5 s. Coût : 800 crédits CapCut (≈ 8 €).

- **Personnage plus net** : coutures de la veste, mains et cheveux plus
  détaillés qu'en B1 (`_detail_b1_b2.jpg`).
- **Netteté globale mesurée plus basse** que B1, à résolution égale :
  Seedance a ajouté un fort contre-jour avec halo et un arrière-plan flou,
  malgré « sharp focus, deep depth of field ».
- **Artefact : l'arche est dédoublée** à partir du milieu du plan. Dans la
  vignette A2, l'arche est visible à gauche alors que la maquette la place
  hors champ ; quand l'orbite fait entrer l'arche de la maquette, le modèle en
  ajoute une seconde. → Confirme qu'en mode B la vignette doit respecter
  exactement le cadrage de la maquette.
- Orbite toujours fidèle ; musique toujours présente.

Fichiers d'analyse : `_sheet_b1_b2.jpg` (en haut B1, en bas B2),
`_detail_b1_b2.jpg` (B1 agrandi à gauche, B2 à droite, image 60).

---

# Test B3 — entièrement dans Magnific (2026-11-13)

Fait par Claude via le connecteur Magnific (projet « Little Prince »).

**Vignette A3** : trois essais à partir de `SC00-TESTB_graybox-first.png`
(dossier `b3/`), comparés par superposition à la maquette (`_b3_candidates.jpg`).
- `A3_reimagine.png` (Flux, structure verrouillée par la profondeur) :
  cadrage parfait, mais Elias hors modèle (cheveux roux, queue-de-pie) et
  1024 px seulement. Écarté.
- `A3_nb_1.png` / `A3_nb_2.png` (Nano Banana 2.1, références : maquette +
  fiche d'Elias, **sans** l'image du jardin) : massif, Rose, arche et cyprès
  à leur place ; Elias à peine décalé à droite. **`A3_nb_2.png` retenue.**
  → Retirer l'image du jardin des références a suffi à faire respecter le
  cadrage.

**Vidéo** : Seedance 2.5 dans Magnific, 1080p, 5 s, option « no music » ;
références : A3_nb_2, `SC00-TESTB_camera-ref-720p.mp4`, fiche d'Elias.
Coût : 5 400 crédits Magnific. Résultat : `result-03-magnific.mp4`.

- **Cadrage et orbite** : le meilleur des trois essais ; les positions suivent
  la maquette d'un bout à l'autre (`_sheet_b3.jpg`).
- **Musique : absente** (ambiance seule, très discrète). L'option fonctionne.
- **Netteté** : comparable à B1 (≈ 20-30 % du détail de la vignette) ; pas de
  halo de contre-jour comme en B2.
- **Arche toujours dédoublée** à partir du milieu du plan, malgré la phrase
  « une seule arche ». Ce n'est donc pas seulement l'écart de la vignette :
  l'arche de la maquette est sans doute lue comme une deuxième arche.
- Elias : cheveux plus bouclés et un peu roux par rapport à la fiche.

---

# Test B4 — arche (2026-11-13, Magnific)
Même génération que B3, avec un prompt qui décrit la maquette élément par
élément (« l'unique arche grise est l'arche de roses déjà visible au bord
gauche de @Image1 ; ne jamais ajouter une seconde arche »). 5 400 crédits.
Résultat : `result-04-magnific-arch.mp4` ; comparaison `_sheet_b4.jpg`
(maquette, B3, B4).
- **Plus d'arche dédoublée.**
- Mais **le cadrage ne suit plus la maquette** : caméra beaucoup plus proche,
  Elias deux fois plus grand. Le sens de l'orbite est conservé.
- Netteté : la plus faible des essais 1080p.
→ La phrase descriptive corrige l'arche mais fait perdre le cadrage. Piste
suivante : colorer l'arche dans la maquette (rendu à refaire) plutôt que de
la décrire.

# Test upscale (2026-11-13, Magnific)
`result-01.mp4` (CapCut 720p) passé dans **Magnific Precision** (sortie
2560×1440) : `result-01-upscaled-1080p.mp4`. 2 297 crédits Magnific.
Netteté ramenée en 1080p (variance du laplacien, images 1/30/60/90/120) :

| Version | Netteté |
|---|---|
| B1 CapCut 720p agrandi simplement | 89 / 48 / 45 / 47 / 60 |
| B1 + Magnific Precision | **267 / 229 / 184 / 223 / 232** |
| B3 Magnific 1080p natif | 138 / 116 / 78 / 71 / 80 |
| B4 Magnific 1080p natif | 81 / 60 / 43 / 55 / 53 |

→ L'upscale Precision rend l'image nettement plus nette que le 1080p natif,
sans changer le contenu (`_detail_upscale.jpg` : à gauche agrandi simplement,
à droite après upscale). **Générer en 720p puis upscaler** coûte à peu près
autant que le 1080p natif (≈ 2 600 + 2 300 crédits contre 5 400) pour un
meilleur résultat.

# Test B5 — arche colorée dans la maquette (2026-11-13, Magnific)
Référence refaite avec l'arche en rose pierre (`make_graybox.py … --hq
--arch-color`) : `SC00-TESTB_camera-ref-720p-arch.mp4`. Vignette A3 (nb_2)
inchangée ; prompt de B3 avec « l'arche rose de @Video1 est l'arche de
roses ». Seedance 2.5, **720p**, no music, 2 600 crédits.
Résultat : `result-05-magnific-arch-720p.mp4` ; comparaison `_sheet_b5.jpg`.
- Cadrage bien suivi au début, un peu plus serré en fin de plan.
- **Pire pour l'arche** : à partir du milieu, Seedance dessine une galerie de
  plusieurs arches. Colorer l'arche ne suffit pas.
- Hypothèse : dans la vignette, l'arche du bord gauche paraît plus proche et
  plus grande que l'arche de la maquette (placée loin derrière le massif). Le
  modèle n'y voit pas le même objet et en invente d'autres quand l'orbite
  dévoile l'arrière-plan.
Upscale non lancé (résultat non retenu).

# Test B6 — piste 1 : vignette de début + vignette de fin (2026-11-13, Magnific)
- Dernière image de la maquette (arche colorée) rendue en 1920×1080 :
  `b6/graybox-arch-last.png`. Vignette de fin par Nano Banana 2.1 (références :
  maquette de fin, fiche d'Elias, **vignette de début** pour garder les mêmes
  matières) : `b6/B_end_1.png` retenue (Elias à gauche, massif, Rose, arche
  derrière ; arche un peu plus grande que dans la maquette). `B_end_2.png`
  écartée (Elias du mauvais côté). Comparaison : `_b6_end_candidates.jpg`.
- Vidéo : Seedance 2.5 Magnific, 720p, no music, 2 600 crédits ; références
  A3 (début), B_end_1 (fin), référence caméra à arche colorée, fiche d'Elias ;
  prompt « @Image1 as the first frame and @Image2 as the last frame ».
  Résultat : `result-06-magnific-start-end-720p.mp4` ; `_sheet_b6.jpg`,
  `_b6_lastframe_vs_B.jpg`.

Constats :
- **Une seule arche du début à la fin** : la vignette de fin règle l'invention
  du décor.
- Orbite dans le bon sens, Elias stable et fidèle ; la dernière image reprend
  bien la composition de la vignette de fin.
- **Mais le cadrage est plus serré que prévu sur tout le plan** (environ ×1,5) :
  la première image n'est pas celle de la vignette A, Elias est plus grand.
  Même dérive qu'en B4. Hypothèses : l'arche de la vignette de fin, plus grande
  que dans la maquette, pousse le modèle à rapprocher la caméra ; ou simple
  variabilité de Seedance (une seule génération par test).

# Test B7 — relance de B6 (2026-11-13)
Mêmes entrées que B6. Résultat : `result-07-magnific-start-end-720p-reroll.mp4`,
`_sheet_b7.jpg` (maquette, B6, B7), `_b7_first_last_vs_AB.jpg`.
- Une seule arche, orbite correcte.
- **Même cadrage serré (≈ ×1,6)** : la dérive est systématique, pas due au
  hasard. Les premières et dernières images ressemblent à des recadrages
  rapprochés des vignettes A et B.

# Test B8 — vraies images clés de début et de fin, sans vidéo de référence
Mode « first / last frame » de Seedance 2.5 (Magnific, 720p, no music,
2 200 crédits) : début = A3, fin = B_end_1, caméra décrite en mots. Ce mode
interdit les références (vidéo, fiche personnage).
Résultat : `result-08-magnific-keyframes-720p.mp4`, `_sheet_b8.jpg`.
- **Début et fin exacts** (PSNR 28 et 27 dB contre les vignettes).
- **Mais le trajet est faux** : la caméra glisse latéralement au lieu de
  tourner, et Elias change de côté par un fondu au milieu du plan
  (morphing entre les deux images, pas une orbite).

# Bilan des essais mode B
| Essai | Trajet caméra | Cadrage | Décor |
|---|---|---|---|
| B3 : vignette de début + vidéo | ✔ | ✔ | ✘ arche dédoublée |
| B6/B7 : début + fin + vidéo (références) | ✔ | ✘ ≈ ×1,6 plus serré | ✔ |
| B8 : vraies images clés début + fin, sans vidéo | ✘ morphing | ✔ début et fin exacts | ✔ |
