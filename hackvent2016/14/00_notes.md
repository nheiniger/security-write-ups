Day 14: Radio War Game
----------------------
An awesome post was written by my favorite CEO on the blog of the best company in the world (yes, I work there :D), [1] This shows some basics for RTL-SDR.

Using inspectrum we visualize the signal and see a list of morse-code like signals. We use OOK and interprete no signal as 0 and signal on as 1 which would give something like (omitting the first sequence of 010101...):
```
100110100110101010011001100101101010010110101001101001011001011010100110
010110011010010110101001101001011010010110100101101001011010010110010101
101001100101100110011001101001101001011010101001100101101001101010010110
011010011010011001011001100101100101010110011001100101011001011010101001
100101011010011010100110010110011001011010010101100101101010100110010110
010110011001011010011001101001100101100110100101101010011010010110100101
1010010110100101101001011001010110101010011001
```

This could probably have been done using GNU radio but I'm not proficient enough with the tool. So after one hour of fiddling with thresholds, throttle and scpoe sink I made it by hand! With the challenge description we are hinted at manchester coding (up flank is a 1, down flank is a 0). I wrote the following python script to decode the sequence.
```python
#!/usr/bin/python3

sdrData = '100110100110101010011001100101101010010110101001101001011001'
+ '01101010011001011001101001011010100110100101101001011010010110100101'
+ '10100101100101011010011001011001100110011010011010010110101010011001'
+ '01101001101010010110011010011010011001011001100101100101010110011001'
+ '10010101100101101010100110010101101001101010011001011001100101101001'
+ '01011001011010101001100101100101100110010110100110011010011001011001'
+ '10100101101010011010010110100101101001011010010110100101100101011010'
+ '1010011001'
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
```

And when running it we get the flag:

> HV16-1337-Radi-oWar-game-1337

\[1\] Software Defined Radio (SDR) and Decoding On-off Keying (OOK), <https://blog.compass-security.com/2016/09/software-defied-radio-sdr-and-decoding-on-off-keying-ook/>
