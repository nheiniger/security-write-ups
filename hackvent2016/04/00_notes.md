Day 04: Language Of Us
----------------------
The given text is shown in leet speak. We can recognize the wikipedia article about steganography and thus we look for some kind of stegano. We see that some characters are replaced by their leet version while others are not.

With a python script we replace all leet characters with 1 and all normal characters by 0. When removing all the rest we obtain a big binary blob. We can then split the blob into 8 char strings, convert these strings to decimal and then to characters and we obtain a string composed of dashes and in the middle lies the flag.

The python script is as follows:
```python
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
```

The flag is:

> HV16-O7oI-W34j-BJH7-cSvk-e5Hz
