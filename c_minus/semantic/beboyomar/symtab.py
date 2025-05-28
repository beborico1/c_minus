# symtab.py - Combined and improved symbol table implementation
# Based on bebo's and omar's implementations

import copy

class SymTabEntry:
    """Class for managing symbol table entries"""
    def __init__(self, name, type_spec, kind, lineno, is_array=False, size=None, params=None, return_type=None):
        self.name = name                  # Name of the identifier
        self.type_spec = type_spec        # Data type (int, void)
        self.kind = kind                  # var, func, param
        self.lines = [lineno]             # List of line numbers where it's used
        self.scope_level = current_scope  # Current scope level
        self.is_array = is_array          # Whether it's an array
        self.size = size                  # Size of array (if applicable)
        self.params = params or []        # Parameters (for functions)
        self.return_type = return_type    # Return type (for functions)

# Symbol table implemented as a dictionary
# The key is a tuple (scope, name) to handle scopes
table = {}
scope_stack = [0]  # Stack of scopes (first is global)
current_scope = 0  # Current scope
scope_count = 0    # Counter to create new scopes
scopes_done = []   # List of all finished scopes (for printing)

def st_enter_scope():
    """Create a new scope and make it the current scope"""
    global scope_count, current_scope, scope_stack
    scope_count += 1
    current_scope = scope_count
    scope_stack.append(current_scope)
    return current_scope

def st_exit_scope():
    """Exit the current scope and return to the previous scope"""
    global current_scope, scope_stack, table, scopes_done
    
    # Save the current scope's entries to scopes_done for printing
    current_entries = {}
    for key, entry in table.items():
        if key[0] == current_scope:
            current_entries[entry.name] = entry
    
    if current_entries:
        scopes_done.insert(0, copy.deepcopy(current_entries))
    
    if len(scope_stack) > 1:
        scope_stack.pop()
        current_scope = scope_stack[-1]
    return current_scope

def st_insert(name, type_spec, kind, lineno, is_array=False, size=None, params=None, return_type=None):
    """
    Insert a symbol into the table
    
    Args:
        name: Name of the identifier
        type_spec: Data type (int, void)
        kind: Kind of symbol (var, func, param)
        lineno: Line number
        is_array: Whether it's an array
        size: Size of array (if applicable)
        params: Parameters (for functions)
        return_type: Return type (for functions)
    
    Returns:
        True if it's a new insertion, False if it already existed
    """
    global table, current_scope
    
    # Create a unique key for this scope and name
    key = (current_scope, name)
    
    # If it already exists in the current scope, just add the line number
    if key in table:
        if lineno not in table[key].lines:
            table[key].lines.append(lineno)
        return False  # Not a new insertion
    else:
        # Create new entry
        table[key] = SymTabEntry(
            name=name,
            type_spec=type_spec,
            kind=kind,
            lineno=lineno,
            is_array=is_array,
            size=size,
            params=params,
            return_type=return_type
        )
        return True  # New insertion

def st_lookup(name, current_scope_only=False):
    """
    Look up a symbol in the table
    
    Args:
        name: Name of the identifier to look up
        current_scope_only: If True, only searches in the current scope
    
    Returns:
        The symbol table entry or None if not found
    """
    global table, current_scope, scope_stack
    
    # First look in the current scope
    key = (current_scope, name)
    if key in table:
        return table[key]
    
    # If only searching in the current scope or it's found, end
    if current_scope_only:
        return None
    
    # Search in parent scopes (from bottom to top)
    for scope in reversed(scope_stack[:-1]):
        key = (scope, name)
        if key in table:
            return table[key]
    
    # Not found
    return None

def st_lookup_all_scopes(name):
    """
    Look up a symbol in all scopes
    
    Args:
        name: Name of the identifier to look up
    
    Returns:
        List of symbol table entries
    """
    global table
    
    entries = []
    for key, entry in table.items():
        if key[1] == name:
            entries.append(entry)
    
    return entries

def printSymTab():
    """Print the symbol table in a readable format"""
    global table
    
    print("\nSymbol Table:")
    print("=" * 90)
    print(f"{'Scope':<8}{'Name':<15}{'Type':<10}{'Kind':<10}{'Lines':<15}{'Attributes':<35}")
    print("-" * 90)
    
    # Sort by scope and then by name
    sorted_keys = sorted(table.keys())
    
    for key in sorted_keys:
        entry = table[key]
        attrs = []
        
        if entry.kind == 'func':
            params_str = ""
            if entry.params:
                params_str = ", ".join([f"{p[0]}{'[]' if p[1] else ''}" for p in entry.params])
            attrs.append(f"params({params_str}) -> {entry.return_type}")
        elif entry.is_array:
            attrs.append(f"array[{entry.size}]")
            
        attrs_str = " ".join(attrs)
        lines_str = ", ".join(map(str, entry.lines))
        
        print(f"{entry.scope_level:<8}{entry.name:<15}{entry.type_spec:<10}{entry.kind:<10}{lines_str:<15}{attrs_str:<35}")
    
    print("=" * 90) 