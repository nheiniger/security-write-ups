22 - Block Jane
===============
> You intercepted an encryped message by Jane. Can you decrypt it?
> 
> You know that AES was used, and that the following service is receiving such encrypted messages:
> 
> whale.hacking-lab.com 5555
> 
> Find the password and enter it in the Egg-o-Matic below!

When sending data to the service it returns either `ok` or `error`. This with the description and the fact that we have no more information than an encrypted message and this service points to a padding oracle attack. To read more about this attack go to [1], a good explanation with a corresponding example is given at [2] and [3].

Knowing that, one can develop code to take advantage of the oracle or use an existing library. being lazy I chose to use the code published at <https://github.com/mwielgoszewski/python-paddingoracle>. It's well documented and worked for me I only had to modify the example file in `22_padding-oracle.py` as follows:
```python
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
```

Running this code takes a looooong time, probably because of some rate limitation on the server. But in the end it works:
```bash
python 22_padding-oracle.py e343f42604ca58a731adbf10b376ee33aa944926cdf954400d86ee4f6e35774ec510fe5767baba99a3ed28fa26dc99b6c1dadd087e4cee27e45507005276c10fd9c15f27d3481a92f34dd46477f7be3c
DEBUG:PadBuster:Attempting to decrypt "\xe3C\xf4&\x04\xcaX\xa71\xad\xbf\x10\xb3v\xee3\xaa\x94I&\xcd\xf9T@\r\x86\xeeOn5wN\xc5\x10\xfeWg\xba\xba\x99\xa3\xed(\xfa&\xdc\x99\xb6\xc1\xda\xdd\x08~L\xee'\xe4U\x07\x00Rv\xc1\x0f\xd9\xc1_'\xd3H\x1a\x92\xf3M\xd4dw\xf7\xbe<" bytes
DEBUG:PadBuster:Processing block '\xe3C\xf4&\x04\xcaX\xa71\xad\xbf\x10\xb3v\xee3'
DEBUG:root:No padding exception raised on 'ok\x00'

[CUT BY NICOLAS]

INFO:PadBuster:Decrypted block 4: '\n\n\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e'
Decrypted plaintext: e343f42604ca58a731adbf10b376ee33aa944926cdf954400d86ee4f6e35774ec510fe5767baba99a3ed28fa26dc99b6c1dadd087e4cee27e45507005276c10fd9c15f27d3481a92f34dd46477f7be3c => bytearray(b'\x0e\x89\xc9\x02\xbf\xebp\xd3\xb0\x8f\xd86\xf7\xfb~\x08assword is: oracl3in3delphi\n\nSee you soon!\n\nJane\n\n\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e\x0e')
```

So we have our password, oracl3in3delphi and with this we get the egg:
![](./22_egg.png)

## References
\[1\] Padding oracle attack, Wikipedia <https://en.wikipedia.org/wiki/Padding_oracle_attack>  
\[2\] Padding oracle attacks: in depth - SkullSecurity <https://blog.skullsecurity.org/2013/padding-oracle-attacks-in-depth>  
\[3\] A padding oracle example - SkullSecurity <https://blog.skullsecurity.org/2013/a-padding-oracle-example>
