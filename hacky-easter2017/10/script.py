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
