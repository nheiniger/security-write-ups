#!/usr/bin/python3

import re

f = open("original.txt")
leet = f.read()
#print(leet)

# complex chars
leet = re.sub('\|\)', 'D', leet)
leet = re.sub('\|-\|', 'H', leet)
leet = re.sub(r'/v\\', 'M', leet)
leet = re.sub('\|/\|', 'N', leet)
leet = re.sub('\|_\|', 'U', leet)
leet = re.sub(r'\\\'', 'V', leet)
leet = re.sub(r'\\/\\/', 'W', leet)
leet = re.sub('><', 'X', leet)
leet = re.sub('`/', 'Y', leet)
leet = re.sub('\|\*', 'P', leet)
leet = re.sub('\|=', 'F', leet)
leet = re.sub('\|2', 'R', leet)
leet = re.sub('\|<', 'K', leet)
leet = re.sub('_\|', 'J', leet)

# simple chars
leet = re.sub('4', 'A', leet)
leet = re.sub('3', 'E', leet)
leet = re.sub('9', 'G', leet)
leet = re.sub('\(', 'C', leet)
leet = re.sub('£', 'L', leet)
leet = re.sub('!', 'I', leet)
leet = re.sub('7', 'T', leet)
leet = re.sub('5', 'S', leet)
leet = re.sub('0', 'O', leet)
leet = re.sub('8', 'B', leet)

# to binary
leet = re.sub('[A-Z]', '1', leet)
leet = re.sub('[a-z]', '0', leet)

# clean
leet = re.sub('[^01]', '', leet)
#print(leet)

bins = [leet[i:i+8] for i in range(0, len(leet), 8)]
#print(bins)

final = ""
for b in bins:
	final += chr(int(b, 2))
print(final)
