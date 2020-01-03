13 - Sagittarius...
===================
> ... is playing with his pila again.
> 
> Can you find the Easter egg QR code he has hidden from you?

Here we are given a `pila.kmz` file that can be opened in google earth. When doing so one sees a circle of points represented. It already looks a bit like a QR-code. My guess was that I had to map this from a circle or a sphere to a square to get the original QR-code.

Doing so was a matter of mathematics and took several tries until I found the right approach to map a circle to a square. In the end I did it as follows. First open the KMZ file to extract all points from the XML data. Each point is represented as a `<Placemark>` element:
```xml
<Placemark>
<styleUrl>#yc10</styleUrl><Point><coordinates>120.70710678118655,-44.792893218813454,0</coordinates></Point></Placemark>
            <Placemark>
<styleUrl>#b10</styleUrl><Point><coordinates>120.67572462851734,-44.762845859799256,0</coordinates></Point></Placemark>
```

On can extract the coordinates. Then I used a python script to make the coordinate transform and plot the result. The formula I used to make the transform comes from <http://squircular.blogspot.ch/2015/09/elliptical-arc-mapping.html> and the script is as follows:
```python
#!/usr/bin/python3

from math import sqrt
import matplotlib.pyplot as plt

def sign(x): return 1 if x >= 0 else -1

coords = [
[120.70710678118655,-44.792893218813454],
[LOTS OF POINTS HERE]
[119.29289321881345,-46.207106781186546]
]

new_coords = [[c[0]-120, c[1]+45.5] for c in coords]

square_coords = []
for [u,v] in new_coords:
    if u**2 >= v**2:
        square_coords.append([
            sign(u) * sqrt(u**2 + v**2),
            sign(u) * (v/u) * sqrt(u**2 + v**2)
            ])
    else:
        square_coords.append([
            sign(v) * (u/v) * sqrt(u**2 + v**2),
            sign(v) * sqrt(u**2 + v**2)
            ])

x = [c[0] for c in square_coords]
y = [c[1] for c in square_coords]

plt.scatter(x, y, c="black", s=100, marker="s", edgecolors=None)
plt.show()
```

This gives almost a QR-code in matplotlib:
![](./13_matplotlib-result.png)

With some work on the picture (scaling, mirroring, rotating and blurring) we have something that can be scanned by the mobile application:
![](./13_egg.png)
