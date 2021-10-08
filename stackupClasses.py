class Stackup:

	def __init__(self, primary, secondary, N):
		self.primary = primary
		self.secondary = secondary
		self.N = N

	def __repr__(self):
		return f'Stack: Primary - {self.primary.__repr__()}; Secondary - {self.secondary.__repr__()}'


	def turnsRatio(self):
		n1 = self.primary.turns
		n2 = self.secondary.turns

		if (n1 > n2):
			return n1/n2
		else: return n2/n1

	def validStackup(self):
		primLayers = self.primary.allLayers()
		secondaryLayers = self.secondary.allLayers()
		primLayers.extend(secondaryLayers)
		layers = sorted(primLayers)
		correct = list(range(1, self.N + 1))
		return (layers == correct)

	def turnCount(self):
		Turns = self.primary.turnCount()
		secTurns = self.secondary.turnCount()
		Turns.extend(secTurns)
		TurnsSort = sorted(Turns, key=lambda x: x[0])
		turnCounts = [0] * self.N
		for i in range(0,self.N):
			turnCounts[i] = TurnsSort[i][1]
		return turnCounts

class Node(object):

	def __init__(self, left, right):
		self.left = left
		self.right = right

	def hasLayer(self):
		return self.left.hasLayer()

	def allLayers(self):
		a = self.left.allLayers()
		a.extend(self.right.allLayers())
		return a

	def turnCount(self):
		a = self.left.turnCount()
		b = self.right.turnCount()
		a.extend(b)
		return a

class ParallelNode(Node):

	kind = 'P'
	
	def __init__(self, left, right):
		super().__init__(left, right)
		self.turns = (.5*(self.left.turns + self.right.turns)) # NOT CORRECT. TO DO

	def __repr__(self):
		return f'(P,{self.left.__repr__()},{self.right.__repr__()})'

	def I_node(self):
		a = self.left.I_node()
		a.extend(self.right.I_node())
		return a

class SeriesNode(Node):

	kind = 'S'
	
	def __init__(self, left, right):
		super().__init__(left, right)
		self.turns = (self.left.turns + self.right.turns)

	def __repr__(self):
		return f'(S,{self.left.__repr__()},{self.right.__repr__()})'

	def I_node(self):
		return self.left.I_node()

class Layer:

	kind = 'L'

	def __init__(self, number, turns):
		if (not isinstance(number, int)): print(type(number))
		self.number = number
		self.turns = turns

	def __repr__(self):
		return f'[L{self.number},{self.turns}T]'

	def I_node(self):
		return [self.number]

	def hasLayer(self):
		return self.number

	def allLayers(self):
		return [self.number]

	def turnCount(self):
		return [[self.number, self.turns]]



#x = Layer(3,1)
#print(x.number)
#print(x.allLayers())
# y = Layer(2,2)
# z = Layer(1,4)
# a = SeriesNode(x,y)
# b = ParallelNode(a,z)
# print(b)
# m = Layer(4,1)
# n = Layer(5,1)
# c = SeriesNode(m,n)

# stack = Stackup(b,c,5)

# print(stack.turnCount())
