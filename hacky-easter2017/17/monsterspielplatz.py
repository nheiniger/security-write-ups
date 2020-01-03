#!/usr/bin/python

import os
import shutil

# Grid size
width = 21
height = 21

# Colors
RED = 1
GRE = 2
BLU = 3
YEL = 4
PIN = 5
BRO = 6

# Displays the grid as text (only cells were >= 1 monsters are present)
def display(monster_list):
    grid = [[False for x in range(width)] for y in range(height)]
    for m in monster_list:
        grid[m['p']['y']][m['p']['x']] = True
    for row in grid:
        line = ''
        for col in row:
            if col:
                line += '#'
            else:
                line += ' '
        print(line)
    print('-' * 27)

# Write HTML to file
def write_html(filename, monster_list):
    # initialize empty grid
    grid = [[[] for x in range(21)] for y in range(21)]
    for m in monster_list:
        grid[m['p']['x']][m['p']['y']].append(m['c'])

    # copy start of HTML
    shutil.copy('start.html', filename)

    # open file
    f = open(filename, 'a')

    # write HTML
    for col in range(21):
        f.write('<tr>')
        line = ''
        for row in range(21):
            line += '<td>' + ','.join(map(str, grid[row][col])) + '</td>'
        f.write(line)
        f.write('</tr>')

    # append end of HTML
    f.write('</tbody></table><script>copyTable();</script></p></article></div></div></div></div></body></html>')

# Shows the value on each line
def display_values(monster_list):
    # initialize empty grid
    grid = [[[] for x in range(21)] for y in range(21)]
    for m in monster_list:
        grid[m['p']['x']][m['p']['y']].append(m['c'])

    for row in grid:
        res = ''
        for cell in row:
            res += ''.join(map(str, cell)) + '-'
        print(res)

# Partial jump 1
def jump1(monster_list):
    for m in monster_list:
        if m['c'] == RED:
            m['p']['x'] = (m['p']['x'] + 1 + width) % width
            m['p']['y'] = (m['p']['y'] - 2 + height) % height
        elif m['c'] == GRE:
            m['p']['x'] = (m['p']['x'] + 1 + width) % width
            m['p']['y'] = (m['p']['y'] - 2 + height) % height
        elif m['c'] == BLU:
            m['p']['x'] = (m['p']['x'] - 1 + width) % width
            m['p']['y'] = (m['p']['y'] + 2 + height) % height
        elif m['c'] == YEL:
            m['p']['x'] = (m['p']['x'] - 1 + width) % width
            m['p']['y'] = (m['p']['y'] - 1 + height) % height
        elif m['c'] == PIN:
            m['p']['x'] = (m['p']['x'] - 1 + width) % width
            m['p']['y'] = (m['p']['y'] - 1 + height) % height
        elif m['c'] == BRO:
            m['p']['x'] = (m['p']['x'] - 1 + width) % width
            m['p']['y'] = (m['p']['y'] - 1 + height) % height

# Partial jump 2
def jump2(monster_list):
    for m in monster_list:
        if m['c'] == RED:
            m['p']['x'] = (m['p']['x'] + 1) % width
            m['p']['y'] = (m['p']['y'] + 2) % height
        elif m['c'] == GRE:
            m['p']['x'] = (m['p']['x'] + 1) % width
            m['p']['y'] = (m['p']['y'] + 1) % height
        elif m['c'] == BLU:
            m['p']['x'] = (m['p']['x'] + 3) % width
            m['p']['y'] = (m['p']['y'] - 1 + height) % height
        elif m['c'] == YEL:
            m['p']['x'] = (m['p']['x'] - 1 + width) % width
            m['p']['y'] = (m['p']['y'] + 2) % height
        elif m['c'] == PIN:
            m['p']['y'] = (m['p']['y'] + 3) % height
        elif m['c'] == BRO:
            m['p']['x'] = (m['p']['x'] - 1 + width) % width
            m['p']['y'] = (m['p']['y'] + 2) % height

# Partial jump 3
def jump3(monster_list):
    for m in monster_list:
        if m['c'] == RED:
            m['p']['x'] = (m['p']['x'] + 1 + width) % width
        elif m['c'] == GRE:
            m['p']['x'] = (m['p']['x'] + 1 + width) % width
            m['p']['y'] = (m['p']['y'] - 2 + height) % height
        elif m['c'] == BLU:
            m['p']['x'] = (m['p']['x'] - 1 + width) % width
            m['p']['y'] = (m['p']['y'] + 1 + height) % height
        elif m['c'] == YEL:
            m['p']['x'] = (m['p']['x'] - 1 + width) % width
            m['p']['y'] = (m['p']['y'] - 3 + height) % height
        elif m['c'] == PIN:
            m['p']['x'] = (m['p']['x'] - 1 + width) % width
            m['p']['y'] = (m['p']['y'] - 1 + height) % height
        elif m['c'] == BRO:
            m['p']['x'] = (m['p']['x'] - 1 + width) % width
            m['p']['y'] = (m['p']['y'] - 1 + height) % height

# Full jump
def full_jump(monster_list):
    jump1(monster_list)
    jump2(monster_list)
    jump3(monster_list)

# Check if final condition is met
def check_final(monster_list):
    for m in monster_list:
        if m['p']['x'] == 0:
            return False
    return True

# Build the monster starting position from the web page
f = open('starting_grid.txt', 'r')
row = 0
monsters = [
    {'c': YEL, 'p': {'x': 0, 'y': 0}},
    {'c': BLU, 'p': {'x': 6, 'y': 0}},
    {'c': BLU, 'p': {'x': 12, 'y': 0}},
    {'c': YEL, 'p': {'x': 19, 'y': 0}},
    {'c': YEL, 'p': {'x': 1, 'y': 1}},
    {'c': BLU, 'p': {'x': 3, 'y': 1}},
    {'c': GRE, 'p': {'x': 5, 'y': 1}},
    {'c': PIN, 'p': {'x': 9, 'y': 1}},
    {'c': GRE, 'p': {'x': 16, 'y': 1}},
    {'c': YEL, 'p': {'x': 4, 'y': 3}},
    {'c': BLU, 'p': {'x': 7, 'y': 3}},
    {'c': PIN, 'p': {'x': 9, 'y': 3}},
    {'c': GRE, 'p': {'x': 0, 'y': 4}},
    {'c': BLU, 'p': {'x': 4, 'y': 4}},
    {'c': GRE, 'p': {'x': 7, 'y': 4}},
    {'c': BRO, 'p': {'x': 15, 'y': 4}},
    {'c': PIN, 'p': {'x': 17, 'y': 4}},
    {'c': RED, 'p': {'x': 5, 'y': 5}},
    {'c': RED, 'p': {'x': 7, 'y': 5}},
    {'c': GRE, 'p': {'x': 8, 'y': 5}},
    {'c': BLU, 'p': {'x': 10, 'y': 5}},
    {'c': BLU, 'p': {'x': 12, 'y': 5}},
    {'c': RED, 'p': {'x': 14, 'y': 5}},
    {'c': BLU, 'p': {'x': 16, 'y': 5}},
    {'c': GRE, 'p': {'x': 17, 'y': 5}},
    {'c': RED, 'p': {'x': 20, 'y': 5}},
    {'c': BLU, 'p': {'x': 1, 'y': 6}},
    {'c': BRO, 'p': {'x': 3, 'y': 6}},
    {'c': RED, 'p': {'x': 8, 'y': 6}},
    {'c': BLU, 'p': {'x': 10, 'y': 6}},
    {'c': BRO, 'p': {'x': 13, 'y': 6}},
    {'c': BRO, 'p': {'x': 15, 'y': 6}},
    {'c': RED, 'p': {'x': 19, 'y': 6}},
    {'c': GRE, 'p': {'x': 0, 'y': 7}},
    {'c': PIN, 'p': {'x': 1, 'y': 7}},
    {'c': PIN, 'p': {'x': 2, 'y': 7}},
    {'c': RED, 'p': {'x': 7, 'y': 7}},
    {'c': RED, 'p': {'x': 8, 'y': 7}},
    {'c': RED, 'p': {'x': 15, 'y': 7}},
    {'c': BRO, 'p': {'x': 4, 'y': 8}},
    {'c': BLU, 'p': {'x': 9, 'y': 8}},
    {'c': BLU, 'p': {'x': 12, 'y': 8}},
    {'c': RED, 'p': {'x': 17, 'y': 8}},
    {'c': BRO, 'p': {'x': 19, 'y': 8}},
    {'c': BLU, 'p': {'x': 1, 'y': 9}},
    {'c': RED, 'p': {'x': 4, 'y': 9}},
    {'c': BRO, 'p': {'x': 7, 'y': 9}},
    {'c': PIN, 'p': {'x': 11, 'y': 9}},
    {'c': BRO, 'p': {'x': 12, 'y': 9}},
    {'c': RED, 'p': {'x': 17, 'y': 9}},
    {'c': BRO, 'p': {'x': 0, 'y': 10}},
    {'c': RED, 'p': {'x': 2, 'y': 10}},
    {'c': PIN, 'p': {'x': 9, 'y': 10}},
    {'c': YEL, 'p': {'x': 14, 'y': 10}},
    {'c': PIN, 'p': {'x': 15, 'y': 10}},
    {'c': BRO, 'p': {'x': 18, 'y': 10}},
    {'c': RED, 'p': {'x': 20, 'y': 11}},
    {'c': YEL, 'p': {'x': 1, 'y': 12}},
    {'c': BRO, 'p': {'x': 5, 'y': 12}},
    {'c': PIN, 'p': {'x': 12, 'y': 12}},
    {'c': PIN, 'p': {'x': 0, 'y': 13}},
    {'c': RED, 'p': {'x': 1, 'y': 13}},
    {'c': YEL, 'p': {'x': 5, 'y': 13}},
    {'c': RED, 'p': {'x': 7, 'y': 13}},
    {'c': RED, 'p': {'x': 14, 'y': 13}},
    {'c': GRE, 'p': {'x': 1, 'y': 14}},
    {'c': RED, 'p': {'x': 4, 'y': 14}},
    {'c': GRE, 'p': {'x': 6, 'y': 14}},
    {'c': RED, 'p': {'x': 8, 'y': 14}},
    {'c': BRO, 'p': {'x': 12, 'y': 14}},
    {'c': BRO, 'p': {'x': 18, 'y': 14}},
    {'c': BRO, 'p': {'x': 4, 'y': 15}},
    {'c': RED, 'p': {'x': 17, 'y': 15}},
    {'c': YEL, 'p': {'x': 1, 'y': 16}},
    {'c': BLU, 'p': {'x': 4, 'y': 16}},
    {'c': RED, 'p': {'x': 6, 'y': 16}},
    {'c': BLU, 'p': {'x': 8, 'y': 16}},
    {'c': YEL, 'p': {'x': 13, 'y': 16}},
    {'c': YEL, 'p': {'x': 14, 'y': 16}},
    {'c': RED, 'p': {'x': 15, 'y': 16}},
    {'c': YEL, 'p': {'x': 20, 'y': 16}},
    {'c': BLU, 'p': {'x': 0, 'y': 17}},
    {'c': GRE, 'p': {'x': 4, 'y': 17}},
    {'c': BRO, 'p': {'x': 7, 'y': 17}},
    {'c': GRE, 'p': {'x': 8, 'y': 17}},
    {'c': BLU, 'p': {'x': 10, 'y': 17}},
    {'c': BLU, 'p': {'x': 12, 'y': 17}},
    {'c': RED, 'p': {'x': 13, 'y': 17}},
    {'c': BRO, 'p': {'x': 5, 'y': 18}},
    {'c': BRO, 'p': {'x': 6, 'y': 18}},
    {'c': GRE, 'p': {'x': 8, 'y': 18}},
    {'c': RED, 'p': {'x': 13, 'y': 18}},
    {'c': RED, 'p': {'x': 17, 'y': 18}},
    {'c': BRO, 'p': {'x': 19, 'y': 18}},
    {'c': YEL, 'p': {'x': 20, 'y': 18}},
    {'c': YEL, 'p': {'x': 1, 'y': 19}},
    {'c': BLU, 'p': {'x': 9, 'y': 19}},
    {'c': RED, 'p': {'x': 15, 'y': 19}},
    {'c': RED, 'p': {'x': 16, 'y': 19}},
    {'c': GRE, 'p': {'x': 17, 'y': 19}},
    {'c': GRE, 'p': {'x': 7, 'y': 20}}
]

# Jumps
for i in range(5):
    jump1(monsters)
    display(monsters)
    jump2(monsters)
    display(monsters)
    jump3(monsters)
    display(monsters)
