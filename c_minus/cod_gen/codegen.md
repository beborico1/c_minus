# Generación de Código

## Diseño de Compiladores
**Dr. Víctor de la Cueva**  
vcueva@tec.mx  
14/05/25

## 1. Introducción a la Generación de Código

Hasta este punto ya estamos completamente seguros que nuestro programa está correctamente escrito. Estamos listos entonces para poder generar código.

### Opciones de Generación:
- **Código binario**: Un compilador debería generar código binario, listo para correr en la máquina (e.g. .exe o .o). Depende completamente de la máquina donde se esté corriendo.
- **Código ensamblador**: También podría generar código en ensamblador listo para poder correrse con un linker para un procesador específico. Cada procesador tiene su propio lenguaje ensamblador.
- **Código intermedio**: Una alternativa intermedia podría ser la generación de código especial (intermedio) para una máquina virtual (e.g. código de tres direcciones o código P, como Java que genera bytecode).

## 2. Nuestra Alternativa

En nuestro proyecto vamos a optar por la opción de ensamblador para un procesador específico.

Lo más común es usar un procesador MIPS, que utiliza una arquitectura RISC y que es muy común en los procesadores actuales.

### Simuladores:
- **QtSpim**: Versión más reciente en https://spimsimulator.sourceforge.net/
- **MARS**: Versión más reciente MARS 4.5 en https://dpetersanderson.github.io/

> **Nota**: Si alguien desea generar código para otro procesador, lo puede hacer sin ningún problema (indicarlo en la documentación).

### Compatibilidad:
- **QtSPIM**: Funciona para todos los sistemas excepto para Mac M1. Instala una serie de ejemplos muy simples.
- **MARS**: Funciona para todos los sistemas, pero deben instalar el JRE. Luego deben dar permiso a la aplicación para abrirla en su Mac.

> **NOTA**: MARS es un poco más general ya que puede funcionar sin main, mientras que QtSpim debe tener una etiqueta main que indica el punto de inicio del programa. Se recomienda consultar sus manuales.

## 3. Preguntas sobre un programa en MIPS

- ¿Cuál es la estructura de un programa en ensamblador?
- ¿Cuáles son las instrucciones del ensamblador?
- ¿Cómo correrlo?
- ¿Cómo ver el resultado?

## 4. Introducción a MIPS

**Referencias**:
- Original: https://www2.engr.arizona.edu/~ece369/Resources/spim/QtSPIM_examples.pdf
- Ahora en SCRIBD: https://www.scribd.com/document/517815566/QtSPIM-Examples

### Formato de un programa en MIPS

Un programa de MIPS usa las siguientes directivas de alto nivel:
- `.text` - indica que lo que sigue debe ser guardado en el segmento de texto del usuario (típicamente son instrucciones)
- `.data` - indica que los datos que le siguen deben almacenarse en el segmento de datos
- `.globl sym` - declara que el símbolo sym es global y puede ser referido por otros archivos

**Características**:
- El orden de las directivas no importa y algunas pueden no estar, si es que no se usan (e.g. .data).
- El cuerpo, indicado por .text, contiene todas las instrucciones.
- Termina con una instrucción de exit o nada (aunque marca un error si no se pone nada).
- La instrucción exit se hace con una llamada al sistema mediante dos instrucciones:
  ```mips
  li $v0, 10
  syscall
  ```
- Los comentarios inician con #.
- El programa se escribe en un archivo de texto plano.

## 5. Escribir y correr un programa en MIPS

### QtSPIM:
1. Cargar el archivo en el simulador con File>Reinitialize and Load File.
2. Seleccione el archivo que contiene su programa.
3. Para correr el programa, considere que son un poco diferentes los simuladores de Windows y Mac.

### MARS:
1. Cargar el archivo con File>Open.
2. Seleccione el archivo que contiene su programa.
3. Ensámblelo con Run>Assemble.
4. Córralo con Run>Go (lo corre todo) o Run>Step (lo corre paso a paso).

## 6. Arquitectura MIPS R2000 CPU y FPU

- MIPS R2000 cuenta con 1 CPU y 2 Coprocesadores.
- Los coprocesadores se encargan del manejo de datos en precisión single (float) y double (double).
- Los coprocesadores manejan los registros cuyo nombre inicia con f.
- En MARS los pueden ver en su IDE en una pestaña a la derecha y en QtSpim en una pestaña a la izquierda.

### Registros
- En un buen resumen (PDF): http://logos.cs.uic.edu/366/notes/mips%20quick%20tutorial.htm
- Ahora en: https://minnie.tuhs.org/CompArch/Resources/mips_quick_tutorial.html

## 7. I/O en MIPS

Las impresiones a pantalla y las lecturas del teclado se manejan por medio de llamadas al sistema mediante la instrucción `syscall`.

### Para imprimir:
1. Colocar el dato a imprimir en el registro adecuado ($a0, $a1 o $f12).
2. Colocar el dato que indica la operación en el registro $v0.
3. Llamar al sistema con la instrucción syscall.

### Para leer:
1. Colocar el dato que indica la operación en el registro $v0.
2. Llamar al sistema con la instrucción syscall.
3. El dato leído quedará en el registro $v0.

## 8. Ejemplos de Programas

### Ejemplo: Hola Mundo
```mips
.globl main
.data
mensaje: .asciiz "Hola Mundo!"
.text
main:
    li $v0, 4
    la $a0, mensaje
    syscall
```

### Ejemplo: Suma simple
```mips
# programa que suma 2 + 3
.text
.globl main
main:
    li $8, 2
    li $9, 3
    add $10, $8, $9
    # Si se quiere imprimir
    add $a0, $8, $9  # o move $a0, $10
    li $v0, 1
    syscall
```

### Ejemplo: Imprimir un float
```mips
.data
PI: .float 3.14
.text
main:
    li $v0, 2
    lwc1 $f12, PI
    syscall
```

## 9. Organización de la Memoria

### En Runtime
Antes de ver la generación de código debemos iniciar con la organización de nuestro programa en runtime:
- Debemos entender qué estamos tratando de generar antes de ver cómo generarlo.
- Hay varias técnicas para generar código ejecutable.
- La parte fundamental para lograrlo es la administración de los recursos de memoria en runtime.

### Al inicio de un programa
Cuando se corre un programa en ensamblador, el OS decide en qué posición de la memoria se debe cargar el código.
- Por esta razón, todas las referencias a memoria se deben hacer con offsets a partir de un valor dado.
- El OS coloca cierta información a ciertos registros al momento de la carga:
  - En el $sp pone la dirección de la siguiente palabra libre del stack alineado por palabra (4 bytes) little-endian.
  - En el $gp pone la dirección donde guarda las variables globales.
  - El $pc lo pone en 0.

## 10. Layout de los datos

El compilador es el responsable de decidir cómo será el layout de los datos y entonces generar código que manipule correctamente estos datos.

### Objetivos de la generación de código:
1. **Correctez**: El código debe implementar correctamente el programa del usuario.
2. **Velocidad**: El código debe ser eficiente y correr rápido.

Es fácil implementar estas dos cosas por separado. La complicación en la generación de código viene al tratar de ser rápido y correcto al mismo tiempo.

## 11. Activaciones y Lifetime

### Activaciones:
- Una invocación de un procedimiento P es una activación de P.
- El tiempo de vida (lifetime) de una activación de P es:
  - Todos los pasos para ejecutar P
  - Incluyendo todos los pasos de las llamadas a procedimientos que haga P

### Lifetime de las activaciones:
- Cuando un procedimiento P llama a un procedimiento Q, entonces, Q regresa antes de que P regrese.
- Los lifetimes de las activaciones están correctamente anidadas.
- Esto implica que los lifetimes de las activaciones pueden ser ilustradas con un árbol.
- Debido a que las activaciones están anidadas, un stack puede mantener los procedimientos activos.

## 12. Activation Records (AR)

La información necesaria para manejar una activación de procedimiento es llamada Activation Record (AR) o Frame.

### Diseño del AR:
Un diseño del AR para una función podría ser:
- **Resultado**: Contiene el valor que regresa la función después de que termina.
- **Argumentos**: Es una porción para mantener los valores de los argumentos con los que se llamó a la función.
- **Control link**: Un apuntador al AR del invocador.
- **Dirección de regreso**: La dirección de memoria a la que tenemos que saltar al terminar la ejecución de la función.

## 13. Variables Globales y Tipos de Datos

### Variables Globales:
- Todas las referencias a una variable global apuntan al mismo objeto.
- Por esta razón no se puede almacenar una variable global en un AR.
- A las globales se les asigna una dirección fija, una sola vez.

### El Heap:
- Un valor que permanece vivo fuera del procedimiento que lo crea no puede mantenerse en el AR.
- Los lenguajes con datos dinámicamente asignados usan un heap para almacenar los datos dinámicos.

### Stack y Heap:
- Muchas implementaciones de lenguajes usan tanto un heap como un stack donde ambos pueden crecer.
- Solución: Iniciar el Heap y el Stack en posiciones opuestas de la memoria y dejarlos que crezcan uno hacia el otro.

## 14. Alineamiento

La mayoría de las máquinas modernas son de 32 a 64 bits (en una palabra):
- 8 bits en un byte
- 4 a 8 bytes por palabra
- Las máquinas son direccionables por byte o por palabra

Si el alineamiento es por palabra, cuando decimos que un registro contiene una dirección de una palabra, en realidad contiene la dirección del byte menos significativo (little-endian) de la palabra.

## 15. Modelos para la Generación de Código

### Stack Machines
Es el modelo más simple para generar código.
- En estas máquinas, el almacenamiento principal es una clase de stack.
- Sólo se almacena en el stack.
- Una instrucción r = F(a₁, ..., aₙ):
  - Pops n operandos del stack
  - Realiza la operación F usando los operandos
  - Pushes el resultado r al stack

### Ejemplo: 7 + 5
```
Push 7
Push 5
Add
```

### Máquina de Stack de 1-registro (Acumulador)
Una alternativa intermedia entre una máquina de stack y una máquina de registros.
- El registro es llamado Acumulador.
- Una instrucción add se hace: acc ← acc + top
- Solo un acceso a memoria.

## 16. Implementación de la Generación de Código

### Enfoque:
- Nos enfocaremos en generar código para una máquina de stack con acumulador.
- El Stack se mantiene en el AR.
- El resultado lo vamos a correr en una máquina real (procesador MIPS o simulador SPIM).
- MIPS es una arquitectura de 32 bits (4 bytes por palabra).

### Decisiones de diseño:
- El acumulador será mantenido en el registro de MIPS llamado $a0.
- El stack se mantiene en memoria.
- El stack crece hacia lower addresses.
- La dirección de la siguiente localización vacía en el stack se mantiene en el registro $sp.

## 17. Generación de Código Práctica

### Algoritmo básico:
```
procedure genCode(T: treenode);
if T no es nil then
    // genere código para preparar el caso del código del hijo izquierdo de T;
    genCode(hijo izquierdo de T);
    // genere código para preparar el caso del código del hijo derecho de T;
    genCode(hijo derecho de T);
    // genere código para implementar la acción de T;
    ...
end
```

### Instrucciones MIPS básicas:
1. **Load Word**: `lw reg1 offset(reg2)` - Carga una palabra de 32 bits de la dirección de memoria reg2+offset en el reg1
2. **Add**: `add reg1 reg2 reg3` - reg1 ← reg2 + reg3
3. **Store Word**: `sw reg1 offset(reg2)` - Almacena una palabra de 32 bits que está en reg1, en la dirección reg2+offset
4. **Add immediate unsigned**: `addiu reg1 reg2 imm` - reg1 ← reg2 + imm
5. **Load immediate**: `li reg imm` - reg ← imm

### Ejemplo: 7 + 5 en MIPS
```mips
li $a0 7
sw $a0 0($sp)
addiu $sp $sp -4
li $a0 5
lw $t1 4($sp)
add $a0 $a0 $t1
addiu $sp $sp 4
```

## 18. Gramática de ejemplo para CG

```
P → D ; P | D
D → def id ( ARGS ) = E ;
ARGS → id , ARGS | id
E → int | id | if E1 = E2 then E3 else E4
    | E1 + E2 | E1 – E2 | id ( E1, ... , En )
```

### Generación de código (CG):
Para cada expresión e vamos a generar código MIPS que:
- Calcule el valor de e y lo deje en $a0
- Preserve el $sp y el contenido del stack (anterior a la expresión)

### Código para evaluar una constante:
```
cgen(i) = li $a0 i
```

### Código para la suma de dos expresiones:
```
cgen(e1 + e2) =
    cgen(e1)
    sw $a0 0($sp)
    addiu $sp $sp -4
    cgen(e2)
    lw $t1 4($sp)
    add $a0 $t1 $a0
    addiu $sp $sp 4
```

### Código para la resta:
```
cgen(e1 – e2) =
    cgen(e1)
    sw $a0 0($sp)
    addiu $sp $sp -4
    cgen(e2)
    lw $t1 4($sp)
    sub $a0 $t1 $a0
    addiu $sp $sp 4
```

### Código para if-then-else:
```
cgen(if e1 = e2 then e3 else e4) =
    cgen(e1)
    sw $a0 0($sp)
    addiu $sp $sp -4
    cgen(e2)
    lw $t1 4($sp)
    addiu $sp $sp 4
    beq $a0 $t1 true_branch
false_branch:
    cgen(e4)
    b end_if
true_branch:
    cgen(e3)
end_if:
```

## 19. Llamada y Definición de Funciones

### Secuencia de activación de una función:
1. Calcula los argumentos y los almacena en sus posiciones correctas en el nuevo AR.
2. Almacena (inserta) en el stack el fp como el vínculo de control del nuevo AR.
3. Cambia el fp de manera que apunte al inicio del nuevo AR.
4. Almacena la dirección de retorno en el nuevo AR.
5. Realiza un salto hacia el código del procedimiento a ser llamado.

### Cuando un procedimiento sale:
1. Carga la dirección de retorno que está en el fp actual o en sp+4.
2. Cambia el sp para borrar (lógicamente) el AR.
3. Carga el vínculo de control (control link u old frame) al fp.
4. Realiza un salto hacia la dirección de retorno.

### El AR a ser usado:
Para este lenguaje es suficiente un AR con:
- Un apuntador al frame del caller (control link)
- Los parámetros actuales
- Y la dirección de regreso

### Lado del caller:
```
cgen(f(e1, ..., en)) =
    sw $fp 0($sp)
    addiu $sp $sp -4
    cgen(en)
    sw $a0 0($sp)
    addiu $sp $sp -4
    ...
    cgen(e1)
    sw $a0 0($sp)
    addiu $sp $sp -4
    jal f_entry
```

### Lado del callee:
```
cgen(def f(x1, ..., xn)=e) =
f_entry:
    move $fp $sp
    sw $ra 0($sp)
    addiu $sp $sp -4
    cgen(e)
    lw $ra 4($sp)
    addiu $sp $sp z
    lw $fp 0($sp)
    jr $ra
```
Donde z = 4*n + 8

### Código para referencia a variables:
```
cgen(xi) = lw $a0 z($fp)
```
Donde z = 4*i

## 20. Variables y la Tabla de Símbolos

Es muy importante recordar que la tabla de símbolos tiene información que puede ser útil para generar código.

Podemos modificarla las veces que haga falta con tal de que guarde información que nos sea útil:
- Una posibilidad es guardar las direcciones (en realidad los offsets) donde se encuentran las variables en la memoria.
- Si se usan las ST para esta tarea se debe tener cuidado de cargar el scope adecuado a la variable en cuestión.

## 21. Write y Read en MIPS

Las instrucciones para impresión y lectura se manejan en MIPS como una llamada al sistema por medio de la instrucción `syscall`.

Para distinguir qué es lo que se quiere hacer, se debe colocar cierta información en ciertos registros antes de hacer la llamada al sistema.

## 22. El Stack y el Heap

- Al iniciar nuestro programa el $sp contiene un apuntador a la siguiente posición libre de la región destinada al stack.
- El heap es una región que también crece y decrece pero que se encuentra en el lado opuesto de la memoria de datos del programa.
- Para solicitar espacio dinámico se hace una llamada al sistema (syscall).

## 23. Sumario

- El AR debe ser diseñado junto con el generador de código.
- La generación de código puede ser hecha por medio de un recorrido recursivo del AST (como el type-checking).
- Se recomienda usar una stack-machine para su proyecto ya que es muy simple.

## 24. Ejemplo de CG

### Generar código para:
```
def sumto(x) = if x=0 then 0 else x+sumto(x-1)
```

### Solución:
```mips
sumto_entry:
    move $fp $sp
    sw $ra 0($sp)
    addiu $sp $sp -4
    lw $a0 4($fp)
    sw $a0 0($sp)
    addiu $sp $sp -4
    li $a0 0
    lw $t1 4($sp)
    addiu $sp $sp 4
    beq $a0 $t1 true1
false1:
    lw $a0 4($fp)
    sw $a0 0($sp)
    addiu $sp $sp -4
    sw $fp 0($sp)
    addiu $sp $sp -4
    lw $a0 4($fp)
    sw $a0 0($sp)
    addiu $sp $sp -4
    li $a0 1
    lw $t1 4($sp)
    sub $a0 $t1 $a0
    addiu $sp $sp 4
    sw $a0 0($sp)
    addiu $sp $sp -4
    jal sumto_entry
    lw $t1 4($sp)
    add $a0 $t1 $a0
    addiu $sp $sp 4
    b endif1
true1:
    li $a0 0
endif1:
    lw $ra 4($sp)
    addiu $sp $sp 12
    lw $fp 0($sp)
    jr $ra
```

## Referencias

- Alex Aiken. Compilers. Stanford Online (2018). https://lagunita.stanford.edu/courses/Engineering/Compilers/Fall2014/about
- K.C. Louden. Construcción de Compiladores: principios y práctica. Thomson (2004).
- Programmed Introduction to MIPS Assembly Language. Central Connecticut State University. QtSpim Edition, August 2015. https://chortle.ccsu.edu/assemblytutorial/
- MIPS Assembly. https://en.wikibooks.org/wiki/MIPS_Assembly
- MIPS Quick Tutorial. https://minnie.tuhs.org/CompArch/Resources/mips_quick_tutorial.html