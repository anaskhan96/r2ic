from symbol_table import table_stack
tac_stack = table_stack()
mult_flag = 0

class ThreeAddressCode:
	def __init__(self):
		self.symbolTable = None
		self.allCode = []
		self.tempVarCount = 1
		self.label_counter = 1
		self.temp_symbol_table = {}

	def generateCode(self, operation, arg1, arg2, result):
		code = Quadruple(operation, arg1, arg2, result)
		#code.print_quadruple()
		self.allCode.append(code)

	def print_code(self):
		print("\tOperation\tArg1\t\tArg2\t\tResult")
		for i in self.allCode:
			print("\t", i.operation, "\t\t", i.arg1, "\t\t", i.arg2, "\t\t", i.result)

	def generate_icg(self, operation, arg1, arg2, result):
		global mult_flag
		if operation == '+' or operation == '-':
			if tac_stack.get_length() == 1:
				if mult_flag == 1:
					mult_flag -= 1
			
				tac_stack.push('t'+str(self.tempVarCount))
				self.temp_symbol_table[self.tempVarCount] = result
				self.tempVarCount += 1

			elif tac_stack.get_length() > 1:
				tac_stack.push('t'+str(self.tempVarCount))
				self.temp_symbol_table[self.tempVarCount] = result
				self.tempVarCount += 1
				mult_flag -= 1
			
			else:
				tac_stack.push('t'+str(self.tempVarCount))
				self.temp_symbol_table[self.tempVarCount] = result
				self.tempVarCount += 1
	
		elif operation == '*' or operation == '/':
		
			if tac_stack.get_length() == 1:
				if not mult_flag == 1:
					mult_flag -= 1
					
				tac_stack.push('t'+str(self.tempVarCount))
				self.temp_symbol_table[self.tempVarCount] = result
				self.tempVarCount += 1

			elif tac_stack.get_length() > 1:
				tac_stack.push('t'+str(self.tempVarCount))
				self.temp_symbol_table[self.tempVarCount] = result
				self.tempVarCount += 1
				mult_flag -= 1
			
			else:

				tac_stack.push('t'+str(self.tempVarCount))
				mult_flag += 1

				self.temp_symbol_table[self.tempVarCount] = result
				self.tempVarCount += 1
		
		elif operation == '=':
				if tac_stack.get_length() > 0:
					self.generateCode(operation, str(self.temp_symbol_table[len(self.temp_symbol_table)]), '', result)
				else:
					self.generateCode(operation, str(arg1), '', result)

		elif operation == "goto":
			self.generateCode(operation, arg1, arg2, result)

		elif operation.endswith('F'):
			self.generateCode(operation, str(arg1), str(arg2), result)
		
		else:
			print("Invalid operation")

	def putLabel(self, kind):
		label = len(self.allCode)
		if kind == 'result':
			for i in reversed(self.allCode):
				if i.result.endswith("S"):
					i.result += str(label)
					break
		else:
			for i in reversed(self.allCode):
				if i.arg1.endswith("S"):
					i.arg1 += str(label)
					break

class Quadruple:
	def __init__(self, operation, arg1, arg2, result):
		self.operation = operation
		self.arg1 = arg1
		self.arg2 = arg2
		self.result = result

	def print_quadruple(self):
		print(self.operation, self.arg1, self.arg2, self.result)