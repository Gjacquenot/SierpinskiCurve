# -*- coding: utf-8 -*-
#
# This script generates a fractal Sierpinsky Peano curve
# showing how a line (dimension 1) can literally fill
# the plane (dimension 2).
#
# The main method takes two arguments:
#   - a user defined pattern, stored as two lists of floats containing
#      X and Y cordinates
#   - a number of recursion level (6 is a good value)
#
# http://mathworld.wolfram.com/SierpinskiCurve.html
# http://www.physics.mcgill.ca/~gang/multifrac/intro/intro.htm
#
# Results can be seen here
#
# https://commons.wikimedia.org/wiki/File:Peano_Curve_Steinhaus_1.svg
# https://commons.wikimedia.org/wiki/File:Peano_Curve_Steinhaus_2.svg
# https://commons.wikimedia.org/wiki/File:Peano_Curve_Steinhaus_3.svg
# https://commons.wikimedia.org/wiki/File:Peano_Curve_Steinhaus_4.svg
# https://commons.wikimedia.org/wiki/File:Peano_Curve_Steinhaus_5.svg
# https://commons.wikimedia.org/wiki/File:Peano_Curve_Steinhaus_6.svg
#
# https://commons.wikimedia.org/wiki/File:Curve_Peano_Steinhaus_1_M2.svg
# https://commons.wikimedia.org/wiki/File:Curve_Peano_Steinhaus_2_M2.svg
# https://commons.wikimedia.org/wiki/File:Curve_Peano_Steinhaus_3_M2.svg
# https://commons.wikimedia.org/wiki/File:Curve_Peano_Steinhaus_4_M2.svg
# https://commons.wikimedia.org/wiki/File:Curve_Peano_Steinhaus_5_M2.svg
# https://commons.wikimedia.org/wiki/File:Curve_Peano_Steinhaus_6_M2.svg
import numpy as np
from matplotlib.pyplot import figure, show, rc, grid

def symmetrize(a = +1.0, b = -1.0, c = 0.0, X = [], Y = []):
    # Create symmetric points over a line, that is described
    # with the following equation
    # ax + by + c = 0
    den = 1.0/(a**2+b**2)
    Xs = []
    Ys = []
    for x,y in zip(X,Y):
        xl = den*(b**2*x-a*b*y-a*c)
        yl = den*(-a*b*x+a**2*y-b*c)
        Xs.append(2*xl-x)
        Ys.append(2*yl-y)
    return Xs,Ys

def generateSymmetries(DX, DY):
    # Create symmetric pattern
    DX[2] = np.flipud(-DX[1])
    DY[2] = np.flipud(DY[1])
    DX[3] = np.flipud(DX[1])
    DY[3] = np.flipud(-DY[1])
    DX[4] = np.flipud(-DX[1])
    DY[4] = np.flipud(-DY[1])

def getOffset(key):
    offsetX, offsetY = 0.0,0.0
    for i,k in enumerate(key):
        scale = 1.0/2**(i+1)
        k = int(k)
        if k%2==1:
            offsetX += -scale
        else:
            offsetX += +scale
        if k<3:
            offsetY += +scale
        else:
            offsetY += -scale
    return offsetX, offsetY

class Pattern(object):
    def __init__(self, rootPattern_X = [-0.5,-0.5,-0.75], rootPattern_Y = [+0.0,+0.25,+0.5]):
        self.level = 0
        Xs,Ys = symmetrize(a = -1.0, b = -1.0, c = 0.0, X = rootPattern_X, Y = rootPattern_Y)
        self.pattern_X = {1:np.append(rootPattern_X, np.flipud(Xs))}
        self.pattern_Y = {1:np.append(rootPattern_Y, np.flipud(Ys))}
        generateSymmetries(self.pattern_X,self.pattern_Y)
        Xs,Ys = symmetrize(a = +1.0, b = -1.0, c = 1.0, X = rootPattern_X[0:-1], Y = rootPattern_Y[0:-1])
        self.patternS_X = {1:np.append(rootPattern_X[0:-1], np.flipud(Xs))}
        self.patternS_Y = {1:np.append(rootPattern_Y[0:-1], np.flipud(Ys))}
        generateSymmetries(self.patternS_X,self.patternS_Y)
        patternE_X,patternE_Y = symmetrize(a = +1.0, b = +1.0, c = 0.0, X = self.patternS_X[1], Y = self.patternS_Y[1])
        self.patternE_X = {1:np.array(patternE_X)}
        self.patternE_Y = {1:np.array(patternE_Y)}
        generateSymmetries(self.patternE_X, self.patternE_Y)

class Steinhaus(object):
    def __init__(self, level = 6, rootPattern_X = [-0.5,-0.5,-0.75], rootPattern_Y = [+0.0,+0.25,+0.5]):
        self.level = level
        self.pattern = Pattern(rootPattern_X, rootPattern_Y)
        self.lines = {1:{str(k):self.get(k) for k in range(1,5)}}
        for n in range(2,self.level+1):
            self.generateLevel(n)
    def generateLevel(self, level = 2):
        self.lines[level] = {}
        for key,lines in self.lines[level-1].iteritems():
            self.lines[level].update({key+str(k):self.getFromKey(key+str(k), len(lines[0])) for k in range(1,5)})
    def get(self, id, idParent = 0, level = 1, offset = (0.0, 0.0), nParent = 1):
        scale = 1.0/2**(level-1)
        if (id == (5-idParent)) or (nParent==2 and idParent==id):
            return [[scale*self.pattern.patternS_X[id]+offset[0], scale*self.pattern.patternE_X[id]+offset[0]],\
                    [scale*self.pattern.patternS_Y[id]+offset[1], scale*self.pattern.patternE_Y[id]+offset[1]]]
        else:
            return [scale*self.pattern.pattern_X[id]+offset[0]], [scale*self.pattern.pattern_Y[id]+offset[1]]
    def getFromKey(self, key, nParent = 1):
        return self.get(id = int(key[-1]), idParent = int(key[-2]), level = len(key), offset = getOffset(key[:-1]), nParent = nParent)
    def makePlot(self, outputFilename = r'Steinhaus.svg', level = 1, plotGrid = False, randomColor = False):
        rc('grid', linewidth = 1, linestyle = '-', color = '#a0a0a0')

        fig = figure()
        ax = fig.add_axes([0.12, 0.12, 0.76, 0.76])
        grid(plotGrid)
        for lines in self.lines[level].itervalues():
            for lineX,lineY in zip(lines[0],lines[1]):
                if randomColor:
                    color = [np.random.random() for _ in range(3)]
                else:
                    color = 'k'
                ax.plot(lineX, lineY, lw = 1, ls = '-', color = color)
        xlimMin, xlimMax = (-1.0, +1.0)
        ylimMin, ylimMax = (-1.0, +1.0)
        ax.set_xlim((xlimMin, xlimMax))
        ax.set_ylim((ylimMin, ylimMax))
        ax.set_aspect('equal')
        ax.set_xticks([])
        ax.set_yticks([])
        fig.savefig(outputFilename)
        fig.show()

def main(\
    TopLeftPattern_X = [-0.5,-0.3,-0.6,-0.75,-0.9],\
    TopLeftPattern_Y = [+0.0,+0.25,+0.1,0.6,+0.85],
    nLevel = 6):
    s = Steinhaus(rootPattern_X = TopLeftPattern_X, rootPattern_Y = TopLeftPattern_Y, level = nLevel)
    for i in range(1,s.level+1):
        s.makePlot(outputFilename = r'Steinhaus_{0}.svg'.format(i), level = i, randomColor = False)
        s.makePlot(outputFilename = r'Steinhaus_{0}.png'.format(i), level = i, randomColor = False)

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='Generate a space filling curve based a user defined pattern.')
    parser.add_argument('--px', nargs = '+', type = float, help='X cordinates of the user defined pattern')
    parser.add_argument('--py', nargs = '+', type = float, help='Y cordinates of the user defined pattern')
    parser.add_argument('--level', type = int, help='Number of recursion level', default = 6)
    args = parser.parse_args()
    if ((args.px is None or len(args.px)==0) and (args.py is None or len(args.py)==0)):
        TopLeftPattern_X, TopLeftPattern_Y = [-0.5,-0.5,-0.75], [+0.0,+0.25,+0.5]
        # TopLeftPattern_X, TopLeftPattern_Y = [-0.5,-0.3,-0.6,-0.75,-0.9], [+0.0,+0.25,+0.1,0.6,+0.85]
    else:
        TopLeftPattern_X, TopLeftPattern_Y = args.px, args.py
    if (len(TopLeftPattern_X)!=len(TopLeftPattern_Y)):
        raise Exception('X and Y cordinates should have the same number of elements')
    nLevel = args.level
    main(TopLeftPattern_X, TopLeftPattern_Y, nLevel)