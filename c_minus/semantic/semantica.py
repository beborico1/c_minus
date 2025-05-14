# semantica.py - Analizador semántico para C-

from globalTypes import *
from symtab import *
from analyze import *

def tabla(tree, imprime=True):
    """
    Construye la tabla de símbolos a partir del AST.
    
    Args:
        tree: El árbol sintáctico abstracto creado por el parser
        imprime: Si es True, imprime la tabla de símbolos
    
    Returns:
        True si hubo errores, False en caso contrario
    """
    # Construir la tabla de símbolos
    error = buildSymtab(tree, imprime)
    return error

def semantica(tree, imprime=True):
    """
    Realiza el análisis semántico completo del programa.
    
    Args:
        tree: El árbol sintáctico abstracto creado por el parser
        imprime: Si es True, imprime la tabla de símbolos
    
    Returns:
        True si hubo errores, False en caso contrario
    """
    # Construir la tabla de símbolos
    symtab_error = tabla(tree, imprime)
    
    # Si hay errores en la tabla, no continuar con el análisis de tipos
    if symtab_error:
        print("\nSe encontraron errores en la construcción de la tabla de símbolos.")
        print("No se realizará la verificación de tipos.")
        return True
    
    # Verificar tipos
    print("\nRealizando verificación de tipos...")
    type_error = typeCheck(tree)
    
    if not type_error:
        print("\nVerificación de tipos completada exitosamente.")
    else:
        print("\nSe encontraron errores en la verificación de tipos.")
    
    return symtab_error or type_error