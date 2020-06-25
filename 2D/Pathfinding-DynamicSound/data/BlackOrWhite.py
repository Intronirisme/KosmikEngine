from PIL import Image

img = Image.open("MapPathfinding.png").convert("RGB")
data = img.getdata()
NewData = []
for pix in data:
    if pix != (255,255,255):
        NewData.append((0,0,0))
    else:
        NewData.append((255,255,255))
img.putdata(NewData)
img.save("mapPathfindingNoirEtBlanc.png", format="png")
