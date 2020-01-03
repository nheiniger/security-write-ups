#!/usr/bin/python3

import hashlib
value = 'genesis'

for i in range(100000, 0, -1):
    concat = (value + str(i)).encode()
    value = hashlib.sha1(concat).hexdigest()

print(value)
