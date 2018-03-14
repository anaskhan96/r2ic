import ply.lex as lex 	# Lexer
import ply.yacc as yacc	# Parser
import lex_analysis		# Lex File
import sys				# Python sys
import symbol_table		# Symbol Table File
import re

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
		digit = find_most_recent_scope(scope_name, symtab)
		scope_name = ''.join([scope_name, str(digit+1)])
		new_symtab = symbol_table.symbol_table(scope_name, symtab.name)
		stack.push(new_symtab)

	elif(tok.type == 'RBRACE'):
		child_symtab = stack.pop()
		symtab = stack.peek()
		symtab.put_child(child_symtab.name, child_symtab)

# Testing
'''print("\n\n\nLine#\tType\tName\tScope\t\tType")
t = 'if'
print(sym_tab.lookup(t)[0],\
	"\t",sym_tab.lookup(t)[1],\
	"\t",sym_tab.lookup(t)[2],\
	"\t",sym_tab.lookup(t)[3],\
	"\t\t",sym_tab.lookup(t)[4])

t = 'abc'
print(sym_tab.lookup(t)[0],\
	"\t",sym_tab.lookup(t)[1],\
	"\t",sym_tab.lookup(t)[2],\
	"\t",sym_tab.lookup(t)[3],\
	"\t\t",sym_tab.lookup(t)[4])'''