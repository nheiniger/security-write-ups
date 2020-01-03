#!/usr/bin/python3

import pexpect
import sys

for i in range(100000, 1000000):
	print(str(i))
	child = pexpect.spawn('perl MandM.gif')
	child.delaybeforesend = None
	child.expect('> ')
	child.sendline(str(i))
	try:
		child.expect('foo')
	except:
		if "HV16" in child.before:
			print(child.before)
			print(str(child))
			exit()
