#!/usr/bin/python3

import sys
import binascii

# assign argument to var70
var70 = sys.argv[1]

# initialize variables (one from hex and one from decimal)
var20 = 0xF66EB887F2B8A620FD03C7D0633791CB4804739CE7FE001C81E6E02783737CA21DB2A0D8AF2D10B200006D10737A0872C667AD142F90407132EFABF8E5D6BD51
var40 = 65537

# import argument into var50
var50 = int.from_bytes(var70.encode(), byteorder='big')

# compare values and fail if argument is bigger
if var50 > var20:
	print('fail, arg is too long')
	exit()

# modular exponentiation
var60 = pow(var50, var40, var20)

print('Crypted: ' + hex(var60)[2:].upper())
