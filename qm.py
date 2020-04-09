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
    def __init__(self, terms, binStr, order):
        self.terms = terms
        self.binStr = binStr
        self.order = math.log2(len(terms))
        self.checked = False
        self.terms.sort()

    def __str__(self):
        nums = ", ".join([str(num) for num in self.terms])
        return f"m({nums}) = {self.binStr}"
    
    def __eq__(self, other):
        if type(other) != Cube:
            return False
        
        return (self.terms == other.terms and self.binStr == other.binStr)
    
    def comb(self, other):
        if self == other: 
            return None

        diff = 0
        combStr = ""

        for i in range(len(self.binStr)):
            if self.binStr[i] != other.binStr[i]:
                combStr += "X"
                diff += 1
            else:
                combStr += self.binStr[i]
            
            if diff > 1:
                return None
        
        return Cube(self.terms + other.terms, combStr, self.order + 1)

# strExtract
# param: input string according to the input specifications
# note that there can be no spaces in the input
    # invalid input is an UNCHECKED RUNTIME ERROR
# return: list of numerical minterms, list of numerical maxterms
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

# def countOnes(n):
#     cnt = 0
#     while n != 0:
#         n = n & (n-1)
#         cnt += 1
    
#     return cnt

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
        numVars = math.ceil(math.log2(maxNum))
        # qmTable = makeTable(minterms, dontcares, maxNum)
        # print(qmTable)
        # test = combineCubes(qmTable)
    

if __name__ == "__main__":
    main()