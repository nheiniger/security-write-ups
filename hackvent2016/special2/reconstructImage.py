#!/usr/bin/python3

from PIL import Image

f = open('bits.txt')
line = f.readline()
im = Image.new('RGB', (291,291), 'white')
pix = im.load()

x = 0
while line:
	print(str(x) + ":" + line)
	y = 0
	for c in line:
		if c == '0':
			print(str(x) + "," + str(y))
			pix[x,y] = (0,0,0)
		y += 1
	line = f.readline()
	print(str(y))
	x += 1

im.save("fromPerl.png")
