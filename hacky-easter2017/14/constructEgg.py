#!/usr/bin/python3

import os
from PIL import Image

os.chdir('shards')
width = range(40)
height = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N']


result = Image.new("RGB", (480, 480), "white")

for x in width:
	yi = 0
	for y in height:
		im = Image.open(y + '_' + str(x) + '.png')
		result.paste(im, (x*12, yi*12))
		yi += 1

result.save('../egg14.png')
