import numpy as np
import sympy as sp
import pandas as pd
import math


# A = 3N * 3N matrix
# N = total layers
# serieslist = list of values in series
# S = series layers
# P = parallel layers
# x = iteration variable
#b,d,f,l,r=sp.symbols("b,d,f,l,r")

#create array of R symbolic values?
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

B=np.zeros((int(3*N),int(1)))


b = float(input('Layer width in cm:'))/100
f = float(input('Operating frequency in MHz:'))*1000000
d = 2/((2*math.pi*f)*(4*math.pi*math.pow(10,-7))*(1.68*math.pow(10,-8)))
l = float(input('Turn length in cm:'))/100
r = float(input('Layer spacing in cm:'))/100

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
	A[j,x-1] = 1
	j=j+1
	if j > S:
		break


for x in range(1,N+1):
	 z = N
	 A[j,x-1] = -1
	 A[j,z+2*(x-1)]=b # A[j][z+2*x-2]
	 A[j,z+2*(x-1)+1]=b #A[j][z+2*x-1]
	 j=j+1


A[j,N] = 1
j=j+1

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
			r_count = r_range - k -1 + parallelList[x]
		else:
			r_count = r_range
		A[j,k] = r_count*r*l/b

	A[j,N + 2*parallelList[x] - 1] = d/2
	A[j,N + 2*parallelList[x+1] - 2] = -d/2
	j=j+1

Ip = sp.symbols('Ip')

C = sp.zeros(int(3*N),1)
for x in parallelList:
    C[z,0] = Ip
    z+=1

print(A)
df = pd.DataFrame (A)

# save to xlsx file

filepath = 'table.csv'

df.to_csv(filepath, index=False)
