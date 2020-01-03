#!/usr/bin/python3

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("bytes", help="The bytes that must be converted.")
args = parser.parse_args()

array = [args.bytes[i:i+8] for i in range(0, len(args.bytes), 8)]
string = ""
for a in array:
	a0 = a[0:2]
	a1 = a[2:4]
	a2 = a[4:6]
	a3 = a[6:8]
	string = string + chr(int(a3, 16)) + chr(int(a2, 16)) + chr(int(a1, 16)) + chr(int(a0, 16))

print(string)
