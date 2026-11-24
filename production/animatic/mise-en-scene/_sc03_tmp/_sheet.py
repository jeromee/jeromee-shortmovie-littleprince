from PIL import Image, ImageDraw
import glob
fs=sorted(glob.glob("test_*.png"))
W,H=480,270; cols=4; rows=(len(fs)+cols-1)//cols
sheet=Image.new("RGB",(W*cols,(H+22)*rows),(20,20,24)); d=ImageDraw.Draw(sheet)
for i,f in enumerate(fs):
    im=Image.open(f).convert("RGB").resize((W,H)); x=(i%cols)*W; y=(i//cols)*(H+22)
    sheet.paste(im,(x,y+22)); d.text((x+6,y+5),f[5:-4],fill=(0,220,220))
sheet.save("_sheet_tests.jpg",quality=88)
vs=sorted(glob.glob("verif_*.png"))
s2=Image.new("RGB",(540*3,540*2),(0,0,0)); d=ImageDraw.Draw(s2)
for i,f in enumerate(vs):
    im=Image.open(f).convert("RGB").resize((540,540)); s2.paste(im,((i%3)*540,(i//3)*540)); d.text(((i%3)*540+8,(i//3)*540+8),f,fill=(255,255,255))
s2.save("_sheet_verif.jpg",quality=88)
