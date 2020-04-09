# Quine Mccluskey logic minimization
# Author: Adam Lipson
# EE26 Spring 2020

import os.path
from os import path
import sys
import string
import re
import math
from itertools import chain, combinations

# class Term:
#     def __init__(self, id, dontcare):
#         self.id = id
#         self.dontcare = dontcare
#     def __repr__(self):
#         return 'id:'+str(self.id) + ' dc: '+str(self.dontcare)
#     def __eq__(self, other):
#         if type(other) == Term:
#             return self.id == other.id
#         else:
#             return False

# Cube class
# used for representing a group of terms in an n-cube
# only method is for combining with another cube
class Cube:
    def __init__(self, terms, binStr, order, numVars):
        self.terms = terms
        self.binStr = binStr
        self.order = math.log2(len(terms))
        self.numVars = numVars
        self.checked = False
        self.terms.sort()

    def __repr__(self):
        nums = ", ".join([str(num) for num in self.terms])
        return f"({nums}) = {self.binStr}"

    def __str__(self):
        nums = ", ".join([str(num) for num in self.terms])
        return f"({nums}) = {self.binStr}"
    
    def __eq__(self, other):
        if type(other) != Cube:
            return False
        
        return (self.terms == other.terms and self.binStr == other.binStr)
    
    # combine this cube with another
    # returns the result of the combination as a new cube, does not alter self
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
        
        return Cube(self.terms + other.terms, combStr, self.order + 1, self.numVars)

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

def countOnes(n):
    cnt = 0
    while n != 0:
        n = n & (n-1)
        cnt += 1
    
    return cnt

# getBinary
# get a string with the binary representation of an integer in numVars variables
# pads with leading zeroes
def getBinary(n, numVars):
    return bin(n)[2:].rjust(numVars, '0')

def buildTable(terms, numVars):
    table = []

    # build a 2d list (is there a better way to do this in python?)
    for _ in range(numVars + 1):
        table.append([])
    
    for i in terms:
        idx = countOnes(i)
        table[idx].append(Cube([i], getBinary(i, numVars), 0, numVars))
    
    return table

# recursively find the PIs of a given list of terms
# returns a list of Cubes
def findPIs(table):
    if len(table) == 1:
        return table[0]
    
    unused = []
    comparisons = range(len(table) - 1)
    new_cubes = [[] for c in comparisons]

    for idx in comparisons:
        group1 = table[idx]
        group2 = table[idx + 1]

        for t1 in group1:
            for t2 in group2:
                t3 = t1.comb(t2)

                if t3 != None:
                    t1.checked = True
                    t2.checked = True
                    if t3 not in new_cubes[idx]:
                        new_cubes[idx].append(t3)

    # get all unused terms after this round of combination
    for group in table:
        for t in group:
            if not t.checked:
                unused.append(t)

    # recurse: also get the unused terms in the next
    for t in findPIs(new_cubes):
        if not t.checked and t not in unused:
            unused.append(t)
    
    return unused

# given a reduced table, find the fewest number of PI's required to cover all
# remaining terms
# this isn't exactly Petrick's method. It minimizes the number of terms rather
# than exact hardware cost, but it is a good approximation
def solveReducedTable(pis, terms):
    piPowerSet = list(chain.from_iterable(list(combinations(pis, r)) for r in range(1, len(pis)+1)))
    minimalCover = None
    for piSet in piPowerSet:
        coveredTerms = [False for idx in range(len(terms))]
        # coveredTerms = []
        for pi in piSet:
            for i in range(len(terms)):
                if terms[i] in pi.terms:
                    coveredTerms[i] = True
        
        
        if all(coveredTerms):
            if minimalCover == None:
                minimalCover = piSet
            elif len(piSet) < len(minimalCover):
                minimalCover = piSet

    minimalList = list(minimalCover)
    
    return minimalList

def findMinimalCover(pis, terms):
    # start by finding the essential PI's
    essential = []
    reducedPIs = pis
    remainingTerms = terms
    for term in terms:
        count = 0
        last = None
        for cube in pis:
            for t in cube.terms:
                if t == term:
                    count += 1
                    last = cube
                
        if count == 1:
            essential.append(last)
            reducedPIs.remove(last)
            # remainingTerms.remove(term)
            for PIterm in last.terms:
                if PIterm in remainingTerms:
                    remainingTerms.remove(PIterm)
    
    # if reduced PI table is empty, just return the essential PIs
    # print(essential)
    if not reducedPIs:
        return essential
    
    # otherwise, solve the reduced table
    return essential + solveReducedTable(pis, terms)

def printSOP(cubes, numVars):
    outstr = "="
    for cube in cubes:
        currVar = 65 # ASCII 'A'
        for i in range(numVars):
            if cube.binStr[i] == "1":
                outstr += chr(currVar)
            elif cube.binStr[i] == "0":
                outstr += chr(currVar) + "'"
            currVar += 1
        outstr += "+"
    # print(cubes)
    print(outstr[:-1])

def printPOS(cubes, numVars):
    outstr = "="
    for cube in cubes:
        # start = True
        currVar = 65
        outstr += "("
        for i in range(numVars):
            if cube.binStr[i] == "0":
                outstr += chr(currVar) + "+"
            elif cube.binStr[i] == "1":
                outstr += chr(currVar) + "'+"
            currVar += 1
        outstr = outstr[:-1]
        outstr += ")"

    # print(cubes)
    print(outstr)




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

        maxterms = []
        for i in range(2 ** numVars):
            if (i not in minterms) and (i not in dontcares):
                maxterms.append(i)

        
        minQmTable = buildTable(sorted(minterms + dontcares), numVars)
        minPIs = findPIs(minQmTable)
        minEssential = findMinimalCover(minPIs, minterms)
        printSOP(minEssential, numVars)


        if maxterms:
            maxQmTable = buildTable(sorted(maxterms + dontcares), numVars)
            maxPIs = findPIs(maxQmTable)
            maxEssential = findMinimalCover(maxPIs, maxterms)
            printPOS(maxEssential, numVars)
        
        print("")
        
    

if __name__ == "__main__":
    main()