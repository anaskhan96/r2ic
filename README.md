# r2ic

`r2ic` converts a rust program (containing only its basic constructs - `if`, `else`, `for`, `while`, and `loop`, along with variable declarations with `let`) to an intermediate code in the form of quadruples. It also generates an abstract syntax tree for expressions and assignments. The intermediate code generated has three kinds of code optimizations:
+ Constant folding
+ Constant propagation
+ Loop unrolling

The tool is built using Python's PLY framework for scanning tokens and parsing the input.

### How to run it

Test cases can be added inside `src/test-cases` with the format specified. The test case number can then be provided as a command line argument to `main.py` inside the src directory. For eg, to run the test case `src/test-cases/case2.txt`, the command would be as given:
```bash
cd src
python3 main.py 2
```
---
This project was built under the course *Compiler Design Laboratory* in *PES University*.
