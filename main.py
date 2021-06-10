import numpy as np
import sympy as sp
import pandas as pd
np.set_printoptions(threshold=np.inf)

# A = 3N * 3N matrix
# N = total layers
# serieslist = list of values in series
# S = series layers
# P = parallel layers
# x = iteration variable 

x=1
N = int(input('Enter the amount of TOTAL LAYERS your transformer has: '))
if(N==0):
    quit()
A=np.zeros((int(3*N),int(3*N)))
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
print(serieslist)
serieslist.sort()

S = len(serieslist)
P = N - S
# series identities == all equal to I_p
j = 0
for x in serieslist:
    A[j][x] = 1
    j=j+1
    if j > S: 
        break


for x in range(1,N+1):
     z = N
     A[j][x-1] = -1
     A[j][z+2*(x-1)]=2 # A[j][z+2*x-2]
     A[j][z+2*(x-1)+1]=2 #A[j][z+2*x-1]
     j=j+1


A[j][N] = 1
j=j+1

for x in range(0,N-1):
    A[j][N+2*x+1]=1
    A[j][N+2*x+2]=1
    j=j+1
A[j][3*N-1]=1

# test at the end 
#print(A)

df = pd.DataFrame (A)

## save to xlsx file

filepath = 'table.xlsx'

df.to_excel(filepath, index=False)

