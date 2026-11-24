# Prompts des images de début et de fin de SC03 (GPT 2.6, 16:9, 2k), 2026-11-22 nuit. @img1 = maquette du plan.
import json
MAQ = {"SH01": ("8a3HLfjIrU", "5jpwisLKxe"), "SH02": ("aFz1wqNfSh", "nVlBCDGYQD"), "SH03": ("79C2ViVJAL", "bxDU6su5Y2"),
       "SH04": ("gOhiW9WSXO", "Syv3cNkUb8"), "SH05": ("w4fZT3n7EI", "Bh6QxEWoQR"), "SH06": ("KLe73w3kqp", "tCZblqGmZJ"),
       "SH07": ("Doya5aXpcl", "s7tNnNDl8e"), "SH08": ("lJm6Y6qgv9", "P3FneYM42C"), "SH09": ("Bh6QxFToQR", "IfRqs5KtvE"),
       "SH10": ("mE25gkNhJQ", "bxDU6JK5Y2"), "SH11": ("KLe73yAkqp", "4RHYd0q9Aa"), "SH12": ("cpUIQhW0eP", "xSoPA6ajfW"),
       "SH13": ("s7tNnZPl8e", "rgBy26Bxtc")}
REF = {"E": "P3EYpgN42C", "G1": "EbWjjlfuuO", "G2": "bxDUUyw5Y2", "W": "3zkVVXyREY", "R": "XmNuutfBfo", "Ra": "XmNuukLBfo",
       "Rw": "yiQzG7fPW9", "A": "cpUIQCV0eP", "B": "6A50op6iJO", "F": "jU84GRWLD0", "P": "3zKY43UREY", "V": "MBJBIcIDCm",
       "C": "1lXOZihr4r"}
DESC = {
 "E": "Prince Elias, a 10-year-old boy, slender and slightly small for his age, fair skin with light freckles, green eyes, medium-blond tousled hair falling across his forehead; deep navy-blue velvet 1830s jacket with gold embroidery on collar, cuffs and hem, gold buttons, small gold signet pin with a crowned-rose crest on the left lapel; cream high-collared shirt; fitted beige trousers; polished brown ankle boots (design exactly as {r})",
 "G1": "the older gardener, stocky, grey moustache, wide worn straw hat, off-white linen shirt, brown canvas waistcoat, sand-coloured canvas apron (exactly as {r})",
 "G2": "the young gardener, lanky, auburn hair, small round straw hat, red neckerchief, linen shirt, canvas apron, patched olive trousers (exactly as {r})",
 "W": "the old wooden wheelbarrow (exactly as {r})",
 "R": "every rose bush of the bed drawn like {r}: a rounded 80 cm bush of dark-green leaves with many small, true-scale pink or peach roses, never a few giant roses",
 "Ra": "the single tall pale-yellow rose at the centre of the bed, asleep: an ordinary rose, no face, no glow (drawn like {r})",
 "Rw": "the tall pale-yellow rose, awake: in her golden heart a gentle stylized face with warm eyes and a small mouth, her heart glowing softly like moonlight (face and style exactly as {r}; the flower itself shaped like {r2})",
 "A": "the stone rose arch covered in pink and lilac climbing roses ({r})", "B": "the wooden bench with curly wrought-iron sides ({r})",
 "F": "the lion-head wall fountain ({r})", "P": "the palace clock tower far away ({r})", "V": "the garden plants and shrubs in the style of {r}",
 "C": "the small sprig of bright cobalt-blue bellflowers (campanula) between his fingers, exactly as he holds it in {r}",
}
STYLE = ("Stylized 3D animated feature-film still (Pixar-like), 16:9. @img1 is a 3D previs render of this exact shot: keep its camera position, lens, "
         "framing and composition exactly, and every character, object and plant exactly at its position, size and pose in @img1; redraw everything at "
         "polished animated-feature quality. Late-morning sunlight, soft warm light, gentle shadows; clear light-blue sky with a few pale stars near the horizon.")
CLEARING = ("The place: a small secret clearing in the royal garden of Aurelia, 1830. A round raised flower bed edged with a low wall of rounded weathered stones, "
            "densely planted with small shrub roses, pink and peach; a narrow straight path of three rectangular stone slabs leads between the rose bushes to a "
            "small round patch of moss at the centre of the bed, where one single tall pale-yellow rose stands, taller than the others. Pale gravel around the bed. "
            "Low curved ivy-covered stone walls, tall Italian cypresses, big round trees; behind the semicircular recess of the clearing, pink climbing roses on "
            "the low wall, tall flowering shrubs (white, lilac) and large trees.")
PLACE = ("In @img1, the smooth flat pastel shapes (soft green, pale lilac or pink ovals) are placeholders for dense flowering shrubs and hedges, the flat grey "
         "slabs are low ivy-covered stone walls, the flat light-grey ground is pale gravel: draw them as such. The small grey disc and the glowing ball on the "
         "yellow rose in @img1 only mark where her face and glowing heart are.")

def build(action, keys):
    refs = []; idx = {}
    for k in keys:
        if k not in idx: refs.append(REF[k]); idx[k] = f"@img{len(refs) + 1}"
    parts = []
    for k in keys:
        d = DESC[k].replace("{r}", idx[k])
        if k == "Rw": d = d.replace("{r2}", idx.get("Ra", idx["Rw"]))
        parts.append(d)
    return STYLE + " " + CLEARING + " " + PLACE + " In this image: " + action + " References: " + "; ".join(parts) + ".", refs

WIDE = ["E", "G1", "G2", "W", "R", "Ra", "A", "B", "F", "P", "V"]
SHOTS = {
 ("SH01", "first"): ("high aerial view looking down on the whole clearing and the lush grove around it. In the semicircular recess south of the bed (lower left), the two gardeners are about to leave: the young gardener rakes the last dead leaves into the wheelbarrow, the older gardener holds its handles. Far away at the top of the frame, on the winding gravel path through the grove, the tiny figure of Prince Elias walks towards the clearing (keep him exactly as tiny as in @img1). The rich vegetation north of the bed is the star of the shot.", WIDE),
 ("SH01", "last"): ("same high aerial view. The two gardeners have just set off along the west side of the bed (lower left), the older one pushing the wheelbarrow, the young one with his rake on his shoulder. Prince Elias, still tiny, a little closer on the winding path through the grove at the top.", WIDE),
 ("SH02", "first"): ("high angle looking down at the rose bed from above the recess. The two gardeners walk past the west side of the bed towards the bench, the older one pushing the wheelbarrow, the young one with his rake on his shoulder; neither glances at the flowers. The rose arch at the top of the frame.", ["G1", "G2", "W", "R", "Ra", "A", "B", "F", "V"]),
 ("SH02", "last"): ("eye-level view: the rose bed in the foreground, the rose arch at the centre, the palace clock tower far away at upper left. On the left, beside the bench, the two gardeners have stopped and are just putting their straw hats back on (they lifted them as the prince passed); the wheelbarrow beside them. Prince Elias has just come through the arch and walks in, head down, sulking, without seeing them.", WIDE),
 ("SH03", "first"): ("low view from the south-west across the rose bed: Prince Elias walks around the far (east) side of the bed near the lion-head fountain, his head and shoulders above the rose bushes, sulking. On the left, the two gardeners walk away towards the arch.", WIDE),
 ("SH03", "last"): ("low view across the gravel: Prince Elias sits on the stone edge of the rose bed, his back to the roses, holding a small sprig of cobalt-blue bellflowers, sulking, looking down. The garden is empty.", ["E", "C", "R", "Ra", "A", "F", "P", "V"]),
 ("SH04", "first"): ("close three-quarter shot of Prince Elias sitting on the stone edge of the bed, sulking, eyes down, the small sprig of cobalt-blue bellflowers between his fingers; behind him the pink and peach rose bushes, the sleeping yellow rose softly out of focus at upper left, the lion-head fountain on the right.", ["E", "C", "R", "Ra", "F", "A", "V"]),
 ("SH04", "last"): ("same close shot: Elias is startled, he has heard a voice behind him; he begins to spring up and turn around, eyes wide.", ["E", "C", "R", "Ra", "F", "A", "V"]),
 ("SH05", "first"): ("over Prince Elias's shoulder (the back of his head and shoulder at the right edge): he has just whirled round towards the rose bed; nobody, only the roses; the yellow rose stands asleep, seen from the side, turned away. The arch, the bench on the left, the palace clock tower far away.", ["E", "R", "Ra", "A", "B", "P", "V"]),
 ("SH05", "last"): ("over Prince Elias's left shoulder (the back of his head at the right edge): he kneels on a stone slab at the edge of the moss, right in front of the tall yellow rose, which has turned towards him and woken up: her face is visible, her golden heart glows softly. The arch and the palace clock tower behind her.", ["E", "R", "Ra", "Rw", "A", "B", "P", "V"]),
 ("SH06", "first"): ("reverse close shot of Prince Elias kneeling, filled with wonder, wide-eyed, whispering, looking at the rose (off-screen left); the yellow petals of the rose blurred in the foreground at the left edge. Behind him: the low wall of the recess covered in pink climbing roses, tall flowering shrubs and trees.", ["E", "Rw", "R", "V"]),
 ("SH06", "last"): ("same reverse close shot: Elias, amazed and surprised, mouth open, eyebrows raised (he has just heard her answer and asks if she can talk).", ["E", "Rw", "R", "V"]),
 ("SH07", "first"): ("over Prince Elias's left shoulder (the back of his head at the right edge): the awake yellow rose speaks to him, gentle and a little sad, her heart glowing; the arch and the trees behind.", ["Rw", "Ra", "E", "R", "A", "B", "P", "V"]),
 ("SH07", "last"): ("same over-the-shoulder shot: the rose, gentle, a little sad; Elias's head tilted slightly as he asks his question.", ["Rw", "Ra", "E", "R", "A", "B", "P", "V"]),
 ("SH08", "first"): ("close-up of the awake yellow rose, tender, her golden heart glowing; the arch and the trees softly out of focus behind.", ["Rw", "Ra", "R", "A", "V"]),
 ("SH08", "last"): ("same close-up: the rose smiles warmly, as if she has waited for him for a very long time.", ["Rw", "Ra", "R", "A", "V"]),
 ("SH09", "first"): ("closer reverse shot of Prince Elias kneeling, surprised that she knows his name; the rose petals blurred at the left edge; the recess with climbing roses and flowering shrubs behind him.", ["E", "Rw", "R", "V"]),
 ("SH09", "last"): ("same closer reverse shot: Elias, determined, chin up, answering 'Not me'.", ["E", "Rw", "R", "V"]),
 ("SH10", "first"): ("very close shot of the awake yellow rose, amused and playful, a teasing little smile.", ["Rw", "Ra", "R", "A", "V"]),
 ("SH10", "last"): ("same very close shot: the glow of her heart has dimmed; she is grave and serious now.", ["Rw", "Ra", "R", "A", "V"]),
 ("SH11", "first"): ("reverse shot of Prince Elias kneeling, casual, a little proud of knowing about the star shower; the rose petals blurred at the left edge; the recess with climbing roses and flowering shrubs behind him.", ["E", "Rw", "R", "V"]),
 ("SH11", "last"): ("same reverse shot: Elias, worried, fear dawning, his eyes lifting towards the sky.", ["E", "Rw", "R", "V"]),
 ("SH12", "first"): ("Elias's point of view, looking up: the top of the rose arch, the tip of a cypress and big round trees against the clear light-blue daytime sky, in which a few pale stars shine.", ["A", "V"]),
 ("SH12", "last"): ("same upward view, tilted a little higher: more sky, a few pale stars shining in broad daylight above the treetops.", ["A", "V"]),
 ("SH13", "first"): ("from behind Prince Elias, slightly to the side: he has stood up on the moss (his back at the right of the frame), facing the awake yellow rose, worried; the bed of pink and peach roses, the arch and the bench behind.", ["E", "Rw", "Ra", "R", "A", "B", "P", "V"]),
 ("SH13", "last"): ("closer on the awake yellow rose over Elias's shoulder (his back at the right edge): her face grave and tender, her heart glowing softly, as she tells him she will need him tonight.", ["E", "Rw", "Ra", "R", "A", "B", "P", "V"]),
}
out = []
for (sh, tag), (action, keys) in SHOTS.items():
    prompt, refs = build(action, keys)
    out.append({"name": f"SC03-{sh}_mes_{tag}", "maquette": MAQ[sh][0 if tag == "first" else 1], "refs": refs, "prompt": prompt})
json.dump(out, open("/mnt/user-data/outputs/sc03img/prompts_sc03.json", "w"), ensure_ascii=False, indent=1)
print(len(out), max(len(o["refs"]) for o in out), max(len(o["prompt"]) for o in out))
