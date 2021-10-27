import numpy as np
import sympy as sp
import pandas as pd
import math
from stackupClasses import Layer, SeriesNode, ParallelNode, Node, Stackup

def current_sharing_numeric(stack, b, f, l, r, Ip = 1):
    '''
    Evaluates current sharing within the specified layer structure & dimensions.

    Parameters:
    -----------
    stack : stackup object
        Valid stackup
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

    Returns:
    --------
    X
        A 3*Nx1 vector, with the first N entries representing the current in layers 1 through N, and the 
        next 2*N entries representing the surface current densities in each layer (starting from the top
        of the structure and moving down).
    '''
    N = stack.N

    #calculate skin depth
    d = 2*(1.68*math.pow(10,-8))/((2*math.pi*f)*(4*math.pi*pow(10,-7)))

    bOverL = b/l

    #input validation
    if (not stack.validStackup()): raise ValueError('Not a valid layer list.')

    N_turns = stack.turnCount()

    #Current relationships based on structure
    SM = sp.Matrix([primary_current_identity(stack.primary, N)])
    primaryEquations = traverse_layer_list(stack.primary, N, d, bOverL, r, N_turns, [])
    if (primaryEquations != None): SM = SM.col_join(sp.Matrix(primaryEquations))

    secondaryEquations = traverse_layer_list(stack.secondary, N, d, bOverL, r, N_turns, [])
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

    X = np.linalg.solve(np.array(SM, dtype=float),np.array(C, dtype=float))
    result = [0] * (3*N)
    for j in range(0,3*N):
        result[j] = X[j][0]
    
    return result

def current_sharing_symbolic(stack,  distanceFlag = 0):
    '''
    Evaluates current sharing within the specified layer structure & dimensions.

    Parameters:
    -----------
    stack : stackup object
        Valid stackup
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
    N = stack.N

    if not distanceFlag: 
        r = sp.symbols('r')
    else:
        r = [sp.symbols('r%d' % i) for i in range(N-1)] #symbolic list

    bOverL = b/l

    #input validation
    if (not stack.validStackup()): raise ValueError('Not a valid layer list.')

    N_turns = stack.turnCount()

    #Current relationships based on structure
    SM = sp.Matrix([primary_current_identity(stack.primary, N)])
    primaryEquations = traverse_layer_list(stack.primary, N, d, bOverL, r, N_turns, [])
    if (primaryEquations != None): SM = SM.col_join(sp.Matrix(primaryEquations))

    secondaryEquations = traverse_layer_list(stack.secondary, N, d, bOverL, r, N_turns, [])
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

    #Generate the LHS of the equality.
    Ip = sp.symbols('Ip')
    C = sp.zeros(int(3*N),1)
    C[0] = Ip

    #Solve
    M = sp.linsolve((sp.Matrix(SM),sp.Matrix(C)))
    X = sp.simplify(M.subs(d,0))
    
    return X

def primary_current_identity(node, N):
    '''
    Returns a list representing a primary current equality.

    Parameters:
    -----------
    node : node or Layer
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
    a = node.I_node() #Identify current in this node
    for j in a:
        identity[j-1] = 1
    return identity

def traverse_layer_list(node, N, d, bOverL, R, N_turns, array):
    '''
    Returns a list of lists, with each inner list representing either a Faraday loop between paralleled layers
    or a series current identity between series connected layers.

    Parameters:
    -----------
    node : Node or Layer object.
        A valid Node or Layer object.
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
    if (node.kind == 'L'):
        return None #Base case.
    elif (node.kind == 'S'): #Series connected node.
        a = node.left.I_node()
        b = node.right.I_node()
        array.append(series_equation(a,b,N))
        traverse_layer_list(node.left, N, d, bOverL, R, N_turns, array)
        traverse_layer_list(node.right, N, d, bOverL, R, N_turns, array)
        return array
    elif (node.kind == 'P'): #Parallel connected node.
        a = node.left.hasLayer()
        b = node.right.hasLayer()
        if (b < a):
            temp = b
            b = a
            a = temp
        array.append(faraday_equation(a,b,N,d,bOverL, N_turns, R))
        traverse_layer_list(node.left, N, d, bOverL, R, N_turns, array)
        traverse_layer_list(node.right, N, d, bOverL, R, N_turns, array)
        return array
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
        raise ValueError('Must specify two different layer sets.')
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
    a : int
        The first layer in the Faraday loop.
    b : int
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