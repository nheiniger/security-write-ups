#!/usr/bin/python

import itertools
import base64

strings = ['XIZLS', 'NVXSI', 'DFMFZ']

start = 'N5XGKIDEN4ZXGIDON52CA43JNVYGY6JAOMYGY5TFEBQSA5DFMEZWK4RAGBTCA2DBM'

for p in itertools.permutations(strings, 3):
	try:
		print(start+''.join(list(p))[:15], " - ", base64.b32decode(start+''.join(list(p))[:15]).decode())
	except:
		1+1
