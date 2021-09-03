import numpy as np
import sympy as sp
import pandas as pd
import math

"""

Accepts the following parameters:
    N = number of layers
   sl = 

    b = Layer width (in m)
    f = Operating frequency (in Hz)
    l = Turn length (in m)
    r = Layer spacing (in m) -- assumption that all layers are evenly spaced by one value.
    Ip = parallel current in (A)
 Returns a list of 3*N elements, where N is the number of layers.

"""

def current_sharing(N, sl, b, f, l, r, Ip):
    #calculate skin depth
    d = 2/((2*math.pi*f)*(4*math.pi*pow(10,-7))*(1.68*math.pow(10,-8)))

    #input validation
    if (N == 0): return 0
    if (valid_layer_list(sl,N) == 0): return 0

    a=series_equation([1,3,4],[5,6,7],8)
    
    return a

'''
Accepts:
    node = 
    N = total layer count

    Returns 1 if the layer list provided meets specifications. Returns 0 otherwise. 
'''
def valid_layer_list(list, N):
    #TO DO
    return 1

def traverse_layer_list(node, N, array):
    if type(node) == int:
        return None
    elif node[0] == 's':
        a = I_node(node[1])
        b = I_node(node[2])
        series_equation(a,b,N)
        traverse_layer_list(node[1], N, array)
        traverse_layer_list(node[2], N, array)
        return None
    elif node[0] == 'p':
        a = node_contains(node[1])
        b = node_contains(node[2])
        #faraday(a,b,N,r)
        traverse_layer_list(node[1], N, array)
        traverse_layer_list(node[2], N, array)
        return None
    else: return 0

'''
Accepts:
    node = 
    array = 

    Returns an array containing 
'''
def I_node(node, array):
    if type(node) == int: 
        array.append(node)
        return array
    elif node[0] == 'p':
        I_node(node[1],array)
        I_node(node[2],array)
        return array
    elif node[0] == 's':
        I_node(node[1],array)
        return array
    else: return 0

'''
Accepts:
    node = 

    Returns a layer value that is in node. 
'''
def node_contains(node):
    if type(node) == int:
        return node
    elif (node[0] == 'p' or node[0] == 's'):
        return node_contains(node[1])
    else: return 0

'''
Accepts:
    node = 

    
'''
def series_equation(a,b,N):
    series = [0] * (3*N)
    for j in a:
        series[j-1] = 1
    for k in b:
        series[k-1] = -1
    return series

'''
Accepts:
    node = 

    
'''
def faraday_equation(a,b,N):
    return 1


    
print(current_sharing(8,[2,3,4,7],80,23,48,89,90))

