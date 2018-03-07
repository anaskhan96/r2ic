class symbol_table:
	def __init__(self, name, parent):
		self.symbols = {}
		self.name = name
		self.children = {}
		self.parent = parent

	def insert(self, symbol, token):
		if symbol in self.symbols:
			pass
		else:
			self.symbols[symbol] = token	

	def lookup(self, symbol):
		return self.symbols[symbol]

	def get_parent(self):
		return self.parent

	def put_child(self, name, child):
		self.children[name] = child

	def get_child(self, name):
		return self.children[name]