import ply.lex as lex 	# Lexer
import ply.yacc as yacc	# Parser
import lex_analysis		# Lex File
import sys				# Python sys
import symbol_table		# Symbol Table File
import parse_analysis
from parse_analysis import threeAddressCode
from parse_analysis import abstractSyntaxTree

lexer = lex.lex(module=lex_analysis)

if sys.argv[1] == None :
	fp = open('./test-cases/case1.txt')
else:
	fp = open('./test-cases/case'+ sys.argv[1]+ '.txt')
data = fp.read()
fp.close()

lexer.input(data)
global_symtab = symbol_table.symbol_table("global", "global")
stack = symbol_table.table_stack()
stack.push(global_symtab)
linecount, items = 0, []

for tok in lexer:
	if(tok.lineno == linecount):
		items.append(tok.value)
	else:
		items = [tok.value]
		linecount+=1
	symtab = stack.peek()
	if(tok.value in lex_analysis.reserved):
		symtab.insert(tok.value, [tok.lineno, tok.type, "reserved", "-", "-"])

	elif(tok.type == 'ID'):
		symtab.insert(tok.value, [tok.lineno, tok.type, '~', "global", "-"])

	elif(tok.type == 'LBRACE'):
		scope_name = ''
		if 'if' in items:
			scope_name = 'if'
		elif 'else' in items:
			scope_name = 'else'
		elif 'for' in items:
			scope_name = 'for'
		elif 'while' in items:
			scope_name = 'while'
		elif 'loop' in items:
			scope_name = 'loop'
		digit = symbol_table.find_most_recent_scope(scope_name)
		scope_name = ''.join([scope_name, str(digit+1)])
		new_symtab = symbol_table.symbol_table(scope_name, symtab)
		stack.push(new_symtab)
	elif(tok.type == 'RBRACE'):
		child_symtab = stack.pop()
		symtab = stack.peek()
		symtab.put_child(child_symtab.name, child_symtab)

final_sym = stack.peek()
parser = yacc.yacc(module=parse_analysis)
final_sym.print_table()
threeAddressCode.symbolTable = final_sym
parse_analysis.initSymbolTable(final_sym)
parser.parse(data)
threeAddressCode.print_code()
