#!/usr/bin/env python3
"""
Script to set up the folder structure for the C- parser
"""
import os
import shutil

def create_dir(directory):
    """Create directory if it doesn't exist"""
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    else:
        print(f"Directory already exists: {directory}")

def create_file(filepath, content):
    """Create a file with the given content"""
    with open(filepath, 'w') as f:
        f.write(content)
    print(f"Created file: {filepath}")

def setup_structure():
    """Set up the folder structure for the C- parser"""
    print("Setting up C- parser project structure...")
    
    # Create main directory and subdirectories
    create_dir("parser")
    
    # Create or copy the sample.c- file if it doesn't exist
    sample_content = '''/* A sample program in C-
   Computing factorial
*/

int factorial(int n)
{
    if (n <= 1)
        return 1;
    else
        return n * factorial(n-1);
}

void main(void)
{
    int x; /* input value */
    int result; /* result */
    
    x = input();
    result = factorial(x);
    output(result);
}
'''
    if not os.path.exists("sample.c-"):
        create_file("sample.c-", sample_content)
    else:
        print("File already exists: sample.c-")
    
    print("\nSetup completed successfully!")
    print("\nTo run the parser, execute the following command:")
    print("python3 main.py")
    print("\nIf you encounter any issues, make sure all required files are in the correct locations.")

if __name__ == "__main__":
    setup_structure()