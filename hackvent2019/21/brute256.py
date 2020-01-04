#!/usr/bin/env python3

from fastecdsa import curve, ecdsa, keys
from hashlib import sha256
import argparse

# provided in the challenge description
expected_x = 0xc58966d17da18c7f019c881e187c608fcb5010ef36fba4a199e7b382a088072f
expected_y = 0xd91b949eaf992c464d3e0d09c45b173b121d53097a9d47c25220c0b4beb943c

def test_pwd(pwd):
    # private key is just a sha256 of the password
    private_key = int(sha256(bytes(pwd, 'utf-8')).hexdigest(), 16)
    
    # compute the public key from the private key
    public_key = keys.get_public_key(private_key, curve.P256)

    # checks if we found the correct password and exits
    if public_key.x == expected_x and public_key.y == expected_y:
        print('Great success, password is: {}'.format(pwd))
        exit(1)
    
def brute(wordlist):
    f = open(wordlist, 'r')
    pwd = f.readline()[:-1]
    test_pwd(pwd)
    while pwd:
        # the [:-1] is to get rid of the newline at the end of the password
        pwd = f.readline()[:-1]
        test_pwd(pwd)
    
    print('Brute force ended, better luck next time :(')
    f.close()
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Brute force this 256 thingy password.')
    parser.add_argument('wordlist')
    args = parser.parse_args()
    brute(args.wordlist)
