Day 11: Crypt-o-Math 2.0
========================
> So you bruteforced last years math lessions? This time you cant escape!
> 
>     c = (a * b) % p
>     c=0x559C8077EE6C7990AF727955B744425D3CC2D4D7D0E46F015C8958B34783
>     p=0x9451A6D9C114898235148F1BC7AA32901DCAE445BC3C08BA6325968F92DB
>     b=0xCDB5E946CB9913616FA257418590EBCACB76FD4840FA90DE0FA78F095873
> 
> find "a" to get your flag.

As the name suggests, his is a crypto problem with modulo arithmetic. We can change the equation into a linear congruence as follows:
```
c = (a * b) % p
0 = (a * b) % p - c % p
0 = (a * b - c) % p
```

Then there exist tools to solve this kind of problems. I used this one <https://www.alpertron.com.ar/QUADMOD.HTM> that actually solves a more complex form but can be adaptedto our purposes. the result is:
```
a = 0x485631372d587444772d30447a4f2d595267422d326232652d55574e7a00
```

Then it's a simple python task to convert this to ascii:
```
>>> import binascii
>>> a = '485631372d587444772d30447a4f2d595267422d326232652d55574e7a00'
>>> binascii.unhexlify(a)
b'HV17-XtDw-0DzO-YRgB-2b2e-UWNz\x00'
```
