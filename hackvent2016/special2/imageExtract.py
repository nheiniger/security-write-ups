#!/usr/bin/python3

import argparse
from PIL import Image, ImagePalette

parser = argparse.ArgumentParser()
parser.add_argument("file", help="The image file on which you want to work.")
args = parser.parse_args()

im = Image.open(args.file)
(width, height) = im.size
if im.format == 'GIF':
	im = im.convert('RGB')
pix = im.load()

im2 = Image.new('RGB', im.size, 'white')
pix2 = im2.load()

x = 0
y = 0
count = 0
colors = []
for x in range(1, width-1):
	for y in range(1, height-1):
		(r, g, b) = pix[x,y]
#		if pix[x,y] != pix[x-1,y] and pix[x,y] != pix[x+1,y] and pix[x,y] != pix[x,y-1] and pix[x,y] != pix[x,y+1]:
		if r != 255 or g != 255 or b != 255:
			colors.append(pix[x,y])
			pix2[x,y] = (0,0,0)
			count += 1
		else:
			pix2[x,y] = (255,255,255)

#im2.save("result.png")

bitstring = ""
bit = 7
for c in colors:
	bitstring += format(c[0], '08b')[bit] + format(c[1], '08b')[bit] + format(c[2], '08b')[bit]

result = ""
array = [bitstring[i:i+8] for i in range(0, len(bitstring), 8)]
for a in array:
	result += format(int(a, 2), '02x')

print(result)
