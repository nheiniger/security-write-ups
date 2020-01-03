Day 23: only perl can parse Perl
================================
> ... but there is always one more way to approach things!
> 
> (in doubt, use perl5.10+ on \*nix)

OK, some perl, when executing it it asks for a password and output some garbage and asks if we are happy now. Let's use some deobfuscation Perl tool:
```
$ perl -MO=Deparse onlyperl.pl > deparsed.pl
```

This is not much better but we can now use perl debugger with `perl -d deparsed.pl`. While browsing through the execution of this program we get through this line:
```
;print("Password:\\n");@a=unpack("C*",$,);@b=unpack("C*",$X);@c=unpack("C*",scalar <>);print(chr(($b[$_]-$a[$_]+$c[$_%8]+0x100)&0xFF)) for(0..$#b);print "\\nDecryption done, are you happy now?\\n"
```

Still with perl debugger we can show the values of `@a` and `@b` after the unpack and `@c` is our password:
```
a = [187, 0, 0, 128, 183, ... ]
b = [147, 38, 197, 62, 125, ... ]
plain = 'HV17-'
```

Assuming that the plaintext starts with HV17- we can compute the first 5 letters of the password with something like:
```
c[i] = chr((plain[i] - b[i] + a[i] + 256) % 156)
```

And we get the first chars of the password, `p0lyg`. Trying to decrypt with this password gives something almost readable:
```
~/D/c/23 ❯❯❯ perl deparsed.pl
Password:
p0lyg
HV17-��s-is-
             -what�
�u-are���oking���r
Are�
�u sur�hat o
�� shel      � perl���n par��Perl?���croso�s ye 
�even n ��w /us��in/pe��

Decryption done, are you happy now?
```

With some guessing on the word I came up with the full password, `p0lyglot` that hints at the next step, just like the decrypted text:
```
~/D/c/23 ❯❯❯ perl deparsed.pl
Password:
p0lyglot
HV17-this-is-not-what-you-are-looking-for
Are you sure that only perl can parse Perl?
Microsoft's ye old shell does not even know /usr/bin/perl.

Decryption done, are you happy now?
```

OK, following the hint we can now load the program in a DOS emulator and it runs. I used freeDOS because of the integrated DEBUG program. Now it asks for the perl password and if you give it it also asks for a "DOS code". It's time for some reversing.

In DEBUG we see that the program XORs itself with 0x4d, this is presented as follows in IDA:
```
seg000:010E loc_1010E:                              ; CODE XREF: seg000:0118j
seg000:010E                 xor     byte ptr [bx+11Ah], 4Dh
seg000:0113                 inc     bx
seg000:0114                 cmp     bx, 30Eh
seg000:0118                 jl      short loc_1010E
```

We can do that in IDA using an IDC script file as explained in <https://www.hex-rays.com/products/ida/support/tutorials/idc/decrypt.shtml>. Let's do that with the values `decrypt(0x11a,0x30e,0x4d);` to get the code.

Then we see in the assembler code and with some debugging that the length of the password must be more than 5 characters. Let's assume, as before that we need to get HV17- and start with AAAAA as a DOS code. This gives something of the correct length and includes already the dashes in the right position, encouraging.

Now by fiddling with the password and an ASCII table we can determin that the DOS code is `S4n7A` once this is given as input to the program, the flag is returned:
```
D:\>onlyperl.com
>> perl password: p0lyglot
>> DOS code: S4n7A
HV17-Ovze-IUGF-W2xs-x2uE-pVRU
```
