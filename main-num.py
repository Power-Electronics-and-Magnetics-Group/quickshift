import numpy as np
import sympy as sp
import pandas as pd
import math

"""

Accepts the following parameters, all in standard units:
    N = number of layers
   sl = a list-type collection of layer #'s in series with each other
    b = Layer width (in m)
    f = Operating frequency (in Hz)
    l = Turn length (in m)
    r = Layer spacing (in m) -- assumption that all layers are evenly spaced by one value.
    Ip = parallel current in (A)
 Returns a list of 3*N elements, where N is the number of layers.

"""

def current_sharing(N, sl, b, f, l, r, Ip):
    d = 2/((2*math.pi*f)*(4*math.pi*pow(10,-7))*(1.68*math.pow(10,-8)))
    if (N == 0): quit()
    A = np.zeros((int(3*N),int(3*N)))
    serieslist = sl
    S = len(serieslist)
    P = N - S

    parallelList = list(range(1,N+1))
    for i in serieslist:
        if i in parallelList:
            parallelList.remove(i)
    j = 0
    for x in serieslist:
        A[j,x-1] = 1
        j=j+1
        if j > S:
            break

    for x in range(1,N+1):
        z = N
        A[j,x-1] = -1
        A[j,z+2*(x-1)]=b
        A[j,z+2*(x-1)+1]=b
        j=j+1

    A[j,N] = 1
    j = j+1

    for x in range(0,N-1):
        A[j,N+2*x+1]=1
        A[j,N+2*x+2]=1
        j=j+1
    A[j,3*N-1]=1
    j=j+1

    for x in range(0,P-1):
        r_range = parallelList[x+1] - parallelList[x]

        for k in range(0,parallelList[x+1]-1):
            if (k+1) > parallelList[x]:
                r_count = r_range - k - 1 + parallelList[x]
            else:
                r_count = r_range
            A[j,k] = r_count*r*l/b
        A[j,N+2*parallelList[x]-1]=d/2
        A[j,N+2*parallelList[x+1]-2]=-d/2
        j=j+1
    
    z=0
    C=np.zeros((int(3*N),1))
    for x in parallelList:
        C[z,0] = Ip
        z+=1

    M = np.linalg.solve(np.matrix(A),np.matrix(C))
    return M
print(current_sharing(8,[2,3,4,7],80,23,48,89,90))

