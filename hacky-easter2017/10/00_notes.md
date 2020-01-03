10 - An egg or not ...
----------------------
The egg displayed on the challenge page is a SVG file. When looking at it we notice that it is composed of 2 parts, the background yellow egg is an embedded png file and the QR-code is a list of black or white "points" (6x6 pixels squares). There is more points than needed to form a QR-code (739 vs 625 required for a QR-code).

One can look at the duplicates, in the picture below, the duplicates are colored in red to show them clearly:  
![](./10/egg-red.png)

We can then choose to keep only the first points appearing in the file (because afterwards they will get covered by the new points and give the wrong QR-code). This can be done using the following python script:
```python
#!/usr/bin/python3

f = open('points.txt', 'r')

points = []
result = []

for line in f:
        line = line.rstrip()
        (x, y, color) = line.split(' ')
        if (x, y) not in points:
                points.append((x, y))
                result.append((x, y, color))
f.close()

for (x, y, color) in result:
        print('<use x="' + x + '" y="' + y + '" xlink:href="' + color + '"/>')
```

And we get the egg:  
![](./10/egg10.png)
