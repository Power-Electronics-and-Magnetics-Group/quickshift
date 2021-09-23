import numpy as np
from itertools import combinations
from itertools import product
import pprint
from scipy.special import comb

def stackups(N, turnsRatio):
	'''
	Generates list of valid stackups for N layer transformer with supplied turns ratio. Maximum 1 turn per layer.

	Parameters:
	-----------
	N : int
		Number of turns.
	turnsRatio : int or float
		Desired turns ratio. 

	Returns:
	--------
	stackupList
		List of valid stackups.
	'''
	#Input Validation
	if (N <=2 or type(N) != int): 
		raise valueError('Invalid N')
	if (turnsRatio <= 0): 
		raise valueError('Invalid turns ratio')

	#TurnsRatio should be >= 1
	if (turnsRatio < 1): turnsRatio = 1/turnsRatio

	#Generate [1,...,N]
	layers = [0] * N
	for i in range(1, N+1):
		layers[i-1] = i

	#Generate valid turn pairs. 
	pairs = turnPairs(N, turnsRatio)

	stackupList =[]

	#Iterate over all the turn pairs
	for pair in pairs:
		primaryLayers = layerAssignments(N,pair)									#Generate primary layer combinations
		for pL in primaryLayers:													#Iterate over them
			sL = tuple(set(layers).difference(pL))									#Secondary list is the remaining layers
			primaryConnection = layerConnections(pL, pair[0])						#Generate primary connections
			secondaryConnection = layerConnections(sL, pair[1])						#Generate secondary connections
			#If primaryConnection is a single entry just iterate over secondary connections
			if (isinstance(primaryConnection,int) or primaryConnection[0] == 's' or primaryConnection[0] == 'p'):
				if (secondaryConnection[0] != 's' and secondaryConnection[0] != 'p'):
						for connect in secondaryConnection:
							stackupList.append((primaryConnection,connect))
				else: 
					stackupList.append((primaryConnection,secondaryConnection))
			#If primaryConnections has multiple entries iterate over both prim and secondary connections
			else:
				for pConnect in primaryConnection:	
					if (secondaryConnection[0] != 's' and secondaryConnection[0] != 'p'):
						for connect in secondaryConnection:
							stackupList.append((pConnect,connect))
					else:
						stackupList.append((pConnect,secondaryConnection))

	return stackupList

def turnPairs(N, turnsRatio):
	'''
	Returns valid pairs of turn counts for a N layer transformer, assuming maximum 1 turn per layer.

	Parameters:
	-----------
	N : int
		Number of turns.
	turnsRatio : int or float
		Desired turns ratio. turnsRatio >= 1

	Returns:
	--------
	turnPairs
		list of lists, with each inner
	'''
	#Input validation
	if (N <=2 or type(N) != int): raise valueError('Invalid N')
	if (turnsRatio <= 0): raise valueError('Invalid turns ratio')

	if (turnsRatio < 1): turnsRatio = 1/turnsRatio


	nFlag = 1						#True while haven't exceeded N
	turnPairs = []					#Empty list to put turn pairs in
	p=1								#start with 1 turn in primary

	while nFlag:
		s = p * turnsRatio														#Set S based on turns ratio
		if ((s + p) > N): nFlag = 0												#Not valid if s+p>N. Break out of loop
		else: 
			if (isinstance(s,int) or s.is_integer()): turnPairs.append([p,s])	#append to list if valid
		p = p+1																	#Increment p counter

	return turnPairs

def layerAssignments(N, turnPair):
	'''
	Selects different combinations of layers for a given set of turns and a layer count.

	Parameters:
	-----------
	N : int
		Number of turns.
	turnPair: int list of length 2
		Pair of turn counts. turnPair[0] turns on the primary, turnPair[1] turns on the secondary.

	Returns:
	--------
	primaryLayerAssignments
		List of lists. Each inner list is a unique set of layers that can function as the primary for
		the specified N and turnPair, with a max of 1 turn per layer.
	'''
	#Input Validation
	if (N <=2 or type(N) != int): raise valueError('Invalid N')
	if (len(turnPair) != 2): raise valueError('Invalid Turn Pairs')

	#Generate list [1,..,N]
	layers = [0] * N
	for i in range(1, N+1):
		layers[i-1] = i

	validPrimaryCounts = range(turnPair[0],N - turnPair[1] + 1)			#Possible number of layers on the primary
	primaryLayerAssignments = []
	for j in validPrimaryCounts:
		primaryLayerAssignments.extend(list(combinations(layers,j)))	#Generate all combinations

	return primaryLayerAssignments

def layerConnections(layers, N):
	'''
	Returns all possible 1 turn/layer combinations that place N turns on the specified layers.

	Parameters:
	-----------
	layers : int list
		Layers that will be connected together with specified amount of turns.
	N : int
		Number of turns.

	Returns:
	--------
	connections
		List of layer connections that put N turns on the provided layers. 
	'''
	if (type(layers) == int): #If called on single layer, just return the layer (if N==1)
		if (N==1): return layers
		else: raise valueError('Invalid turn number for specified layers.')
	if (len(layers) == 1): return layers[0]

	#Since 1 turn per layer max, can't have more layers than turns
	if (len(layers) < N): raise valueError('Invalid turn number for specified layers.')

	num = len(layers)
	p_count = num-N 	#number of parallel connections
	s_count = N-1 		#number of series connections

	if (p_count==0): return seriesConnect(layers) 	#Only need to do series connections
	if (s_count==0): return parallelConnect(layers) #Only need to do parallel connections
	else:
		#Otherwise we will create one turn and put it in series with the remainder of the turns
		connections = [] 
		for i in range(1, num - N + 1):							#Can put 1 turn on up to p_count layers
			oneTurnOptions = list(combinations(layers,i))		#Generate layer combinations for the one turn
			for s in oneTurnOptions:							#Iterate over each layer set
				s2 = tuple(set(layers).difference(s))			#Specify the layers not included in the turn
				a = layerConnections(s,1)						#Generate the 1 turn connection
				b = layerConnections(s2,N-1)					#Generate the remaining turn connections
				if (type(b[0]) == str):							#If b only has one entry, it will start with a string
					connections.append(['s',a,b])				
				else:
					for connection in b:						#iterate over all elements of b to generate all the valid connections
						connections.append(['s',a,connection])
		return connections

def seriesConnect(layers):
	'''
	Connects specified layers in series.

	Parameters:
	-----------
	layers : int list
		layers to be connected in series

	Returns:
	--------
		Series connection of all input layers.
	'''
	if (len(layers) == 2): #Base Case
		return ['s',layers[0],layers[1]]
	else: #Put first layer in series with the remaining layers
		return ['s',layers[0],seriesConnect(layers[1:])]

def parallelConnect(layers):
	'''
	Connects specified layers in parallel.

	Parameters:
	-----------
	layers : int list
		layers to be connected in parallel

	Returns:
	--------
		Parallel connection of all input layers.
	'''
	if (len(layers) == 2): #Base Case
		return ['p',layers[0],layers[1]]
	else: #Put first layer in series with the remaining layers
		return ['p',layers[0],parallelConnect(layers[1:])]
