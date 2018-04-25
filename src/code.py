class ThreeAddressCode:
	def __init__(self):
		self.symbolTable = None
		self.allCode = []
		self.tempVarCount = 0

	def generateCode(self, operation, arg1, arg2, result):
		code = Quadruple(operation, arg1, arg2, result)
		self.allCode.append(code)

	def print_code(self):
		print("\tOperation\tArg1\t\tArg2\t\tResult")
		for i in self.allCode:
			print("\t", i.operation, "\t\t", i.arg1, "\t\t", i.arg2, "\t\t", i.result)

	def generate_icg(self, operation, arg1, arg2, result):
		if operation == "goto":
			self.generateCode(operation, arg1, arg2, result)
		elif operation.endswith("F"):
			self.generateCode(operation, str(arg1), str(arg2), result)
		elif operation == "=":
			if type(arg1) == str:
				if arg1 in self.symbolTable.symbols.keys():
					value = self.symbolTable.lookup(arg1)[2]
					if type(value) == int:
						self.generateCode(operation, value, '', result)
						# updation of id in symbol table
						value1 = self.symbolTable.lookup(result)
						value1[2] = value
						self.symbolTable.symbols[result] = value1
					else:
						self.generateCode(operation, arg1, '', result)
			else:
				self.generateCode(operation, arg1, '', result)
				# updation of id in symbol table
				value = self.symbolTable.lookup(result)
				value[2] = arg1
				self.symbolTable.symbols[result] = value
		else:
			# operation is either +,-,*,/
			if type(arg1) == int and type(arg2) == int:
				self.tempVarCount += 1
				temp = 't'+str(self.tempVarCount)
				self.symbolTable.insert(temp, [0, 'ID', result, "global", "-"])
			else:
				self.tempVarCount += 1
				temp = 't'+str(self.tempVarCount)
				self.generateCode(operation, arg1, arg2, temp)
				self.symbolTable.insert(temp, [0, 'ID', '~', "global", "-"])

	def putLabel(self, kind):
		label = len(self.allCode)
		if kind == 'result':
			for i in reversed(self.allCode):
				if i.result.endswith("S"):
					i.result += str(label)
					break
		elif kind == 'arg1':
			for i in reversed(self.allCode):
				if i.arg1.endswith("S"):
					i.arg1 += str(label)
					break
		else:
			allCodeReverse = self.allCode[::-1]
			for i in range(len(allCodeReverse)):
				if allCodeReverse[i].result.endswith("S"):
					self.generate_icg("goto", "S"+str(label-i-1), '', '')
					break

	def getLatestTemp(self):
		return 't'+str(self.tempVarCount)

class Quadruple:
	def __init__(self, operation, arg1, arg2, result):
		self.operation = operation
		self.arg1 = arg1
		self.arg2 = arg2
		self.result = result

	def print_quadruple(self):
		print(self.operation, self.arg1, self.arg2, self.result)