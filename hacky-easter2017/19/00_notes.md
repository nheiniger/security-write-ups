19 - Disco Time
---------------
Here we have 3 nice GIF pictures, the two cats are nice but one can easily see that the important file is the `disco2.gif` because it has 4172 frames of 2x2 pixels which is suspicious.

I started by extracting the frames using a python script found here [1]. Then after several unsuccessful attempts at extracting data from the pixel color values I tried to apply a similar method than for challenges 13 and 14, reconstruct a bigger image using those frames. I used the following script to do that:
```python
#!/usr/bin/python

import os
from PIL import Image

os.chdir('frames')
width = 28
height = 4172 / width

result = Image.new('RGB', (width*2, height*2), 'white')

for i in range(4172):
    x = i % width
    y = (i - x) / width
    im = Image.open('disco2-' + str(i) + '.png')
    result.paste(im, (x*2, y*2))

result.save('../result.png')
```

I guessed the width because of the number of frames, 4172 = 2x2x7x149 so i tried with 28. The result of the script is a picture that need to be rotated then flipped horizontally to provide a readable flag:  
![](./19/flag.png)

And when putting this flag in the egg-o-matic the egg is displayed:
![](./19/egg19.png)

\[1\]: Extract frames from GIF in python, <https://gist.github.com/BigglesZX/4016539>
