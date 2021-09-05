import numpy as np
from itertools import combinations
import pprint
from scipy.special import comb

'''

    Most basic fundamental case == round integer turns ratio of integer "turnsRatio" : 1. 
    For example, 3:1 == 3:1 != 6:2 != 1.5:0.5
    Returns a hash-table of n C r elements, where n = N and r = turnsRatio. ("N" choose "turnsRatio")
'''


def subset(array, num):
    return list(combinations(array,num))
def stackups(N, turnsRatio):
    possibilities = int(comb(N,turnsRatio))
    layerList = list(range(1,N+1))

    # FOR RIGHT NOW
    primaryTurns = turnsRatio # series
    secondaryTurns = 1 # parallel

    seriesList = subset(list(range(1,N+1)),primaryTurns)
    for i in range(0,len(seriesList)):
        seriesList[i]=list(seriesList[i])

    parallelList = []
    for i in range(0,possibilities):
        parallelList.append(list(range(1,N+1)))
        parallelList[i]=list(set(parallelList[i])^set(seriesList[i]))
    stackup_hash = {tuple(key): tuple(value) for key, value in zip(tuple(seriesList),tuple(parallelList))}  
    return stackup_hash

pprint.pprint(stackups(8,3))
