import re

class table_stack:
	def __init__(self):
		self.items = []

	def push(self, item):
		self.items.append(item)

	def pop(self):
		return self.items.pop()

	def peek(self):
		return self.items[len(self.items)-1]

	def get_length(self):
		return len(self.items)

class symbol_table:
	def __init__(self, name, parent): # parent is another object of the symbol_table class
		self.symbols = {}
		self.name = name
		self.children = {} # to store all scopes inside an enclosing one
		self.parent = parent

	def insert(self, symbol, token): # eg. symbol = 'if', token = ['KEYWORD', 'if']
		if symbol not in self.symbols:
			self.symbols[symbol] = token	

	def lookup(self, symbol):
		return self.symbols[symbol]
	
	def get_symbols(self):
		return (self.symbols.keys(), self.symbols.values())

	def get_name(self):
		return self.name

	def get_parent(self):
		return self.parent

	def put_child(self, name, child): # eg. name = 'if_scope_1', child = the symbol_table object of the scope
		self.children[name] = child

	def get_child(self, name):
		return self.children[name]

	def get_children(self):
		return self.children.keys(), 

def find_most_recent_scope(scope_name, symtab):
	pattern = re.compile("{}\d+".format(scope_name))
	key_digits = []
	for key in symtab.children:
		if pattern.match(key):
			key_digits.append(int(key[-1]))
	if len(key_digits) == 0:
		return 0
	else:
		return max(key_digits)


def print_symbol_table(symbol_table):
	print ("Table = ", symbol_table.get_name())
	
	print(symbol_table.get_symbols())
	for i in symbol_table.get_children():
		print_symbol_table(symbol_table.get_child(i))	

		