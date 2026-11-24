# Prompts des images de début et de fin de SC03 v5 (GPT 2.6, 16:9, 2k, une candidate), 2026-11-23 nuit. @img1 = maquette v5.
import json
M = {"SH01": ("Bh69l6NoQR", "iGKbhkp3uK"), "SH02": ("MBO71PBDCm", "DoyJr4npcl"), "SH03": ("lJmITamgv9", "3zk5vjfREY"),
     "SH04": ("s7t80fzl8e", "jU8BWa2LD0"), "SH05": ("oviNgzq829", "P3Fuorn42C"), "SH06": ("huAZJTBvqL", None),
     "SH07": ("N2bHts16D9", "1lXezfDr4r"), "SH08": ("JNEfdr0Oq4", "MBO71ACDCm"), "SH09": ("6A5qmUJiJO", "Bh69l0coQR"),
     "SH10": ("yiQEBlFPW9", "CqYz4IzEEy"), "SH11": ("JNEfdlpOq4", "Td7UKnuVNR"), "SH12": ("LwIoc1NswO", "O6uCXw2ynm"),
     "SH13": ("u5cYNCKQLD", "UPahDgqwny"), "SH14": ("gOhtVlXSXO", "0ewS5ccTfW")}
REF = {"E": "P3EYpgN42C", "G1": "EbWjjlfuuO", "G2": "bxDUUyw5Y2", "W": "3zkVVXyREY", "R": "XmNuutfBfo", "Ra": "LwIBSBVswO",
       "Rw": "4RHC4EK9Aa", "A": "cpUIQCV0eP", "B": "6A50op6iJO", "F": "jU84GRWLD0", "P": "3zKY43UREY", "V": "MBJBIcIDCm",
       "C": "1lXOZihr4r", "S": "1lXDouRr4r"}
D = {
 "E": "Prince Elias, a 10-year-old boy, slender and slightly small for his age, fair skin with light freckles, green eyes, medium-blond tousled hair falling across his forehead; deep navy-blue velvet 1830s jacket with gold embroidery on collar, cuffs and hem, gold buttons, small gold signet pin with a crowned-rose crest on the left lapel; cream high-collared shirt; fitted beige trousers; polished brown ankle boots (design exactly as {r})",
 "G1": "the older gardener, stocky, grey moustache, wide worn straw hat, off-white linen shirt, brown canvas waistcoat, sand-coloured canvas apron (exactly as {r})",
 "G2": "the young gardener, lanky, auburn hair, small round straw hat, red neckerchief, linen shirt, canvas apron, patched olive trousers (exactly as {r})",
 "W": "the old wooden wheelbarrow (exactly as {r})",
 "R": "every rose bush of the bed drawn like {r}: rounded bushes of dark-green leaves with many small, true-scale pink or peach roses, never giant roses",
 "Ra": "the single pale-yellow rose at the centre of the bed, asleep: a bloom 20 cm in diameter on a long thin dark-green stem with a few small leaves and only tiny dull brownish-green thorns (never red), no face, no glow (plant exactly as {r})",
 "Rw": "the Speaking Rose, awake: a pale-yellow bloom 20 cm in diameter on a long thin stem, tiny dull brownish-green thorns (never red); in her golden heart a small gentle stylized face, about 40 % of the bloom width, with warm eyes and a small mouth, her heart glowing softly like moonlight (face, petals and proportions exactly as {r})",
 "Ra2": "the rose plant itself (long thin dark-green stem, a few small leaves, tiny dull brownish-green thorns) exactly as {r}",
 "S": "the look, light and the size of the rose relative to the boy exactly as in {r}",
 "A": "the stone rose arch covered in pink and lilac climbing roses ({r})", "B": "the wooden bench with curly wrought-iron sides ({r})",
 "F": "the lion-head wall fountain ({r})", "P": "the palace clock tower far away ({r})", "V": "the garden plants and shrubs in the style of {r}",
 "C": "the small sprig of bright cobalt-blue bellflowers (campanula) in his hands, exactly as in {r}",
}
STYLE = ("Stylized 3D animated feature-film still (Pixar-like), 16:9. @img1 is a 3D previs render of this exact shot: keep its camera position, lens, "
         "framing and composition exactly, and every character, object and plant exactly at its position, size and pose in @img1; redraw everything at "
         "polished animated-feature quality. Late-morning sunlight, soft warm light, gentle shadows; clear light-blue sky.")
CLEARING = ("The place: a small secret clearing in the royal garden of Aurelia, 1830. A round raised flower bed edged with a low wall of rounded weathered stones, "
            "densely planted with small shrub roses, pink and peach; a narrow straight path of three rectangular stone slabs leads from the south-south-east "
            "edge of the bed to a small round patch of moss at its centre, where one single pale-yellow rose stands on a long stem, a little above the other roses. "
            "Pale gravel around the bed; low curved ivy-covered stone walls, tall Italian cypresses, big round trees, tall flowering shrubs (white, lilac).")
PLACE = ("In @img1, the smooth flat pastel shapes (soft green, pale lilac or pink ovals) are placeholders for dense flowering shrubs and hedges, the flat grey "
         "areas are sky, pale gravel or low ivy-covered stone walls: draw them as such. The small grey disc and the glowing ball on the yellow rose in @img1 "
         "only mark where her face and glowing heart are.")
def build(action, keys):
    refs = []; idx = {}
    for k in keys:
        if k not in idx: refs.append(REF[k]); idx[k] = f"@img{len(refs) + 1}"
    parts = [(D["Ra2"] if k == "Ra" and "Rw" in keys else D[k]).replace("{r}", idx[k]) for k in keys]
    for k, v in idx.items(): action = action.replace("{" + k + "}", v)
    return STYLE + " " + CLEARING + " " + PLACE + " In this image: " + action + " References: " + "; ".join(parts) + ".", refs
WIDE = ["E", "G1", "G2", "W", "R", "Ra", "A", "B", "F", "P", "V"]
DLG_R = ["Rw", "Ra", "E", "R", "S", "A", "V"]
SH = {
 ("SH01", 0): ("high aerial view looking down on the whole clearing and the lush grove around it. In the semicircular recess south of the bed (lower left), the two gardeners set off: the young gardener puts his rake on his shoulder, the older one pushes the wheelbarrow. Far away at the top of the frame, on the winding gravel path through the grove, the tiny figure of Prince Elias RUNS towards the clearing, upset (keep him as tiny as in @img1).", WIDE),
 ("SH01", 1): ("same high aerial view: the two gardeners walk along the west side of the bed; Prince Elias, still tiny, runs down the winding path, a little closer.", WIDE),
 ("SH02", 0): ("high angle looking down at the bed from above the recess: the two gardeners walk past the west side of the bed towards the bench, the older one pushing the wheelbarrow, the young one with his rake on his shoulder; neither glances at the flowers. The rose arch at the top of the frame.", ["G1", "G2", "W", "R", "Ra", "A", "B", "F", "V"]),
 ("SH02", 1): ("eye-level view: the rose bed in the foreground, the rose arch at the centre, the palace clock tower far away. On the left, beside the bench, the two gardeners are putting their straw hats back on (they lifted them as the prince ran past); the wheelbarrow beside them. Prince Elias has just run through the arch without seeing them: he is now on the right, near the lion-head fountain, slowing down, head down, upset.", WIDE),
 ("SH03", 0): ("low view from the south-west across the rose bed: Prince Elias walks around the far (east) side of the bed near the lion-head fountain, slowing down, angry and sulking, his head and shoulders above the rose bushes. On the left, the two gardeners walk away through the arch.", WIDE),
 ("SH03", 1): ("low view: Prince Elias has dropped onto the stone edge of the rose bed, at the entrance of the slab path, his back to the roses, facing us; he sulks, looking down at the small sprig of cobalt-blue bellflowers in his hands.", ["E", "C", "R", "Ra", "A", "F", "V"]),
 ("SH04", 0): ("close three-quarter front shot of Prince Elias sitting on the stone edge of the bed, sulking, eyes down, the sprig of cobalt-blue bellflowers in his fingers; behind him the rose bushes, the arch, and on the left, far away, the two gardeners leaving through the arch; the lion-head fountain on the right.", ["E", "C", "G1", "G2", "R", "A", "F", "V"]),
 ("SH04", 1): ("same close shot: Elias is startled, he has heard a voice behind him (\"Tu boudes, petit prince ?\"); eyes wide, he is about to spring up.", ["E", "C", "R", "A", "F", "V"]),
 ("SH05", 0): ("wide view from the west across the rose bed: on the right, Prince Elias sits on the stone edge at the entrance of the slab path and is just springing up; on the left, in the middle of the bed, the single pale-yellow rose, asleep, small at this distance; the lion-head fountain behind.", ["E", "R", "Ra", "F", "V"]),
 ("SH05", 1): ("high angle from behind Prince Elias: he kneels on the slab path among the rose bushes, seen from behind; just in front of him, above his head, the Speaking Rose, awake, her heart glowing, looks down at him; the bench on the left and the stone arch behind.", ["E", "Rw", "Ra", "R", "A", "B", "V"]),
 ("SH06", 0): ("high angle from behind Prince Elias: he kneels on the slab path among the rose bushes, seen from behind; just in front of him, above his head, the Speaking Rose, awake, her heart glowing, looks down at him; the bench on the left and the stone arch behind.", ["E", "Rw", "Ra", "R", "A", "B", "V"]),
 ("SH07", 0): ("over Prince Elias's left shoulder (the back of his head cut by the right edge of the frame): the Speaking Rose, on the left third, speaks to him, gentle and a little sad, her heart glowing; a pillar of the rose arch and the trees behind her.", DLG_R),
 ("SH07", 1): ("same over-the-shoulder shot: the Rose listens to his question, gentle, a little sad.", DLG_R),
 ("SH08", 0): ("closer over-the-shoulder shot (the back of Elias's head at the right edge): the Speaking Rose, on the left third, tender, her heart glowing.", DLG_R),
 ("SH08", 1): ("same shot: the Rose smiles warmly, as if she had waited for him for a very long time.", DLG_R),
 ("SH09", 0): ("profile two-shot, like {S}: on the right, Prince Elias kneels in profile, surprised that she knows his name; on the left, about 40 cm from his face, the Speaking Rose turned towards him, gentle, a little sad; the lion-head fountain behind.", ["E", "Rw", "R", "F", "S", "V"]),
 ("SH09", 1): ("same profile two-shot: Elias, determined, chin up, says \"Pas moi.\"; the Rose looks at him tenderly.", ["E", "Rw", "R", "F", "S", "V"]),
 ("SH10", 0): ("close-up of the Speaking Rose on the left third, amused and teasing, a little smile, her heart glowing; small pink roses of the bed around her give the scale; a pillar of the arch and cypresses behind.", ["Rw", "Ra", "R", "S", "A", "V"]),
 ("SH10", 1): ("same close-up: the glow of her heart has dimmed; she is grave and serious now.", ["Rw", "Ra", "R", "S", "A", "V"]),
 ("SH11", 0): ("reverse close shot of Prince Elias kneeling, on the right third, casual and a little proud (\"Je sais. Ils vont regarder le spectacle.\"); the yellow petals of the Rose blurred in the foreground at the left edge; tall flowering shrubs behind him.", ["E", "Rw", "R", "S", "V"]),
 ("SH11", 1): ("same reverse shot: his little smile is fading as he sees her face.", ["E", "Rw", "R", "S", "V"]),
 ("SH12", 0): ("close-up of the Speaking Rose on the left third, grave and afflicted (\"Ce n'est pas un spectacle.\"), her glow dim; small pink roses of the bed around her; a pillar of the arch and cypresses behind.", ["Rw", "Ra", "R", "S", "A", "V"]),
 ("SH12", 1): ("same close-up, a little closer: the Rose, deeply sad and worried, eyes lowered (\"Ta planète entière.\").", ["Rw", "Ra", "R", "S", "A", "V"]),
 ("SH13", 0): ("Elias's point of view, looking up: the top of the rose arch and big round trees against the clear light-blue daytime sky, in which a few pale stars shine.", ["A", "V"]),
 ("SH13", 1): ("same upward view, tilted a little higher: more sky, a few pale stars shining in broad daylight above the treetops.", ["A", "V"]),
 ("SH14", 0): ("from behind Prince Elias, slightly to the side: he has stood up among the rose bushes on the slab path (his back in the middle of the frame), facing the Speaking Rose on the left, worried; the arch, the bench and the fountain behind.", ["E", "Rw", "Ra", "R", "A", "B", "F", "V"]),
 ("SH14", 1): ("closer over Elias's shoulder (his back and head at the right): the Speaking Rose on the left third, her face grave and tender, her heart glowing softly, as she tells him she will need him tonight.", ["E", "Rw", "Ra", "R", "S", "A", "B", "V"]),
}
out = []
for (sh, j), (act, keys) in SH.items():
    m = M[sh][j]
    if m is None: continue
    pr, refs = build(act, keys)
    out.append({"name": f"SC03-{sh}_{'first' if j == 0 else 'last'}", "refs": [m] + refs, "prompt": pr})
json.dump(out, open("/mnt/user-data/outputs/sc03v5/prompts_sc03_v5.json", "w"), ensure_ascii=False, indent=1)
for o in out: print("###", o["name"], json.dumps(o["refs"])); print(o["prompt"][len(STYLE)+len(CLEARING)+len(PLACE)+3:])
