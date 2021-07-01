import numpy as np
import sympy as sp
import pandas as pd
import math
np.set_printoptions(threshold=np.inf)

# A = 3N * 3N matrix
# N = total layers
# serieslist = list of values in series
# S = series layers
# P = parallel layers
# x = iteration variable 
b,d,f=sp.symbols("b,d,f")
x=1
N = int(input('Enter the amount of TOTAL LAYERS your transformer has: '))
if(N==0):
    quit()
A=np.zeros((int(3*N),int(3*N)))
SM=sp.Matrix(A)
serieslist = []

while 1:
    x = int(input('Enter, one by one, a series of layer #\'s that are in series: (sentinel is 0)'))
    if(x==0): break
    if x in serieslist:
        print("Already entered this layer #, please enter another layer #")
    elif((x<0) or (x>N)):
        print("Out of bounds with range, layer not counted; please enter another value")
    else:
        serieslist.append(x)
#print(serieslist)
serieslist.sort()

#b = float(input('Layer width in cm:'))/100; 
#f = float(input('Operating frequency in MHz:'))/1000000
#d = 2/((2*math.pi*f)*(4*math.pi*math.pow(10,-7))*(1.68*math.pow(10,-8)));

parallelList = list(range(1,N+1))
for i in serieslist:
	if i in parallelList:
		parallelList.remove(i)

#print(parallelList)
S = len(serieslist)
P = N - S
# series identities == all equal to I_p
j = 0
for x in serieslist:
    SM[j,x] = 1
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
    for k in range(0,parallelList[x]):
        SM[j,k] = k + 1
    SM[j,N + 2*parallelList[x] - 1] = d/2
    SM[j,N + 2*parallelList[x+1] - 2] = -d/2
    j=j+1

var_b = float(input('Layer width in cm:'))/100; 
var_f = float(input('Operating frequency in MHz:'))*1000000
var_d = 2/((2*math.pi*f)*(4*math.pi*math.pow(10,-7))*(1.68*math.pow(10,-8)))

SM.subs(b, var_b)
SM.subs(d, var_d)
sp.pprint(SM)

#df = pd.DataFrame (A)

## save to xlsx file

#filepath = 'table.csv'

#df.to_csv(filepath, index=False)
