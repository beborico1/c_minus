# -----------------------------------------------------------------------------
# semantica.py
#
# Análisis semántico consolidado para C-
# Combina funcionalidad de semantica.py y semantica_fixed.py
# Incluye todas las correcciones para el manejo adecuado de tipos y scopes
#
# Autor: Omar Rivera Arenas
# -----------------------------------------------------------------------------

from globalTypes import *
from symtab import *
import copy

# Variables globales para el análisis
Error = False
current_function = None
function_return_type = None

def error(lineno, message):
    """Reportar un error semántico"""
    global Error
    Error = True
    print(f">>> Error semántico en línea {lineno}: {message}")

def traverse(t, preProc, postProc):
    """
    Recorrido genérico del árbol sintáctico:
    - preProc se aplica en preorden
    - postProc se aplica en postorden
    """
    if t is not None:
        preProc(t)
        # Recorrer hijos
        for i in range(MAXCHILDREN):
            if t.child[i] is not None:
                traverse(t.child[i], preProc, postProc)
        postProc(t)
        # Recorrer hermanos
        traverse(t.sibling, preProc, postProc)

def nullProc(t):
    """Procedimiento que no hace nada"""
    pass

def insertNode(t):
    """Inserta nodos en la tabla de símbolos durante la primera pasada"""
    global current_function, function_return_type, Error
    
    if t.nodekind == NodeKind.StmtK:
        # Declaración de variable
        if t.stmt == StmtKind.VarDeclK:
            # Verificar si ya existe en el scope actual
            if st_lookup_current_scope(t.name) is not None:
                error(t.lineno, f"Variable '{t.name}' ya declarada en este ámbito")
            else:
                # Verificar que las variables no sean void
                var_type = getattr(t, 'var_type', getattr(t, 'typ', ExpType.Integer))
                if var_type == ExpType.Void and not getattr(t, 'is_array', False):
                    error(t.lineno, f"Variable '{t.name}' no puede ser de tipo void")
                
                st_insert(
                    name=t.name,
                    kind='var',
                    typ=var_type,
                    is_array=getattr(t, 'is_array', False),
                    size=getattr(t, 'array_size', None),
                    lineno=t.lineno
                )
        
        # Declaración de función
        elif t.stmt == StmtKind.CompoundK and hasattr(t, 'name') and hasattr(t, 'return_type'):
            # Es una función
            if st_lookup_current_scope(t.name) is not None:
                error(t.lineno, f"Función '{t.name}' ya declarada")
            else:
                current_function = t.name
                function_return_type = t.return_type
                
                # Procesar parámetros
                params = []
                if hasattr(t, 'params'):
                    for param in t.params:
                        if isinstance(param, dict):
                            params.append((param.get('typ', ExpType.Integer), param.get('is_array', False)))
                        else:
                            params.append((getattr(param, 'typ', ExpType.Integer), getattr(param, 'is_array', False)))
                
                st_insert(
                    name=t.name,
                    kind='func',
                    typ=t.return_type,
                    params=params,
                    return_type=t.return_type,
                    lineno=t.lineno
                )
                
                # Crear nuevo ámbito para la función
                st_enter_scope()
                
                # Insertar parámetros en el nuevo ámbito
                # Los nombres de parámetros están en child[0] como nodos IdK
                if t.child[0] is not None:
                    param_node = t.child[0]
                    param_index = 0
                    while param_node is not None:
                        if param_node.nodekind == NodeKind.ExpK and param_node.exp == ExpKind.IdK:
                            # Obtener tipo del parámetro correspondiente
                            param_type = ExpType.Integer  # Default
                            is_array = False
                            
                            if hasattr(t, 'params') and param_index < len(t.params):
                                if isinstance(t.params[param_index], dict):
                                    param_type = t.params[param_index].get('typ', ExpType.Integer)
                                    is_array = t.params[param_index].get('is_array', False)
                                else:
                                    param_type = getattr(t.params[param_index], 'typ', ExpType.Integer)
                                    is_array = getattr(t.params[param_index], 'is_array', False)
                            
                            if param_type == ExpType.Void and not is_array:
                                if hasattr(t, 'params') and len(t.params) > 1:
                                    error(t.lineno, f"Parámetro '{param_node.name}' no puede ser de tipo void")
                            
                            st_insert(
                                name=param_node.name,
                                kind='param',
                                typ=param_type,
                                is_array=is_array,
                                lineno=t.lineno
                            )
                            param_index += 1
                        
                        param_node = param_node.sibling
        
        # Bloque compuesto (no función)
        elif t.stmt == StmtKind.CompoundK and not hasattr(t, 'name'):
            # Solo crear nuevo scope si no es el cuerpo de una función
            if not hasattr(t, 'is_func_body'):
                st_enter_scope()
    
    elif t.nodekind == NodeKind.ExpK:
        # Uso de identificador
        if t.exp in [ExpKind.IdK, ExpKind.CallK, ExpKind.SubscriptK]:
            # Buscar en todos los scopes
            sym = st_lookup(t.name)
            if sym is None:
                error(t.lineno, f"Identificador '{t.name}' no declarado")
            else:
                # Agregar línea de uso
                if hasattr(sym, 'lines') and t.lineno not in sym.lines:
                    sym.lines.append(t.lineno)

def exitScope(t):
    """Maneja la salida de ámbitos durante la primera pasada"""
    global current_function, function_return_type
    
    if t.nodekind == NodeKind.StmtK:
        if t.stmt == StmtKind.CompoundK:
            # Si es una función, salir del scope
            if hasattr(t, 'name') and hasattr(t, 'return_type'):
                st_exit_scope()
                current_function = None
                function_return_type = None
            # Si es un bloque compuesto normal
            elif not hasattr(t, 'is_func_body'):
                st_exit_scope()

def checkNode(t):
    """Realiza verificación de tipos en un nodo durante la segunda pasada"""
    global Error
    
    if t.nodekind == NodeKind.ExpK:
        checkExp(t)
    elif t.nodekind == NodeKind.StmtK:
        checkStmt(t)

def checkExp(t):
    """Verifica tipos para nodos de expresión"""
    global Error
    
    if t.exp == ExpKind.OpK:
        # Verificar operadores
        if t.child[0] is None or t.child[1] is None:
            error(t.lineno, "Operador necesita dos operandos")
            t.type = ExpType.Integer
            return
        
        # Verificar tipos de operandos
        if t.op in [TokenType.PLUS, TokenType.MINUS, TokenType.TIMES, TokenType.DIVIDE]:
            # Operadores aritméticos requieren enteros
            if t.child[0].type != ExpType.Integer:
                error(t.lineno, f"Operando izquierdo del operador {t.op.name} debe ser entero")
            if t.child[1].type != ExpType.Integer:
                error(t.lineno, f"Operando derecho del operador {t.op.name} debe ser entero")
            t.type = ExpType.Integer
        
        elif t.op in [TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE, TokenType.EQ, TokenType.NEQ]:
            # Operadores de comparación
            if t.child[0].type != ExpType.Integer:
                error(t.lineno, f"Operando izquierdo del comparador {t.op.name} debe ser entero")
            if t.child[1].type != ExpType.Integer:
                error(t.lineno, f"Operando derecho del comparador {t.op.name} debe ser entero")
            t.type = ExpType.Boolean
        
        elif t.op == TokenType.ASSIGN:
            # Assignment operator
            if t.child[0] is None or t.child[1] is None:
                return
            
            left = t.child[0]
            right = t.child[1]
            
            # El lado izquierdo debe ser una variable o elemento de arreglo
            if left.exp == ExpKind.SubscriptK:
                # Asignación a elemento de arreglo
                if right.type != ExpType.Integer:
                    error(t.lineno, "Solo se pueden asignar valores enteros a elementos de arreglo")
            
            elif left.exp == ExpKind.IdK:
                # Asignación a variable
                sym = st_lookup(left.name)
                if sym is not None:
                    if getattr(sym, 'is_array', False):
                        error(t.lineno, f"No se puede asignar a un arreglo completo '{left.name}'")
                    elif getattr(sym, 'typ', ExpType.Integer) == ExpType.Integer and right.type != ExpType.Integer:
                        error(t.lineno, f"No se puede asignar un valor no entero a la variable entera '{left.name}'")
    
    elif t.exp == ExpKind.ConstK:
        # Las constantes son siempre enteras
        t.type = ExpType.Integer
    
    elif t.exp == ExpKind.IdK:
        # Set identifier type based on symbol table lookup
        sym = st_lookup(t.name)
        if sym is not None:
            if getattr(sym, 'is_array', False):
                t.type = ExpType.Array
            else:
                # Convert type to expression type
                sym_type = getattr(sym, 'typ', ExpType.Integer)
                if sym_type == ExpType.Integer:
                    t.type = ExpType.Integer
                elif sym_type == ExpType.Void:
                    t.type = ExpType.Void
                else:
                    t.type = ExpType.Integer  # Default
        else:
            # Identifier not found - error already reported in first pass
            t.type = ExpType.Integer  # Default to avoid cascading errors
    
    elif t.exp == ExpKind.SubscriptK:
        # Acceso a arreglo
        sym = st_lookup(t.name)
        if sym is not None:
            if not getattr(sym, 'is_array', False):
                error(t.lineno, f"'{t.name}' no es un arreglo")
                t.type = ExpType.Integer
            else:
                t.type = ExpType.Integer  # Elementos del arreglo son enteros
                
                # Verificar que el índice sea entero
                if t.child[0] is not None and t.child[0].type != ExpType.Integer:
                    error(t.lineno, "El índice del arreglo debe ser entero")
        else:
            t.type = ExpType.Integer  # Error ya reportado
    
    elif t.exp == ExpKind.CallK:
        # Llamada a función
        sym = st_lookup(t.name)
        if sym is not None:
            if getattr(sym, 'kind', '') != 'func':
                error(t.lineno, f"'{t.name}' no es una función")
                t.type = ExpType.Integer
            else:
                # Establecer tipo de retorno
                return_type = getattr(sym, 'return_type', ExpType.Integer)
                t.type = ExpType.Integer if return_type == ExpType.Integer else ExpType.Void
                
                # Verificar argumentos
                expected_params = getattr(sym, 'params', [])
                actual_args = []
                arg = t.child[0]
                while arg is not None:
                    actual_args.append(arg)
                    arg = arg.sibling
                
                if len(actual_args) != len(expected_params):
                    error(t.lineno, f"Función '{t.name}' espera {len(expected_params)} argumentos, pero recibió {len(actual_args)}")
                else:
                    # Verificar tipos de argumentos
                    for i, (arg_node, param_info) in enumerate(zip(actual_args, expected_params)):
                        param_type = param_info[0] if isinstance(param_info, tuple) else param_info
                        param_is_array = param_info[1] if isinstance(param_info, tuple) and len(param_info) > 1 else False
                        
                        if param_type == ExpType.Integer and arg_node.type != ExpType.Integer:
                            error(t.lineno, f"Argumento {i+1} debe ser entero")
                        
                        # Verificar arreglos
                        if param_is_array:
                            if arg_node.exp != ExpKind.IdK:
                                error(t.lineno, f"Argumento {i+1} debe ser un arreglo")
                            else:
                                # Buscar el símbolo del argumento
                                arg_sym = st_lookup(arg_node.name)
                                if arg_sym is None or not getattr(arg_sym, 'is_array', False):
                                    error(t.lineno, f"Argumento {i+1} debe ser un arreglo")
        else:
            t.type = ExpType.Integer  # Error ya reportado

def checkStmt(t):
    """Verifica tipos para nodos de sentencia"""
    global Error, function_return_type
    
    if t.stmt == StmtKind.IfK:
        # Verificar condición
        if t.child[0] is not None:
            if t.child[0].type != ExpType.Boolean and t.child[0].type != ExpType.Integer:
                error(t.lineno, "La condición del if debe ser booleana o entera")
    
    elif t.stmt == StmtKind.WhileK:
        # Verificar condición
        if t.child[0] is not None:
            if t.child[0].type != ExpType.Boolean and t.child[0].type != ExpType.Integer:
                error(t.lineno, "La condición del while debe ser booleana o entera")
    
    elif t.stmt == StmtKind.ReturnK:
        # Verificar retorno
        if t.child[0] is None:
            # Retorno vacío
            if function_return_type != ExpType.Void:
                error(t.lineno, "Retorno sin valor en función no void")
        else:
            # Retorno con valor
            if function_return_type == ExpType.Void:
                error(t.lineno, "Retorno con valor en función void")
            elif function_return_type == ExpType.Integer and t.child[0].type != ExpType.Integer:
                error(t.lineno, "El valor de retorno debe ser entero")

def tabla(tree, imprime=True):
    """Construye la tabla de símbolos"""
    global Error
    Error = False
    
    # Reset symbol table
    st_reset()
    
    # Registrar funciones predefinidas
    st_insert(
        name="input",
        kind='func',
        typ=ExpType.Integer,
        params=[],
        return_type=ExpType.Integer,
        lineno=0
    )
    st_insert(
        name="output",
        kind='func',
        typ=ExpType.Void,
        params=[(ExpType.Integer, False)],
        return_type=ExpType.Void,
        lineno=0
    )
    
    # Primera pasada: construir tabla de símbolos
    traverse(tree, insertNode, exitScope)
    
    if imprime:
        print_symtab()
    
    return Error

def type_check(tree):
    """Realiza la verificación de tipos"""
    global Error
    
    # Segunda pasada: verificar tipos
    traverse(tree, nullProc, checkNode)
    
    return Error

def semantica(tree, imprime=True):
    """Función principal del análisis semántico"""
    # Construir tabla de símbolos
    tabla_error = tabla(tree, imprime)
    
    # Verificar tipos
    type_error = type_check(tree)
    
    # Imprimir resultado
    if not tabla_error and not type_error:
        print("\nAnálisis semántico completado sin errores.")
    else:
        print("\nSe encontraron errores durante el análisis semántico.")
    
    return tabla_error or type_error