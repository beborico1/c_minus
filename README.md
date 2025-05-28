# Python
__pycache__/
*.py[cod]
*$py.class
*.pyc
.Python
env/
venv/
.env

# IDE specific files
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Generated MIPS assembly files (except test references)
*.s
!tests/*.s
!sample.s

# C- source files (except examples and tests)
*.c-
!sample.c-
!tests/*.c-

# Output files
*.out
*.o
*.exe

# MARS/SPIM specific
*.log
*.dump
Mars*.jar

# Documentation build files
docs/_build/
*.pdf
!document.pdf

# Temporary files
*.tmp
*.temp
*.bak
.cache/

# Test output
test_output/
test_results/

# Coverage reports
htmlcov/
.coverage
.coverage.*
coverage.xml
*.cover

# Distribution / packaging
dist/
build/
*.egg-info/

# Project specific - intermediate compilation files
*.tokens
*.ast
*.sym
symbol_table.txt
parse_tree.txt

# Keep the file.s as it seems to be a reference file
!file.s

# Jupyter Notebook checkpoints (if used for testing)
.ipynb_checkpoints/

# macOS
.DS_Store
.AppleDouble
.LSOverride

# Windows
Thumbs.db
ehthumbs.db
Desktop.ini

# Linux
.directory

# Editor backups
*~
\#*\#
.\#*

# Debug files
*.log
debug/
logs/
