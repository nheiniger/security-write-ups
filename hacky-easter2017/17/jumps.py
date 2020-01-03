#!/usr/bin/python

# Grid size
width = 27
height = 27

# Colors
RED = 1
GRE = 2
BLU = 3
YEL = 4
PIN = 5
BRO = 6

class Monster():
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

    def __str__(self):
        return '{0} @ ({1}, {2})'.format(COLORS[self.color], str(self.x), str(self.y))

# Displays the grid as text (only cells were >= 1 monsters are present in black, the rest in white)
def display(monster_list):
    grid = [[False for x in range(width)] for y in range(height)]
    for m in monster_list:
        grid[m.y][m.x] = True
    for row in grid:
        line = ''
        for col in row:
            if col:
                line += ' '
            else:
                line += u"\u2588"
        print(line)
    print('-' * 27)

# Partial jump 1
def jump1(monster_list):
    for m in monster_list:
        if m.color == RED:
            m.x = (m.x + 1 + width) % width
            m.y = (m.y - 2 + height) % height
        if m.color == GRE:
            m.x = (m.x + 1 + width) % width
            m.y = (m.y - 2 + height) % height
        if m.color == BLU:
            m.x = (m.x - 1 + width) % width
            m.y = (m.y + 2 + height) % height
        if m.color == YEL:
            m.x = (m.x - 1 + width) % width
            m.y = (m.y - 1 + height) % height
        if m.color == PIN:
            m.x = (m.x - 1 + width) % width
            m.y = (m.y - 1 + height) % height
        if m.color == BRO:
            m.x = (m.x - 1 + width) % width
            m.y = (m.y - 1 + height) % height

# Partial jump 2
def jump2(monster_list):
    for m in monster_list:
        if m.color == RED:
            m.x = (m.x + 1) % width
            m.y = (m.y + 2) % height
        if m.color == GRE:
            m.x = (m.x + 1) % width
            m.y = (m.y + 1) % height
        if m.color == BLU:
            m.x = (m.x + 3) % width
            m.y = (m.y - 1 + height) % height
        if m.color == YEL:
            m.x = (m.x - 1 + width) % width
            m.y = (m.y + 2) % height
        if m.color == PIN:
            m.y = (m.y + 3) % height
        if m.color == BRO:
            m.x = (m.x - 1 + width) % width
            m.y = (m.y + 2) % height

# Partial jump 3
def jump3(monster_list):
    for m in monster_list:
        if m.color == RED:
            m.x = (m.x + 1 + width) % width
        if m.color == GRE:
            m.x = (m.x + 1 + width) % width
            m.y = (m.y - 2 + height) % height
        if m.color == BLU:
            m.x = (m.x - 1 + width) % width
            m.y = (m.y + 1 + height) % height
        if m.color == YEL:
            m.x = (m.x - 1 + width) % width
            m.y = (m.y - 3 + height) % height
        if m.color == PIN:
            m.x = (m.x - 1 + width) % width
            m.y = (m.y - 1 + height) % height
        if m.color == BRO:
            m.x = (m.x - 1 + width) % width
            m.y = (m.y - 1 + height) % height

# Check if final condition is met (looking for QR-code so no monster on the border)
def check_final(monster_list):
    for m in monster_list:
        if m.x == 0:
            return False
        if m.y == 0:
            return False
        if m.x == 26:
            return False
        if m.y == 26:
            return False
    return True

# Build the monster starting position by parsing the table from the web page
f = open('starting_grid.txt', 'r')
row = 0
monsters = []
for line in f:
    cells = line.split('</td><td>')
    col = 0
    for cell in cells:
        if str(RED) in cell:
            monsters.append(Monster(RED, col, row))
        if str(GRE) in cell:
            monsters.append(Monster(GRE, col, row))
        if str(BLU) in cell:
            monsters.append(Monster(BLU, col, row))
        if str(YEL) in cell:
            monsters.append(Monster(YEL, col, row))
        if str(PIN) in cell:
            monsters.append(Monster(PIN, col, row))
        if str(BRO) in cell:
            monsters.append(Monster(BRO, col, row))
        col += 1
    row += 1

# Jumps in the right order and check final condition between each partial jump
for i in range(27): 
    jump2(monsters)
    if check_final(monsters):
        display(monsters)
    jump3(monsters)
    if check_final(monsters):
        display(monsters)
    jump1(monsters)
    if check_final(monsters):
        display(monsters)
