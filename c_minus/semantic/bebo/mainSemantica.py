from globalTypes import *
from Parser import recibeParser, parse
from semantica import *
from symtab import inferTypes  # Import from symtab instead of type_inference
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Obtener nombre de archivo desde el argumento de la linea de comandos
if len(sys.argv) > 1:
    fileName = sys.argv[1]
    # Eliminar la extension .c- si esta presente
    if fileName.endswith('.c-'):
        fileName = fileName[:-3]
else:
    fileName = "programs/sample1" # Nombre de archivo por defecto

try:
    f = open(fileName + '.c-', 'r')
    program = f.read() # lee todo el archivo a compilar
    f.close() # cerrar el archivo con programa fuente
    progLong = len(program) # longitud original del programa
    program = program + '$' # agregar un caracter $ que represente EOF
    position = 0 # posicion del caracter actual del string

    Error = False
    recibeParser(program, position, progLong) # para mandar los globales al parser
    syntaxTree, Error = parse(False)

    if not(Error):
        print("\nAnalizando semantica...")
        
        # Run type inference first to set expression types
        print("Infiriendo tipos de expresiones...")
        inferTypes(syntaxTree)
        
        semantica(syntaxTree, True)
except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo '{fileName}.c-'")
    sys.exit(1)