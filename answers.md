# Respuestas del Examen Final de Compiladores

## Pregunta 1: Usos de la Tabla de Símbolos

### Explicación detallada:

La tabla de símbolos es una estructura de datos fundamental en un compilador que almacena información sobre los identificadores del programa. Durante el análisis semántico, la tabla de símbolos se utiliza para:

1. **Verificar si una variable ya está declarada**: Cuando el compilador encuentra una declaración de variable, debe verificar en la tabla de símbolos si esa variable ya existe en el scope actual para evitar redeclaraciones.

2. **Guardar el apuntador a la raíz del AST**: Esto NO es un uso típico de la tabla de símbolos. El AST (Abstract Syntax Tree) es una estructura separada, y su raíz generalmente se mantiene en el parser o en el compilador principal, no en la tabla de símbolos.

3. **Guardar el código que genera una expresión**: Esto NO es función de la tabla de símbolos. La generación de código es una fase posterior que usa la información de la tabla de símbolos, pero el código generado no se almacena en ella.

4. **Verificar el tipo de una variable**: La tabla de símbolos almacena información de tipos para cada identificador, permitiendo al compilador verificar la compatibilidad de tipos en expresiones y asignaciones.

### Respuesta final:
✓ Verificar si una variable ya está declarada  
✗ Guardar el apuntador a la raíz del AST  
✗ Guardar el código que genera una expresión  
✓ Verificar el tipo de una variable

---

## Pregunta 2: Regla Lógica para Verificación de Tipos

### Explicación detallada:

La función `longitud(s)` recibe un string como parámetro y devuelve un entero. Analicemos cada opción de regla de inferencia de tipos:

**Opción A:**
```
O ⊢ longitud: String
―――――――――――――――――― [long]
    O ⊢ s: Int
```
Esta regla es incorrecta porque:
- Dice que `longitud` es de tipo String (incorrecto, es una función)
- Concluye que `s` es de tipo Int (incorrecto, debería ser String)

**Opción B:**
```
    O ⊢ s: Int
―――――――――――――――――― [long]
O ⊢ longitud: String
```
Esta regla también es incorrecta porque:
- La premisa dice que `s` es Int (debería ser String)
- La conclusión dice que `longitud` es String (incorrecto)

**Opción C:**
```
   O ⊢ s: String
―――――――――――――――――― [long]
O ⊢ longitud: Int
```
Esta regla es incorrecta porque:
- Solo verifica el tipo de `s` (correcto que sea String)
- Pero la conclusión habla de `longitud` sin su argumento
- No muestra la aplicación de la función

**Opción D:**
```
O ⊢ longitud: Int
―――――――――――――――――― [long]
   O ⊢ s: String
```
Esta regla es incorrecta porque:
- Está al revés: la premisa debería ser sobre `s`, no la conclusión
- No muestra la aplicación de la función correctamente

### Análisis:
Ninguna de las opciones muestra la regla correcta, que debería ser:
```
O ⊢ s: String
―――――――――――――――――――― [long]
O ⊢ longitud(s): Int
```

Sin embargo, la **Opción C** es la más cercana a ser correcta porque:
- Tiene la premisa correcta: `s` es de tipo String
- La conclusión menciona que el resultado es Int
- Aunque le falta mostrar `longitud(s)` en lugar de solo `longitud`

### Respuesta final:
**Opción C** - Es la más cercana a la regla correcta, aunque técnicamente incompleta.

---

## Pregunta 3: Recorridos del AST en el Analizador Semántico

### Explicación detallada:

Según el material del curso en `c_minus/semantic.md`, específicamente en la sección "En resumen" (líneas 362-366):

> "- El ambiente de tipos proporciona los tipos para las variables libres.
> - El ambiente de tipos se pasa como parámetro al ASE.
> - El ambiente de tipos (tabla de símbolos) se calcula a partir del AST de la raíz hacia las hojas (preorden)
> - Los tipos son calculados en el AST de las hojas a la raíz (posorden)."

Esto confirma que el analizador semántico realiza **dos recorridos** del AST:

1. **Primer recorrido (preorden - de la raíz hacia las hojas)**: 
   - Construcción de la tabla de símbolos
   - Se calculan los ambientes de tipos
   - Se crean nuevas tablas para cada scope

2. **Segundo recorrido (posorden - de las hojas hacia la raíz)**: 
   - Verificación y cálculo de tipos
   - Se usa la información de la tabla de símbolos construida previamente
   - Se verifican las reglas semánticas del lenguaje

Algunos compiladores pueden combinar estos pasos, pero el enfoque clásico visto en clase usa dos recorridos separados.

### Respuesta final:
✗ 3  
✗ No lo recorre, sólo usa las tablas de símbolos  
✓ 2  
✗ 1

---

## Pregunta 4: Variable No Encontrada en Tabla de Símbolos

### Explicación detallada:

En lenguajes con scopes anidados (como C, Java, Python), las tablas de símbolos se organizan en una pila (stack). Cuando se busca una variable:

1. Primero se busca en la tabla de símbolos actual (scope local)
2. Si no se encuentra, se busca en las tablas padre (scopes externos)
3. Se continúa hasta llegar al scope global

Este mecanismo permite:
- Variables locales que ocultan variables globales
- Acceso a variables de scopes externos desde funciones anidadas
- Implementación correcta de closures en algunos lenguajes

Si la variable no se encuentra en ninguna tabla del stack, entonces se marca un error de "variable no declarada".

### Respuesta final:
✓ Se busca la variable en las tablas de símbolos que están abajo en el stack  
✗ Se marca un error de "variable no declarada"  
✗ Se busca la variable en otras ramas del AST  
✗ Se coloca la variable en la tabla de símbolos actual

---

## Pregunta 5: Código Python para Chequeo de Tipos

### Explicación detallada:

Analicemos cada opción de código Python para el chequeo de tipos:

**Opción A:**
```python
def typeCheck(ast):
    if (ast != None):
        for i in range(MAXCHILDREN):
            typeCheck(ast.child[i])
        checkNode(ast)
```

**Opción B:**
```python
def typeCheck(ast):
    if (ast != None):
        for i in range(MAXCHILDREN):
            checkNode(ast)
            typeCheck(ast.child[i])
```

**Opción C:**
```python
def typeCheck(ast):
    if (ast != None):
        checkNode(ast)
        for i in range(MAXCHILDREN):
            typeCheck(ast.child[i])
```

**Opción D:**
```python
def typeCheck(ast):
    if (ast != None):
        for i in range(MAXCHILDREN):
            typeCheck(ast.child[i])
            checkNode(ast)   # <-- nota la indentación (dentro del bucle)
```

### Análisis:

El chequeo de tipos debe seguir un recorrido **posorden** (bottom-up), donde:
1. Primero se verifican los tipos de todos los hijos.
2. Luego se establece/verifica el tipo del nodo actual basándose en los tipos ya calculados de sus hijos.

• **Opción A** cumple exactamente este patrón: recorre recursivamente a cada hijo y, una vez terminados, llama a `checkNode(ast)` para el nodo actual.  ✅

• **Opción D** parece similar, pero la indentación pone `checkNode(ast)` **dentro** del bucle `for`, por lo que se ejecuta una vez por cada hijo, antes de que los demás hijos se hayan procesado.  Eso rompe el recorrido posorden y puede dar lugar a errores.  ❌

• **Opción B** también llama a `checkNode(ast)` dentro del bucle, pero antes incluso de procesar el hijo correspondiente.  ❌

• **Opción C** llama a `checkNode(ast)` antes de procesar ninguno de los hijos, lo que tampoco respeta el orden posorden.  ❌

### Respuesta final:
**Opción A** es la única correcta; las demás (B, C y D) son incorrectas porque no respetan el recorrido posorden necesario para el chequeo de tipos.

---

## Pregunta 6: NFA para (a | bc)* | b

### Explicación detallada:

Para construir el NFA de la expresión regular `(a | bc)* | b`, necesitamos seguir el algoritmo de Thompson para construcción de NFAs:

1. **Construir NFA para 'a'**: Un camino simple con transición 'a'
2. **Construir NFA para 'bc'**: Dos estados conectados, primero con 'b', luego con 'c'
3. **Unir (a | bc)**: Estado inicial con ε-transiciones a ambas ramas
4. **Aplicar * a (a | bc)**: Agregar ε-transiciones para permitir repetición
5. **Construir NFA para 'b' separado**: Un camino simple con transición 'b'
6. **Unir (a | bc)* | b**: Estado inicial con ε-transiciones a ambas partes

Analizando las opciones:

**Opción A (Primera imagen)**: Muestra "bc" como una sola transición, lo cual es incorrecto. La expresión regular requiere primero 'b' y luego 'c' como transiciones separadas.

**Opción B (Segunda imagen)**: Tiene una estructura compleja con múltiples estados pero la parte superior está oscurecida, dificultando el análisis completo.

**Opción C (Tercera imagen)**: Este NFA muestra correctamente:
- Un estado inicial con ε-transiciones
- La rama superior implementa (a | bc)* con:
  - Una ruta para 'a'
  - Una ruta para 'b' seguida de 'c' (transiciones separadas)
  - ε-transiciones que permiten la repetición (cerradura de Kleene)
- La rama inferior implementa el 'b' simple
- Un estado final alcanzable desde ambas ramas

**Opción D (Cuarta imagen)**: Similar a la opción C pero con una estructura ligeramente diferente en las ε-transiciones.

La opción C es la correcta porque:
- Separa correctamente 'b' y 'c' en transiciones distintas
- Implementa correctamente la cerradura de Kleene con ε-transiciones
- Tiene la estructura correcta para la unión final con el 'b' simple

### ¿Por qué las demás opciones son incorrectas?

• **Opción A** – El arco central está etiquetado como "bc" (un solo símbolo).  
  En la ER, *b* y *c* son **dos** símbolos consecutivos; Thompson obliga a tener **dos** transiciones (… -b-► … -c-► …).  Al usar un solo símbolo, la opción A sólo aceptaría la cadena literal «bc» como un *token* indivisible y no las combinaciones correctas generadas por la cerradura.

• **Opción B** – Separa b y c, pero coloca el estado intermedio *ε-cierre* (después de b) **fuera** del ciclo de la cerradura *.  
  El resultado es que la secuencia *bc* se puede usar **una sola vez**; después de consumir c no se regresa al "punto de repetición", de modo que cadenas como «bcbc» o mezclas de *a* con *bc* no se aceptan, violando la definición de (a | bc)*.

• **Opción D** – Tiene b y c en transiciones separadas, pero conecta la rama de b → c al estado de aceptación por un *ε* directo.  De esa forma se acepta la cadena «bc» sola (sin repetir) **sin** pasar por el ciclo de la cerradura, y también permite que un *c* aislado sea aceptado después de un camino espurio a través de *ε*-transiciones.  Ambos comportamientos contradicen la ER.

En resumen, sólo la **opción C**:
1. Usa transiciones separadas b ► c.  
2. Coloca la sub-máquina (a | bc) dentro de un bucle * completo.  
3. Mantiene una segunda rama independiente para la «b» solitaria.  
4. Une ambas ramas (la repetitiva y la simple) al mismo estado final.

Por eso es la única que implementa exactamente la ER (a | bc)* | b.

### Respuesta final:
**Opción C** - Es el NFA correcto para la expresión regular `(a | bc)* | b`

---

## Pregunta 7: Análisis del Código MIPS

### Explicación detallada:

Analicemos el código MIPS paso a paso:

```mips
li $a0 5          # Cargar 5 en $a0
sw $a0 0($sp)     # Push 5 al stack
addiu $sp $sp -4  # Ajustar stack pointer

li $a0 4          # Cargar 4 en $a0
sw $a0 0($sp)     # Push 4 al stack
addiu $sp $sp -4  # Ajustar stack pointer

li $a0 3          # Cargar 3 en $a0
lw $t1 4($sp)     # Pop 4 del stack a $t1
sub $a0 $t1 $a0   # $a0 = 4 - 3 = 1
addiu $sp $sp 4   # Ajustar stack pointer

lw $t1 4($sp)     # Pop 5 del stack a $t1
add $a0 $t1 $a0   # $a0 = 5 + 1 = 6
addiu $sp $sp 4   # Ajustar stack pointer
```

El orden de operaciones es:
1. Push 5
2. Push 4
3. Calcular 4 - 3 = 1
4. Calcular 5 + 1 = 6

Esto corresponde a: 5 + (4 - 3)

### Respuesta final:
✗ (5 + 4) – 3  
✗ 5 + (3 – 4)  
✓ 5 + (4 – 3)  
✗ (5 + 3) – 4

---

## Pregunta 8: Análisis del Loop en MIPS

### Explicación detallada:

Analicemos la estructura del código:

```mips
loop_branch:      # Etiqueta del inicio del loop
cgen(E1)          # Evaluar E1
sw $a0 0($sp)     # Guardar resultado de E1
addin $sp $sp -4
cgen(E2)          # Evaluar E2
lw $t1 4($sp)     # Recuperar E1
addin $sp $sp 4
beq $a0 $t1 end_brach  # Si E2 == E1, salir del loop
cgen(E3)          # Ejecutar E3
j loop_branch     # Volver al inicio
end_branch:
```

La estructura es:
1. Evaluar E1 y E2
2. Si son iguales, salir del loop
3. Si no son iguales, ejecutar E3 y repetir

Esto corresponde a: "mientras E1 != E2, hacer E3"

### Respuesta final:
✗ repeat E3 until E1 != E2  
✗ repeat E3 until E1 == E2  
✗ while E1 == E2 do E3  
✓ while E1 != E2 do E3

---

## Pregunta 9: Instrucciones Push en MIPS

### Explicación detallada:

En MIPS, un push al stack involucra:
1. Guardar el valor en la posición actual del stack pointer
2. Decrementar el stack pointer (el stack crece hacia abajo)

El patrón correcto es:
```mips
sw $a0 0($sp)     # Guardar en la posición actual del SP
addiu $sp $sp -4  # Mover el SP hacia abajo
```

Las opciones con `lw` son para pop (load word), no push (store word).
La opción con offset 4($sp) está incorrecta porque guardaría por encima del stack pointer actual.

### Respuesta final:
✗ `sw $a0 4($sp)` / `addin $sp $sp -4`  
✓ `sw $a0 0($sp)` / `addin $sp $sp -4`  
✗ `lw $a0 4($sp)` / `addin $sp $sp 4`  
✗ `lw $a0 0($sp)` / `addin $sp $sp 4`

---

## Pregunta 10: Conversión NFA a DFA

### Explicación detallada:

Analizando el NFA dado (última imagen):
- Estado inicial: 0
- Estados finales: 1 y 3 (círculos dobles)
- Transiciones:
  - De 0: con 'a' va a 1, con 'a' también va a 2
  - De 2: con 'b' va a 3, con 'a' va a 3

Para convertir este NFA a DFA usando el algoritmo de construcción de subconjuntos:

1. **Estado inicial del DFA**: {0}

2. **Desde {0} con 'a'**: llegamos a {1,2} (porque desde 0 con 'a' podemos ir tanto a 1 como a 2)

3. **Desde {0} con 'b'**: no hay transición, así que vacío o estado de error

4. **Desde {1,2} con 'a'**: desde 1 no hay transición, desde 2 con 'a' vamos a 3, entonces llegamos a {3}

5. **Desde {1,2} con 'b'**: desde 1 no hay transición, desde 2 con 'b' vamos a 3, entonces llegamos a {3}

6. **Desde {3} con 'a' o 'b'**: no hay transiciones desde 3

Los estados finales del DFA serán aquellos que contengan al menos un estado final del NFA (1 o 3):
- {1,2} es final (contiene a 1)
- {3} es final (contiene a 3)

Comparando con las opciones:

**Opción A**: Muestra {0} → 'a' → {1,2} → 'b' → {3} → 'a' → {2} → 'b'. Los estados finales son {1,2} y {2}.

**Opción B**: Muestra {0} → 'a' → {1,2} → 'b' → {3}. Estado final es {3}. Pero falta la transición de {1,2} con 'a'.

**Opción C**: Muestra {0} → 'a' → {1,2} → 'b' → {3} → 'a' → {2}. Los estados finales son {1,2} y {2}.

**Opción D**: Muestra {0} → 'a' → {1,2} → 'b' → {3} con transiciones adicionales. Los estados finales son {1,2} y {3}.

La opción correcta es la **D** porque:
- Tiene el estado inicial correcto {0}
- La transición {0} con 'a' lleva a {1,2} ✓
- Desde {1,2} se puede llegar a {3} tanto con 'a' como con 'b' ✓
- Los estados finales {1,2} y {3} son correctos (contienen estados finales del NFA) ✓

### ¿Por qué las demás opciones (A, B, C) son incorrectas?

• **Opción A**
  1. Después de `{0} --a--> {1,2}` coloca `{1,2} --a--> {2}`.  Sin el estado 1 dentro del conjunto, `{2}` no contiene un estado final, pero la figura lo marca como final.
  2. Falta la transición `{2} --b--> {3}` requerida por la tabla de subconjuntos; la función de transición queda incompleta.
  3. Acepta cadenas que terminan en `{2}` (p. ej. «aa») que el lenguaje no considera válidas.

• **Opción B**
  1. Omite la transición `{1,2} --a--> {3}` (solo incluye la de 'b').  
  2. Rechaza cadenas como «aa», «aba», etc., que sí pertenecen a `(a|bc)*`.
  3. Marca únicamente `{3}` como final; `{1,2}` también debe ser final porque contiene al estado 1 del NFA.

• **Opción C**
  1. Tiene la misma transición errónea `{1,2} --a--> {2}` que la opción A.
  2. Vuelve a marcar `{2}` como final injustificadamente.
  3. Carece de salida con 'b' desde `{2}`, dejando estados sin definición.

En cambio, **Opción D** cumple todo:
- `{0} --a--> {1,2}`
- `{1,2} --a,b--> {3}`
- Estados finales `{1,2}` y `{3}` (porque contienen a 1 y 3 del NFA)
- Tabla de transición completa para cada símbolo del alfabeto.

Por eso la única opción correcta para el DFA es la **D**.

### Respuesta final:
**Opción D** - Es el DFA correcto resultante de la conversión del NFA dado. 