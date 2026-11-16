# Superpose le rendu de maquette et l'image de référence du palais (aide au recalage).
import sys
from PIL import Image, ImageChops, ImageOps
ref = Image.open(sys.argv[1]).convert('RGB').resize((1280, 720))
gb = Image.open(sys.argv[2]).convert('RGB').resize((1280, 720))
edges = ImageOps.invert(ImageOps.autocontrast(ImageChops.difference(gb, gb.transform(gb.size, Image.AFFINE, (1, 0, 1, 0, 1, 1))).convert('L')))
mix = Image.blend(ref, gb, 0.45)
out = Image.new('RGB', (1280 * 2 + 8, 720), (20, 20, 20)); out.paste(mix, (0, 0)); out.paste(gb, (1288, 0))
out.save(sys.argv[3], quality=88)
