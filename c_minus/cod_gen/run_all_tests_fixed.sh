#!/bin/bash

# Script to run all test cases systematically
echo "=========================================="
echo "Running C- Compiler Test Suite"
echo "=========================================="

PASSED=0
FAILED=0
TOTAL=15

for i in $(seq -f "%02g" 0 15); do
    if [ "$i" = "00" ]; then
        testfile="test_programs/test0_simple"
    else
        testfile="test_programs/test${i}_"
        case $i in
            01) testfile="${testfile}arithmetic" ;;
            02) testfile="${testfile}globals" ;;
            03) testfile="${testfile}locals" ;;
            04) testfile="${testfile}multiple_functions" ;;
            05) testfile="${testfile}nested_calls" ;;
            06) testfile="${testfile}single_param" ;;
            07) testfile="${testfile}no_params" ;;
            08) testfile="${testfile}complex_expr" ;;
            09) testfile="${testfile}constants" ;;
            10) testfile="${testfile}subtraction" ;;
            11) testfile="${testfile}division" ;;
            12) testfile="${testfile}large_nums" ;;
            13) testfile="${testfile}mixed_vars" ;;
            14) testfile="${testfile}chain_calls" ;;
            15) testfile="${testfile}comprehensive" ;;
        esac
    fi
    
    echo "----------------------------------------"
    echo "Test $i: $testfile"
    echo "----------------------------------------"
    
    # Compile test
    if python main.py "$testfile" >/dev/null 2>&1; then
        echo "✅ Compilation: SUCCESS"
        
        # Run test with safe runner
        if ./run_spim_safe.sh "${testfile}.s" >/tmp/test_output 2>&1; then
            echo "✅ Execution: SUCCESS"
            echo "Output:"
            grep -v "Running SPIM\|Max output\|Timeout\|WARNING\|Loaded:\|----------------------------------------\|NOTE:" /tmp/test_output | head -10
            PASSED=$((PASSED + 1))
        else
            echo "❌ Execution: FAILED"
            echo "Error output:"
            cat /tmp/test_output | head -5
            FAILED=$((FAILED + 1))
        fi
    else
        echo "❌ Compilation: FAILED" 
        FAILED=$((FAILED + 1))
    fi
    
    echo ""
done

echo "=========================================="
echo "Test Suite Results:"
echo "PASSED: $PASSED"
echo "FAILED: $FAILED"
echo "TOTAL:  $TOTAL"
echo "SUCCESS RATE: $(( PASSED * 100 / TOTAL ))%"
echo "=========================================="