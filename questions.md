
Saltar al contenido
Luis Carlos Rico Almada
Cuenta
Tablero
Cursos
Grupos
Calendario
Bandeja de entrada
Historial
Ayuda
bot_imageTECbot
TC3002B.502EvaluacionesExamen Final B
Semestral Ene - Jun de 2025
Página de Inicio
Anuncios
Módulos
Personas
Programa del curso
Plan de evaluación
Pase de lista
Examen Final B
Comenzado: 27 de mayo en 17:07
Instrucciones del examen
INSTRUCCIONES:

El examen tiene una duración de 2 hr, iniciando a las 5:05 PM y terminando a las 7:05 PM.
Para cada pregunta, haga su desarrollo en hojas de papel o papel electrónico.
Una vez terminado el examen, suba sus respuestas en un archivo PDF a la liga RESPUESTAS EXAMEN FINAL, que se encuentra en el módulo EXÁMENES, la cual se cierra a las 7:20 PM.
No se puede hacer revisión de ninguna pregunta que no tenga desarrollo en el archivo PDF.
Por ningún motivo se aceptan archivos de respuestas enviados por otro medio que no sea la liga correspondiente.
Si alguna respuesta no coincide con el desarrollo realizado en las hojas de respuestas, la pregunta será tomada como errónea aún y cuando se haya seleccionado la respuesta correcta.
Seleccione la(s) respuesta(s) correcta(a) de acuerdo a lo que se pide en cada pregunta.

Nota: Este examen tiene plazo. Podrá comprobar el tiempo que le queda en cualquier momento del examen presionando la combinación de teclas SHIFT, ALT y T... De nuevo: SHIFT, ALT y T...
 
Pregunta de la marca: Pregunta 1
Pregunta 110 pts
Seleccione las opciones que contienen algún uso de la tabla de símbolos en un compilador, de los vistos en la clase. Marque todas las que apliquen.

Grupo de opciones de respuesta

Verificar si una variable ya está declarada

Guardar el apuntador a la raíz del AST

Guardar el código que genera una expresión

Verificar el tipo de una variable
 
Pregunta de la marca: Pregunta 2
Pregunta 210 pts
Si en un lenguaje de programación existe una función llamada longitud(s), que está predefinida y que calcula el número de caracteres en un string s que recibe como parámetro (e.g. longitud(“hola”) regresa un 4), escriba una regla lógica para verificar el tipo de esta función. No pierda de vista que el parámetro puede ser una variable o una expresión que contenga variables.
Grupo de opciones de respuesta

EFP1 202011-3.png

EFP1 202011-1.png

EFP1 202011-4.png

EFP1 202011-2.png
 
Pregunta de la marca: Pregunta 3
Pregunta 310 pts
Seleccione la opción que contiene el número de recorridos del AST que tiene que realizar el analizador semántico visto en clase:
Grupo de opciones de respuesta

3

No lo recorre, sólo usa las tablas de símbolos

2

1
 
Pregunta de la marca: Pregunta 4
Pregunta 410 pts
Suponga que se está compilando un programa en un lenguaje con declaración de variables y tipado estático. Seleccione la opción que tiene la acción que se debe realizar cuando una variable no se encuentra en la tabla de símbolos actual.
Grupo de opciones de respuesta

Se busca la variable en las tablas de símbolos que están abajo en el stack.

Se marca un error de "variable no declarada"

Se busca la variable en otras ramas del AST

Se coloca la variable en la tabla de símbolos actual
 
Pregunta de la marca: Pregunta 5
Pregunta 510 pts
Seleccione la opción que contiene un posible código en Python que puede realizar el chequeo de tipos de un analizador semántico. Considere que:

Los hijos de un nodo se manejan con un arreglo, debido a que puede tener más de dos.
Para la función checkNode no se escribe su código, pero ya se encuentra definida y su funcionamiento es el siguiente:
Establece el tipo del nodo t basado en el tipo de sus hijos.
Si hay un error manda a llamar a la función typeError para manejarlo.
Grupo de opciones de respuesta

P7.1 202211.png

P7.3 202211.png

P7.2 202211.png

P7.4 202211.png
 
Pregunta de la marca: Pregunta 6
Pregunta 610 pts
De acuerdo al algoritmo visto en clase, cuál es el NFA equivalente para la expresión regular (a | bc)* | b  (escriba su justificación en las hojas de respuesta).
Grupo de opciones de respuesta

EFP1 202211.png

P1P3202011-3.png

P1P3202011-4.png

P1P3202011-2.png
 
Pregunta de la marca: Pregunta 7
Pregunta 710 pts
Seleccione la expresión aritmética de la cual se generó el siguiente código MIPS (32 bits). Aunque varias respuestas dan el mismo resultado numérico, seleccione la que hace las operaciones en el mismo orden que el código.

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

Grupo de opciones de respuesta

(5 + 4) – 3

5 + (3 – 4)

5 + (4 – 3)

(5 + 3) – 4
 
Pregunta de la marca: Pregunta 8
Pregunta 810 pts
Seleccione la instrucción cuyo cgen generó el siguiente código MIPS:

 

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

Grupo de opciones de respuesta

repeat E3 until E1 != E2

repeat E3 until E1 == E2

while E1 == E2 do E3

while E1 != E2 do E3
 
Pregunta de la marca: Pregunta 9
Pregunta 910 pts
Seleccione la opción que contiene las instrucciones que hacen un push de lo que está en el acumulador, de acuerdo al modelo visto en clase.
Grupo de opciones de respuesta

sw $a0 4($sp)

addin $sp $sp -4


sw $a0 0($sp)

addin $sp $sp -4


lw $a0 4($sp)

addin $sp $sp 4


lw $a0 0($sp)

addin $sp $sp 4

 
Pregunta de la marca: Pregunta 10
Pregunta 1010 pts
Seleccione la opción que contiene el DFA equivalente al siguiente NFA, de acuerdo al algoritmo visto en clase:

image.png

Grupo de opciones de respuesta

image.png

image.png

image.png

image.png
Examen guardado en 17:16 
Preguntas
ContestadoPregunta 1
ContestadoPregunta 2
ContestadoPregunta 3
No han respondido todavíaPregunta 4
No han respondido todavíaPregunta 5
No han respondido todavíaPregunta 6
No han respondido todavíaPregunta 7
No han respondido todavíaPregunta 8
No han respondido todavíaPregunta 9
No han respondido todavíaPregunta 10
Tiempo de ejecución:
Intento vencido: 27 de mayo en 19:05
1 hora, 48 minutos, 57 segundos
