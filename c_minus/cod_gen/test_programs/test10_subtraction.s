# C- Compilation to MIPS
# File: test_programs/test10_subtraction.s
.data
newline: .asciiz "\n"

.text
.globl main

# -> Function: subtract
func_subtract:
    addi $sp, $sp, -12
    sw $ra, 8($sp)
    sw $a0, 0($sp)
    sw $a1, 4($sp)
# -> compound
# -> return
# -> Op
# -> Id
    lw $a0, 0($sp)
# <- Id
    move $t0, $a0
# -> Id
    lw $a0, 4($sp)
# <- Id
    sub $a0, $t0, $a0
# <- Op
    lw $ra, 8($sp)
    addi $sp, $sp, 12
    jr $ra
# <- return
# <- compound
# <- Function: subtract
# -> Function: main
main:
# -> compound
# -> Call: output
# -> Call: subtract
# -> Const
    li $a0, 20
# <- Const
    move $t0, $a0
# -> Const
    li $a0, 7
# <- Const
    move $a1, $a0
    move $a0, $t0
    jal func_subtract
# <- Call: subtract
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
