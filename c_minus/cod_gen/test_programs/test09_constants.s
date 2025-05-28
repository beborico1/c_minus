# C- Compilation to MIPS
# File: test_programs/test09_constants.s
.data
newline: .asciiz "\n"

.text
.globl main

# -> Function: main
main:
# -> compound
# -> Call: output
# -> Const
    li $a0, 100
# <- Const
    li $v0, 1
    syscall
    li $v0, 4
    la $a0, newline
    syscall
# <- Call: output
# -> Call: output
# -> Const
    li $a0, 0
# <- Const
    li $v0, 1
    syscall
    li $v0, 4
    la $a0, newline
    syscall
# <- Call: output
# -> Call: output
# -> Const
    li $a0, 999
# <- Const
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
