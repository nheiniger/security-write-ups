#!/usr/bin/python

import os
from PIL import Image

os.chdir('frames')
width = 28
height = 4172 / width

result = Image.new('RGB', (width*2, height*2), 'white')

for i in range(4172):
    x = i % width
    y = (i - x) / width
    im = Image.open('disco2-' + str(i) + '.png')
    result.paste(im, (x*2, y*2))

result.save('../result.png')
