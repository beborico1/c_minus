# C- Compilation to MIPS
# File: test_programs/test06_single_param.s
.data
newline: .asciiz "\n"

.text
.globl main

# -> Function: square
func_square:
    addi $sp, $sp, -8
    sw $ra, 4($sp)
    sw $a0, 0($sp)
# -> compound
# -> return
# -> Op
# -> Id
    lw $a0, 0($sp)
# <- Id
    move $t0, $a0
# -> Id
    lw $a0, 0($sp)
# <- Id
    mul $a0, $t0, $a0
# <- Op
    lw $ra, 4($sp)
    addi $sp, $sp, 8
    jr $ra
# <- return
# <- compound
# <- Function: square
# -> Function: main
main:
# -> compound
# -> Call: output
# -> Call: square
# -> Const
    li $a0, 6
# <- Const
    jal func_square
# <- Call: square
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
