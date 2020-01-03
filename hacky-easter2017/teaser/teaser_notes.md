Hacky-easter teaser notes
=========================

## 01
Read backwards:
Easy, peasy! A2DBM

## 02
Base64:
Piece of cake! ZXGID

## 03
Text in white:
One for free here: ERROR XIZLS

## 04
Analyse script, alert a string:
VYGY6

## 05
MD5 hash crack:
EBQSA

## 06
Morse code:
ONE MORE HERE: JAOMY

## 07
Cesar code:
ETIAM TU BRUTE NVXSI

## 08
Ascii code:
Take this: GY5TF

## 09
bit.ly :)
http://lmgtfy.com/?q=5DFME

## 10
Comment indeed:
<!-- A43JN -->

## 11
Each unicode char is a bit, then to ascii:
CONGRATS! N5XGK

## 12
XOR 2 hex strings:
XOR IS FUN! ON52C

## 13
ROT13:
HERE YOU GO: ZWK4R

## 14
PNG data, image gives string:
AGBTC

## 15
Regexp over string gives:
(FR)(ID)(AY THE THIRTEE)(N)(TH, 4:00 PM)
=> IDEN4

## 16
Ascii85:
This is the last one! DFMFZ

## Final riddle
Assembly of 16 strings is:
> A2DBMZXGIDXIZLSVYGY6EBQSAJAOMYNVXSIGY5TF5DFMEA43JNN5XGKON52CZWK4RAGBTCIDEN4DFMFZ

The string looks like base32 but is not decodable as such (non-ascii character in the result). By trying all the permutations incrementally we can find the final string. To do this we start by base32 decode all combinations of 3 strings among 16 but only if they contain ascii characters exclusively. Then we remove the 3 valid strings from the pool and try allcombinations of 3 strings among 13 and so on until we can form the final string:
> N5XGKIDEN4ZXGIDON52CA43JNVYGY6JAOMYGY5TFEBQSA5DFMEZWK4RAGBTCA2DBMNVXSIDFMFZXIZLS

Which decodes via base32 as:
> one do3s not simply s0lve a tea3er 0f hacky easter
