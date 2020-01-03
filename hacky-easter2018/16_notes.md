16 - git cloak --hard
=====================
> This one requires your best Git-Fu! Find the hidden egg in the repository.

Actually I did not need to use that much git for this challenge. I started by downloading and unpacking the repository. Then I wrote a python script that will uncompress a git object:
```python
#!/usr/bin/python3

import zlib
import sys

in_file = sys.argv[1]
compressed = open(in_file, 'rb').read()
decompressed = zlib.decompress(compressed)
data = decompressed[decompressed.find(b'\x00') + 1:]

out_file = sys.argv[2]
f = open(out_file, 'wb')
f.write(data)
f.close()
```

Then I ran the script on all git objects, creating decoded copies:
```bash
for i in `ls .git/objects/*/*`; do python3 uncompress.py $i "${i}.decoded"; done;
```

Then I had a look at the file types of those copies:
```bash
for i in `ls .git/objects/*/*.decoded`; do file $i; done;
.git/objects/03/ed59cca1ea7ea0922d6fcbdb98c52931a8d3b0.decoded: JPEG image data, JFIF standard 1.01, resolution (DPI), density 300x300, segment length 16, Exif Standard: [TIFF image data, big-endian, direntries=4, manufacturer=Canon, model=Canon EOS 70D], baseline, precision 8, 870x720, frames 3
.git/objects/04/93a710296b7a684a46eed377029f7077622768.decoded: PNG image data, 480 x 480, 8-bit/color RGBA, non-interlaced
.git/objects/0e/45662a541fee91d4652c5ba57300276eb7fa29.decoded: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 650x434, frames 3
.git/objects/17/9ec0d76ecdc903ac12c4f3971efefbfb02aacb.decoded: PNG image data, 550 x 481, 8-bit/color RGBA, non-interlaced
.git/objects/22/8b603ed45ddaf1b1d3fe502e168fa2508ee5ed.decoded: ASCII text
.git/objects/24/5735e32ed8174bdabe9655f00f1deb4ebaa3ad.decoded: PNG image data, 444 x 659, 8-bit/color RGB, non-interlaced
.git/objects/34/41837df545268c05da59d6d280a62a21343680.decoded: PNG image data, 600 x 700, 8-bit/color RGB, non-interlaced
.git/objects/38/39c14d2863fd850794661677352305ea798eb6.decoded: ASCII text
.git/objects/57/a17c1a44414c5973a7d967f2ca07eccf530ff4.decoded: PNG image data, 480 x 480, 8-bit/color RGBA, non-interlaced
.git/objects/5e/5e98caaa4ed1f6edee5aced3ff0b92457d6549.decoded: data
.git/objects/69/ee0b67f2701bc83cd64eec1e01c045c8a53bd3.decoded: PNG image data, 277 x 182, 8-bit colormap, non-interlaced
.git/objects/6f/5568ed00eb893db28616497f18749efd4bfd89.decoded: data
.git/objects/74/1583e168e0723aef4ca0253f875a1f50144567.decoded: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, baseline, precision 8, 480x320, frames 3
.git/objects/8d/9faa7ebaac3b61cc29cc309d11b923e9bcd5ab.decoded: JPEG image data, JFIF standard 1.01, resolution (DPI), density 96x96, segment length 16, progressive, precision 8, 400x400, frames 3
.git/objects/9a/29769663d029f1b3ad83fec7e7f19ca1cf8e78.decoded: ASCII text
.git/objects/9d/69bfb2dc3b3fd28389c7f709c3656e5c78c8c4.decoded: data
.git/objects/9d/7c9b5a1c8773ea48caac90d05401679b0a8897.decoded: ASCII text
.git/objects/b9/820d55ce59799992648672a5a43fff4effd56b.decoded: ASCII text
.git/objects/b9/e860f47fe6990cbda4ac5bb3d2829d2191f1eb.decoded: ASCII text
.git/objects/bc/83275bcea7da814743f1c478cb3a8771e0f1ac.decoded: data
.git/objects/be/98f627fa5d3251be77bbb7a64f5a34b6baf709.decoded: PNG image data, 480 x 480, 8-bit/color RGBA, non-interlaced
.git/objects/c5/9568e4b945199366ad7ea486efbda76a07887c.decoded: data
.git/objects/d0/c6562ce74c54358445fc3b6cc0584e32057ad5.decoded: JPEG image data, JFIF standard 1.01, aspect ratio, density 1x1, segment length 16, progressive, precision 8, 454x330, frames 3
.git/objects/d7/995a259ff0dfa28da06618d06e78b346738a6b.decoded: JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16, baseline, precision 8, 620x455, frames 3
.git/objects/da/cecafa877bd2346bd3a2c0a8a4026418491ccd.decoded: PNG image data, 480 x 480, 8-bit/color RGB, non-interlaced
.git/objects/db/ab6618f6dc00a18b4195fb1bec5353c51b256f.decoded: PNG image data, 480 x 480, 8-bit colormap, non-interlaced
.git/objects/e7/237971df563c82e85eb74a50ca41a218dc85ed.decoded: data
.git/objects/f7/d946ebee06ee65e422530355c08ff2f06d456b.decoded: JPEG image data, JFIF standard 1.01, resolution (DPI), density 72x72, segment length 16, baseline, precision 8, 475x562, frames 3
```

Then I only had to look at all picture file to find the right one. It was `.git/objects/db/ab6618f6dc00a18b4195fb1bec5353c51b256f.decoded`. This is the egg:
![](./16_egg.png)
