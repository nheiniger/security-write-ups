Day 10: I want to play a Game
-----------------------------
The file we are given is a playstation executable:
```bash
$ file HV16.EXE
HV16.EXE: Sony Playstation executable PC=0x8001626c, .text=[0x80010000,0x8800], Stack=0x801ffff0, (Japan area)
```

When running it into an emulator we get a nice green screen asking us to decrypt the flag. And looking at the file in an hex editor we notice the following section:
```
00006C60  08 00 40 01  3F 00 09 24   00 00 00 00  64 65 63 72      ..@.?..$....decr
00006C70  79 70 74 20  74 68 65 20   66 6C 61 67  20 79 6F 75      ypt the flag you
00006C80  20 6E 30 30  62 00 00 00   4B 52 34 30  2A 5E 64 3F       n00b...KR40*^d?
00006C90  72 21 43 64  68 58 3C 77   24 60 42 3B  47 7F 54 7B      r!CdhX<w$`B;G.T{
00006CA0  36 2A 2C 54  57 00 00 00   50 73 08 00  00 00 46 00      6*,TW...Ps....F.
```

We can see the string that asks us to decrypt the flag and then another string starting with KR40 and ending with TW. This string is exactly 29 bytes long, like a flag :)

We use this as a ciphertext: `0x4B5234302A5E643F7221436468583C772460423B477F547B362A2C5457`

We know that the flag starts with HV16- so plaintext is: `0x485631362d????????2d????????2d????????2d????????2d????????`

If we XOR the start of plaintext and ciphertext we get:
```
    0x4B5234302A
XOR 0x485631362d
  = 0x0304050607
```

We guess that the key could go on that way with `08090a0b...` and thus the full key would be: `0x030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f`

We can make the xor with this python script:
```python
cipher = 0x4B5234302A5E643F7221436468583C772460423B477F547B362A2C5457
key = 0x030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
plain = cipher ^ key

flag=""
for i in range(29):
	b = plain & 0xff
	flag = chr(b) + flag
	plain = plain >> 8

print(flag)
```

And we get the flag:

> HV16-Vm5y-NjgH-e7tW-PgMa-61JH
