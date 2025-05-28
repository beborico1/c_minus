# Autómatas Finitos No Determinísticos

## Diseño de Compiladores
**Dr. Víctor de la Cueva**  
vcueva@tec.mx  
20/05/25

## 1. Autómata Finito No Determinístico (NFA)

En realidad, cualquier conjunto que sea aceptado por un NFA podrá ser aceptado por un FA (o DFA).

Sin embargo, el NFA es un concepto útil en la prueba de teoremas y el concepto de no-determinístico juega un papel fundamental tanto en la teoría de lenguajes como en la teoría de la computación.

Para crear el nuevo modelo NFA considere modificar el modelo de FA para permitir **0, 1 o más transiciones** de un estado con el mismo símbolo de entrada.

También se pueden formar diagramas de transición para un NFA.

## 2. Control de movimientos

Una de las distinciones cruciales entre las clases de autómatas finitos es si el control es:

- **Determinístico**: significa que el autómata no puede estar en más de un estado en cualquier tiempo.
- **No-determinístico**: significa que puede estar en muchos estados a la vez.

### Ventajas del no-determinismo:
- Descubriremos que agregando no-determinismo no nos ayuda a definir ningún lenguaje que no pueda ser definido usando autómatas determinísticos, pero son más eficientes las describir la aplicación.
- El no-determinismo nos ayuda a "programar" la solución en lenguaje de "alto-nivel".
- Posteriormente, el Autómata No Determinístico es "compilado" para transformarlo en uno Determinístico, el cual es ejecutado.

## 3. Secuencia aceptada por un NFA

Una secuencia de entrada a₁a₂...aₙ es aceptada por un NFA si existe una secuencia de transiciones, correspondientes a la secuencia de entrada, que lleva al NFA de un estado inicial a un estado final.

### Diferencias entre DFA y NFA:
- En un **DFA**, para un string w y un estado q dados, existe una única transición para cada símbolo.
  - Para determinar si un string es aceptado por un DFA basta verificar si existe este único camino.
- Para un **NFA** hay muchos caminos etiquetados con w.
  - Para determinar si un string w es aceptado, TODOS deben ser checados para verificar si al menos 1 termina en un estado final.

## 4. Ejemplo

```
    a,b
q0 -----> q0
 |         |
 | b       | b
 v         v
q1 -----> q2
    b
```

Representa el conjunto de strings en el alfabeto {a,b} que terminan en bb.

Su tabla de transición es a conjuntos de estados:

| Estado | a | b |
|--------|---|---|
| 0 | {0} | {0,1} |
| 1 | {} | {2} |
| 2 | {} | {} |

## 5. Ejemplo de aceptación de un string

Veamos si el string w = abb es aceptado por el autómata anterior:

```
         a           b           b
    q0 -----> q0 -----> {q0,q1} -----> {q0,q1,q2}
                            |
                            | b
                            v
                           {q2}
```

## 6. Definición formal

Denotamos un NFA por medio de una 5-tupla (Q, Σ, δ, q₀, F), donde todos los elementos tienen el mismo significado que un FA excepto δ que ahora mapea:

**Q × Σ → 2^Q**

donde 2^Q es el conjunto potencia de Q (el conjunto de todos los posibles subconjuntos de Q).

La intención es que δ(q,a) es el conjunto de todos los estados p tales que hay una transición de q a p etiquetada con a.

### Función extendida δ̂

La función δ puede ser extendida a δ̂ que mapea de Q × Σ* → 2^Q y se refiere a secuencias de entradas:
1. δ̂(q, ε) = {q}
2. δ̂(q, wa) = {p | para algún estado r en δ̂(q, w), p está en δ(r, a)}

## 7. Extensión

Note que δ̂(q, a) = δ(q, a) para un símbolo de entrada a.

De esta forma, nuevamente usaremos el símbolo δ en lugar de δ̂.

También es útil extender δ a argumentos en 2^Q × Σ*:
3. δ(P, w) = ⋃_{q∈P} δ(q, w)

para cada conjunto de estados P ⊆ Q

**L(M)**, donde M es el NFA (Q, Σ, δ, q₀, F), es:
{w | δ(q₀, w) contiene un estado en F}

## 8. Equivalencia de DFAs y NFAs

**Teorema**: Sea L un conjunto aceptado por un NFA. Entonces, existe un DFA que acepta a L.

**Demostración (construcción)**: La prueba dependerá de mostrar que los DFAs pueden simular NFAs; esto es, para cada NFA podemos construir un DFA equivalente (uno que acepte el mismo lenguaje).

- La forma en la que un DFA simula un NFA es permitiendo que los estados de un DFA correspondan a conjuntos de estados del NFA.
- El DFA que se construye así, realiza un seguimiento en su control finito de todos los estados en los que el NFA podría estar después de leer la misma entrada que el DFA ha leído.

## 9. Creación de un DFA a partir de un NFA

La demostración anterior proporciona un método para crear un DFA que acepte el mismo lenguaje que un NFA (un DFA equivalente).

- El estado inicial es el subconjunto [q₀], donde q₀ es el estado inicial del NFA.
- En la práctica, es común que muchos de los estados de un DFA equivalente no puedan ser alcanzados a partir de [q₀], por lo que no deben estar en la tabla final.
- Se recomienda iniciar con [q₀] e ir agregando estados a la tabla, dependiendo de cuáles sí se pueden alcanzar.

## 10. NFA con movimientos-ε

Se puede extender el modelo de NFA para que incluya transiciones con la entrada nula ε.

**Ejemplo**: Un NFA que acepta el lenguaje consistente en cualquier número de 0's (incluyendo 0), seguido de cualquier número de 1's y seguido de cualquier número de 2's.

Desde luego, se pueden incluir aristas etiquetadas con ε en el camino de aceptación aún y cuando las ε's no aparezcan explícitamente en el string w.

### Definición formal

Un NFA con ε-moves es una quíntupla (5-tupla) (Q, Σ, δ, q₀, F) con todos los componentes definidos igual que para un NFA, pero con δ, la función de transición, que mapea:

**Q × (Σ ∪ {ε}) → 2^Q**

La intención es que δ(q,a) consista de todos los estados p tales que hay una transición de p a q, etiquetada con a, donde a es un símbolo de Σ o ε.

## 11. ε-CLOSURE

Para extender δ a δ̂ es necesario calcular el conjunto de estados alcanzables a partir de un estado q usando una transición ε.

Se utiliza **ε-CLOSURE(q)** para denotar el conjunto de todos los vértices p tales que hay un camino de q a p etiquetado con ε.

También se puede calcular ε-CLOSURE(P), donde P es un conjunto de estados, como:

ε-CLOSURE(P) = ⋃_{q∈P} ε-CLOSURE(q)

### Definición formal de ε-CLOSURE

Se hace en forma recursiva. La ε-CLOSURE de un estado qᵢ, denotada por ε-CLOSURE(qᵢ), es definida recurrentemente por:
- **Base**: qᵢ ∈ ε-CLOSURE(qᵢ)
- **Recursivo**: Sea qⱼ un elemento de ε-CLOSURE(qᵢ). Si qₖ ∈ δ(qⱼ, ε), entonces qₖ ∈ ε-CLOSURE(qᵢ).
- **Cerradura**: ...

## 12. Definición de δ̂

Se puede entonces definir δ̂ como sigue:
1. δ̂(q, ε) = ε-CLOSURE(q)
2. Para w ∈ Σ* y a ∈ Σ, δ̂(q, wa) = ε-CLOSURE(P), donde P = {p | para alguna r ∈ δ̂(q,w), p ∈ δ(r,a)}

Es conveniente extender δ y δ̂ a conjuntos de estados R como:
3. δ(R, a) = ⋃_{q∈R} δ(q, a)
4. δ̂(R, w) = ⋃_{q∈R} δ̂(q, w)

En este caso δ(q,a) no necesariamente es igual a δ̂(q,a) ya que incluye paths etiquetados con a (incluyendo paths etiquetados por ε). Ni δ̂(q, ε) es necesariamente igual a δ(q,ε).

## 13. Función de transición de entrada τ

La función de transición de entrada τ de un NFA-ε M es una función de Q × Σ → 2^Q, definida por:

τ(qᵢ, a) = ⋃_{qⱼ ∈ ε-CLOSURE(qᵢ)} ε-CLOSURE(δ(qⱼ, a))

Donde δ es la función de transición de M.

### Tres partes para τ

τ(qᵢ,a) puede ser separada en 3 partes:
1. Obtener el conjunto de estados que pueden ser alcanzados de qᵢ sin procesar un solo símbolo, es decir, con ε-moves, los cuales NO están en τ.
2. Obtener el conjunto de estados que pueden ser alcanzados al procesar un símbolo a de todos los estados del conjunto, los cuales están en τ.
3. Obtener el conjunto de estados a los que se puede llegar con los ε-arcos a partir del conjunto obtenido en 2, los cuales, también están en τ.

**NOTA**: Para un NFA (sin ε-moves) la τ es la misma que su δ. La función τ es usada para construir un DFA equivalente.

## 14. Equivalencia entre NFA y NFA-ε

Igual que el no-determinismo, la habilidad para hacer transiciones con ε no permite a un NFA aceptar conjuntos no regulares.

Esto se mostrará simulando un NFA con ε-moves por medio de un NFA sin tales transiciones.

**Teorema**: Si L es aceptado por un NFA con ε-moves, entonces L es aceptado por un NFA sin ε-moves.

**Demostración**: Es por un procedimiento de construcción...

### Lenguaje aceptado

Se define L(M), el lenguaje aceptado por M = (Q, Σ, δ, q₀, F) como:
{w | δ̂(q₀, w) contiene un estado en F}

## 15. Equivalencia de DFA y RE

El plan será mostrar por inducción sobre el tamaño (número de operadores en) de una expresión regular que hay un NFA con ε-transitions denotando el mismo lenguaje.

Esta demostración, junto con los teoremas de equivalencia anteriores:

```
        NFA ←→ NFA con ε-transitions
         ↑              ↓
        DFA ←→         RE
```

### RE a NFA

**Teorema**: Sea r una expresión regular. Entonces, existe un NFA con ε-transitions que acepte L(r).

**Demostración**: ...

### Construcción de un NFA a partir de una RE

- r = ε
- r = ∅
- r = a
- r = r₁ + r₂
- r = r₁r₂
- r = r₁*

### DFA a RE

**Teorema**: Si L es aceptado por un DFA, entonces, L es denotado por una expresión regular.

**Demostración**: ...

## 16. Construcción de una RE a partir de un DFA

La equivalencia de procesos de un DFA y sus caminos nos proporciona un método heurístico para determinar el lenguaje que es aceptado por un DFA.

Los strings aceptados en un estado qᵢ (estado final) son precisamente aquellos deletreados por el camino de q₀ a qᵢ.

Podemos entonces separar la determinación de esos caminos en dos partes:
- Encontrar las expresiones regulares u₁, ..., uₙ para los strings en todos los caminos de q₀ que alcanzan qᵢ por primera vez.
- Encontrar las expresiones regulares v₁, ..., vₘ para todos los caminos que dejan qᵢ y regresan a qᵢ.
- Los strings aceptados por qᵢ son (u₁ ∪ ... ∪ uₙ)(v₁ ∪ ... ∪ vₘ)*.

Los strings aceptados por el DFA son la unión de los aceptados por cada estado final qᵢ.

## Referencias

1. T.A. Sudkamp. Languages and Machines: An Introduction to the Theory of Computer Science. Pearson, 3rd Edition (2005).
2. J.E. Hopcroft, R. Motwani, J.D. Ullman. Introduction to Automata Theory, Languages, and Computation. Pearson, 3rd Edition (2006).