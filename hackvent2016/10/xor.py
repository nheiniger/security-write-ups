cipher = 0x4B5234302A5E643F7221436468583C772460423B477F547B362A2C5457
key = 0x030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f
plain = cipher ^ key

flag=""
for i in range(29):
	b = plain & 0xff
	flag = chr(b) + flag
	plain = plain >> 8

print(flag)
