from globalTypes import *
from Parser import recibeParser, parse
from semantica import *

fileName = "sample4"
f = open(fileName + '.c-', 'r')
program = f.read()         # lee todo el archivo a compilar
f.close()                  # cerrar el archivo con programa fuente
progLong = len(program)    # longitud original del programa
program = program + '$'    # agregar un caracter $ que represente EOF
position = 0               # posición del caracter actual del string

Error = False
recibeParser(program, position, progLong)  # para mandar los globales al parser
syntaxTree, Error = parse(False)

if not(Error):
    print("\nAnalizando semántica...")
    semantica(syntaxTree, True)