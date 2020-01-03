#!/usr/bin/python3

from pwn import *
import re

# parse response and returns the current state
def parse_response(resp):
	p = re.compile('([*XO])')
	# find all occurences and keep only the game where the bot played 
	m = p.findall(resp)[-9:]
	return(m)

# establish connection and pass preamble
c = remote('challenges.hackvent.hacking-lab.com', 1037)
c.recvuntil('enter to start the game')

# start to play with a list of moves that wins against the "AI" every time
while True:
	c.sendline('')
	state = parse_response(str(c.recvuntil('Field:')))
	c.sendline('1')
	state = parse_response(str(c.recvuntil('Field:')))
	c.sendline('9')
	state = parse_response(str(c.recvuntil('Field:')))
	if state == ['X', '*', 'O', '*', 'O', '*', '*', '*', 'X']:
		c.sendline('7')
		state = parse_response(str(c.recvuntil('Field:')))
		c.sendline('4')
		print(c.recvuntil('enter to start again'))
	elif state == ['X', 'O', '*', '*', 'O', '*', '*', '*', 'X']:
		c.sendline('8')
		state = parse_response(str(c.recvuntil('Field:')))
		if state == ['X', 'O', '*', '*', 'O', '*', 'O', 'X', 'X']:
			c.sendline('3')
			state = parse_response(str(c.recvuntil('Field:')))
			if state == ['X', 'O', 'X', '*', 'O', 'O', 'O', 'X', 'X']:
				c.sendline('4')
				print(c.recvuntil('enter to start again'))
			elif state == ['X', 'O', 'X', 'O', 'O', '*', 'O', 'X', 'X']:
				c.sendline('6')
				print(c.recvuntil('enter to start again'))
		elif state == ['X', 'O', 'O', '*', 'O', '*', '*', 'X', 'X']:
			c.sendline('7')
			print(c.recvuntil('enter to start again'))
	elif state == ['X', 'O', 'O', '*', '*', '*', '*', '*', 'X']:
		c.sendline('5')
		print(c.recvuntil('enter to start again'))
	else:
		print('Alternative')
		print(state)
		exit()
