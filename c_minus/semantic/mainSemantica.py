from globalTypes import *
from Parser import recibeParser, parse
from semantica import *
import sys

# Obtener nombre de archivo desde el argumento de la linea de comandos
if len(sys.argv) > 1:
    fileName = sys.argv[1]
    # Eliminar la extension .c- si esta presente
    if fileName.endswith('.c-'):
        fileName = fileName[:-3]
else:
    fileName = "sample" # Nombre de archivo por defecto

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
        semantica(syntaxTree, True)
except FileNotFoundError:
    print(f"Error: No se pudo encontrar el archivo '{fileName}.c-'")
    sys.exit(1)