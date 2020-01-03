13 - Lost the Thread
--------------------
The provided file is a picture of 3x14500 pixels. When looking at it one can see that only the middle line contains color, the rest is only transparent. I wrote a python script that would extract the pixels from the middle line and rearrange them as lines of 17 pixels, giving an image of 17x852 pixels. The value of 17 was obtaind by trial and error, I kept this value because we get two nice columns that looks like they contain more data in the first and third columns.

Using the same script and the same process I extracted the first column as columns or 29 pixels. This gives a final image of 29x29 pixels that is actually a QR-code:  
![](./13/step3.png)

When scanning the code, we get the password "kiwisarekewl" and when entering this into the egg-o-matic we get the egg:  
![]('./13/egg13.png')

The python script I used is as follows:
```python
#!/usr/bin/python

from PIL import Image

im = Image.open('thread.png')
pix = im.load()

width = 17
height = 14500 / width

im2 = Image.new('RGBA', (width, height), 'white')
pix2 = im2.load()

for x in range(width):
        for y in range(height):
                pix2[x,y] = pix[width*y + x, 1]

im2.save('step2.png')

w3 = 29
h3 = height / w3

im3 = Image.new('RGBA', (w3, h3), 'white')
pix3 = im3.load()

for x in range(w3):
        for y in range(h3):
                pix3[x,y] = pix2[0, w3*y + x]

im3.save('step3.png')
```
