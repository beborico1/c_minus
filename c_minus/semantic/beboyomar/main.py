#!/usr/bin/env python3
# main.py - Main file for the semantic analyzer
# Combined implementation from bebo and omar

import sys
import os
import shutil

# Check if Parser.py and Lexer.py exist
# If not, copy them from either bebo or omar
if not os.path.exists("Parser.py"):
    print("Copying Parser.py from bebo...")
    shutil.copy("../bebo/Parser.py", ".")

if not os.path.exists("Lexer.py"):
    print("Copying Lexer.py from bebo...")
    shutil.copy("../bebo/Lexer.py", ".")

if not os.path.exists("globalTypes.py"):
    print("Copying globalTypes.py from bebo...")
    shutil.copy("../bebo/globalTypes.py", ".")

# Import the modules after copying files
from globalTypes import *
import Parser
import analyze

def main():
    # Check command line arguments
    if len(sys.argv) != 2:
        print("Usage: python main.py <filename.c->")
        sys.exit(1)
    
    filename = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(filename):
        print(f"Error: File '{filename}' not found.")
        sys.exit(1)
    
    # Parse the file (creates syntax tree)
    print(f"Parsing {filename}...")
    tree = Parser.parse(filename)
    
    if tree is None:
        print("Syntax analysis failed.")
        sys.exit(1)
    
    print("\nSyntax analysis completed successfully.")
    
    # Semantic analysis
    print("\nStarting semantic analysis...")
    result = analyze.semantica(tree)
    
    if result:
        print("\nSemantic analysis completed with errors.")
    else:
        print("\nSemantic analysis completed successfully.")

if __name__ == "__main__":
    main() 