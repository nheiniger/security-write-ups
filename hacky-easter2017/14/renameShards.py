#!/usr/bin/python3

import glob
import os
import re

os.chdir('shards')
for filename in glob.glob('*.png'):
	(foo, bar, x, sugus, y) = re.split('_', filename)
	y = y[:-4]
	os.rename(filename, x + '_' + y + '.png')
