15 - Manila greetings
=====================
> Randy Waterhouse receives a package from his friend Enoch Root containing a deck of cards and a letter:
> 
> Dear Randy,
> 
> even though our stay in Manila was not very pleasant, I fondly think of our discussions there:
> 
> GTIFL RVLEJ TAVEY ULDJO KCCOK P
> Wishing you happy Easter
> 
> Enoch
> 
> Decrypt the message and enter the password in the Egg-o-Matic below. Uppercase only!

Additionally we get a `deck.txt` file with the following content:
```
d8
s3
d7
d3
c2
s5
da
c6
s7
d6
jr
dk
hq
sj
cj
h7
h3
h9
s9
s8
c9
sa
h4
c8
c3
hk
ha
s6
h6
s10
sk
ca
d10
dq
cq
jb
sq
s4
d9
s2
c5
hj
h10
c4
c10
d5
h8
h2
d2
dj
c7
ck
h5
d4
```

The hints point to the Pontifex or Solitaire cipher, designed by Bruce Schneier. Once we know that it's only a matter of finding a tool to decrypt the message. I used <https://ermarian.net/services/encryption/solitaire> with the following parameters:
```
Ciphertext:
GTIFL RVLEJ TAVEY ULDJO KCCOK P

Key as cards:
8d 3s 7d 3d 2c 5s Ad 6c 7s 6d A Kd Qh Js Jc 7h 3h 9h 9s 8s 9c As 4h 8c 3c Kh Ah 6s 6h Ts Ks Ac Td Qd Qc B Qs 4s 9d 2s 5c Jh Th 4c Tc 5d 8h 2h 2d Jd  7c Kc 5h 4d
```

Which returns:
```
THEPA SSWOR DISCR YPTON OMICO N
```

Thus the password is CRYPTONOMICON and this validates to get the egg:
![](./15_egg.png)
