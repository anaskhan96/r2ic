import ply.lex as lex
import lex_analysis
import sys
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

print("Reserved words: ", lex_analysis.reserved)