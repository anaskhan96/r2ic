class symbol_table:
	def __init__(self, name, parent):
		self.symbols = {}
		self.name = name
		self.parent = parent

	def insert(self, symbol, token):
		self.symbols[symbol] = token	

	def lookup(self, symbol):
		return self.symbols[symbol]

	def getParent(self):
		return self.parent