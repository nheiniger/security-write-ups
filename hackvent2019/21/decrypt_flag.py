#!/usr/bin/env python3

import hashlib
import base64
from Crypto.Cipher import AES

pwd = b'santacomesatxmas'
salt = b'TwoHundredFiftySix'
iterations = 256*256*256

enc_flag = base64.b64decode('Hy97Xwv97vpwGn21finVvZj5pK/BvBjscf6vffm1po0=')

key = hashlib.pbkdf2_hmac('sha256', pwd, salt, iterations)
print('Key is {}'.format(key.hex()))

aes = AES.new(key, AES.MODE_ECB)
flag = aes.decrypt(enc_flag)
print(flag)
