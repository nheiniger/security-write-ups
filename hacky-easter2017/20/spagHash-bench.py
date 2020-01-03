#!/usr/bin/python

from sha512 import sha512
import datetime

assert (sha512('a').hexdigest() == '2552d46012e2cee9c48f2238b10ec560'), 'Precondition error'
assert (sha512('b').hexdigest() == '580b7ef5583b650e55788477165ecbcf'), 'Precondition error'
assert (sha512('c').hexdigest() == 'da1b8782a23ed2c5d041cc218b952631'), 'Precondition error'
assert (sha512('d').hexdigest() == 'ad50cdc041f4001d08766c78548a54bc'), 'Precondition error'

hashes = ['2552d46012e2cee9c48f2238b10ec560', 'ff17891414f7d15aa4719689c44ea039', 'ff17891414f7d15aa4719689c44ea039', '6ad211c3f933df6e5569adf21d261637']

wordlist = open('wordlists/crackstation-human-only.txt')
counter = 0
for line in wordlist:
	counter += 1
	if counter % 10000 == 0:
		print(counter)
	guess = line.strip("\n".lower())
	hash = sha512(guess).hexdigest()
	if hash in hashes:
		print("[=] " + str(datetime.datetime.now()) + " " + hash + " => " + guess)
