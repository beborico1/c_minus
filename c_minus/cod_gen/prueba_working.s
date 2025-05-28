# Simple Factorial Program for MARS
# This version uses minimal stack manipulation

.data
    prompt: .asciiz "Enter a number: "
    result: .asciiz "Factorial is: "
    newline: .asciiz "\n"

.text
.globl main

main:
    # Hardcode input value 5
    li $a0, 5             # Load 5 directly into $a0 for factorial
    
    # Call factorial
    jal factorial
    move $s0, $v0         # Save result
    
    # Print result message
    li $v0, 4
    la $a0, result
    syscall
    
    # Print factorial result
    li $v0, 1
    move $a0, $s0
    syscall
    
    # Print newline
    li $v0, 4
    la $a0, newline
    syscall
    
    # Exit
    li $v0, 10
    syscall

# Factorial function
# Input: $a0 = n
# Output: $v0 = n!
factorial:
    # Save return address
    addi $sp, $sp, -8
    sw $ra, 4($sp)
    sw $a0, 0($sp)        # Save n
    
    # Base case: if n <= 1, return 1
    li $t0, 1
    ble $a0, $t0, return_one
    
    # Recursive case: n * factorial(n-1)
    addi $a0, $a0, -1     # n-1
    jal factorial         # factorial(n-1)
    
    # Multiply by n
    lw $t0, 0($sp)        # Reload n
    mul $v0, $t0, $v0     # n * factorial(n-1)
    
    j factorial_done
    
return_one:
    li $v0, 1
    
factorial_done:
    lw $ra, 4($sp)
    addi $sp, $sp, 8
    jr $ra