#! /usr/bin/python3

import binascii

startOfGameFile = binascii.unhexlify('ce55954e38c589a51b6f5e25d21d2a2b5e7b39148ed0f0f8f8a5')
updateFile = 'PS4UPDATE.PUP'

local_4e0 = bytearray(startOfGameFile)
lVar8 = 0x1337
f = open(updateFile, 'rb')
while True:
    f.seek(lVar8, 0)
    local_4c0 = f.read(0x1a)
    lVar9 = 0
    while True:
        local_4e0[lVar9] = local_4e0[lVar9] ^ local_4c0[lVar9]
        lVar9 += 1
        if lVar9 == 0x1a:
            break
    lVar8 += 0x1337
    if lVar8 == 0x1714908:
        break

f.close()
print(local_4e0.decode())
