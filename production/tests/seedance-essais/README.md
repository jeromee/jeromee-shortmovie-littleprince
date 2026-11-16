# Essais Seedance avant la préparation complète

Statut : fait et validé (2026-11-15, auteur) · Origine : [auteur] (décision 0006), protocole [claude]

But : vérifier, avant de préparer tout le film, trois choses jamais testées qui conditionnent la forme des fiches de plan. Tous les essais : Magnific, Seedance 2.5, 720p, 16:9, *no music*, sans vidéo de référence caméra (caméra décrite en mots), première image imposée (« @Image1 as the first frame ») + fiches de personnages en références.

| Essai | Ce qu'on teste | Durée | Références | Vignette retenue |
|---|---|---:|---|---|
| E1 — dialogue | Répliques en français, synchronisation des lèvres d'Elias **et** de la Rose, cohérence des deux personnages en plan à deux | 8 s | vignette, fiche d'Elias, fiche de la Rose | `vignettes/E1_dialogue_A_nb2.png` |
| E2 — éveil de la Rose | Rose sans visage → visage qui s'éveille (transformation), voix de la Rose et bouche d'une fleur en gros plan | 6 s | vignette, fiche de la Rose | `vignettes/E2_eveil_A_nb1.png` |
| E3 — dôme d'or | Plan à effets de nuit : le pétale s'embrase, le dôme se déploie, les étoiles s'y brisent ; Elias de dos | 8 s | vignette, fiche d'Elias | `vignettes/E3_dome_A_nb2.png` |

Vignettes : Nano Banana 2.1, avec les fiches officielles (et la référence du palais pour E3). Prompts et résultats ci-dessous.

## E1 — dialogue (scène 3)
Répliques : Elias (chuchotant) « Tu es... vivante ? » — la Rose « Bien sûr que je suis vivante. » — Elias « Tu sais parler ? »

**EN (collé)**
```text
@Image1 as the first frame. Prince Elias looks exactly like @Image2; the Rose looks exactly like @Image3. Static camera, medium two-shot, very slow push-in.
[0s] Elias, seated on the stone edge of the round flower bed, stares at the yellow Rose with wide eyes and whispers, in French, in a hushed child's voice: "Tu es... vivante ?"
[2.5s] The Rose's golden heart glows brighter as she answers, amused and warm, her small mouth moving with the words, in French, in a soft, ancient, gentle female voice: "Bien sûr que je suis vivante."
[5.5s] Elias leans a little closer, still whispering, in French: "Tu sais parler ?" The Rose smiles.
Lip movements match each line exactly; only the speaker's mouth moves. The rest of the garden is still: no wind, no birds.
Style: stylized 3D animated feature-film look, warm golden daylight, shallow depth of field, magical calm.
Sound: the two voices clearly, very faint garden ambience, silence around them; no music.
```

## E2 — éveil de la Rose (scène 3)
**EN (collé)**
```text
@Image1 as the first frame. When she wakes, the Rose looks exactly like @Image2. Static camera, slow push-in toward the yellow rose.
[0s] An ordinary pale-yellow rose with no face, in the middle of the flower bed. No wind; nothing moves.
[1s] Without any wind, the yellow rose slowly turns toward the camera; her golden heart begins to glow from within.
[2.5s] In the hollow of her petals, a gentle stylized face slowly awakens: warm eyes open, a small mouth appears, softly lit by the golden glow.
[4s] She smiles and says, in French, in a soft, ancient, warm female voice, her small mouth moving with the words: "Il y a longtemps que je t'attends, Elias."
Style: stylized 3D animated feature-film look, warm golden daylight, shallow depth of field, magical calm, never scary.
Sound: the garden falls silent, a faint airy shimmer as the heart lights up, then her voice clearly; no music.
```

## E3 — dôme d'or (scène 11)
**EN (collé)**
```text
@Image1 as the first frame. Prince Elias looks exactly like @Image2. The camera slowly pulls back and rises a little to reveal more of the sky and the palace below.
[0s] Night, on the gallery of the clock-tower belfry. Wind in his hair, Elias holds the glowing rose petal against his chest; silver shooting stars streak across the sky.
[1.5s] He lifts the petal high above his head with both hands.
[3s] The petal blazes with golden light. From the top of the tower, a translucent golden dome of light unfolds outward and downward, its surface faintly patterned with interlocking rose petals, covering the palace roofs, the garden and the forests below.
[5.5s] Silver shooting stars hit the golden dome and burst harmlessly into showers of golden sparks, one after another; a gentle golden snow begins to fall.
Style: stylized 3D animated feature-film look, deep blue night, cold silver starlight and warm golden glow, epic but gentle.
Sound: strong wind, the deep hum of the bell vibrating, a rising shimmering whoosh as the dome unfolds, soft crackling bursts as stars hit it; no music, no dialogue.
```

## Résultats (2026-11-15)
Fichiers : `E1_dialogue_720p.mp4`, `E2_eveil_720p.mp4`, `E3_dome_720p.mp4`, et les trois à la suite dans `essais_E1-E2-E3.mp4`. Coût : 3 520 + 2 640 + 3 520 crédits (≈ 440 crédits par seconde en 720p, sans vidéo de référence) + 6 vignettes (390).

| Essai | Image | Son (analyse d'énergie, à écouter) | Verdict provisoire |
|---|---|---|---|
| E1 — dialogue | Elias et la Rose fidèles à leurs fiches tout du long ; cadre un peu plus serré que la vignette dès le début ; la Rose sourit, ferme les yeux à la fin | Quatre blocs de parole aux bons moments : 0,5–0,8 s et 1,5–1,9 s (Elias), 3,4–4,8 s (la Rose), 6,7–7,1 s (Elias) | ✔ à confirmer à l'écoute (langue, voix, lèvres) |
| E2 — éveil | La rose sans visage se tourne, son cœur s'allume, le visage apparaît progressivement (2–3,5 s), sourit ; poussée avant marquée | Réplique de la Rose entre 4,0 et 5,8 s | ✔ ; visage un peu plus « poupée » que la fiche |
| E3 — dôme | Elias fidèle de dos puis de profil ; il lève le pétale, qui s'embrase ; le dôme se déploie avec un motif de roses, la caméra recule jusqu'au palais entier sous le dôme ; une étoile s'y brise | Vent et effets (pas de dialogue) | ✔ très bon ; la caméra recule plus que demandé |

Écoute de l'auteur (2026-11-15) : « convaincant ». Les voix sonnent bien français, la synchronisation des lèvres en français est très bonne, la voix d'Elias est très bien. La voix de la Rose est un peu grave, plus celle d'une dame que d'une jeune fille : à corriger dans les prompts.

Leçons :
- La première image imposée + les fiches de personnages suffisent pour garder Elias et la Rose cohérents sur 8 s, sans vidéo de référence.
- Les répliques tombent aux horodatages demandés : on peut écrire les dialogues directement en timeline dans les prompts.
- Les effets (transformation, dôme) se décrivent bien en mots ; pour les plans à effets, Blender n'est pas nécessaire.
