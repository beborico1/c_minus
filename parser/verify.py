#!/usr/bin/env python3
"""
Script to verify and fix the sample.c- file
"""
import os

def verify_and_fix_sample():
    """Verify that sample.c- exists and has the correct content"""
    sample_path = "sample.c-"
    
    # Check if file exists
    if not os.path.exists(sample_path):
        print(f"Creating {sample_path}...")
        create_sample_file(sample_path)
        return
    
    # Check file content
    with open(sample_path, 'r') as f:
        content = f.read()
    
    # Check if content looks right
    if "factorial" in content and "main" in content:
        print(f"File {sample_path} seems OK.")
    else:
        print(f"File {sample_path} doesn't seem to contain a valid C- program.")
        response = input("Do you want to replace it with a valid C- sample? (y/n): ")
        if response.lower() == 'y':
            create_sample_file(sample_path)

def create_sample_file(path):
    """Create a valid sample.c- file"""
    sample_content = """/* A sample program in C-
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
"""
    with open(path, 'w') as f:
        f.write(sample_content)
    print(f"Created valid sample file: {path}")

if __name__ == "__main__":
    verify_and_fix_sample()