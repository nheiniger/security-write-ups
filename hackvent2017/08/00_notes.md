Day 08: True 1337s
==================
> *... can read this instantly*
> 
> I found this obfuscated code on a public FTP-Server. But I don't understand what it's doing...

This time it looks like some kind of program. Given the creator of the program and seing the code we may as well try with python:
```
~/D/c/08 ❯❯❯ python3 True.1337
?foo
```

OK, looks like the program runs and asks for some input. Let's try to understand what it wants. To deobfuscate this I started with the first part, `exec(many Truths)`. One can simply take this part, replace the `exec` by a `print` and run it through python to get the following output:
```
A=chr;__1337=exec;SANTA=input;FUN=print
def _1337(B):return A(B//1337)
```

Knowing this, we notice that the second part starts with `__1337(`, so let's apply this trick again, replace the `__1337` by a `print` in the original file and execute the whole modified file to get:
```
C=SANTA("?")
if C=="1787569":FUN(''.join(chr(ord(a) ^ ord(b)) for a,b in zip("{gMZF_M
                                                                           C_X
                                                                                \ERF[X","31415926535897932384626433832")))
```

Now the behavior is kind of obvious, if the input is 1787569, print something. Then let's run the original file again and provide the expected input to get the flag:
```
~/D/c/08 ❯❯❯ python3 True.1337
?1787569
HV17-th1s-ju5t-l1k3-j5sf-uck!
```
