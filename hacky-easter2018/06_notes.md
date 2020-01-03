06 - Cooking for Hackers
========================
> You've found this recipe online:
> 
> 1 pinch: c2FsdA==
> 
> 2 tablesspoons: b2ls
> 
> 1 teaspoon: dDd3Mmc=
> 
> 50g: bnRkby4=
> 
> 2 medium, chopped: b25pb24=
> 
> But you need one more secret ingredient! Find it!

Decoding the ingredient from base64 gives:
```
1 pinch: salt
2 tablespoons: oil
1 teaspoon: t7w2g
50g: ntdo.
2 medium, chopped: onion
```

This could be a .onion URL: <http://saltoilt7w2gntdo.onion> and indeed when visiting this page using the Tor browser we get a page that gives us the flag:
![](./06_egg.png)
