#!/usr/bin/python3

f = open('data.txt', 'r')
flag = ""

for line in f:
	(n1, n2, n3) = line.split(',')
	m = int(n1)
	b = int(n2)
	p = int(n3)
	for a in range(255):
		if m == a * 0x1337 * b % p:
			flag = flag + chr(a)

print(flag)
