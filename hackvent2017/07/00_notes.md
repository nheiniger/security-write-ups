Day 07: i know ...
==================
> *... what you did last xmas*
> 
> We were able to steal a file from santas computer. We are sure, he prepared a gift and there are traces for it in this file.
> 
> Please help us to recover it:

In this challenge we are given a file called `SANTA.FILE`, let's try to know what kind of file it is:
```
~/D/c/07 ❯❯❯ file SANTA.FILE
SANTA.FILE: Zip archive data, at least v1.0 to extract
```

OK, zip file, this unzip to a `SANTA.IMA` file, let's check the file type again:
```
~/D/c/07 ❯❯❯ file SANTA.IMA
SANTA.IMA: DOS/MBR boot sector, code offset 0x58+2, OEM-ID "WINIMAGE", sectors/cluster 4, root entries 16, sectors 3360 (volumes <=32 MB), sectors/FAT 3, sectors/track 21, serial number 0x2b523d5, label: "           ", FAT (12 bit), followed by FAT
```

Not so easy now... I don't want to find a way of mounting this image so let's first try with `strings`:
```
~/D/c/07 ❯❯❯ strings SANTA.IMA | grep HV17
Y*C:\Hackvent\HV17-UCyz-0yEU-d90O-vSqS-Sd64.exe
```

And I'm lucky, this is the correct flag:
```
HV17-UCyz-0yEU-d90O-vSqS-Sd64
```
