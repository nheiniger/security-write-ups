25 - Hidden Egg #1
==================
`Heads up! You gonna find this hidden egg!`

This one is easy, the hint says heads up, let's look at the headers and indeed we find the following HTTP response header:
```
Content-Eggcoding: aHR0cHM6Ly9oYWNreWVhc3Rlci5oYWNraW5nLWxhYi5jb20vaGFja3llYXN0ZXIvaW1hZ2VzL2VnZ3MvYmEwYzc0ZWQ0MzlhYjQ3OTVmYzM2OTk5ZjU0MmJhNTBiMzI2ZTEwOS5wbmc=
```

Decoding this from base64 gives an URL:
```
https://hackyeaster.hacking-lab.com/hackyeaster/images/eggs/ba0c74ed439ab4795fc36999f542ba50b326e109.png
```

And when accessing it we get the egg:
![](./25_egg.png)
