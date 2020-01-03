#!/usr/bin/python3

sdrData = '1001101001101010100110011001011010100101101010011010010110010110101001100101100110100101101010011010010110100101101001011010010110100101100101011010011001011001100110011010011010010110101010011001011010011010100101100110100110100110010110011001011001010101100110011001010110010110101010011001010110100110101001100101100110010110100101011001011010101001100101100101100110010110100110011010011001011001101001011010100110100101101001011010010110100101101001011001010110101010011001'
array = [sdrData[i:i+2] for i in range(0, len(sdrData), 2)]

bitString = ""
for a in array:
	if a == '01':
		bitString += "1"
	elif a == '10':
		bitString += "0"
	else:
		print("Error!")
		exit()

chars = [chr(int(bitString[i:i+8], 2)) for i in range(0, len(bitString), 8)]
flag = "".join(chars)
print(flag)