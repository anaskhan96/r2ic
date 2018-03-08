import ply.lex as lex 	# Lexer
import ply.yacc as yacc	# Parser
import lex_analysis		# Lex File
import sys				# Python sys
import symbol_table		# Symbol Table File

lexer = lex.lex(module=lex_analysis)

enclosing_scopes = 1
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
sym_tab = symbol_table.symbol_table('global', 'global')

for tok in lexer:
	print(tok)
	
	if(tok.value in lex_analysis.reserved):
		sym_tab.insert(tok.value, [tok.lineno, tok.type, tok.value, "-", "-"])
	
	elif(tok.type == 'ID'):
		sym_tab.insert(tok.value, [tok.lineno, tok.type, tok.value, "global", "-"])

	elif(tok.type == 'LBRACE'):
		for tok in lexer:				
			print("Inner:",tok)
		#sym_tab.put_child(sym_tab.name, 'sym_tab'+str(enclosing_scopes))
		enclosing_scopes += 1

	previous_token = tok

# Testing
print("\n\n\nLine#\tType\tName\tScope\t\tType")
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
	"\t\t",sym_tab.lookup(t)[4])