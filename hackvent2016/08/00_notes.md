Day 08: Lost In Encoding
------------------------
The provided files starts with a header that is for yencode (after some googling). I first decoded it using python library for yenc and this simple script:
```python
#!/usr/bin/python2

import yenc

yenc.decode('l0st_1n_7ranslation.fun', 'lost2')
```

The script returns some data but it is not usable. After much tests to decode the output I tried using another tool yEnc32 - only available for Windows by the way :( And this time I got a readable file, `lost_in_translation_2.txt`

This file looks like base64, let's try it using:
```bash
$ cat lost_in_translation_2.txt | base64 -d > lost_in_translation_3.txt
$ cat lost_in_translation_3.txt
<~6Z6g\F`_28+EM%,ASu!h+D#)+@psInDf-\-@;]t$F<GF/CLnVsDL#]0A9f;+DBNM8E+O'3+E2@>B6%EtD.R`1@;^?5D/XH++EV:*DBO"BF_#c3DJ()$EclG:ATJu&DIal/BkM9oDKI"2@;[3)@;BEsF)Po,@W,e&+CT.1AU&0*Ec`FC@;0V$ATBCG/KdK&Bk&8a/g+&#H#7J;A0=ED0fCV"0QV=f0lApj/Mq?dCb7J&0eb1s0JHr~>
```

This looks now like Base85 (Ascii85) and can be decoded using this command:
```bash
$ ascii85 -d lost_in_translation_3.txt
Computer science education cannot make anybody an expert programmer any more than studying brushes and pigment can make somebody an expert painter. - Eric S. Raymond HV16-l0st-1n7r-4nsl-4710-n00b
```

And we have the flag:

> HV16-l0st-1n7r-4nsl-4710-n00b
