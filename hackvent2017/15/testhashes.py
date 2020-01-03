#!/usr/bin/python3

import base64
import hashlib

md5 = hashlib.md5()
sha1 = hashlib.sha1()
sha224 = hashlib.sha224()
sha256 = hashlib.sha256()
sha384 = hashlib.sha384()
sha512 = hashlib.sha512()

f = open('dannies.csv', 'r')
for line in f:
	md5.update(line.encode('utf-8'))
	print(md5.hexdigest())
	sha1.update(line.encode('utf-8'))
	print(sha1.hexdigest())
	sha224.update(line.encode('utf-8'))
	print(sha224.hexdigest())
	sha256.update(line.encode('utf-8'))
	print(sha256.hexdigest())
	sha384.update(line.encode('utf-8'))
	print(sha384.hexdigest())
	sha512.update(line.encode('utf-8'))
	print(sha512.hexdigest())

f.close()
