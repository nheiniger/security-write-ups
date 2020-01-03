# -*- coding: utf-8 -*-
from paddingoracle import BadPaddingException, PaddingOracle
from base64 import b64encode, b64decode
from urllib import quote, unquote
import requests
import socket
import time
import binascii

HOST = 'whale.hacking-lab.com'
PORT = 5555
BUFFER_SIZE = 1024

class PadBuster(PaddingOracle):
    def __init__(self, **kwargs):
        super(PadBuster, self).__init__(**kwargs)
        self.wait = kwargs.get('wait', 2.0)

    def oracle(self, data, **kwargs):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(data)
        response = s.recv(BUFFER_SIZE)
        s.close()

        if b'ok' in response:
            logging.debug('No padding exception raised on %r', data)
        elif b'error' in response:
            raise BadPaddingException
        else:
            print('=== ALERT === This should never happen !')


if __name__ == '__main__':
    import logging
    import sys

    if not sys.argv[1:]:
        print 'Usage: %s <ciphertext (hex)>' % (sys.argv[0], )
        sys.exit(1)

    logging.basicConfig(level=logging.DEBUG)

    ciphertext = binascii.unhexlify(sys.argv[1])

    padbuster = PadBuster()

    plaintext = padbuster.decrypt(ciphertext, block_size=16, iv=bytearray(16))

    print('Decrypted plaintext: %s => %r' % (sys.argv[1], plaintext))
