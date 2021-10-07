import numpy as np
import sympy

x = 1
s = int(input('Enter the amount of layers your transformer has:'))
if(s==0):
    quit() 
z = np.zeros(s)
serieslist = []
while 1:
    x = int(input('Enter, one by one, a series of layer #\'s that are in series: (sentinel is 0)'))
    if(x==0): break
    if x in serieslist:
        print("Already entered this layer #, please enter another layer #")
    elif((x<0) or (x>s)):
        print("Out of bounds with range, layer not counted; please enter another value")
    else:
        serieslist.append(x)
print(serieslist)
serieslist.sort()
for x in serieslist:
    f=np.zeros(s)
    f[x-1]=1
    z=np.vstack([z,f])
z = np.delete(z,0,0)
print(z)
