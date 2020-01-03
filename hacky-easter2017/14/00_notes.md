14 - Shards
-----------
We are given 1600 small image files with weird names. When looking closer we see that the names always contain a letter from a to N and a number from 0 to 39. Seeing this we can assume that these are x and y coordinates to place the shards in a bigger picture. It fits nicely since it would be 40*40 = 1600 pictures. To make sure of that I renamed the files using the following python script:
```python
#!/usr/bin/python3

import glob
import os
import re

os.chdir('shards')
for filename in glob.glob('*.png'):
        (foo, bar, x, sugus, y) = re.split('_', filename)
        y = y[:-4]
        os.rename(filename, x + '_' + y + '.png')
```

From there we can see in a file browser that the small pictures are fitting because of the new listing order. I then wrote a second python script to construct the bigger picture from all the small ones. It will simply iterate over the numbers from 0 to 39 and the letters from a to N and copy the corresponding picture in a bigger one:
```python
#!/usr/bin/python3

import os
from PIL import Image

os.chdir('shards')
width = range(40)
height = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z','A','B','C','D','E','F','G','H','I','J','K','L','M','N']


result = Image.new("RGB", (480, 480), "white")

for x in width:
        yi = 0
        for y in height:
                im = Image.open(y + '_' + str(x) + '.png')
                result.paste(im, (x*12, yi*12))
                yi += 1

result.save('../egg14.png')
```

In the end we get the flag:  
![](./14/egg14.png)
