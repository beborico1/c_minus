# Examen Final de Compiladores

## Pregunta 1 (10 puntos)
Seleccione las opciones que contienen algún uso de la tabla de símbolos en un compilador, de los vistos en la clase. Marque todas las que apliquen.

- [ ] Verificar si una variable ya está declarada
- [ ] Guardar el apuntador a la raíz del AST
- [ ] Guardar el código que genera una expresión
- [ ] Verificar el tipo de una variable

## Pregunta 2 (10 puntos)
Si en un lenguaje de programación existe una función llamada `longitud(s)`, que está predefinida y que calcula el número de caracteres en un string `s` que recibe como parámetro (e.g. `longitud("hola")` regresa un 4), escriba una regla lógica para verificar el tipo de esta función. No pierda de vista que el parámetro puede ser una variable o una expresión que contenga variables.

Opciones:
- A) O ⊢ longitud: String / O ⊢ s: Int
- B) O ⊢ s: Int / O ⊢ longitud: String
- C) O ⊢ s: String / O ⊢ longitud: Int
- D) O ⊢ longitud: Int / O ⊢ s: String

## Pregunta 3 (10 puntos)
Seleccione la opción que contiene el número de recorridos del AST que tiene que realizar el analizador semántico visto en clase:

- [ ] 3
- [ ] No lo recorre, sólo usa las tablas de símbolos
- [ ] 2
- [ ] 1

## Pregunta 4 (10 puntos)
Suponga que se está compilando un programa en un lenguaje con declaración de variables y tipado estático. Seleccione la opción que tiene la acción que se debe realizar cuando una variable no se encuentra en la tabla de símbolos actual.

- [ ] Se busca la variable en las tablas de símbolos que están abajo en el stack
- [ ] Se marca un error de "variable no declarada"
- [ ] Se busca la variable en otras ramas del AST
- [ ] Se coloca la variable en la tabla de símbolos actual

## Pregunta 5 (10 puntos)
Seleccione la opción que contiene un posible código en Python que puede realizar el chequeo de tipos de un analizador semántico. Considere que:
- Los hijos de un nodo se manejan con un arreglo, debido a que puede tener más de dos.
- Para la función `checkNode` no se escribe su código, pero ya se encuentra definida y su funcionamiento es el siguiente:
  - Establece el tipo del nodo `t` basado en el tipo de sus hijos.
  - Si hay un error manda a llamar a la función `typeError` para manejarlo.

Opciones:
- A) Recorre hijos primero, luego checkNode
- B) checkNode dentro del loop antes de cada hijo
- C) checkNode antes de recorrer hijos
- D) Recorre hijos primero, luego checkNode (idéntica a A)

## Pregunta 6 (10 puntos)
De acuerdo al algoritmo visto en clase, cuál es el NFA equivalente para la expresión regular `(a | bc)* | b` (escriba su justificación en las hojas de respuesta).

Opciones:
- A) Primera imagen (con "bc" como una sola transición)
- B) Segunda imagen (con estructura compleja oscurecida)
- C) Tercera imagen (con 'b' y 'c' como transiciones separadas)
- D) Cuarta imagen (similar a C con diferentes ε-transiciones)

## Pregunta 7 (10 puntos)
Seleccione la expresión aritmética de la cual se generó el siguiente código MIPS (32 bits). Aunque varias respuestas dan el mismo resultado numérico, seleccione la que hace las operaciones en el mismo orden que el código.

```mips
li $a0 5
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 4
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 3
lw $t1 4 ($sp)
sub $a0 $t1 $a0
addiu $sp $sp 4
lw $t1 4($sp)
add $a0 $t1 $a0
addiu $sp $sp 4
```

- [ ] (5 + 4) – 3
- [ ] 5 + (3 – 4)
- [ ] 5 + (4 – 3)
- [ ] (5 + 3) – 4

## Pregunta 8 (10 puntos)
Seleccione la instrucción cuyo cgen generó el siguiente código MIPS:

```mips
loop_branch:
cgen(E1)
sw $a0 0($sp)
addin $sp $sp -4
cgen(E2)
lw $t1 4($sp)
addin $sp $sp 4
beq $a0 $t1 end_brach
cgen(E3)
j loop_branch
end_branch:
```

- [ ] repeat E3 until E1 != E2
- [ ] repeat E3 until E1 == E2
- [ ] while E1 == E2 do E3
- [ ] while E1 != E2 do E3

## Pregunta 9 (10 puntos)
Seleccione la opción que contiene las instrucciones que hacen un push de lo que está en el acumulador, de acuerdo al modelo visto en clase.

- [ ] `sw $a0 4($sp)` / `addin $sp $sp -4`
- [ ] `sw $a0 0($sp)` / `addin $sp $sp -4`
- [ ] `lw $a0 4($sp)` / `addin $sp $sp 4`
- [ ] `lw $a0 0($sp)` / `addin $sp $sp 4`

## Pregunta 10 (10 puntos)
Seleccione la opción que contiene el DFA equivalente al siguiente NFA, de acuerdo al algoritmo visto en clase:

[NFA dado: Estado inicial 0, estados finales 1 y 3, con transiciones múltiples desde 0 con 'a']

Opciones:
- A) DFA con {0} → {1,2} → {3} → {2}, estados finales {1,2} y {2}
- B) DFA con {0} → {1,2} → {3}, estado final {3} solamente
- C) DFA con {0} → {1,2} → {3} → {2}, estados finales {1,2} y {2}
- D) DFA con {0} → {1,2} → {3}, estados finales {1,2} y {3} 