# C- Compilation to MIPS
# File: test_programs/test11_division.s
.data
newline: .asciiz "\n"

.text
.globl main

# -> Function: divide
func_divide:
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
    div $t0, $a0
    mflo $a0
# <- Op
    lw $ra, 8($sp)
    addi $sp, $sp, 12
    jr $ra
# <- return
# <- compound
# <- Function: divide
# -> Function: main
main:
# -> compound
# -> Call: output
# -> Call: divide
# -> Const
    li $a0, 15
# <- Const
    move $t0, $a0
# -> Const
    li $a0, 3
# <- Const
    move $a1, $a0
    move $a0, $t0
    jal func_divide
# <- Call: divide
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
