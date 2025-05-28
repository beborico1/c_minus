# C- Semantic Analyzer (Combined Implementation)

This is a combined implementation of the C- semantic analyzer, based on the best aspects of both Bebo's and Omar's projects while fixing the issues highlighted in their respective error files.

## Issues Fixed

From Bebo's implementation:
- Improved verification of undeclared variables
- Added checking for incorrectly assigned types

From Omar's implementation:
- Fixed the issue where all variables were being marked as undeclared
- Fixed false positive type error detection

## Project Structure

- `main.py`: The main entry point for the semantic analyzer
- `analyze.py`: The combined semantic analysis implementation
- `symtab.py`: The improved symbol table implementation
- `Parser.py`: Reused from Bebo's implementation
- `Lexer.py`: Reused from Bebo's implementation
- `globalTypes.py`: Reused from Bebo's implementation

## Usage

```bash
python main.py <filename.c->
```

## Key Improvements

1. **Robust Symbol Table**: Enhanced symbol table implementation with better scope handling and more comprehensive information tracking.

2. **Improved Type Checking**: Fixed issues with type checking to avoid false positives and negatives.

3. **Better Variable Declaration Checking**: Ensures variables are properly declared before being used.

4. **Clearer Error Messages**: More descriptive error messages that indicate the exact nature of the problem.

5. **Combined Architecture**: Took the best design aspects from both implementations for a more maintainable codebase.

## Implementation Details

- The symbol table now tracks both the type and the kind (var, func, param) of each identifier
- Scope handling is improved with a stack-based approach and proper entry/exit management
- Type checking correctly handles arrays, function calls, and assignments
- Error reporting is more precise and includes line numbers

## Contributors

This combined implementation was created by merging and improving the work of Bebo and Omar. 