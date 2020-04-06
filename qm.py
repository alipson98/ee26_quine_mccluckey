# Quine Mccluskey logic minimization
# Author: Adam Lipson
# EE26 Spring 2020

import os.path
from os import path
import sys
import string
import re
import math

class Term:
    def __init__(self, id, dontcare):
        self.id = id
        self.dontcare = dontcare
    def __repr__(self):
        return 'id:'+str(self.id) + ' dc: '+str(self.dontcare)
    def __eq__(self, other):
        if type(other) == Term:
            return self.id == other.id
        else:
            return False

class Cube:
    def __init__(self, terms):
        self.terms = terms
        self.n = math.log2(len(terms))
        self.diffs = []
        self.checked = False


def strExtract(instring):
    bothStrings = instring.split('d')
    mString = bothStrings[0]
    dontCares = []
    minterms = []
    if len(bothStrings) > 1:
        dString = bothStrings[1]
        dSplit = dString.split(',')
        dNums = re.findall("(\\d+)", dString)
        for i in range(len(dSplit)):
            dontCares.append(int(dNums[i]))

    mSplit = mString.split(',')
    mNums = re.findall("(\\d+)", mString)
    # print("mNums: ", mNums)

    for i in range(len(mSplit)):
        minterms.append(int(mNums[i]))
    return minterms, dontCares

def countOnes(n):
    cnt = 0
    while n != 0:
        n = n & (n-1)
        cnt += 1
    
    return cnt

def makeTable(minterms, dontcares, maxNum):
    table = []
    # print(maxNum)
    for i in range(math.ceil(math.log2(maxNum)) + 1):
        # print(i)
        table.append([])

    while minterms:
        curr = minterms.pop()
        term = Term(curr, False)
        table[countOnes(curr)].append(term)

    while dontcares:
        curr = dontcares.pop()
        term = Term(curr, True)
        table[countOnes(curr)].append(term)
    
    for i in range(len(table)):
        table[i] = sorted(table[i], key=lambda Term: Term.id)
    
    cubeTable = []
    for i in range(math.ceil(math.log2(maxNum)) + 1):
        cubeTable.append([])
        for j in range(len(table[i])):
            cubeTable[i].append(Cube(table[i][j]))

    return cubeTable

def canCombine(cube1, cube2):
    if cube1.diffs:
        diffsEqual = sorted(cube1.diffs) == sorted(cube2.diffs)

    else:
        diff = cube1.terms[0].id - cube2.terms[0].id
        return countOnes(diff) == 1

# combine cubes
# args: table of cubes all of the same order
# rets: list of PIs, list of next order cubes
def combineCubes(table):
    pis = []
    for i in range(len(table) - 1):
        for j in range(len(table[i])):
            for k in range(len(table[i+1])):
                if table[i][j].diffs:
                    if 
                print(k)


    return pis

def main():
    if path.exists("input.txt") == False:
        print("input.txt not found! aborting...\n")
        sys.exit(1)

    fp = open("input.txt")
    inlines = fp.read().splitlines()
    fp.close()

    for i in inlines:
        print(i)
        minterms, dontcares = strExtract(i)
        maxNum = max(minterms)
        if (dontcares and (max(dontcares) > max(minterms))):
            maxNum = max(dontcares)
        qmTable = makeTable(minterms, dontcares, maxNum)
        print(qmTable)
        test = combineCubes(qmTable)
    

if __name__ == "__main__":
    main()