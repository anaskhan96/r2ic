import ply.lex as lex
import lex_analysis
import sys
import symbol_table
lexer = lex.lex(module=lex_analysis)

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

for tok in lexer:
	print(tok)
	if(tok.value in lex_analysis.reserved):
		symbol_table.st.append(['KEYWORD',tok.value])
	elif(tok.type == 'ID'):
		symbol_table.st.append([tok.type, tok.value])

print(symbol_table.st)