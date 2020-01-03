Day 09: Illegal Prime Number
----------------------------
We get this big number that has nothing to do with a prime. When converting it to hexadecimal we have the following:
0x504b0304140009000800910a83495435eceb2b0000001d00000008000000466c61672e
747874567168e0247901d8bae9376014e1dba33d60231a36996b43e1f94d8fc0f9fa53e9
dd803ecdae6d5f164db2504b07085435eceb2b0000001d000000504b01021f0014000900
0800910a83495435eceb2b0000001d000000080024000000000000002000000000000000
466c61672e7478740a0020000000000001001800e4f6c610fb4cd201e90d9380f84cd201
54178980f84cd201504b050600000000010001005a0000006100000000000195

We see that it starts with 50 4b 03 04 ... these are the magic bytes for zip file. So we convert this hex number to a file using:
```bash
$ echo "504b0304140009000800910a83495435eceb2b0000001d00000008000000466c\ 
61672e747874567168e0247901d8bae9376014e1dba33d60231a36996b43e1f94d8fc0f9\ 
fa53e9dd803ecdae6d5f164db2504b07085435eceb2b0000001d000000504b01021f0014\ 
0009000800910a83495435eceb2b0000001d000000080024000000000000002000000000\ 
000000466c61672e7478740a0020000000000001001800e4f6c610fb4cd201e90d9380f8\ 
4cd20154178980f84cd201504b050600000000010001005a0000006100000000000195"\ 
 | xxd -p -r > file.zip
```

When trying to unzip it we get a password prompt. We must thus crack the password. Using fcrackzip we do a dictionnary attack with a small wordlist present by default on Kali Linux:
```bash
$ fcrackzip -v -m zip1 -D -u -p /usr/share/dict/cracklib-small file.zip
found file 'Flag.txt', (size cp/uc     43/    29, flags 9, chk 0a91)


PASSWORD FOUND!!!!: pw == qwerty
```

Then we only have to unzip the file and read Flag.txt which contains the flag:

> HV16-0228-d75b-40cd-8a0e-1f3e
