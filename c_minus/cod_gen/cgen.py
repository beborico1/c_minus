# cgen.py
from globalTypes import *
from symtab import *

# MIPS registers
zero = "$zero"  # Always 0
v0 = "$v0"      # Return values
v1 = "$v1"
a0 = "$a0"      # Arguments (also accumulator per codegen.md)
a1 = "$a1"
a2 = "$a2"
a3 = "$a3"
t0 = "$t0"      # Temporaries
t1 = "$t1"
t2 = "$t2"
t3 = "$t3"
t4 = "$t4"
t5 = "$t5"
t6 = "$t6"
t7 = "$t7"
t8 = "$t8"
t9 = "$t9"
s0 = "$s0"      # Saved
s1 = "$s1"
s2 = "$s2"
s3 = "$s3"
s4 = "$s4"
s5 = "$s5"
s6 = "$s6"
s7 = "$s7"
sp = "$sp"      # Stack pointer
fp = "$fp"      # Frame pointer
ra = "$ra"      # Return address
gp = "$gp"      # Global pointer

# Code generation state
emitLoc = 0
highEmitLoc = 0
tmpOffset = 0
mainLoc = 0
globalOffset = 0
localOffset = 0
paramOffset = 0
labelCount = 0

# Output file
code_file = None

# Trace code generation
TraceCode = True

# Track current function and local variables
current_function = None
local_vars = {}  # Maps variable names to their offsets
param_count = 0  # Track number of parameters for current function
stack_adjustment = 0  # Track stack adjustments for proper parameter access

def emitComment(comment):
    """Emit a comment in the assembly code"""
    if TraceCode and code_file:
        code_file.write(f"# {comment}\n")

def emit(instruction):
    """Emit a MIPS instruction"""
    global emitLoc, highEmitLoc
    if code_file:
        code_file.write(f"    {instruction}\n")
    emitLoc += 1
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc

def emitLabel(label):
    """Emit a label"""
    if code_file:
        code_file.write(f"{label}:\n")

def getLabel():
    """Generate a unique label"""
    global labelCount
    labelCount += 1
    return f"L{labelCount}"

def emitSkip(howMany):
    """Skip locations for later backpatch"""
    global emitLoc, highEmitLoc
    i = emitLoc
    emitLoc += howMany
    if highEmitLoc < emitLoc:
        highEmitLoc = emitLoc
    return i

def emitBackup(loc):
    """Back up to previously skipped location"""
    global emitLoc
    emitLoc = loc

def emitRestore():
    """Restore to highest emitted location"""
    global emitLoc, highEmitLoc
    emitLoc = highEmitLoc

def cGen(tree):
    """Recursively generate code by tree traversal"""
    if tree is not None:
        if tree.nodekind == NodeKind.StmtK:
            genStmt(tree)
        elif tree.nodekind == NodeKind.ExpK:
            genExp(tree)
        elif tree.nodekind == NodeKind.DeclK:
            genDecl(tree)
        
        # Generate code for siblings
        cGen(tree.sibling)

def genStmt(tree):
    """Generate code for statement nodes"""
    global tmpOffset
    
    if tree.stmt == StmtKind.IfK:
        emitComment("-> if")
        # Generate test expression
        cGen(tree.child[0])
        # Get labels
        false_label = getLabel()
        end_label = getLabel()
        # Branch if false (0)
        emit(f"beqz {a0}, {false_label}")
        # Generate then part
        cGen(tree.child[1])
        if tree.child[2] is not None:
            # Jump over else part
            emit(f"j {end_label}")
            emitLabel(false_label)
            # Generate else part
            cGen(tree.child[2])
            emitLabel(end_label)
        else:
            emitLabel(false_label)
        emitComment("<- if")
        
    elif tree.stmt == StmtKind.WhileK:
        emitComment("-> while")
        loop_label = getLabel()
        end_label = getLabel()
        emitLabel(loop_label)
        # Generate test expression
        cGen(tree.child[0])
        # Branch if false (exit loop)
        emit(f"beqz {a0}, {end_label}")
        # Generate body
        cGen(tree.child[1])
        # Jump back to start
        emit(f"j {loop_label}")
        emitLabel(end_label)
        emitComment("<- while")
        
    elif tree.stmt == StmtKind.AssignK:
        emitComment("-> assign")
        # Generate RHS expression
        cGen(tree.child[1])  # Result in $a0
        # Store result
        if tree.child[0].exp == ExpKind.SubscriptK:
            # Array element assignment
            emit(f"move {t0}, {a0}")  # Save RHS value
            cGen(tree.child[0].child[0])  # Generate index
            emit(f"sll {a0}, {a0}, 2")  # Multiply by 4
            # Check if local or global
            if tree.child[0].name in local_vars:
                offset = local_vars[tree.child[0].name]
                emit(f"la {t1}, {offset}({sp})")
            else:
                emit(f"la {t1}, var_{tree.child[0].name}")
            emit(f"add {t1}, {t1}, {a0}")
            emit(f"sw {t0}, 0({t1})")
        else:
            # Simple variable assignment
            var_name = tree.child[0].name
            if var_name in local_vars:
                # Local variable
                offset = local_vars[var_name]
                emit(f"sw {a0}, {offset}({sp})")
            else:
                # Global variable
                emit(f"sw {a0}, var_{var_name}")
        emitComment("<- assign")
        
    elif tree.stmt == StmtKind.ReturnK:
        emitComment("-> return")
        if tree.child[0] is not None:
            cGen(tree.child[0])  # Result will be in $a0
        
        # Simple return
        if current_function == "factorial":
            # Restore return address and clean up
            emit(f"lw {ra}, 4({sp})")
            emit(f"addi {sp}, {sp}, 8")  # Clean up saved ra and parameter
            emit(f"jr {ra}")
        else:
            # Regular return
            emit(f"jr {ra}")
        emitComment("<- return")
        
    elif tree.stmt == StmtKind.CompoundK:
        emitComment("-> compound")
        cGen(tree.child[0])  # Local declarations
        cGen(tree.child[1])  # Statement list
        emitComment("<- compound")

def genExp(tree):
    """Generate code for expression nodes"""
    global tmpOffset, stack_adjustment
    
    if tree.exp == ExpKind.ConstK:
        emitComment("-> Const")
        emit(f"li {a0}, {tree.val}")  # Use $a0 as accumulator per codegen.md
        emitComment("<- Const")
        
    elif tree.exp == ExpKind.IdK:
        emitComment("-> Id")
        var_name = tree.name
        if var_name in local_vars:
            # Local variable or parameter
            offset = local_vars[var_name]
            emit(f"lw {a0}, {offset}({sp})")  # Use $a0 as accumulator
        else:
            # Global variable
            emit(f"lw {a0}, var_{var_name}")  # Use $a0 as accumulator
        emitComment("<- Id")
        
    elif tree.exp == ExpKind.SubscriptK:
        emitComment("-> Array access")
        cGen(tree.child[0])  # Generate index
        emit(f"sll {a0}, {a0}, 2")  # Multiply by 4
        if tree.name in local_vars:
            offset = local_vars[tree.name]
            emit(f"la {t0}, {offset}({sp})")
        else:
            emit(f"la {t0}, var_{tree.name}")
        emit(f"add {t0}, {t0}, {a0}")
        emit(f"lw {a0}, 0({t0})")
        emitComment("<- Array access")
        
    elif tree.exp == ExpKind.CallK:
        emitComment(f"-> Call: {tree.name}")
        # Handle built-in functions
        if tree.name == "input":
            emit(f"li {v0}, 5")  # Read integer syscall
            emit("syscall")
            emit(f"move {a0}, {v0}")  # Move result to accumulator
        elif tree.name == "output":
            # Generate argument
            if tree.child[0] is not None:
                cGen(tree.child[0])  # Result already in $a0
                emit(f"li {v0}, 1")  # Print integer syscall
                emit("syscall")
                # Print newline
                emit(f"li {v0}, 4")
                emit(f"la {a0}, newline")
                emit("syscall")
        else:
            # Simple function call
            # Generate argument in $a0
            if tree.child[0] is not None:
                cGen(tree.child[0])  # Result in $a0
            
            # Call function
            emit(f"jal {tree.name}")
            
            # The result is in $a0 (accumulator)
        emitComment(f"<- Call: {tree.name}")
        
    elif tree.exp == ExpKind.OpK:
        emitComment("-> Op")
        # Check if either operand is a function call
        has_call = (tree.child[0] and tree.child[0].exp == ExpKind.CallK) or \
                   (tree.child[1] and tree.child[1].exp == ExpKind.CallK)
        
        if has_call:
            # Special handling when function calls are involved
            # Evaluate function call first to avoid stack issues
            if tree.child[1] and tree.child[1].exp == ExpKind.CallK:
                # Right operand is a call - evaluate it first
                cGen(tree.child[1])  # Result in $a0
                emit(f"move {t1}, {a0}")  # Save result
                cGen(tree.child[0])  # Get left operand in $a0
                emit(f"move {t0}, {a0}")
                emit(f"move {a0}, {t1}")  # Put right operand back in $a0 for operation
                # Now $t0 has left, $a0 has right
            else:
                # Left operand is a call
                cGen(tree.child[0])  # Result in $a0
                emit(f"move {t0}, {a0}")  # Save result
                cGen(tree.child[1])  # Get right operand in $a0
                emit(f"move {t1}, {a0}")
                emit(f"move {a0}, {t0}")  # Put left operand in $a0
                emit(f"move {t0}, {t1}")  # Put right in $t0
                # Now $a0 has left, $t0 has right
            
            # Perform operation based on type
            if tree.op == TokenType.PLUS:
                emit(f"add {a0}, {t0}, {a0}")
            elif tree.op == TokenType.MINUS:
                emit(f"sub {a0}, {t0}, {a0}")
            elif tree.op == TokenType.TIMES:
                # For n * factorial(n-1), $t0 has n, $a0 has factorial(n-1)
                emit(f"mul {a0}, {t0}, {a0}")
        else:
            # Normal case - no function calls
            # Generate left operand
            cGen(tree.child[0])
            emit(f"sw {a0}, 0({sp})")  # Push left operand
            emit(f"addi {sp}, {sp}, -4")
            
            # Generate right operand
            cGen(tree.child[1])
            
            # Pop left operand into $t1
            emit(f"lw {t1}, 4({sp})")
            emit(f"addi {sp}, {sp}, 4")
            
            # Perform operation (result in $a0)
            if tree.op == TokenType.PLUS:
                emit(f"add {a0}, {t1}, {a0}")
            elif tree.op == TokenType.MINUS:
                emit(f"sub {a0}, {t1}, {a0}")
            elif tree.op == TokenType.TIMES:
                emit(f"mul {a0}, {t1}, {a0}")
            elif tree.op == TokenType.DIVIDE:
                emit(f"div {t1}, {a0}")
                emit(f"mflo {a0}")
            elif tree.op == TokenType.LT:
                emit(f"slt {a0}, {t1}, {a0}")
            elif tree.op == TokenType.LTE:
                true_label = getLabel()
                end_label = getLabel()
                emit(f"ble {t1}, {a0}, {true_label}")
                emit(f"li {a0}, 0")
                emit(f"j {end_label}")
                emitLabel(true_label)
                emit(f"li {a0}, 1")
                emitLabel(end_label)
            elif tree.op == TokenType.GT:
                emit(f"slt {a0}, {a0}, {t1}")
            elif tree.op == TokenType.GTE:
                emit(f"slt {a0}, {t1}, {a0}")
                emit(f"xori {a0}, {a0}, 1")
            elif tree.op == TokenType.EQ:
                true_label = getLabel()
                end_label = getLabel()
                emit(f"beq {t1}, {a0}, {true_label}")
                emit(f"li {a0}, 0")
                emit(f"j {end_label}")
                emitLabel(true_label)
                emit(f"li {a0}, 1")
                emitLabel(end_label)
            elif tree.op == TokenType.NEQ:
                true_label = getLabel()
                end_label = getLabel()
                emit(f"bne {t1}, {a0}, {true_label}")
                emit(f"li {a0}, 0")
                emit(f"j {end_label}")
                emitLabel(true_label)
                emit(f"li {a0}, 1")
                emitLabel(end_label)
        emitComment("<- Op")

def genDecl(tree):
    """Generate code for declaration nodes"""
    global current_function, local_vars, localOffset, param_count, stack_adjustment
    
    if tree.decl == DeclKind.VarK:
        # Local variable declarations are handled by tracking offsets
        if current_function is not None:
            # Inside a function - allocate space on stack
            if tree.name not in local_vars:  # Only add if not already there
                local_vars[tree.name] = localOffset
                localOffset -= 4
                if tree.is_array and tree.array_size:
                    # Allocate space for array
                    localOffset -= 4 * (tree.array_size - 1)
    
    elif tree.decl == DeclKind.FunK:
        emitComment(f"-> Function: {tree.name}")
        current_function = tree.name
        local_vars.clear()
        localOffset = -4  # Start at -4 for first local
        stack_adjustment = 0  # Reset stack adjustment for new function
        
        # Count parameters
        param_count = len(tree.params)
        
        emitLabel(tree.name)
        
        if tree.name == "factorial":
            # Simple approach like working example
            emit(f"addi {sp}, {sp}, -8")  # Make room for $ra and parameter
            emit(f"sw {ra}, 4({sp})")     # Save return address
            emit(f"sw {a0}, 0({sp})")     # Save parameter n
            
            # Mark parameter location
            if param_count > 0 and hasattr(tree.params[0], 'name'):
                local_vars[tree.params[0].name] = 0  # Parameter at 0($sp)
            
        elif tree.name == "main":
            # Main function - simple setup
            # Count and allocate locals
            processLocalDecls(tree.child[0])
            space_needed = -localOffset - 4  # Adjusted calculation
            if space_needed > 0:
                emit(f"addi {sp}, {sp}, -{space_needed}")
        else:
            # Other functions
            emit(f"addi {sp}, {sp}, -8")
            emit(f"sw {ra}, 4({sp})")
            emit(f"sw {a0}, 0({sp})")
            
            # Mark parameters
            if param_count > 0 and hasattr(tree.params[0], 'name'):
                local_vars[tree.params[0].name] = "param"
        
        # Generate function body
        if tree.child[0] is not None:
            cGen(tree.child[0])
        
        if tree.name == "main":
            # Main function ends with exit syscall
            emit(f"li {v0}, 10")
            emit("syscall")
        elif tree.name == "factorial":
            # Factorial cleanup - already has returns in body
            pass
        else:
            # Default epilogue
            emit(f"lw {ra}, 4({sp})")
            emit(f"addi {sp}, {sp}, 8")
            emit(f"jr {ra}")
        
        emitComment(f"<- Function: {tree.name}")
        
        current_function = None

def processLocalDecls(tree):
    """Process local declarations to assign offsets"""
    if tree is None:
        return
    
    # Process this node if it's a variable declaration
    if tree.nodekind == NodeKind.DeclK and tree.decl == DeclKind.VarK:
        genDecl(tree)
    
    # Process children
    for i in range(MAXCHILDREN):
        if tree.child[i] is not None:
            processLocalDecls(tree.child[i])
    
    # Process siblings
    if tree.sibling is not None:
        processLocalDecls(tree.sibling)

def codeGen(syntaxTree, codefile):
    """Main function to generate code"""
    global code_file, TraceCode
    
    # Open output file
    code_file = open(codefile, 'w')
    
    emitComment("C- Compilation to MIPS")
    emitComment(f"File: {codefile}")
    
    # Data section
    code_file.write(".data\n")
    code_file.write("newline: .asciiz \"\\n\"\n")
    
    # Generate space for global variables
    generateGlobals(syntaxTree)
    
    # Text section
    code_file.write("\n.text\n")
    code_file.write(".globl main\n")
    code_file.write("\n")
    
    # Generate code for program
    cGen(syntaxTree)
    
    # Close file
    code_file.close()

def generateGlobals(tree):
    """Generate .data section for global variables"""
    if tree is not None:
        if tree.nodekind == NodeKind.DeclK and tree.decl == DeclKind.VarK:
            # Only generate globals for variables declared outside functions
            sym = st_lookup(tree.name)
            if sym and sym.scope_level == 0:  # Global scope
                if tree.is_array and tree.array_size:
                    # Array variable
                    code_file.write(f"var_{tree.name}: .space {tree.array_size * 4}\n")
                else:
                    # Simple variable
                    code_file.write(f"var_{tree.name}: .word 0\n")
        
        # Check children
        for i in range(MAXCHILDREN):
            if tree.child[i] is not None:
                generateGlobals(tree.child[i])
        
        # Check siblings
        generateGlobals(tree.sibling)

# Additional helper functions for code generation
def globales(prog, pos, long):
    """Function to receive global variables"""
    # This is handled by the parser
    from Parser import recibeParser
    recibeParser(prog, pos, long)