#!/usr/bin/python3

import pexpect
import sys

for i in range(111110, 111113):
	print(str(i))
	child = pexpect.spawn('perl MandM.gif')
	child.delaybeforesend = None
	child.expect('> ')
	child.sendline(str(i))
	try:
		child.expect('')
		print(child.before)
	except:
		print("Exception")
