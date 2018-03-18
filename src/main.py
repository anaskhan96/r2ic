import ply.lex as lex 	# Lexer
import ply.yacc as yacc	# Parser
import lex_analysis		# Lex File
import sys				# Python sys
import symbol_table		# Symbol Table File
import parse_analysis

lexer = lex.lex(module=lex_analysis)

data = '''
// Single Comment
(print!)
let abc = 10
if n%2.0 == 0 {
	println!(even)
} else {
	println!(odd)
}
/* Multiline Comments */
/// Generate library docs for the following item.
//! Generate library docs for the enclosing item.
'''

lexer.input(data)
global_symtab = symbol_table.symbol_table("global", "global")
stack = symbol_table.table_stack()
stack.push(global_symtab)
linecount, items = 0, []

for tok in lexer:
	print(tok)
	if(tok.lineno == linecount):
		items.append(tok.value)
	else:
		items = [tok.value]
		linecount+=1
	symtab = stack.peek()
	if(tok.value in lex_analysis.reserved):
		symtab.insert(tok.value, [tok.lineno, tok.type, tok.value, "-", "-"])

	elif(tok.type == 'ID'):
		symtab.insert(tok.value, [tok.lineno, tok.type, tok.value, "global", "-"])

	elif(tok.type == 'LBRACE'):
		scope_name = ''
		if 'if' in items:
			scope_name = 'if'
		elif 'else' in items:
			scope_name = 'else'
		elif 'for' in items:
			scope_name = 'for'
		digit = symbol_table.find_most_recent_scope(scope_name, symtab)
		scope_name = ''.join([scope_name, str(digit+1)])
		new_symtab = symbol_table.symbol_table(scope_name, symtab.name)
		stack.push(new_symtab)

	elif(tok.type == 'RBRACE'):
		child_symtab = stack.pop()
		symtab = stack.peek()
		symtab.put_child(child_symtab.name, child_symtab)

final_sym = stack.peek()

parser = yacc.yacc(module=parse_analysis)

while True:
	try:
		s = input("calc -> ")
	except EOFError:
		break
	if not s:
		continue
	result = parser.parse(s)
	print(result)