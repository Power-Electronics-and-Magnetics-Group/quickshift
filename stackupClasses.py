class Stackup:

	def __init__(self, primary, secondary, N):
		self.primary = primary
		self.secondary = secondary
		self.N = N

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

class ParallelNode(Node):

	kind = 'P'
	
	def __init__(self, left, right):
		super().__init__(left, right)
		self.turns = (.5*(self.left.turns + self.right.turns))

	def I_node(self):
		a = self.left.I_node()
		a.extend(self.right.I_node())
		return a

class SeriesNode(Node):

	kind = 'S'
	
	def __init__(self, left, right):
		super().__init__(left, right)
		self.turns = (self.left.turns + self.right.turns)

	def I_node(self):
		return self.left.I_node()

class Layer:

	kind = 'L'

	def __init__(self, number, turns):
		self.number = number
		self.turns = turns

	def I_node(self):
		return [self.number]

	def hasLayer(self):
		return self.number

	def allLayers(self):
		return [self.number]

# x = Layer(4,1)
# y = Layer(8,2)
# z = Layer(2,4)
# a = SeriesNode(x,y)
# b = ParallelNode(a,z)
# print(b.hasLayer())
# print(b.allLayers())