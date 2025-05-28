from globalTypes import *
from symtab import *
from analyze import *

def tabla(tree, imprime=True):
    """
    Construye la tabla de simbolos a partir del AST.
    
    Args:
        tree: El arbol sintactico abstracto creado por el parser
        imprime: Si es True, imprime la tabla de simbolos
    
    Returns:
        True si hubo errores, False en caso contrario
    """
    # Construir la tabla de simbolos
    error = buildSymtab(tree, imprime)
    return error

def semantica(tree, imprime=True):
    """
    Realiza el analisis semantico completo del programa.
    
    Args:
        tree: El arbol sintactico abstracto creado por el parser
        imprime: Si es True, imprime la tabla de simbolos
    
    Returns:
        True si hubo errores, False en caso contrario
    """
    # Construir la tabla de simbolos
    symtab_error = tabla(tree, imprime)
    
    # Si hay errores en la tabla, no continuar con el analisis de tipos
    if symtab_error:
        print("\nSe encontraron errores en la construccion de la tabla de simbolos.")
        print("No se realizara la verificacion de tipos.")
        return True
    
    # Verificar tipos
    print("\nRealizando verificacion de tipos...")
    type_error = typeCheck(tree)
    
    if not type_error:
        print("\nVerificacion de tipos completada exitosamente.")
    else:
        print("\nSe encontraron errores en la verificacion de tipos.")
    
    return symtab_error or type_error