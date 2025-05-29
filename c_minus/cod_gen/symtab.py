# Tabla de simbolos para C- con inferencia de tipos integrada
class SymTabEntry:
    """Clase para manejar entradas en la tabla de simbolos"""
    def __init__(self, name, type_spec, line_numbers, scope_level, attr=None):
        self.name = name # Nombre del identificador
        self.type_spec = type_spec # Tipo de dato (int, void, array)
        self.line_numbers = line_numbers # Lista de numeros de linea
        self.scope_level = scope_level # Nivel de ambito
        self.attr = attr # Atributos adicionales (tamaño de array, params para funciones)

# Tabla de simbolos implementada como un diccionario
# La clave es una tupla (scope, name) para manejar ambitos
table = {}
scope_stack = [0] # Pila de ambitos (el primero es el global)
current_scope = 0 # ambito actual
scope_count = 0 # Contador para crear nuevos ambitos

def st_enter_scope():
    """Crear un nuevo ambito y hacerlo el ambito actual"""
    global scope_count, current_scope, scope_stack
    scope_count += 1
    current_scope = scope_count
    scope_stack.append(current_scope)
    return current_scope

def st_exit_scope():
    """Salir del ambito actual y volver al ambito anterior"""
    global current_scope, scope_stack
    if len(scope_stack) > 1:
        scope_stack.pop()
        current_scope = scope_stack[-1]
    return current_scope

def st_insert(name, type_spec, lineno, attr=None):
    """
    Insertar un simbolo en la tabla
    
    Args:
        name: Nombre del identificador
        type_spec: Tipo de dato (int, void)
        lineno: Numero de linea
        attr: Atributos adicionales
    
    Returns:
        True si es nueva insercion, False si ya existia
    """
    global table, current_scope
    
    # Crear clave unica para este ambito y nombre
    key = (current_scope, name)
    
    # Si ya existe en el ambito actual, solo agregar el numero de linea
    if key in table:
        if lineno not in table[key].line_numbers:
            table[key].line_numbers.append(lineno)
        return False # No es una nueva insercion
    else:
        # Crear nueva entrada
        table[key] = SymTabEntry(
            name=name,
            type_spec=type_spec,
            line_numbers=[lineno],
            scope_level=current_scope,
            attr=attr
        )
        return True # Nueva insercion

def st_lookup(name, current_scope_only=False):
    """
    Buscar un simbolo en la tabla
    
    Args:
        name: Nombre del identificador a buscar
        current_scope_only: Si True, solo busca en el ambito actual
    
    Returns:
        La entrada en la tabla de simbolos o None si no se encuentra
    """
    global table, current_scope, scope_stack
    
    # Primero buscar en el ambito actual
    key = (current_scope, name)
    if key in table:
        return table[key]
    
    # Si solo se busca en el ambito actual o se encuentra, terminar
    if current_scope_only:
        return None
    
    # Buscar en ambitos padre (de abajo hacia arriba)
    for scope in reversed(scope_stack[:-1]):
        key = (scope, name)
        if key in table:
            return table[key]
    
    # No se encontro
    return None

def st_lookup_all_scopes(name):
    """
    Buscar un simbolo en todos los ambitos
    
    Args:
        name: Nombre del identificador a buscar
    
    Returns:
        Lista de entradas en la tabla de simbolos
    """
    global table
    
    entries = []
    for key, entry in table.items():
        if key[1] == name:
            entries.append(entry)
    
    return entries

def printSymTab():
    """Imprimir tabla de simbolos en un formato legible"""
    global table
    
    print("\nTabla de simbolos:")
    print("=" * 80)
    print(f"{'Ambito':<8}{'Nombre':<15}{'Tipo':<10}{'Lineas':<20}{'Atributos':<30}")
    print("-" * 80)
    
    # Ordenar por ambito y luego por nombre
    sorted_keys = sorted(table.keys())
    
    for key in sorted_keys:
        entry = table[key]
        attr_str = str(entry.attr) if entry.attr else ""
        lines_str = ", ".join(map(str, entry.line_numbers))
        print(f"{entry.scope_level:<8}{entry.name:<15}{entry.type_spec:<10}{lines_str:<20}{attr_str:<30}")
    print("=" * 80)

from globalTypes import *

def inferTypes(t):
    """
    Inferir y establecer tipos para nodos de expresion
    Esto deberia llamarse como una pasada separada antes de la verificacion de tipos
    """
    if t is None:
        return
    
    # Primero procesar hijos para obtener sus tipos
    for i in range(MAXCHILDREN):
        if t.child[i] is not None:
            inferTypes(t.child[i])
    
    # Luego inferir tipo para el nodo actual
    if t.nodekind == NodeKind.ExpK:
        inferExpType(t)
    
    # Procesar hermanos
    if t.sibling is not None:
        inferTypes(t.sibling)

def inferExpType(t):
    """Inferir tipo para nodos de expresion"""
    
    if t.exp == ExpKind.OpK:
        # Para operadores, verificar tipos de operandos
        if t.child[0] is not None and t.child[1] is not None:
            # Operadores aritmeticos y de comparacion
            if t.op in [TokenType.PLUS, TokenType.MINUS, TokenType.TIMES, TokenType.DIVIDE]:
                t.type = ExpType.Integer
            elif t.op in [TokenType.LT, TokenType.LTE, TokenType.GT, TokenType.GTE, TokenType.EQ, TokenType.NEQ]:
                t.type = ExpType.Boolean
            else:
                t.type = ExpType.Integer  # Por defecto
        else:
            t.type = ExpType.Integer  # Por defecto para operadores incompletos
    
    elif t.exp == ExpKind.ConstK:
        # Las constantes siempre son enteros en C-
        t.type = ExpType.Integer
    
    elif t.exp == ExpKind.IdK:
        # Buscar variable en la tabla de simbolos
        sym = st_lookup(t.name)
        if sym is not None:
            if sym.attr and sym.attr.get('is_array'):
                t.type = ExpType.Array
            else:
                t.type = ExpType.Integer if sym.type_spec == "int" else ExpType.Void
        else:
            t.type = ExpType.Integer  # Por defecto para no declarados (el error se detectara despues)
    
    elif t.exp == ExpKind.SubscriptK:
        # El subindice de arreglo siempre devuelve entero (tipo de elemento)
        t.type = ExpType.Integer
    
    elif t.exp == ExpKind.CallK:
        # Llamada a funcion - buscar tipo de retorno
        sym = st_lookup(t.name)
        if sym is not None:
            if sym.type_spec == "void":
                t.type = ExpType.Void
            else:
                t.type = ExpType.Integer
        else:
            t.type = ExpType.Integer  # Por defecto para funciones no declaradas
    
    elif t.exp == ExpKind.AssignK:
        # La expresion de asignacion toma el tipo del lado izquierdo
        if t.child[0] is not None:
            t.type = getattr(t.child[0], 'type', ExpType.Integer)
        else:
            t.type = ExpType.Integer
    
    # Asegurar que el tipo este establecido (por defecto Integer si no esta establecido)
    if not hasattr(t, 'type'):
        t.type = ExpType.Integer