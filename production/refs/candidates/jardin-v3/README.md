# Références du jardin v3 — candidates (2026-11-19)

Statut : provisoire, à valider par l'auteur · Origine : [claude] d'après la maquette Blender du jardin v3 (objets Tripo), à la demande de l'auteur (« Ok pour tout », 2026-11-19).

Les références actuelles de `production/refs/` ne sont **pas** remplacées tant que l'auteur n'a pas choisi. Planche de comparaison : `_planche_refs_jardin_v3.jpg` (actuelle | nb1 | nb2).

| Référence | Maquette (`@img1`) | Candidates | Proposition |
|---|---|---|---|
| palace-aerial | `storyboard/candidates/_jardin_v3/v3b_aerien.png` (caméra `CAM_aerien_ref`) | `palace-aerial_v3_gpt26_nb1|nb2.png` | nb1 |
| garden-day | `storyboard/candidates/_jardin_v3/v3b_massif_ouest.png` (caméra `CAM_massif_ouest`) | `garden-day_v3_gpt26_nb1|nb2.png` | nb1 |
| garden-night | — (retouche de garden-day nb1) | `garden-night_v3_gpt26_nb1|nb2.png` | nb1 |
| garden-night-golden-snow | — (retouche de garden-day nb1) | `garden-night-golden-snow_v3_gpt26_nb1|nb2.png` | nb1 |
| garden-dawn | — (retouche de garden-day nb1) | `garden-dawn_v3_gpt26_nb1|nb2.png` | nb1 |

GPT 2.6, 16:9, 2k, 2 images par référence (1 350 crédits au total).

## Points d'attention
- **La serre n'est plus visible depuis le massif** : dans le jardin v3, elle est à la lisière est, cachée par le bosquet. Les vues neige d'or et aube ne montrent donc plus son squelette ; elles montrent seulement de la fumée qui monte derrière les arbres, à droite. La serre détruite des scènes 12 et 13 demandera son propre plan et sa propre référence.
- **garden-day** suit la maquette : le massif est en bas à droite et la clairière de gravier occupe le premier plan. L'image de concept d'origine plaçait le massif au centre, au premier plan. On peut rapprocher la caméra du massif si l'auteur préfère cette composition.

## Références jointes
- **palace-aerial** : @img1 maquette ; @img2 `palace-ref.png` ; @img3 ancien `palace-aerial.png` (aspect et alentours) ; @img4 planche de la serre ; @img5 fontaine à vasques ; @img6 végétaux ; @img7 arche de roses.
- **garden-day** : @img1 maquette ; @img2 ancien `garden-day.png` (aspect, massif, Rose) ; @img3 `palace-ref.png` ; @img4 arche ; @img5 banc ; @img6 fontaine murale ; @img7 végétaux.
- **nuit, neige d'or, aube** : @img1 garden-day v3 nb1 ; @img2 l'ancienne référence du même moment (ambiance et lumière) ; @img3 `palace-ref.png`.

## Prompts
Les prompts palace-aerial et garden-day contiennent le **bloc canonique du jardin v3**, recopié mot pour mot (voir `kb/world/royal-garden.md`) ; il n'est pas répété ci-dessous.

### palace-aerial
**FR (référence)**
```text
Image fixe de long métrage d'animation 3D stylisé, 16:9, vue aérienne de référence, personne dans la scène. @img1 est un rendu de prévisualisation 3D de cette vue exacte : garder exactement la position de la caméra, le cadrage, la composition et les proportions, et l'implantation du palais, du jardin et des terres alentour (chaque allée, parterre, muret, arbre, bâtiment et objet exactement à sa place et à sa taille) ; tout redessiner avec la finition d'un long métrage d'animation.
Déjà de vrais modèles 3D dans @img1, à garder exactement à leur place et à leur taille : le palais (dessiné exactement comme @img2, le dessin officiel du palais) ; la serre victorienne au bord droit du jardin (@img4) ; la fontaine à vasques dans le parterre de gauche (@img5) ; les ifs en cône, les cyprès d'Italie et les arbres à couronne ronde du bosquet (@img6) ; les arches de roses (@img7).
Les formes plates et pâles de @img1 sont des emplacements : dans les parterres, surfaces gris-vert = gazon fin, fines lignes vertes = broderies de buis, bandes lilas pâle et petits ovales pâles = massifs de roses et de lavande ; bandes blanches = allées de gravier clair ; petit disque rose au bout du jardin = le grand massif rond de roses dans sa clairière ; ligne courbe = muret de pierre dorée à balustrade. Hors du jardin : ruban bleu pâle = rivière sinueuse avec ponts de pierre, lignes grises = chemins de terre, rangées de petites formes sombres à droite = verger et champs bordés de haies, bouquets de formes rondes = forêts, petites formes rouges à l'horizon = village aux toits rouges. @img3 est l'ancienne vue aérienne : s'en servir pour l'aspect, les couleurs et les terres autour du jardin, mais suivre @img1 pour le jardin lui-même.
[bloc canonique du jardin v3, FR]
Une petite planète à l'horizon doucement courbe. Ciel bleu clair, quelques nuages doux, quelques étoiles pâles près de l'horizon. Lumière dorée et chaude du matin venant de la droite (l'est), longues ombres douces, couleurs riches.
```
**EN (à coller)**
```text
Stylized 3D animated feature-film still, 16:9, aerial reference view, nobody in the scene. @img1 is a 3D previs render of this exact view: keep its camera position, framing, composition and proportions exactly, and keep the layout of the palace, the garden and the land around exactly as in @img1 (every path, parterre, wall, tree, building and object at exactly its position and size); redraw everything at polished animated-feature quality.
Already real 3D models in @img1, to keep exactly there and at exactly their size: the palace (its architecture drawn exactly like @img2, the official design of the palace: golden stone, U-shaped, the square clock tower with a white clock face and a slate spire, steep blue-grey slate roofs, round towers with conical roofs); the Victorian glass greenhouse on the right edge of the garden (drawn exactly like @img4); the tiered stone fountain in the left parterre (drawn exactly like @img5); the cone-clipped yews, the Italian cypresses and the round-crowned trees of the grove (drawn exactly like @img6); the rose arches (drawn exactly like @img7).
The flat pale shapes in @img1 are placeholders, to be drawn at exactly their positions: in the four parterres, the grey-green surfaces = fine lawn, the thin green lines = low clipped box hedges in curving embroidery patterns, the pale lilac bands and the many small pale ovals = beds of roses and lavender; the white strips = pale gravel paths; at the near end of the garden, the small pink disc = the large round stone-edged bed of pink and peach roses in its clearing; the curved line around the garden = a low golden-stone wall with a balustrade. Outside the garden: the pale blue ribbon = a meandering river with stone bridges, the grey lines = dirt paths, the rows of small dark shapes on the right = an orchard and hedged fields, the clumps of round shapes = forests, the small red shapes on the horizon = a red-roofed village. @img3 is the previous aerial view of this place: use it for the look, the colours and the land around the garden (river, bridges, paths, meadows with wildflowers, fields, forests, village), but follow @img1 for the garden itself.
[canonical garden v3 block, EN]
A small planet whose horizon curves gently. Light-blue sky, a few soft clouds, a few faint stars near the horizon. Warm golden morning light from the right (the east), long soft shadows, rich colours.
```

### garden-day
**FR (référence)**
```text
Image fixe de long métrage d'animation 3D stylisé, 16:9, vue de référence d'un décor de jardin, personne dans la scène. @img1 est un rendu de prévisualisation 3D de cette vue exacte : garder exactement la position de la caméra, le cadrage, la composition, les proportions et l'implantation (chaque allée, muret, arbre et objet exactement à sa place et à sa taille) ; tout redessiner avec la finition d'un long métrage d'animation.
Déjà de vrais modèles 3D dans @img1, à garder exactement à leur place et à leur taille : l'arche de pierre couverte de rosiers grimpants roses et lilas, au centre (@img4) ; le banc de bois à gauche (@img5) ; la fontaine murale à tête de lion dans le muret de droite (@img6) ; les grands arbres à couronne ronde et le cyprès d'Italie (@img7) ; au loin, en haut à gauche, au-dessus des arbres, la tour de l'horloge du palais, son cadran blanc et sa flèche d'ardoise, et une bande de toits du palais (dessinés exactement comme @img3, petits et adoucis par la distance).
Les formes simples de @img1 sont des emplacements : le grand disque rose à droite = le grand massif rond bordé de pierres, plein de roses roses et pêche ; la petite boule jaune en son centre = une rose jaune pâle plus grande, sur sa tige, un peu plus haute que les autres (rien d'autre ne la distingue) ; le sol gris pâle = une clairière de gravier clair ; les murs blancs de part et d'autre de l'arche = des murets courbes de pierre dorée drapés de lierre et de rosiers grimpants ; les bosses vert pâle derrière = des massifs d'arbustes fleuris et de roses. @img2 est l'ancienne version de ce lieu : s'en servir pour l'aspect, l'ambiance, les matières, la lumière et le massif avec sa rose jaune pâle, mais suivre @img1 pour l'implantation (ici la serre de verre n'est pas visible).
[bloc canonique du jardin v3, FR]
Ce que montre cette vue : la clairière secrète, vue de son côté sud, en regardant vers le nord à travers l'arche de roses ; le bosquet touffu ferme la vue, seule la tour de l'horloge le dépasse. Jour ensoleillé, ciel bleu clair avec quelques nuages doux et quelques étoiles pâles près de l'horizon, lumière dorée et chaude, ombres douces, couleurs riches.
```
**EN (à coller)**
```text
Stylized 3D animated feature-film still, 16:9, reference view of a garden set, nobody in the scene. @img1 is a 3D previs render of this exact view: keep its camera position, framing, composition and proportions exactly, and keep the layout exactly as in @img1 (every path, wall, tree and object at exactly its position and size); redraw everything at polished animated-feature quality.
Already real 3D models in @img1, to keep exactly there and at exactly their size: the stone arch covered in pink and lilac climbing roses in the centre (drawn exactly like @img4); the wooden bench on the left (drawn exactly like @img5); the lion-head wall fountain set in the wall on the right (drawn exactly like @img6); the tall round-crowned trees and the Italian cypress (drawn exactly like @img7); far away, upper left, above the trees, the palace clock tower with its white clock face and slate spire, and a strip of the palace roofs (drawn exactly like @img3, the official design of the palace, small and softened by distance).
The simple shapes in @img1 are placeholders, to be drawn at exactly their positions: the large pink disc on the right = the large round stone-edged flower bed, densely filled with pink and peach roses; the small yellow ball at its centre = one larger pale-yellow rose on its stem, standing a little taller than the others (nothing else distinguishes it); the pale grey ground = a clearing of pale gravel; the plain white walls on both sides of the arch = low curved golden-stone walls draped with ivy and climbing roses; the pale green humps behind the walls = clumps of flowering shrubs and roses. @img2 is the previous version of this place: use it for the look, the mood, the materials, the light and the rose bed with its pale-yellow rose, but follow @img1 for the layout (here the glass greenhouse is not visible).
[canonical garden v3 block, EN]
What this view shows: the secret clearing, seen from its south side, looking north through the rose arch; the dense grove closes the view, only the clock tower rises above it. Sunlit day, light-blue sky with a few soft clouds and a few pale stars near the horizon, warm golden light, soft shadows, rich colours.
```

### garden-night
**FR (référence)**
```text
La même clairière du jardin royal que @img1 — exactement le même cadrage, la même composition, la même implantation et les mêmes éléments (l'arche de roses, les murets courbes couverts de lierre, le banc à gauche, la fontaine murale à tête de lion à droite, le massif rond bordé de pierres de roses roses et pêche avec la rose jaune pâle au centre, les arbres, le cyprès, la tour de l'horloge au loin en haut à gauche) — mais de nuit, avec l'ambiance et la lumière de @img2 : nuit bleu profond, allées et gravier sous un clair de lune bleu, arbres et cyprès en silhouettes sombres, ciel strié d'étoiles filantes d'argent de plus en plus nombreuses. La rose jaune pâle luit doucement comme une lanterne et éclaire le massif et l'arche d'une chaude lueur dorée. La tour de l'horloge (@img3, le dessin officiel du palais) garde sa pierre dorée sous la lune bleue, son cadran doucement éclairé, quelques fenêtres allumées. Rendu de long métrage d'animation 3D stylisé, magique, calme, mystérieux. Personne dans la scène.
```
**EN (à coller)**
```text
The same royal garden clearing as @img1 — exactly the same framing, composition, layout and elements (the rose arch, the curved ivy-covered walls, the bench on the left, the lion-head wall fountain on the right, the round stone-edged bed of pink and peach roses with the pale-yellow rose at its centre, the trees, the cypress, the palace clock tower far away upper left) — but at night, with the mood and light of @img2: deep blue night, paths and gravel in deep blue moonlight, trees and cypress in dark silhouettes, the sky streaked with more and more silver shooting stars. The pale-yellow rose glows softly like a lantern and lights the round flower bed and the arch with a warm golden glow. The clock tower (@img3, the official design of the palace) keeps its golden stone in blue moonlight, its clock face softly lit, a few warm lit windows. Stylized 3D animated feature-film look, magical, quiet, mysterious. Nobody in the scene.
```

### garden-night-golden-snow
**FR (référence)**
```text
La même clairière du jardin royal que @img1 — exactement le même cadrage, la même composition, la même implantation et les mêmes éléments (l'arche de roses, les murets courbes couverts de lierre, le banc à gauche, la fontaine murale à tête de lion à droite, le massif rond de roses roses et pêche, les arbres, le cyprès, la tour de l'horloge au loin en haut à gauche) — mais de nuit, une fois le danger passé, avec l'ambiance et la lumière de @img2 : nuit bleu profond, paillettes d'or qui descendent lentement comme de la neige sur tout le jardin et se posent sur les feuilles, les murets et le gravier ; le ciel de nouveau calme. Au centre du massif, la rose jaune pâle est pâle et faible, penchée, quelques pétales tombés sur la terre ; sa lueur s'est éteinte. De minces filets de fumée montent derrière les arbres, à droite, là où se trouve la serre de verre, hors de vue. La tour de l'horloge (@img3, le dessin officiel du palais) garde sa pierre dorée sous la lune bleue, poudrée de paillettes d'or, son cadran doucement éclairé. Rendu de long métrage d'animation 3D stylisé, feutré, doux-amer, magique. Personne dans la scène.
```
**EN (à coller)**
```text
The same royal garden clearing as @img1 — exactly the same framing, composition, layout and elements (the rose arch, the curved ivy-covered walls, the bench on the left, the lion-head wall fountain on the right, the round stone-edged bed of pink and peach roses, the trees, the cypress, the palace clock tower far away upper left) — but at night, after the danger has passed, with the mood and light of @img2: deep blue night, golden sparkles drifting down slowly like snow over the whole garden and settling on the leaves, the walls and the gravel; the sky calm again. In the centre of the round bed, the pale-yellow rose is pale and weak, drooping, a few of her petals fallen on the soil; her glow has gone out. Thin wisps of smoke rise from behind the trees on the right, where the glass greenhouse stands out of sight. The clock tower (@img3, the official design of the palace) keeps its golden stone in blue moonlight dusted with golden sparkles, its clock face softly lit. Stylized 3D animated feature-film look, hushed, bittersweet, magical. Nobody in the scene.
```

### garden-dawn
**FR (référence)**
```text
La même clairière du jardin royal que @img1 — exactement le même cadrage, la même composition, la même implantation et les mêmes éléments (l'arche de roses, les murets courbes couverts de lierre, le banc à gauche, la fontaine murale à tête de lion à droite, le massif rond bordé de pierres de roses roses et pêche avec la rose jaune pâle au centre, les arbres, le cyprès, la tour de l'horloge au loin en haut à gauche) — à l'aube, le lendemain matin, avec l'ambiance et la lumière de @img2 : lumière rasante rose et dorée, longues ombres, rosée sur les feuilles et les pierres, légère brume matinale. Deux ou trois petits cratères fumants dans le gravier de la clairière ; une mince fumée monte derrière les arbres, à droite, là où se trouve la serre de verre, hors de vue ; le reste du jardin intact. Dans le massif, la rose jaune pâle se tient tranquille, redevenue une rose ordinaire, sans lueur. La tour de l'horloge (@img3, le dessin officiel du palais) dans la douce lumière de l'aube. Rendu de long métrage d'animation 3D stylisé, calme, plein d'espoir, un peu mélancolique. Personne dans la scène.
```
**EN (à coller)**
```text
The same royal garden clearing as @img1 — exactly the same framing, composition, layout and elements (the rose arch, the curved ivy-covered walls, the bench on the left, the lion-head wall fountain on the right, the round stone-edged bed of pink and peach roses with the pale-yellow rose at its centre, the trees, the cypress, the palace clock tower far away upper left) — at dawn the morning after, with the mood and light of @img2: low pink-and-gold light, long shadows, dew on the leaves and stones, a light morning mist. Two or three small smoking craters in the gravel of the clearing; thin smoke rising from behind the trees on the right, where the glass greenhouse stands out of sight; the rest of the garden intact. In the round flower bed, the pale-yellow rose stands quietly, an ordinary rose again, with no glow. The clock tower (@img3, the official design of the palace) in soft dawn light. Stylized 3D animated feature-film look, calm, hopeful, a little melancholic. Nobody in the scene.
```
