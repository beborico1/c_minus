# -----------------------------------------------------------------------------
# symtab.py
#
# Symbol table implementation consolidada para C-
# Combina funcionalidad de symtab.py y symtab_fixed.py
# Autor: Omar Rivera Arenas
# -----------------------------------------------------------------------------

from globalTypes import *

class SymbolEntry:
    """Entrada en la tabla de símbolos"""
    def __init__(self, name, kind, typ,
                 is_array=False, size=None,
                 params=None, return_type=None, lineno=0):
        self.name = name
        self.kind = kind          # 'var' | 'param' | 'func'
        self.typ = typ            # ExpType.Integer | ExpType.Void | ExpType.Boolean
        self.is_array = is_array
        self.size = size          # solo para arrays
        self.params = params or []    # lista de (typ, is_array)
        self.return_type = return_type
        self.lines = [lineno]     # Lista de líneas donde aparece
        self.lineno = lineno      # Línea de declaración
        self.scope = None         # Se establece al insertar

# Global scope stack
scope_stack = [{}]  # Start with global scope
scopes_done = []

def st_reset():
    """Reset the symbol table to initial state"""
    global scope_stack, scopes_done
    scope_stack = [{}]
    scopes_done = []

def st_push():
    """Push a new scope onto the stack"""
    global scope_stack
    scope_stack.append({})
    return len(scope_stack) - 1

def st_pop():
    """Pop the current scope from the stack"""
    global scope_stack, scopes_done
    if len(scope_stack) > 1:
        finished = scope_stack.pop()
        # Make a deep copy to preserve the scope state
        scopes_done.append(dict(finished))

def st_enter_scope():
    """Enter a new scope"""
    return st_push()

def st_exit_scope():
    """Exit the current scope"""
    st_pop()

def st_insert(name, lineno=0, **kwargs):
    """
    Insert a symbol into the current scope
    
    Args:
        name: Symbol name
        lineno: Line number where declared
        **kwargs: Additional attributes (kind, typ, params, etc.)
    """
    global scope_stack
    current_scope = scope_stack[-1]
    
    if name in current_scope:
        # Symbol already exists in current scope - add line number
        if hasattr(current_scope[name], 'lines'):
            if lineno not in current_scope[name].lines:
                current_scope[name].lines.append(lineno)
        return False
    
    # Create symbol entry
    entry = SymbolEntry(
        name=name,
        kind=kwargs.get('kind', 'var'),
        typ=kwargs.get('typ', ExpType.Integer),
        is_array=kwargs.get('is_array', False),
        size=kwargs.get('size', None),
        params=kwargs.get('params', []),
        return_type=kwargs.get('return_type', None),
        lineno=lineno
    )
    
    # Set scope level
    entry.scope = len(scope_stack) - 1
    
    # Insert into current scope
    current_scope[name] = entry
    return True

def st_lookup(name):
    """
    Look up a symbol in all visible scopes
    Returns the symbol entry or None if not found
    """
    global scope_stack
    
    # Search from current scope up to global
    for i in range(len(scope_stack) - 1, -1, -1):
        if name in scope_stack[i]:
            return scope_stack[i][name]
    
    return None

def st_lookup_current_scope(name):
    """
    Look up a symbol only in the current scope
    """
    global scope_stack
    return scope_stack[-1].get(name, None)

def current_scope():
    """Return the current scope dictionary"""
    return scope_stack[-1]

def print_symtab():
    """Print the symbol table"""
    print("\nTabla de símbolos:")
    print("=" * 84)
    print(f"{'Ámbito':<8} {'Nombre':<15} {'Tipo':<15} {'Líneas':<15} {'Atributos':<30}")
    print("-" * 84)
    
    # Combine active scopes and completed scopes
    all_scopes = []
    
    # Add active scopes
    for i, scope in enumerate(scope_stack):
        for name, symbol in scope.items():
            if hasattr(symbol, 'scope'):
                symbol.scope = i
            all_scopes.append((i, name, symbol))
    
    # Add completed scopes
    base_scope = len(scope_stack)
    for i, scope in enumerate(scopes_done):
        for name, symbol in scope.items():
            all_scopes.append((base_scope + i, name, symbol))
    
    # Sort by scope then by name
    all_scopes.sort(key=lambda x: (x[0], x[1]))
    
    # Print all symbols
    for scope_num, name, symbol in all_scopes:
        if isinstance(symbol, SymbolEntry):
            scope_str = str(symbol.scope if hasattr(symbol, 'scope') else scope_num)
            name_str = symbol.name
            
            # Determine type string
            typ = symbol.typ
            if hasattr(typ, 'name'):
                type_str = typ.name
            elif isinstance(typ, ExpType):
                if typ == ExpType.Integer:
                    type_str = 'int'
                elif typ == ExpType.Void:
                    type_str = 'void'
                elif typ == ExpType.Boolean:
                    type_str = 'boolean'
                else:
                    type_str = str(typ)
            else:
                type_str = str(typ)
            
            # Lines string
            if hasattr(symbol, 'lines'):
                lines_str = ', '.join(map(str, symbol.lines))
            else:
                lines_str = str(symbol.lineno)
            
            # Build attributes string
            attrs = []
            if symbol.kind:
                attrs.append(f"kind={symbol.kind}")
            if symbol.params:
                attrs.append(f"params={len(symbol.params)}")
            if symbol.is_array:
                attrs.append(f"array={symbol.is_array}")
                if symbol.size:
                    attrs.append(f"size={symbol.size}")
            
            attrs_str = ', '.join(attrs) if attrs else ''
            
            # Ensure no None values
            scope_str = scope_str or ''
            name_str = name_str or ''
            type_str = type_str or ''
            lines_str = lines_str or ''
            attrs_str = attrs_str or ''
            
            print(f"{scope_str:<8} {name_str:<15} {type_str:<15} {lines_str:<15} {attrs_str:<30}")
    
    print("=" * 84)