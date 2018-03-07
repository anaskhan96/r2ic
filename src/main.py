import ply.lex as lex
import lex_analysis
import sys
import symbol_table
lexer = lex.lex(module=lex_analysis)

enclosing_scopes = 1
data = '''
// Single Comment
(print!)
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
		sym_tab.insert(tok.value, [tok.type, tok.value])
	
	elif(tok.type == 'ID'):
		sym_tab.insert('id', [tok.type, tok.value])

	elif(tok.type == 'LBRACE'):
		sym_tab.put_child(sym_tab.name, 'sym_tab1')

	previous_token = tok

# Testing
print(sym_tab.lookup('if'))