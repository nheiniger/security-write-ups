#!/usr/bin/python

from PIL import Image

im = Image.open('thread.png')
pix = im.load()

width = 17
height = 14500 / width

im2 = Image.new('RGBA', (width, height), 'white')
pix2 = im2.load()

for x in range(width):
	for y in range(height):
		pix2[x,y] = pix[width*y + x, 1]

im2.save('step2.png')

w3 = 29
h3 = height / w3

im3 = Image.new('RGBA', (w3, h3), 'white')
pix3 = im3.load()

for x in range(w3):
	for y in range(h3):
		pix3[x,y] = pix2[0, w3*y + x]

im3.save('step3.png')
