#!/usr/bin/python3

from json import load, loads
from gzip import decompress
from base64 import b64decode
from itertools import cycle

def peel_list(l, count):
	return([peel_layer(layer, count) for layer in l])

# recursively decode layers
def peel_layer(layer, count):
	op = layer['op']
	print('Decoding layer {} with operator {}.'.format(count, op))
	if op == 'map':
		# map is a simple character substitution, create the mapping and apply it
		subst = dict(zip([c for c in layer['mapFrom']], [c for c in layer['mapTo']]))
		result = ''.join([subst[c] for c in layer['content']])
		return(peel_list(loads(result), count+1))
	elif op == 'gzip':
		# gzip encoded data, just decode it
		result = decompress(b64decode(layer['content']))
		return(peel_list(loads(result), count+1))
	elif op == 'b64':
		# just decode b64 data
		result = b64decode(layer['content'])
		return(peel_list(loads(result), count+1))
	elif op == 'nul':
		# nothing to do, get content
		result = layer['content']
		return(peel_list(loads(result), count+1))
	elif op == 'xor':
		# apply xor on content and a repetition of the mask
		result = bytes(b1^b2 for b1, b2 in zip(b64decode(layer['content']), cycle(b64decode(layer['mask']))))
		return(peel_list(loads(result), count+1))
	elif op == 'rev':
		# reverse the content using extended slice
		result = layer['content'][::-1]
		return(peel_list(loads(result), count+1))
	
	return(layer)	

# load the JSON data from the file
def load_onion():
	f = open('jsonion.json', 'r')
	onion = load(f)
	f.close()
	return onion

if __name__ == "__main__":
	# load data
	onion = load_onion()

	# peel recursively
	result = peel_list(onion, 0)
	print(result)
