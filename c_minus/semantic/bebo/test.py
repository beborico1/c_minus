#!/usr/bin/env python3
# -----------------------------------------------------------------------------
# test_consolidated.py
#
# Script para probar los archivos consolidados de Bebo
# Ejecuta pruebas con varios archivos .c- para verificar que todo funciona
# -----------------------------------------------------------------------------

import subprocess
import os
import sys

def run_test(test_file, test_name):
    """Run a single test and capture output"""
    print(f"\n{'='*60}")
    print(f"Test: {test_name}")
    print(f"File: {test_file}")
    print(f"{'='*60}")
    
    try:
        # Run mainSemantica.py with the test file
        result = subprocess.run(
            [sys.executable, 'mainSemantica.py', test_file],
            capture_output=True,
            text=True,
            cwd=os.path.dirname(os.path.abspath(__file__))
        )
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("\nSTDERR:")
            print(result.stderr)
        
        print(f"\nReturn code: {result.returncode}")
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"Error running test: {e}")
        return False

def main():
    """Run all tests"""
    # Test files to run
    test_cases = [
        ("../test_programs/test0_simple.c-", "Simple valid program"),
        ("../test_programs/test1_basic_declarations.c-", "Basic declarations"),
        ("../test_programs/test2_undeclared_vars.c-", "Undeclared variables (should error)"),
        ("../test_programs/test3_type_mismatch_ops.c-", "Type mismatches (should error)"),
        ("../test_programs/test4_array_operations.c-", "Array operations"),
        ("../test_programs/test5_function_calls.c-", "Function calls"),
        ("../test_programs/test6_return_types.c-", "Return type checking"),
        ("../test_programs/test7_control_flow.c-", "Control flow"),
        ("../test_programs/test8_scope_checking.c-", "Scope checking"),
        ("../test_programs/test9_complex_expressions.c-", "Complex expressions"),
        ("../test_programs/test10_redeclarations.c-", "Redeclarations (should error)"),
        ("../test_programs/test11_void_restrictions.c-", "Void restrictions (should error)"),
        ("../test_programs/test12_builtin_functions.c-", "Built-in functions"),
    ]
    
    # Also test with Bebo's sample programs if they exist
    bebo_samples = [
        ("programs/sample1.c-", "Bebo sample 1"),
        ("programs/sample2.c-", "Bebo sample 2"),
        ("programs/sample3.c-", "Bebo sample 3"),
        ("programs/sample4.c-", "Bebo sample 4"),
        ("programs/sample5.c-", "Bebo sample 5"),
    ]
    
    # Check which sample files exist and add them
    for sample_file, sample_name in bebo_samples:
        if os.path.exists(os.path.join(os.path.dirname(__file__), sample_file)):
            test_cases.append((sample_file, sample_name))
    
    passed = 0
    failed = 0
    
    print("Running tests for consolidated Bebo implementation...")
    print("Using type inference integrated into symtab.py")
    
    for test_file, test_name in test_cases:
        if run_test(test_file, test_name):
            passed += 1
            print("✓ Test completed")
        else:
            failed += 1
            print("✗ Test had issues")
    
    print(f"\n{'='*60}")
    print(f"Test Summary:")
    print(f"  Passed: {passed}")
    print(f"  Failed: {failed}")
    print(f"  Total:  {len(test_cases)}")
    print(f"{'='*60}")
    
    # Additional info about consolidation
    print("\nConsolidation Notes:")
    print("- type_inference.py has been merged into symtab.py")
    print("- inferTypes() function is now part of symtab module")
    print("- All imports have been updated accordingly")
    print("- Original type_inference.py can be deleted")

if __name__ == "__main__":
    main()