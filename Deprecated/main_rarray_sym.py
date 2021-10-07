import numpy as np
import sympy as sp
import pandas as pd
import math
np.set_printoptions(threshold=np.inf)

"""
    This case makes no assumptions on the layer spacing between each pair of layers. 
    Accepts the following parameters:
        N = number of layers
       sl = list-type collection of layer #'s in series with each other.
    Returns a tuple (immutable collection) of 3*N symbolic expressions.

"""
def current_sharing(N, sl):
    b,d,l,r = sp.symbols('b,d,l,r')
    if (N==0): quit()
    serieslist = sl 
    S = len(serieslist)
    P = N - S

    parallelList = []
    SM = sp.zeros(int(3*N),int(3*N))
    numR = N-1
    R = [sp.symbols('r%d' % i) for i in range(numR)] #symbolic list
    R_distances = [0] * numR #empty list in case you want to solve symbolic

    for s in range(1,N+1):
        if (s in serieslist) == False:
            parallelList.append(s)
    j = 0
    for x in serieslist:
	    SM[j,x-1] = 1
	    j=j+1
	    if j > S: 
		    break


    for x in range(1,N+1):
	    z = N
	    SM[j,x-1] = -1
	    SM[j,z+2*(x-1)]=b # A[j][z+2*x-2]
	    SM[j,z+2*(x-1)+1]=b #A[j][z+2*x-1]
	    j=j+1


    SM[j,N] = 1
    j=j+1

    for x in range(0,N-1):
	    SM[j,N+2*x+1]=1
	    SM[j,N+2*x+2]=1
	    j=j+1
    SM[j,3*N-1]=1
    j=j+1

    for x in range(0,P-1):
        r_range = parallelList[x+1] - parallelList[x]
        for k in range(0,parallelList[x+1] - 1):
            r_start = max(parallelList[x]-1,k)
            for g in range(r_start, parallelList[x+1]-1):
                SM[j,k] = SM[j,k] + R[g]
            SM[j,k] = SM[j,k]*l/b

        SM[j,N + 2*parallelList[x] - 1] = d/2
        SM[j,N + 2*parallelList[x+1] - 2] = -d/2
        j=j+1

    Ip = sp.symbols('Ip')
    z = 0
    C = sp.zeros(int(3*N),1)
    for x in parallelList:
        C[z,0] = Ip
        z+=1

    M = sp.linsolve((sp.Matrix(SM),sp.Matrix(C)))
    X = sp.simplify(M.subs(d,0))
    return X.args[0]

F = current_sharing(8,[2,3,4,7]) 
print(F)
