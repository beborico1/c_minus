# C- Compilation to MIPS
# File: test_programs/test04_multiple_functions.s
.data
newline: .asciiz "\n"

.text
.globl main

# -> Function: multiply
func_multiply:
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
    mul $a0, $t0, $a0
# <- Op
    lw $ra, 8($sp)
    addi $sp, $sp, 12
    jr $ra
# <- return
# <- compound
# <- Function: multiply
# -> Function: add
func_add:
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
    add $a0, $t0, $a0
# <- Op
    lw $ra, 8($sp)
    addi $sp, $sp, 12
    jr $ra
# <- return
# <- compound
# <- Function: add
# -> Function: main
main:
    addi $sp, $sp, -4
# -> compound
# -> assign
# -> Call: add
# -> Call: multiply
# -> Const
    li $a0, 3
# <- Const
    move $t0, $a0
# -> Const
    li $a0, 4
# <- Const
    move $a1, $a0
    move $a0, $t0
    jal func_multiply
# <- Call: multiply
    move $t0, $a0
# -> Const
    li $a0, 5
# <- Const
    move $a1, $a0
    move $a0, $t0
    jal func_add
# <- Call: add
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
