Day 02: Wishlist
================
> *The fifth power of two*
> 
> Something happened to my wishlist, please help me.

In this challenge we get a text file with a long blob of what seems to be Base64 encoded data. Given the subtitle "The fifth power of 2" I guess it must be encoded 32 times. So go to the terminal and use:

```
Cat Wishlist.txt | base64 -d | base64 -d | ... | base64 -d
```

But for some reason the last decode was not working as expected. In ended up doing 31 in a first round and then the last one looked like:
```
❯❯❯ echo 'SFYxNy1UaDNGLTFmdGgtUG93My1yMGYyLWlzMzI' | base64 -d                                ⏎
HV17-Th3F-1fth-Pow3-r0f2-is32base64: invalid input
```

It is not very clean but we see the flag:
```
HV17-Th3F-1fth-Pow3-r0f2-is32
```
