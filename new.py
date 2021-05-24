import numpy as np
import sympy

x = 1
s = int(input('Enter the amount of layers your transformer has:'))
z = np.zeros(s)
while 1:
    x = int(input('Enter, one by one, a series of layer #\'s that are in series: (sentinel is 0)'))
    if(x==0): break
    f = np.zeros(s)
    f[x-1] = 1
    z = np.vstack([z,f])

z = np.delete(z,0,0)
print(z)
