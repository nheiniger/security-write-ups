#!/usr/bin/python

from sha512 import sha512
import datetime

assert (sha512('a').hexdigest() == '2552d46012e2cee9c48f2238b10ec560'), 'Precondition error'
assert (sha512('b').hexdigest() == '580b7ef5583b650e55788477165ecbcf'), 'Precondition error'
assert (sha512('c').hexdigest() == 'da1b8782a23ed2c5d041cc218b952631'), 'Precondition error'
assert (sha512('d').hexdigest() == 'ad50cdc041f4001d08766c78548a54bc'), 'Precondition error'

hashes = ['87017a3ffc7bdd5dc5d5c9c348ca21c5', 'ff17891414f7d15aa4719689c44ea039', '5b9ea4569ad68b85c7230321ecda3780']

wordlist = open('wordlists/crackstation-human-only.txt')
for line in wordlist:
	guess = line.strip("\n".lower())
	hash = sha512(guess).hexdigest()
	if hash in hashes:
		print("[=] " + str(datetime.datetime.now()) + " " + hash + " => " + guess)
