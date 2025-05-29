# main.py
from globalTypes import *
from Parser import *
from semantic import *
from symtab import inferTypes  # Importar inferTypes desde symtab
from cgen import *

# Obtener nombre de archivo de linea de comandos o usar predeterminado
import sys
if len(sys.argv) > 1:
    fileName = sys.argv[1]
else:
    fileName = "sample"

try:
    f = open(fileName + '.c-', 'r')
    programa = f.read()  # Leer archivo completo para compilar
    f.close()  # Cerrar archivo fuente
    progLong = len(programa)  # Longitud original del programa
    programa = programa + '$'  # Agregar caracter $ para representar EOF
    posicion = 0  # Posicion actual del caracter

    Error = False
    recibeParser(programa, posicion, progLong)  # Enviar globales al parser
    syntaxTree, Error = parse(False)

    if not Error:
        print()
        success = semantica(syntaxTree, True)
        Error = not success
        
    if not Error:
        print()
        print("Generando Codigo...")
        codeGen(syntaxTree, fileName + ".s")
        print(f"Codigo generado en {fileName}.s")
        
except FileNotFoundError:
    print(f"Error: Archivo '{fileName}.c-' no encontrado")
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()