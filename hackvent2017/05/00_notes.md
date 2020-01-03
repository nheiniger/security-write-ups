Day 05: Only one hint
=====================
> *OK, 2nd hint: Its XOR not MOD*
> 
> Here is your flag:
> 
>     0x69355f71
>     0xc2c8c11c
>     0xdf45873c
>     0x9d26aaff
>     0xb1b827f4
>     0x97d1acf4
> 
> and the one and only hint:
> 
>     0xFE8F9017 XOR 0x13371337

This time the hint was misleading but in the end, with the new hint, searching with google lead to CRC32. It was then a matter of finding a tool to revers a CRC32 and give the 4 bytes of the flag for each hex number that were given.

I used `crc32.py` available at <https://github.com/theonlypwner/crc32> to reverse the CRC32 as follows:
```
~/t/crc32 ❯❯❯ python crc32.py reverse 0x69355f71 | head -n 1
4 bytes: {0x48, 0x56, 0x31, 0x37}
~/t/crc32 ❯❯❯ python crc32.py reverse 0xc2c8c11c | head -n 1
4 bytes: {0x37, 0x70, 0x4b, 0x73}
~/t/crc32 ❯❯❯ python crc32.py reverse 0xdf45873c | head -n 1
4 bytes: {0x77, 0x68, 0x79, 0x7a}
~/t/crc32 ❯❯❯ python crc32.py reverse 0x9d26aaff | head -n 1
4 bytes: {0x6f, 0x36, 0x77, 0x46}
~/t/crc32 ❯❯❯ python crc32.py reverse 0xb1b827f4 | head -n 1
4 bytes: {0x68, 0x34, 0x72, 0x70}
~/t/crc32 ❯❯❯ python crc32.py reverse 0x97d1acf4 | head -n 1
4 bytes: {0x51, 0x6c, 0x74, 0x36}
```

Converting the bytes to characters and adding the `-` in between gives the flag:
```
HV17-7pKs-whyz-o6wF-h4rp-Qlt6
```
