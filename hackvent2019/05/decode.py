#!/usr/bin/python

from PIL import Image

im = Image.open('barcode.png')
pix = im.load()

width = im.width

rgb_values = []

# initialize with first pixel
rgb_values.append(pix[0,30])

for x in range(width):
    if rgb_values[-1] != pix[x,30] and pix[x,30] != (255, 255, 255):
        rgb_values.append(pix[x,30])

# remove first white pixel
del rgb_values[0]

b = ""
for p in rgb_values:
    b += chr(p[2])

print(b)
