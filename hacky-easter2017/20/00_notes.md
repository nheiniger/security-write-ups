20 - Spaghetti Hash
-------------------
To compute spaghetti hashes ourselves, we first map which sha512 char is mapped to which custom hash char:
```
sha512[65] -> custom[0]
sha512[17] -> custom[1]
sha512[115] -> custom[2]
sha512[31] -> custom[3]
sha512[45] -> custom[4]
sha512[11] -> custom[5]
sha512[67] -> custom[6]
sha512[92] -> custom[7]
sha512[0] -> custom[8]
sha512[7] -> custom[9]
sha512[123] -> custom[10]
sha512[37] -> custom[11]
sha512[5] -> custom[12]
sha512[22] -> custom[13]
sha512[87] -> custom[14]
sha512[124] -> custom[15]
sha512[25] -> custom[16]
sha512[89] -> custom[17]
sha512[38] -> custom[18]
sha512[61] -> custom[19]
sha512[90] -> custom[20]
sha512[109] -> custom[21]
sha512[63] -> custom[22]
sha512[28] -> custom[23]
sha512[102] -> custom[24]
sha512[12] -> custom[25]
sha512[47] -> custom[26]
sha512[59] -> custom[27]
sha512[110] -> custom[28]
sha512[86] -> custom[29]
sha512[24] -> custom[30]
sha512[18] -> custom[31]
```

This was done by manually comparing the output for same value column by column. For example, for custom hash column 0 we must find a corresponding column with chars (2,5,d,a) in the sha512 hashes. Indeed, it appears at column 65:
```
custom hash:
a -> 2552d46012e2cee9c48f2238b10ec560
b -> 580b7ef5583b650e55788477165ecbcf
c -> da1b8782a23ed2c5d041cc218b952631
d -> ad50cdc041f4001d08766c78548a54bc

sha512:
a -> 1f40fc92da241694750979ee6cf582f2d5d7d28e18335de05abc54d0560e0f5302860c652bf08d560252aa5e74210546f369fbbbce8c12cfc7957b2652fe9a75
b -> 5267768822ee624d48fce15ec5ca79cbd602cb7f4c2157a516556991f22ef8c7b5ef7b18d1ff41c59370efb0858651d44a936c11b7b144c48fe04df3c6a3e8da
c -> acc28db2beb7b42baa1cb0243d401ccb4e3fce44d7b02879a52799aadff541522d8822598b2fa664f9d5156c00c924805d75c3868bd56c2acb81d37e98e35adc
d -> 48fb10b15f3d44a09dc82d02b06581e0c0c69478c9fd2cf8f9093659019a1687baecdbb38c9e72b12169dc4148690f87467f9154f5931c5df665c6496cbfd5f5
```

Now we can reproduce the spaghetti hashing algorithm, I used a not so efficient python implementation with the crackstation-human-only wordlist. This ran for some hours and gave me the following results:

- hash 1: 87017a3ffc7bdd5dc5d5c9c348ca21c5 = Prodigy
- hash 2: ff17891414f7d15aa4719689c44ea039 = Cleveland
- hash 3: 5b9ea4569ad68b85c7230321ecda3780 = benchmark
- hash 4: 6ad211c3f933df6e5569adf21d261637 = 12345678

When entering these 4 passwords in the egg-o-matic we get the egg:  
![](./20/egg20.png)
