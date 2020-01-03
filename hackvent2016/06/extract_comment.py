#!/usr/bin/python3

import zipfile
from PIL import Image

im = Image.new("RGB", (25,25))
pix = im.load()

x = 0
y = 0

zf = zipfile.ZipFile('holiday.zip', 'r')
for info in zf.infolist():
	y = 0
	for c in info.comment:
		if c == 32:
			pix[x,y] = (0,0,0)
			y += 1
		elif c == 9:
			pix[x,y] = (255,255,255)
			y += 1
	x += 1

im.save("qr.png", "PNG")
