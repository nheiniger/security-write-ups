06 - Message to Ken
-------------------
There exist a Barbie typewriter that has builtin "crypto" capabilities. One can find some details about that in [1]. The hint gives the exact subsitution to use (although it's wrong and gives code 2 where code 1 is used).

This is actually a simple substitution cipher with the following substitution table:
```
Clear:  abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ 0123456789
Cipher: icolapxstvybjeruknfhqg;dzw >FAUTCYOLVJDZINQKSEHG<.1PB 523406789-

Clear:  - ' ! " # % & ( ) * , . ¨ / : ; ? @ ^ _ + < = > ¢ £ § €
Cipher: ¨ _ & m @ : " * ( # W M § ^ , ¢ / ? ! ) % X ' R + € £ =
```

When applying the substitution backward one get the following:
```
Fabrgal JaeM Hsa faonah uiff;rnl tf btuxbrffuinhzoroyhitbM Fincta dd
Beloved Ken. The secret password is lipglosspartycocktail. Barbie xx
```

When entering th password inthe egg-o-matic we get the egg:
![](./06/egg06.png)

\[1\]: Barbie™ Typewriter, <http://www.cryptomuseum.com/crypto/mehano/barbie/>
