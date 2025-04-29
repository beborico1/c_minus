#!/usr/bin/env python3
"""
Programa principal para el analizador sintáctico de C-minus
"""
from globalTypes import *
from Lexer import globales as lexer_globales
from Parser import parser, globales as parser_globales

def main():
    """Función principal del analizador sintáctico de C-minus"""
    print("Compilador de C-minus")
    print("---------------------")
    
    try:
        # Abrir y leer el archivo fuente
        filename = input("Ingrese el nombre del archivo a compilar (default: sample.c-): ") or "sample.c-"
        with open(filename, 'r') as f:
            programa = f.read()     # lee todo el archivo a compilar
            progLong = len(programa)   # longitud original del programa
            programa = programa + '$'   # agregar un caracter $ que represente EOF
            posicion = 0       # posición del caracter actual del string
            
            # Inicializar variables globales
            print(f"\nInicializando compilador con archivo: {filename}, longitud: {progLong}")
            lexer_globales(programa, posicion, progLong)
            parser_globales(programa, posicion, progLong)
            
            # Parsear el programa
            print("\nAnálisis sintáctico en proceso...")
            print("--------------------------------")
            
            AST = parser(True)  # True para imprimir el AST
            
            if AST is not None:
                print("\nAnálisis sintáctico completado exitosamente.")
            else:
                print("\nEl programa contiene errores y no pudo ser compilado correctamente.")
            
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{filename}'")
    except Exception as e:
        print(f"Error inesperado: {e}")
        # Imprimir más detalles sobre el error
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()