#!/usr/bin/python2

import re
from pwn import *

r = remote('hackyeaster.hacking-lab.com', 8888)

r.recvline()
r.sendline('y')
r.recvline()
while True:
	h = r.recvline().strip()
	print('Hash is ' + h)
	print('Starting hashcat')
	try:
		hashcat = process('hashcat --force --potfile-disable --weak=0 -m 1400 ' + h + ' rockyou.txt', shell=True)
		print('Going to sleep for 9.5s')
		sleep(9.5)
		line = hashcat.recvline_regex('[0-9a-f]{64}:(.*)').strip()
		m = re.search(r'[0-9a-f]{64}:(.*)$', line)
		if m:
			pwd = m.group(1)
			print('Hash cracked: ' + pwd)
			r.sendline(pwd)
		else:
			print('FAIL')
			r.sendline('fail')
	except EOFError:
		r.sendline('fail')

	print(r.recvline().strip())
	print(r.recvline().strip())
	print(r.recvline().strip())
	print(r.recvline().strip())
	print(r.recvline().strip())
