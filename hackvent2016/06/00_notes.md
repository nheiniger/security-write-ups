Day 06: Back 2 Work
-------------------
We can unzip the file using the password "confidential" but this helps in no way...

We actually had to look at the comment for each files in the original archive. The comments are made our of tabs and spaces (bytes 0x09 and 0x20). We can extract the comments within python interpreter and see that it looks like a QR code:
```python
>>> import zipfile
>>> zf = zipfile.ZipFile('holiday.zip', 'r')
>>> for info in zf.infolist():
...     print(info.comment)
... 
b'       \t\t\t\t\t \t \t\t\t       \x00'
b' \t\t\t\t\t \t \t \t     \t \t\t\t\t\t \x00'
b' \t   \t \t\t\t\t \t\t  \t\t \t   \t \x00'
b' \t   \t \t     \t \t\t\t \t   \t \x00'
b' \t   \t \t\t \t\t\t \t\t \t \t   \t \x00'
b' \t\t\t\t\t \t  \t\t    \t\t \t\t\t\t\t \x00'
b'       \t \t \t \t \t \t       \x00'
b'\t\t\t\t\t\t\t\t\t  \t \t \t \t\t\t\t\t\t\t\t\x00'
b'     \t    \t   \t   \t \t \t \t\x00'
b' \t    \t\t\t\t  \t \t  \t\t\t\t \t \t\x00'
b' \t  \t\t \t \t \t\t\t    \t  \t\t\t \x00'
b'\t\t\t   \t\t\t\t\t \t\t        \t\t\t\x00'
b'\t\t\t        \t\t\t \t\t  \t\t\t   \x00'
b'   \t \t\t \t\t\t  \t \t\t \t \t\t\t  \x00'
b' \t \t      \t\t  \t  \t  \t    \x00'
b' \t\t   \t \t \t \t\t\t \t \t\t  \t\t \x00'
b' \t\t \t  \t\t  \t\t\t         \t\t\x00'
b'\t\t\t\t\t\t\t\t   \t\t\t \t \t\t\t \t \t \x00'
b'       \t \t \t\t  \t \t \t \t\t  \x00'
b' \t\t\t\t\t \t\t\t\t\t\t\t   \t\t\t \t\t  \x00'
b' \t   \t \t \t           \t  \t\x00'
b' \t   \t \t  \t  \t \t    \t    \x00'
b' \t   \t \t   \t\t\t\t\t \t  \t\t\t\t \x00'
b' \t\t\t\t\t \t \t \t \t      \t \t\t \x00'
b'       \t  \t\t\t \t\t\t\t \t \t   \x00'
```

We then create a simple python script to save this data as a picture:
```python
!/usr/bin/python3

import zipfile
from PIL import Image

im = Image.new("RGB", (25,25))
pix = im.load()

x = 0
y = 0

zf = zipfile.ZipFile('holiday.zip', 'r')
for info in zf.infolist():
        y = 0
        for c in info.comment:
                if c == 32:
                        pix[x,y] = (0,0,0)
                        y += 1
                elif c == 9:
                        pix[x,y] = (255,255,255)
                        y += 1
        x += 1

im.save("qr.png", "PNG")
```

When scanning the resulting QR code we get the flag:

> HV16-y9YO-sDo1-Vi7O-RWq1-V7hN
