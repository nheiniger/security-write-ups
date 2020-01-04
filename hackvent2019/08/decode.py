#!/usr/bin/python

visa = 'RPQRSTUVWXYZ[\]^'
flag = 'SlQRUPXWVo\Vuv_n_\\ajjce'

res = ''
i = 0
for c in flag:
    res = res + chr(ord(c)-30-i)
    i = i + 1

print(res)
