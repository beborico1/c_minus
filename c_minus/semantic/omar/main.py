# ----------------------------------------------------------------------------
# main.py
# 
# Programa principal consolidado para el analizador semántico de C-
# Combina funcionalidad de main.py, main_fixed.py y main_flexible.py
#
# Autor: Omar Rivera Arenas
# Fecha: 28 de abril de 2025
# ----------------------------------------------------------------------------

from globalTypes import *
from lexer import *
from Parser import *
from semantica import semantica
import sys
import os

def main():
    # Get filename from command line or use default
    if len(sys.argv) > 1:
        fileName = sys.argv[1]
        # Remove .c- extension if present
        if fileName.endswith('.c-'):
            fileName = fileName[:-3]
    else:
        fileName = "sample"
    
    # Check if file exists
    if not os.path.exists(fileName + ".c-"):
        print(f"No se encontró el archivo '{fileName}.c-'")
        return

    try:
        with open(fileName + ".c-", "r") as f:
            source = f.read()
    except FileNotFoundError:
        print(f"No se encontró el archivo '{fileName}.c-'")
        return
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return

    programa = source + "$"
    progLong = len(programa)
    posicion = 0

    # Initialize lexer globals properly
    globales(programa, posicion, progLong)

    # Parse the program
    print(f"Analizando archivo: {fileName}.c-")
    print("=" * 50)
    
    # Parse with or without printing based on command line arguments
    imprime_ast = "--print-ast" in sys.argv or "-p" in sys.argv
    AST = parser(imprime=imprime_ast)
    
    if AST is not None:
        print("\nAnalizando semántica...")
        # Run semantic analysis with symbol table printing
        semantica(AST, imprime=True)
    else:
        print("ERROR: Parser returned None - No se pudo construir el AST")

if __name__ == "__main__":
    main()