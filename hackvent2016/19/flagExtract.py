#!/usr/bin/python3

from PIL import Image

def get_line(start, end):
    """Bresenham's Line Algorithm
    Produces a list of tuples from start and end
 
    >>> points1 = get_line((0, 0), (3, 4))
    >>> points2 = get_line((3, 4), (0, 0))
    >>> assert(set(points1) == set(points2))
    >>> print points1
    [(0, 0), (1, 1), (1, 2), (2, 3), (3, 4)]
    >>> print points2
    [(3, 4), (2, 3), (1, 2), (1, 1), (0, 0)]
    """
    # Setup initial conditions
    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
 
    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)
 
    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2
 
    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True
 
    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1
 
    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1
 
    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx
 
    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

# copied from SVG file
polyline = "804,409,746,430,772,395,742,379,776,340,707,346,712,383,808,325,747,291,688,331,635,406,587,325,622,312,651,279,622,307,638,347,626,412,633,454,668,418,651,381,622,412,615,313,590,402,550,352,567,370,584,344,609,275,620,323,641,282,676,302,654,323,659,363,669,400,698,359,730,359,762,340,806,360,736,390,777,388,770,419,791,412,793,387,752,402,782,362,771,321,756,344,720,317,751,310,738,262,701,242,669,296,675,337,656,376,627,399,633,347,611,323,650,283,672,262,645,293,641,322,610,352,607,375,617,410,661,353,640,328,689,275,691,319,732,315,759,352,794,319,763,368,819,355,814,305,777,284,753,352,693,368,748,304,710,281,693,317,619,310,647,340,696,321,730,276,775,268,732,311,809,318,761,373,732,349,749,316,812,323,742,302,707,326,689,258,660,308,662,361,625,429,605,391,606,340,648,281,666,309,651,330,736,277,735,312,759,339,783,264,721,271,666,323,649,328,650,274,619,278,615,318,607,398,622,438,625,391,655,409,654,326,692,329,705,290,675,305,718,239,780,300,719,316,755,292,801,334,770,336,787,360,735,365,731,393,815,380,766,368,731,353,760,341,714,328,740,308,694,306,652,330,685,274,633,296,619,320,631,357,657,323,766,305,700,250,636,343,651,392,701,367,711,287,680,356,682,288,756,278,740,241,705,284,632,286,618,311,673,311,614,335,603,455,627,409,648,439,672,392,696,368,715,384,745,352,741,301,788,298,722,281,781,343,715,338,708,280,798,295,752,274,798,285,729,322,755,363,774,295,793,332,763,341,728,420,778,420,810,406,766,389,805,382,743,413,757,372,784,331,728,366,713,328,744,310,706,288,679,346,629,365,611,325,651,333,696,265,715,291,709,339,744,277,802,293,747,307,786,324,799,366,768,327,721,380,771,288,819,319,783,326,744,310,797,362,738,340,730,393,775,366,710,340,779,291,805,342,715,266,712,352,648,420,624,363,644,276,598,319,633,312,585,359,565,306,571,346,591,410,584,327,624,319,656,303,691,330,656,372,690,318,734,313,719,269,687,270,669,299,762,274,780,299,703,304,711,342,819,329,768,287,718,335,757,343,735,262,697,249,632,351,601,354,665,243,687,241,664,300,729,260,694,321,749,298,808,290,785,326,710,276,677,294,648,333"
array = polyline.split(',')

# split the polyline in a list of (x,y) coords
coords = [(int(array[i]), int(array[i+1])) for i in range(0, len(array), 2)]

coords_list = []
for i in range(0, len(coords)-1):
	# extend the list with all pixel coords in the line between two points using Bresenham's algorithm
	coords_list.extend(get_line(coords[i], coords[i+1]))
	# remove last pixel because otherwise it gets added twice
	del coords_list[-1]

# open zebra image
im = Image.open('zebra4.png')
pix = im.load()

# create new result image using pixels at the coordinates given by Bresenham's algorithm
width = len(coords_list)
height = 1
im2 = Image.new('RGB', (width,height), 'white')
pix2 = im2.load()

for x in range(width):
	for y in range(height):
		pix2[x,y] = pix[coords_list[x][0], coords_list[x][1]]

im2.save("barcode.png")
