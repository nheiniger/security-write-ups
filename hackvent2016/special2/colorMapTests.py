#!/usr/bin/python3

from PIL import Image

string = 'ffffffffffff0a3b73a7a7f0f2e9eef4a0a2d0c9cebfdceebea0a2bbf3f2e1eee4a8e9eef4a8bcbea9a9bbf0f2e9eef4a8f0e1e3eba8a2c3aaa2acede1f0fba0a8a4dfabe9eef4a8f2e1eee4a8b0f8c6c6a9a9a9a6b0f8c6c6fdf5eef0e1e3eba8a2c3aaa2aca24fe490a13c37627b5a9d9e43cc55e2c869dbfd9e633af03bb91f52ccb95c40620939e87d9ae3e9ecac91e528f1766e9888ce55a2a9a9aea2dceea2a9bba726267926802dff002d7f26002dff26262673a7a7245fa765653b0460793c60f93a38cc66f80343a0794398f99ab7f99aff039cd6ab9bd7794370f99777793c78eba017fa976ff9963fd46ac2799f1f225af0f99c3784e7e104a9a7f93ff8033cd07aa44f7aa437faa4c7032bc479a97ff452a4f86f370dd9a3ee17df780a156b23566940750e3577f01b76a81ce69129b608a4866e5d178e8227f2794f78fedce9a610cb867aca289f9c325e400fd17b11d5673ba5f06717f7eae4d5100fe80387ff8bb8cdfeee1e8ebd1daf054ee30e79fc1b9d69d846fbcd00fc5ec76d0cc7fcb727e0d3e87c05170ed047db5f69fc0eb1e4a0c4f531f57b549f772c6ec3d72ffcdc236b4e4afcfb9672bb376312cc7bad56f6be37f9d7e4f58a10ffce90f6bfffeacdff4fc41f0fdb9fca9cc8fdff287d44754bb71ef8cc40f9ca67efd529fe0dd4ae864aedbc00ff8780e4f1f78ff2e7fb5c5f25aef7ffff07883a0207d6e267f0a0c11c0116320ce00ba1c1ffffff2e24310f224684a4282e6c816720c887186bfd3164b2a4a1891c9b656cd9b29cc998289970ac6993219698270dd5a8d9e01ac67986400ec4b3f324a98ce44a328d4993638d8f44ebb07469f560b90b1c2f94bbfeeaf52b44950d4542ecc911c345b01b395e016bf0cc4d8e0daabac5d82c2edebc7a19fe74ebab668eb4088bed5d58a76eddac5bbb226e1c562e598462199260fc752dc5b66ee1ee9deb1861b3068547936e40ce2d618e3932a6de7bf8f355c514b9c2fe3c7961e483b703a0758bb9a166b09cf7d2fd1c9a3472bd7dc116134d7135c6bf855fd77ea975b6e5ea6025d6cc9db0a645df35'
array = [string[i:i+6] for i in range(0, len(string), 6)]

colormap = []
for a in array:
	colormap.append((int(a[0:2],16), int(a[2:4], 16), int(a[4:6], 16)))

im = Image.open('MandM.gif')
(width, height) = im.size
if im.format == 'GIF':
	im = im.convert('RGB')
pix = im.load()

x = 0
y = 0
for x in range(width):
	for y in range(height):
		if pix[x,y] in colormap:
			colormap.remove(pix[x,y])

for c in colormap:
	print(format(c[0], '02x') + format(c[1], '02x') + format(c[2], '02x'))

exit()
for bit in range(8):
	bitstring = ""
	for c in colormap:
		bitstring = bitstring + format(c[0], '08b')[bit] + format(c[1], '08b')[bit] + format(c[2], '08b')[bit]
	
	res = ""
	byteArray = [bitstring[i:i+8] for i in range(0, len(bitstring), 8)]
	for b in byteArray:
		res += chr(int(b, 2))
	
	print(res)
