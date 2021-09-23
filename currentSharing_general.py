import numpy as np
import sympy as sp
import pandas as pd
import math

def current_sharing_numeric(N, pl, sl, b, f, l, r, N_turns = 1, Ip = 1):
    '''
    Evaluates current sharing within the specified layer structure & dimensions.

    Parameters:
    -----------
    N : int
        Total layer number.
    pl : list
        A valid layer list representing the primary winding.
    sl : list
        A valid layer list representing the secondary winding. Elements in the sl should not be in the pl.
    b : float
        Layer width (m)
    f : int
        Operating frequency (Hz)
    l : float
        Turn length (m)
    r : float or float list
        Distances between layers (m). Can either be a single value (in which case distances are assumed to be the 
        same) or a list of floats with N-1 entries.
    Ip : float
        Primary current value (A). If it is not specified, will be set to 1.
    N_turns : int list
        Number of turns of each layer. Should have N entries. If not specified, all layers will be assumed to
        have 1 layer each.

    Returns:
    --------
    X
        A 3*Nx1 vector, with the first N entries representing the current in layers 1 through N, and the 
        next 2*N entries representing the surface current densities in each layer (starting from the top
        of the structure and moving down).
    '''
    #calculate skin depth
    #d = 2*(1.68*math.pow(10,-8))/((2*math.pi*f)*(4*math.pi*pow(10,-7)))
    d=0
    bOverL = b/l

    #input validation
    if (N == 0): return 0

    if (valid_layer_list(sl,N) == 0): raise ValueError('Not a valid layer list.')

    if (N_turns == 1): N_turns = [1] * (N)
    if (len(N_turns) != (N)): raise ValueError('Not a valid turn count list.')

    #Current relationships based on structure
    SM = sp.Matrix([primary_current_identity(pl, N)])
    primaryEquations = traverse_layer_list(pl, N, d, bOverL, r, N_turns, [])
    if (primaryEquations != None): SM = SM.col_join(sp.Matrix(primaryEquations))
    secondaryEquations = traverse_layer_list(sl, N, d, bOverL, r, N_turns, [])
    if (secondaryEquations != None): SM = SM.col_join(sp.Matrix(secondaryEquations))

    #Layer level current identities
    KSummation = sp.zeros(N,3*N)
    for i in range(0,N):
        KSummation[i,i] = -1 * N_turns[i]
        KSummation[i, N + 2*i] = b
        KSummation[i, N + (2*i) + 1] = b
    SM = SM.col_join(KSummation)

    #Amperian Loops
    AmperianLoops = sp.zeros(N+1,3*N)
    for j in range(1,N):
        AmperianLoops[j, N + 2*j - 1] = 1
        AmperianLoops[j, N + 2*j] = 1
    AmperianLoops[0, N] = 1
    AmperianLoops[N, 3*N-1] = 1
    SM = SM.col_join(AmperianLoops)
    #print(SM)
    #Generate the LHS of the equality.
    C = sp.zeros(int(3*N),1)
    C[0] = Ip
    #print(SM)
    #print(sp.shape(SM))
    #Solve
    #print(SM)
    #print(np.array(SM))
    #print(np.array(SM, dtype=float))

    X = np.linalg.solve(np.array(SM, dtype=float),np.array(C, dtype=float))
    result = [0] * (3*N)
    for j in range(0,3*N):
        result[j] = X[j][0]
    
    return result

def current_sharing_symbolic(N, pl, sl, N_turns = 1,  distanceFlag = 0):
    '''
    Evaluates current sharing within the specified layer structure & dimensions.

    Parameters:
    -----------
    N : int
        Total layer number.
    pl : list
        A valid layer list representing the primary winding.
    sl : list
        A valid layer list representing the secondary winding. Elements in the sl should not be in the pl.
    N_turns : int list
        Number of turns of each layer. Should have N entries. If not specified, all layers will be assumed to
        have 1 layer each.
    distanceFlag: bool
        0 if all interlayer distances should be treated as the same. 1 otherwise.

    Returns:
    --------
    X
        A 3*Nx1 vector, with the first N entries representing the current in layers 1 through N, and the 
        next 2*N entries representing the surface current densities in each layer (starting from the top
        of the structure and moving down).
    '''
    b,d,l,Ip = sp.symbols('b,d,l,Ip')

    if not distanceFlag: 
        r = sp.symbols('r')
    else:
        r = [sp.symbols('r%d' % i) for i in range(N-1)] #symbolic list

    bOverL = b/l

    #input validation
    if (N == 0): return 0
    if (valid_layer_list(sl,N) == 0): raise ValueError('Not a valid layer list.')

    if (N_turns == 1): N_turns = [1] * (N)
    if (len(N_turns) != (N)): raise ValueError('Not a valid turn count list.')

    #Current relationships based on structure
    SM = sp.Matrix([primary_current_identity(pl, N)])
    primaryEquations = traverse_layer_list(pl, N, d, bOverL, r, N_turns, [])
    if (primaryEquations != None): SM = SM.col_join(sp.Matrix(primaryEquations))
    secondaryEquations = traverse_layer_list(sl, N, d, bOverL, r, N_turns, [])
    if (secondaryEquations != None): SM = SM.col_join(sp.Matrix(secondaryEquations))
    
    #Layer level current identities
    KSummation = sp.zeros(N,3*N)
    
    for i in range(0,N):
        KSummation[i,i] = -1
        KSummation[i, N + 2*i] = b
        KSummation[i, N + (2*i) + 1] = b
    SM = SM.col_join(KSummation)

    #Amperian Loops
    AmperianLoops = sp.zeros(N+1,3*N)
    for j in range(1,N):
        AmperianLoops[j, N + 2*j - 1] = 1
        AmperianLoops[j, N + 2*j] = 1
    AmperianLoops[0, N] = 1
    AmperianLoops[N, 3*N-1] = 1
    SM = SM.col_join(AmperianLoops)
    #print(SM)
    #print(sp.shape(SM))
    #Generate the LHS of the equality.
    Ip = sp.symbols('Ip')
    C = sp.zeros(int(3*N),1)
    C[0] = Ip

    #Solve
    M = sp.linsolve((sp.Matrix(SM),sp.Matrix(C)))
    X = sp.simplify(M.subs(d,0))
    
    return X

def valid_layer_list(node, N):
    '''
    Evaluates whether a layer list is valid. 

    Parameters:
    -----------
    node : int or list
        A potential layer list.
    N : int
        Total number of layers.

    Returns:
    --------
    1 if the layer list is valid, and 0 if it is not valid. A valid layer list can have three 
    acceptable entries: an integer (of value between 1 and N inclusive), a series list (['s', 
    valid list, valid list]), or a parallel list (['p', valid list, valid list]).
    '''
    if (type(node) == int or len(node)==1):
        if (type(node) == list): node = node[0]
        if (node > N or node < 1): return 0
        else: return 1 #Base case.
    elif node[0] == 's': #Series connected node.
        if (len(node) != 3): return 0
        s1 = valid_layer_list(node[1],N)
        s2 = valid_layer_list(node[2],N)
        return (s1 and s2)
    elif node[0] == 'p': #Parallel connected node.
        if (len(node) != 3): return 0
        p1 = valid_layer_list(node[1],N)
        p2 = valid_layer_list(node[2],N)
        return (p1 and p2)
    else: return 0

def primary_current_identity(node, N):
    '''
    Returns a list representing a primary current equality.

    Parameters:
    -----------
    node : int or list
        A valid layer list or layer number.
    N : int
        Total number of layers

    Returns:
    --------
    identify
        A list representing a primary current equality, with the left hand side of the equality implied to be 
        nonzero
    '''
    identity = [0] * 3 * N
    a = I_node(node,[]) #Identify current in this node
    for j in a:
        identity[j-1] = 1
    return identity

def traverse_layer_list(node, N, d, bOverL, R, N_turns, array):
    '''
    Returns a list of lists, with each inner list representing either a Faraday loop between paralleled layers
    or a series current identity between series connected layers.

    Parameters:
    -----------
    node : int or list
        A valid layer list or layer number.
    N : int
        Total number of layers.
    d : float
          Skin depth
    bOverL : float
        Ratio of layer width to turn length.
    R : float or float list
        Distances between layers. Can either be a single value (in which case distances are assumed to be the 
        same) or a list of floats with N-1 entries.
    N_turns : int list
        Number of turns of each layer. Should have N entries. If not specified, all layers will be assumed to
        have 1 layer each.
    array : list
        Top level calls should pass in an empty list.

    Returns:
    --------
    array
        a list of lists, with each inner list representing either a Faraday loop between paralleled layers
        or a series current identity between series connected layers.

    '''
    if (type(node) == int or len(node)==1):
        return None #Base case.
    elif node[0] == 's': #Series connected node.
        a = I_node(node[1],[])
        b = I_node(node[2],[])
        array.append(series_equation(a,b,N))
        traverse_layer_list(node[1], N, d, bOverL, R, N_turns, array)
        traverse_layer_list(node[2], N, d, bOverL, R, N_turns, array)
        return array
    elif node[0] == 'p': #Parallel connected node.
        a = node_contains(node[1])
        b = node_contains(node[2])
        array.append(faraday_equation(a,b,N,d,bOverL, N_turns, R))
        traverse_layer_list(node[1], N, d, bOverL, R, N_turns, array)
        traverse_layer_list(node[2], N, d, bOverL, R, N_turns, array)
        return array
    else: return 0

def I_node(node, array):
    '''
    Given a layer list, returns a list of layers directly connected to the top level node.

    Parameters:
    -----------
    node : int or list
        A valid layer list or layer number.
    array : list
        Top level calls of this function should pass an empty list.

    Returns:
    --------
    array
        List of layers directly connected to the top level node - e.g. if the top level node specifies
        three layers in parallel (each of which has several layers in series), it will return the indices 
        of each of the three parallel layers. If the node specifies two layers in series, it will return
        the first layer.
    '''
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

def node_contains(node):
    '''
    Returns the number of a layer that is contained by the node given.

    Parameters:
    -----------
    node : int or list
        A valid layer list or layer number.

    Returns:
    --------
    val
        Int representing a layer number that is contained by this node.
    '''
    if type(node) == int:
        return node
    elif (node[0] == 'p' or node[0] == 's'):
        return node_contains(node[1])
    else: return 0


def series_equation(a,b,N):
    '''
    Generates a list representing a current equality between layer sets a and b.

    Parameters:
    -----------
    a : int or int list
        The first layer set to be connected.
    b : int or int list
        The second layer set to be connected. a != b
    N : int
        The total number of layers. N > a,b

    Returns:
    --------
    series
        List of length 3*N that specifies a series connection. First N entries are the coefficients multiplied
        by I_1 to I_N, and the next 2*N entries are the coefficients to be multiplied by K_1T through K_NB. The 
        right hand side of the equation is assumed to be zero.
    '''

    if(a==b):
        raise ValueError('Must specify two different layers.')
    if(max(a)>N or max(b)>N):
        raise ValueError('Layer out of range.')

    series = [0] * (3*N)
    for j in a:
        series[j-1] = 1
    for k in b:
        series[k-1] = -1
    return series

def faraday_equation(a,b,N,d, bOverL, N_turns, r=1):
    '''
    Generates a list representing a Faraday Loop taken between layer numbers a and b.

    Parameters:
    ----------
    a : int or int list of len 1
        The first layer in the Faraday loop.
    b : int or int list of len 1
        The second layer in the Faraday loop. a != b.
    N : int
        The total number of layers. N > a, b.
    d : float
        Skin depth 
    bOverL: float
        Ratio of layer width to turn length.
    r : float or float list
        Distances between layers. Can either be a single value (in which case distances are assumed to be the 
        same) or a list of floats with N-1 entries.
    N_turns : int list
        Number of turns of each layer. Should have N entries. If not specified, all layers will be assumed to
        have 1 layer each.

    Returns:
    --------
    faraday
        List of length 3*N that specifies a Faraday loop. First N entries are the coefficients multiplied by
        I_1 to I_N, and the next 2*N entries are the coefficients to be multiplied by K_1T through K_NB. The 
        right hand side of the equation is assumed to be zero.
    '''
    if(type(a)==list): a = a[0]
    if(type(b)==list): b = b[0]

    if(a==b):
        raise ValueError('Must specify two different layers.')
    if(a>N or b>N):
        raise ValueError('Layer out of range.')

    faraday = [0] * (3*N)
    if (type(r)==int or type(r)==float or type(r)==sp.core.symbol.Symbol):
        r=[r] * int(N)
    elif (len(r) != (N-1)):
        raise ValueError('Incorrect r array length.')

    for i in range(0,b-1):
        val = 0
        for j in range(max(a-1,i),b-1):
            val = val + r[j]
        faraday[i] = val*bOverL*N_turns[i]
    
    faraday[N + a*2 - 1] = d/2
    faraday[N + b*2 - 2] = -d/2
    return faraday

#stack=(1, ['s', 2, ['s', ['p', 3, 4], ['p', 5, 6]]])
#stack=(1, ['s', 2, ['s', 3, ['s', ['p', 6, ['p', 7, 8]], ['p', 4, 5]]]])
#print(current_sharing_symbolic(8, stack[0], stack[1]))
#print(current_sharing_numeric(8, stack[0], stack[1], .02, 1000000, .2, .001))
