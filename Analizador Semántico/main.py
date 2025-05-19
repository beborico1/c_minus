# ----------------------------------------------------------------------------
# main.py
# 
# Programa basado en los documentos de clase proporcionados.
# Se utilizó también apoyo de herramientas de inteligencia artificial (como GPT) 
# para estructurar, corregir y perfeccionar algunas secciones del código.
#
# Autor: Omar Rivera Arenas
# Fecha: 28 de abril de 2025
#
# Descripción:
# Este archivo contiene el script principal que carga un programa fuente C-,
# inicializa las variables globales necesarias para el lexer y parser,
# y genera el Árbol Sintáctico Abstracto (AST) del programa.
# ----------------------------------------------------------------------------

from globalTypes import *
from lexer import *
from Parser import *
from semantica import * 

def main():
    try:
        with open("sample.c-", "r") as f:
            source = f.read()
    except FileNotFoundError:
        print("No se encontró el archivo 'sample.c-'")
        return

    programa = source + "$"
    progLong = len(programa)
    posicion = 0

    globales(programa, posicion, progLong)

    AST = parser(imprime=True)
    semantica(AST, imprime=True)

if __name__ == "__main__":
    main()