Day 23: From another time
-------------------------
For this challenge we receive a C64 program, SANTACLS.PRG. When running it using VICE we have a nice 8-bit music with a message:
```
HV16-HOHO-HOHO-HOHO-HOHO-HOHO
 ... NOT THE RIGHT FLAG ...


            MEAN OLD SANTA CLAUS
```

One could disassemble the program and try to reverse it but I found a shorter path. While running the program I saved a snapshot from VICE with "Snapshot -> Save snapshot image..." as `memory.vsf` I could then use the strings program and the flag is displayed right there:
```bash
$ strings memory.vsf
[CUT BY TROLLI101]
 2064
x >	 f	 
HV16-siZy-UzxY-u7qV-nr3D-FSk4      
            ... 
[CUT BY TROLLI101]
```

The flag is:

> HV16-siZy-UzxY-u7qV-nr3D-FSk4
