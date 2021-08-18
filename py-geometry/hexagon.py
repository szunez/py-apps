import numpy as n
import math as m
def hexagonA() :
    side = float(input('\nEnter the distance of the side for a right hexagon: '))
    width = side*(1+2*n.sin(m.radians(30)))
    height = side*2*n.cos(m.radians(30))
    hexagonPrint(side, height, width)
def hexagonW() :
    width = float(input('\nEnter the distance of the width [distance from opposing apexes] for a right hexagon: '))
    side = width/(1+2*n.sin(m.radians(30)))
    height = side*2*n.cos(m.radians(30))
    hexagonPrint(side, height, width)
def hexagonH() :
    height = float(input('\nEnter the distance of the height [distance from opposing sides] for a right hexagon: '))
    side = height/2/n.cos(m.radians(30))
    width = side*(1+2*n.sin(m.radians(30)))
    hexagonPrint(side, height, width)
def hexagonPrint(side, height, width) :
    print('\nFor a rectangle containing a right hexagon of side = '+str(side)+' :')
    print('    height = '+str(height))
    print('    width = '+str(width)+'\n')
    print('             a = '+str(side))
    print('          ______')
    print('        /        \  |')
    print('       /          \ |')
    print('       \          / | h = '+str(height))
    print('        \        /  |')
    print('          ──────    |')
    print('       ─────────────')
    print('          w = '+str(width))
hexagon=input('\n             a = side\
        \n          ______\
        \n        /        \  |\
        \n       /          \ |\
        \n       \          / | h = heigth\
        \n        \        /  |\
        \n          ──────    |\
        \n       ─────────────\
        \n          w = width\n\
        \nWhich dimension of a right hexagon do you wish to specify [side, width, height]? : ')
if hexagon[0]=='h' :
    hexagonH()
elif hexagon[0]=='w' :
    hexagonW()
else :
    hexagonA()