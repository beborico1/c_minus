# main.py
from globalTypes import *
from Parser import *
from analyze import *
from symtab import inferTypes  # Import inferTypes from symtab
from cgen import *

# Get filename from command line or use default
import sys
if len(sys.argv) > 1:
    fileName = sys.argv[1]
else:
    fileName = "sample"

try:
    f = open(fileName + '.c-', 'r')
    programa = f.read()  # Read entire file to compile
    f.close()  # Close source file
    progLong = len(programa)  # Original program length
    programa = programa + '$'  # Add $ character to represent EOF
    posicion = 0  # Current character position

    Error = False
    recibeParser(programa, posicion, progLong)  # Send globals to parser
    syntaxTree, Error = parse(False)

    if not Error:
        print()
        print("Building Symbol Table...")
        Error = buildSymtab(syntaxTree, True)  # Changed to True to print symbol table
        
        if not Error:
            # IMPORTANT: Infer types before type checking
            print("Inferring Types...")
            inferTypes(syntaxTree)
            
            print()
            print("Checking Types...")
            Error = typeCheck(syntaxTree)
            print()
            print("Type Checking Finished")
        
    if not Error:
        print()
        print("Generating Code...")
        codeGen(syntaxTree, fileName + ".s")
        print(f"Code generated in {fileName}.s")
        
except FileNotFoundError:
    print(f"Error: File '{fileName}.c-' not found")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()