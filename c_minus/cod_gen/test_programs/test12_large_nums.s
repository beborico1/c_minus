# C- Compilation to MIPS
# File: test_programs/test12_large_nums.s
.data
newline: .asciiz "\n"

.text
.globl main

# -> Function: main
main:
    addi $sp, $sp, -4
# -> compound
# -> assign
# -> Const
    li $a0, 12345
# <- Const
    sw $a0, -4($sp)
# <- assign
# -> Call: output
# -> Id
    lw $a0, -4($sp)
# <- Id
    li $v0, 1
    syscall
    li $v0, 4
    la $a0, newline
    syscall
# <- Call: output
# <- compound
    li $v0, 10
    syscall
# <- Function: main
