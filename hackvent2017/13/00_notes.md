Day 13: muffin_asm
==================
> *As M. said, kind of a different architecture!*
> 
> ohai \o/
> 
> How about some custom asm to obsfucate the codez?

Here we get a python file that implements some kind of assembly with an interpreter, when run we have the following results:
```bash
~/D/c/13 ❯❯❯ python muffin_asm.py
[ muffin asm ]
muffinx: Did you ever codez asm?
<< flag_getter v1.0 >>
ohai, gimmeh flag: test
[-] nope!
```

The script asks for the flag and if it is not correct returns an error. Since I don't want to deal with the assembly code, I've chosen another path. I assume that at some point the `_cmp` or `_cmpv` function must be used to compare the input with the actual flag. After some tests I came up with the following alternative definition of the `_cmp` function:
```python
def _cmp(r1, r2):
        f[0] = (r[r1] == r[r2])
        if r[r1] != r[r2]:
                print 'You gave '+chr(r[r1])
                print 'I want '+chr(r[r2])
```

This will show the input and expected result for the current character comparison. Then it is only a matter of rebuilding the flag character by character:
```bash
~/D/c/13 ❯❯❯ python muffin_asm.py
[ muffin asm ]
muffinx: Did you ever codez asm?
<< flag_getter v1.0 >>
ohai, gimmeh flag: HV17-?
You gave ?
I want m
[-] nope!
```

OK, we need to add `m` after `HV17-` Let's go on for a new character:
```bash
~/D/c/13 ❯❯❯ python muffin_asm.py
[ muffin asm ]
muffinx: Did you ever codez asm?
<< flag_getter v1.0 >>
ohai, gimmeh flag: HV17-m?
You gave ?
I want U
[-] nope!
```

And so on until we get the full flag:
```
~/D/c/13 ❯❯❯ python muffin_asm.py
[ muffin asm ]
muffinx: Did you ever codez asm?
<< flag_getter v1.0 >>
ohai, gimmeh flag: HV17-mUff!n-4sm-!s-cr4zY
[+] valid! by muffinx :D if you liked the challenge, troll me @ twitter.com/muffiniks =D
```
