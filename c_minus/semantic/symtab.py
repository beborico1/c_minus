# Tabla de símbolos para C-
class SymTabEntry:
    """Clase para manejar entradas en la tabla de símbolos"""
    def __init__(self, name, type_spec, line_numbers, scope_level, attr=None):
        self.name = name                # Nombre del identificador
        self.type_spec = type_spec      # Tipo de dato (int, void, array)
        self.line_numbers = line_numbers  # Lista de números de línea
        self.scope_level = scope_level  # Nivel de ámbito
        self.attr = attr                # Atributos adicionales 
                                        # (tamaño de array, params para funciones)

# Tabla de símbolos implementada como un diccionario
# La clave es una tupla (scope, name) para manejar ámbitos
table = {}
scope_stack = [0]   # Pila de ámbitos (el primero es el global)
current_scope = 0   # Ámbito actual
scope_count = 0     # Contador para crear nuevos ámbitos

def st_enter_scope():
    """Crear un nuevo ámbito y hacerlo el ámbito actual"""
    global scope_count, current_scope, scope_stack
    scope_count += 1
    current_scope = scope_count
    scope_stack.append(current_scope)
    return current_scope

def st_exit_scope():
    """Salir del ámbito actual y volver al ámbito anterior"""
    global current_scope, scope_stack
    if len(scope_stack) > 1:
        scope_stack.pop()
        current_scope = scope_stack[-1]
    return current_scope

def st_insert(name, type_spec, lineno, attr=None):
    """
    Insertar un símbolo en la tabla
    
    Args:
        name: Nombre del identificador
        type_spec: Tipo de dato (int, void)
        lineno: Número de línea
        attr: Atributos adicionales
    
    Returns:
        True si es nueva inserción, False si ya existía
    """
    global table, current_scope
    
    # Crear clave única para este ámbito y nombre
    key = (current_scope, name)
    
    # Si ya existe en el ámbito actual, solo agregar el número de línea
    if key in table:
        if lineno not in table[key].line_numbers:
            table[key].line_numbers.append(lineno)
        return False  # No es una nueva inserción
    else:
        # Crear nueva entrada
        table[key] = SymTabEntry(
            name=name,
            type_spec=type_spec,
            line_numbers=[lineno],
            scope_level=current_scope,
            attr=attr
        )
        return True  # Nueva inserción

def st_lookup(name, current_scope_only=False):
    """
    Buscar un símbolo en la tabla
    
    Args:
        name: Nombre del identificador a buscar
        current_scope_only: Si True, solo busca en el ámbito actual
    
    Returns:
        La entrada en la tabla de símbolos o None si no se encuentra
    """
    global table, current_scope, scope_stack
    
    # Primero buscar en el ámbito actual
    key = (current_scope, name)
    if key in table:
        return table[key]
    
    # Si solo se busca en el ámbito actual o se encuentra, terminar
    if current_scope_only:
        return None
    
    # Buscar en ámbitos padre (de abajo hacia arriba)
    for scope in reversed(scope_stack[:-1]):
        key = (scope, name)
        if key in table:
            return table[key]
    
    # No se encontró
    return None

def st_lookup_all_scopes(name):
    """
    Buscar un símbolo en todos los ámbitos
    
    Args:
        name: Nombre del identificador a buscar
    
    Returns:
        Lista de entradas en la tabla de símbolos
    """
    global table
    
    entries = []
    for key, entry in table.items():
        if key[1] == name:
            entries.append(entry)
    
    return entries

def printSymTab():
    """Imprimir tabla de símbolos en un formato legible"""
    global table
    
    print("\nTabla de símbolos:")
    print("=" * 80)
    print(f"{'Ámbito':<8}{'Nombre':<15}{'Tipo':<10}{'Líneas':<20}{'Atributos':<30}")
    print("-" * 80)
    
    # Ordenar por ámbito y luego por nombre
    sorted_keys = sorted(table.keys())
    
    for key in sorted_keys:
        entry = table[key]
        attr_str = str(entry.attr) if entry.attr else ""
        lines_str = ", ".join(map(str, entry.line_numbers))
        print(f"{entry.scope_level:<8}{entry.name:<15}{entry.type_spec:<10}{lines_str:<20}{attr_str:<30}")
    print("=" * 80)