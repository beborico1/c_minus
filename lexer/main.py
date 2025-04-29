from globalTypes import *
from lexer import *

def main():
    """Funcion principal del analizador lexico"""
    print("Analizador Lexico para C-minus")
    print("-------------------------------")
    
    try:
        # Abrir y leer el archivo fuente
        filename = input("Ingrese el nombre del archivo a analizar (default: sample.c-): ") or "sample.c-"
        with open(filename, 'r') as f:
            programa = f.read()  # lee todo el archivo a compilar
            progLong = len(programa)  # longitud original del programa
            programa = programa + '$'  # agregar un caracter $ que represente EOF
            posicion = 0  # posicion del caracter actual del string
            
            # Inicializar variables globales
            globales(programa, posicion, progLong)
            
            # Escanear todos los tokens
            print("\nResultados del analisis lexico:")
            print("--------------------------------")
            print(" Linea: Token      = Lexema")
            print("--------------------------------")
            
            token, _ = getToken(True)
            while token != TokenType.ENDFILE:
                token, _ = getToken(True)
            
            print("--------------------------------")
            print("Analisis lexico completado.")
            
    except FileNotFoundError:
        print(f"Error: No se pudo encontrar el archivo '{filename}'")
    except Exception as e:
        print(f"Error inesperado: {e}")

if __name__ == "__main__":
    main()