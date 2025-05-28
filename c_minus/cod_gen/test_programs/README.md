# Semantic Analyzer Test Suite

This directory contains comprehensive test cases for the C- semantic analyzers.

## Test Files

### test0_simple.c-
**Purpose**: Basic valid program  
**Expected**: No errors  
- Variable declarations
- Function definitions
- Function calls
- Built-in functions (input/output)

### test1_basic_declarations.c-
**Purpose**: Basic variable and array declarations  
**Expected**: No errors  
- Global variables
- Local variables
- Array declarations
- Array element access

### test2_undeclared_vars.c-
**Purpose**: Test undeclared variable detection  
**Expected**: 2 errors  
- `y` not declared (line 7)
- `z` not declared (line 8)

### test3_type_mismatch_ops.c-
**Purpose**: Type checking in arithmetic operations  
**Expected**: 3 errors  
- void + int (line 20)
- int - void (line 21)
- void * void (line 22)

### test4_array_operations.c-
**Purpose**: Array type checking  
**Expected**: 3 errors  
- Cannot assign to whole array (line 16)
- x is not an array (line 17)
- Index must be integer (line 21)

### test5_function_calls.c-
**Purpose**: Function call argument checking  
**Expected**: 6 errors  
- Too few arguments (line 26)
- Too many arguments (line 27)
- Too many arguments (line 28)
- Unknown function (line 29)
- First arg should be int, not void (line 32)
- First arg should be array (line 33)

### test6_return_types.c-
**Purpose**: Return type checking  
**Expected**: 3 errors  
- Missing return value in int function (line 12)
- Return value in void function (line 16)
- Return type mismatch (line 20)

### test7_control_flow.c-
**Purpose**: Control flow condition type checking  
**Expected**: 2 errors  
- Invalid if condition (line 28)
- Invalid while condition (line 32)

### test8_scope_checking.c-
**Purpose**: Variable scope checking  
**Expected**: 4 errors  
- `local1` not in scope (line 17)
- `y` not in scope (line 31)
- `z` not in scope (line 40)

### test9_complex_expressions.c-
**Purpose**: Complex expression type checking  
**Expected**: 2 errors  
- factorial argument must be int (line 33)
- Array index must be int (line 36)

### test10_redeclarations.c-
**Purpose**: Variable and function redeclaration detection  
**Expected**: 4 errors  
- x already declared (line 4)
- func already declared (line 10)
- a already declared (line 17)
- b already declared (line 21)

### test11_void_restrictions.c-
**Purpose**: Void type restrictions  
**Expected**: 3 errors  
- Variables cannot be void (line 3)
- Parameters cannot be void (line 5)
- Variables cannot be void (line 18)

### test12_builtin_functions.c-
**Purpose**: Built-in function usage  
**Expected**: 3 errors  
- output requires 1 argument (line 13)
- output takes only 1 argument (line 14)
- input takes no arguments (line 16)

## Running Tests

### Option 1: Run all tests
```bash
python run_all_tests.py
```

### Option 2: Run simple test
```bash
python test_simple.py
```

### Option 3: Run individual test with specific analyzer
```bash
# For Bebo's analyzer
cd bebo
python mainSemantica.py ../test_programs/test1_basic_declarations.c-

# For Omar's analyzer
cd omar
cp ../test_programs/test1_basic_declarations.c- sample.c-
python main.py
```

## Expected Results

Both semantic analyzers should:
1. ✅ Detect all undeclared variables
2. ✅ Check type compatibility in operations
3. ✅ Verify function argument types
4. ✅ Check array usage
5. ✅ Validate return types
6. ✅ Handle scope correctly
7. ✅ Detect redeclarations
8. ✅ Enforce void type restrictions

## Notes

- Bebo's analyzer was fixed to check types instead of forcing them
- Omar's analyzer fixed version is in `semantica_fixed.py`
- Both analyzers now properly implement all semantic checks required for C-