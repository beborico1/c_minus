# Analizador Sintáctico
## Diseño de Compiladores
**Dr. Víctor de la Cueva**  
vcueva@tec.mx

## Parseo

- Es un proceso que tiene como objetivo realizar el análisis sintáctico o gramatical de un programa.
  - Debe asegurarse que el programa tiene una estructura que cumple con las reglas sintácticas del lenguaje
  - Recibe como entrada la secuencia de tokens y entrega como salida el árbol sintáctico
  - Tiene la responsabilidad de detectar errores en la sintaxis
- Árbol sintáctico: es una estructura para representar la estructura sintáctica del programa, también se le conoce como árbol de análisis gramatical.

## Ejemplo

- Si una parte del programa es: `if x = y then 1 else 2 end`
- El Lexer da como salida los siguientes tokens: `IF ID EQUAL ID THEN INT ELSE INT END`
- El Parser recibe como entrada estos token y da como salida el siguiente árbol:

```
     IF-THEN-ELSE
       /    \   \
   EQUAL   INT  INT
  /    \
 ID    ID
```

## Herramientas

- Se requieren al menos dos herramientas:
  - Una que nos ayude a especificar las reglas sintácticas del lenguaje
  - Otra que nos ayude a realizar la implementación de dichas reglas en un parser
  - Desde luego que puede ser la misma
- Los lenguajes regulares son unos de los lenguajes más simples (tienen muchas aplicaciones)
  - Muchos lenguajes, incluyendo los de programación, no son regulares: e.g. paréntesis balanceados: `{(i)i | i ≥ 0}`

## Representación

- Los lenguajes de programación tienen una estructura recursiva (e.g. una expresión se define en función de una expresión)
- Las Gramáticas Libres de Contexto (CFG, por sus siglas en inglés) son una notación natural para representar esta naturaleza recursiva.

## Gramáticas libres de contexto (CFG)

Una CFG consiste en:
- Un conjunto de terminales T
- Un conjunto de no-terminales N
- Un símbolo de inicio S (S∈N)
- Un conjunto de producciones X→Y₁...Yₙ
  - X∈N
  - Yᵢ∈N∪T∪{ε}

## Reglas

- Las producciones pueden verse como reglas.
- El proceso completo es:
  1. Iniciar con el string con sólo el símbolo inicial S
  2. Reemplazar cada no-terminal X por el lado derecho de alguna producción X→Y₁...Yₙ
  3. Repetir 2 hasta que no haya no-terminales
- Si al sustituir se tiene la secuencia de strings:
  - α₀→α₁→α₂→...→αₙ
  - Se dice que el string α₀ se reescribe como αₙ en n pasos: α₀ →* αₙ (n ≥ 0)

## Lenguaje

- Definición: Sea G una CFG con símbolo inicial S. Entonces, el lenguaje L(G) de G es:  
  {a₁...aₙ|∀i aᵢ∈T ∧ S→* a₁...aₙ}
- En las aplicaciones de Lenguajes de Programación, los terminales de la CFG son los tokens.

## Comentarios

- Se usa EBNF para representar la gramática del lenguaje.
- La idea de las CFG es excelente pero la membresía es "Sí" o "No" y en realidad se requiere como salida el parse-tree (este mecanismo es adicional).
- Necesita un buen manejador de errores, dando retroalimentación al programador.
- Se requiere implementar una CFG para crear el parser.
- La forma que tenga la gramática es muy importante:
  - Muchas gramáticas generan el mismo lenguaje
  - Las implementaciones son sensibles a la gramática

## Derivaciones

- Es una secuencia de producciones
- Puede ser dibujada como un árbol (parse tree)
  - El símbolo inicial es la raíz
  - Para una producción X→Y₁...Yₙ agregar hijos Y₁...Yₙ al nodo X.
- En el parse tree:
  - Las hojas son terminales
  - Los nodos interiores son no-terminales
  - El recorrido en inorden de las hojas nos da el string de entrada
  - El parse tree muestra la asociación de las operaciones, el string de entrada no (e.g. cuál se hace primero, * o +)
- ¿Varias derivaciones dan el mismo árbol? 
  - rmd o lmd (rightmost derivation o leftmost derivation)

## Ambigüedad

- Se dice que una gramática es ambigua si existe más de un árbol de derivación para algún string.
  - La ambigüedad es mala para los lenguajes ya que el significado de las hojas para algunos programas queda mal definido
- Hay muchas forma de eliminar la ambigüedad para una gramática:
  - El método más directo es reescribir la gramática para quitarla
  - La nueva gramática debe generar el mismo lenguaje pero sólo un parse tree para cada string (el nuevo árbol no es exactamente igual pero genera el mismo lenguaje)

## Notas

- El problema de ver si una gramática es ambigua o no es indecidible.
  - Existen algunas herramientas que lo logran para ciertas gramáticas.
- No existe una forma automática de quitar la ambigüedad.
- Muchas implementaciones deciden usar la gramática ambigua:
  - Es más natural
  - Se deben colocar ciertas reglas de precedencia y asociación para guiar el árbol (declaraciones de desambigüedad)

## Errores

- Los compiladores tienen dos propósitos:
  - Traducir los programas válidos
  - Detectar los programas inválidos (y guiar al usuario sobre cómo hacerlos válidos)
- Existe una gran cantidad de errores posibles:

| Tipo de error | Ejemplo           | Detectado por |
|---------------|-------------------|---------------|
| Léxico        | ... $...          | Lexer         |
| Sintáctico    | ... x*% ...       | Parser        |
| Semántico     | ... int x;y = x[3];... | Typechecker |
| Correctez     | Tu programa favorito | Tester/Usuario (un bug) |

## Manejo de errores

- Los requisitos de un buen manejador de errores:
  - Reportar los errores exacta y claramente
  - Recuperarse de un error rápidamente
  - No bajar la velocidad de compilación de un código válido
- Hay diferentes tipos de manejo de errores:
  - Modo pánico
  - Producciones de error
  - Corrección automática local o global

## Modo pánico

- Es el modo más simple y el más popular.
- Cuando se detecta un error:
  - Desechar los tokens hasta encontrar uno con un rol claro
  - Continuar desde aquí
- Busca tokens de sincronización:
  - Típicamente los terminadores de estatutos o expresiones (e.g. ;, end, endfor)

## Árbol Sintáctico Abstracto (AST)

- Un parser traza la derivación de una secuencia de tokens.
- El resto de la compilación necesita una representación estructural del programa.
- El AST es como un parse tree pero ignora algunos detalles:
  - Cuando un nodo sólo tiene un sucesor se sustituye por él
  - Los paréntesis son muy importantes en el parser (muestran la asociación) pero una vez hecho el parseo no se requieren
  - El AST hace más reducciones

## Algoritmos de parseo

- Las CFG son una excelente herramienta para representar la gramática de los lenguajes de programación.
- Su implementación se basa en ellas y se clasifica en dos tipos de algoritmos:
  - Top-down: forma el AST de la raíz hacia abajo
    - Descendente recursivo
    - Predictivo (gramáticas LL(k)): entrada L-R, derivación L
  - Bottom-up
    - Semantic Role Labeling o SLR (gramáticas LR(k))

## Top-Down Parsing: Descendente Recursivo

- Es un algoritmo de parseo Top-Down
  - El parse tree es construido:
    - Desde arriba (top)
    - De izquierda a derecha
  - Los terminales son revisados en el orden de aparición en el token stream
- Algoritmo:
  - Inicia con el no-terminal de nivel superior
  - Si la producción falla se hace un backtracking para probar producciones alternativas

## Implementación del algoritmo

- Sea TOKEN el tipo token
  - INT, OPEN, CLOSE, PLUS, TIMES, son instancias del tipo TOKEN
- Sea la variable global next un apuntador al siguiente token de entrada (→).
- Se definen algunas funciones booleanas que chequen un match de:
  - Un token terminal dado tok:
    ```
    bool terminal(TOKEN tok) {return *next++ == tok}
    ```
  - La n-ésima producción de S:
    ```
    bool Sn() {...} // checa el éxito de una producción S
    ```
  - Intentar todas las producciones de S:
    ```
    bool S() {...} // tiene éxito si alguna producción de S tiene éxito
    ```

## Ejemplo

- Implementación de la siguiente gramática:
  ```
  E → T | T+E
  T → int | int * T | (E)
  ```
- Para iniciar el parser:
  - Inicializa next al apuntador del primer token
  - Invoca E()
- Muy simple de implementar a mano.

## Limitaciones del algoritmo

- Pruebe la gramática implementada con `int * int`
- El problema es que no hay backtracking cuando la producción tiene éxito.
  - Eso significa que el algoritmo presentado no es completamente general
  - Sin embargo, es suficiente para gramáticas en las que para algún no terminal, a lo más una producción puede tener éxito
  - La gramática puede ser reescrita para trabajar con el algoritmo presentado:
    - Haciendo factorización por la izquierda

## Recursión por la izquierda

- Implemente la gramática S → Sa
  - S() se va a un loop infinito.
- La razón es que la gramática es left-recursive
- Una gramática left-recursive tiene un no-terminal S de la forma S →* Sα para alguna α.
- El algoritmo Recursive Descent no trabaja con este tipo de gramáticas.
  - Es un problema, pero no es muy grave

## Eliminando la recursión por la izquierda

- En general, la gramática que genera todos los strings que inician con β₁| ... |βₖ y continúan con varias instancias de α₁, ... , αₙ, es decir:  
  S → Sα₁|...|Sαₙ|β₁|...|βₘ
- Se puede reescribir a una gramática con right-recursion:
  ```
  S → β₁S′|...|βₘS′
  S′ → α₁S′|...|αₙS′|ε
  ```

NOTA: Ver bibliografía para un algoritmo general que se puede implementar para hacerlo automáticamente.

## El método básico descendente recursivo

- La idea del análisis sintáctico descendente recursivo es muy simple:
  - Observamos la regla gramatical para un no terminal A como una definición para un procedimiento que reconocerá una A.
  - El lado derecho de la regla gramatical para A especifica la estructura del código para este procedimiento:
    - La secuencia de terminales y no terminales es una selección corresponde a concordancias de la entrada y llamadas a otros procedimientos.
    - Las selecciones corresponden a las alternativas (sentencias case o if) dentro del código.

## Primer ejemplo: gramática para expresión en BNF

```
exp → exp opsuma term | term
opsuma → + | -
term → term opmult factor | factor
opmult → *
factor → ( exp ) | número
```

## Repetición y selección

- Consideremos como segundo ejemplo la regla gramatical (simplificada) para un sentencia if:
  ```
  sent-if → if ( exp ) sentencia
          | if ( exp ) sentencia else sentencia
  ```
  - En este ejemplo podríamos no distinguir de inmediato cuál es la regla seleccionada ya que ambas comienzan con el token if.
  - En su lugar, debemos aplazar la decisión acerca de reconocer la parte else opcional hasta que veamos el token else en la entrada,
  - De esta forma, el código correspondería más a la EBNF:
    ```
    sent-if → if ( exp ) sentencia [ else sentencia ]
    ```

## La notación EBNF

- La notación EBNF está diseñada para reflejar muy de cerca el código real de un analizador sintáctico descendente recursivo
- Una gramática deberá siempre traducirse a EBNF si se está utilizando este modo

NOTA: Aún cuando la gramática anterior es ambigua es natural escribir un analizador sintáctico que haga concordar cada token else tan pronto como se encuentre en la entrada. Esto corresponde precisamente a la regla de eliminación de la ambigüedad mas cercanamente anidada.

## Caso de una exp

- En BNF:
  ```
  exp → exp opsuma term | term
  ```
  - Se observa de inmediato que es recursiva por la izquierda y llevaría a un ciclo infinito (se puede evitar pero hacerlo sería muy problemático)
- La solución es utilizar EBNF:
  ```
  exp → term { opsuma term }
  ```
  - Las llaves expresan la repetición que se puede traducir al código con un ciclo (o bucle)
- De la misma forma se hace para term:
  ```
  term → factor { opmult factor }
  ```

## Pseudocódigo a código real

- Es muy importante tomar en cuenta que el pseudocódigo presentado se debe traducir a código real, para lo cual, muchas veces se requiere que los procedimientos regresen algo, lo que los convierte en funciones.
  - Si se está verificando pertenencia a un lenguaje sólo contestaría true o false, para una entrada dada. Ejercicio de parser
  - Si se desean hacer operaciones (e.g. implementar una calculadora) podría regresar un entero correspondiente a la evaluación
  - Si se está haciendo un parser debe regresar el AST

## Construyendo el AST

- En realidad, la implementación de un parser simplemente responde a la pregunta de si un programa está bien escrito con un "Sí" o "No".
- Si se desea que haga más cosas se le deben agregar en el código de los procedimientos.
- Para el caso de un AST, se le debe agregar la creación del árbol en cada nodo, por ejemplo:
  - exp: crear un nodo con + o – en la raíz y formar sus hijos
  - ifStatement: crear un nodo (de tipo if) con tres hijos:
    - Condición (nodo exp), then (nodo sentencia) y else, si es que existe (nodo sentencia)

## Top-Down Parsing: Predictivo

- Es como el descendente-recursivo pero puede predecir cuál producción usar:
  - Viendo los siguientes (unos cuantos) tokens (lookahead)
  - Sin backtracking
  - También usa formas restrictivas de las gramáticas
  - Acepta lo que llamamos gramáticas LL(k)
    - L - Left to right scan
    - L - Left-most derivation
    - k - k tokens of lookahead, (en la práctica k=1)

## Predictivo vs descendente recursivo

- En descendente-recursivo:
  - En cada paso se usan muchas opciones de producción
  - Se usa backtracking para deshacer malas selecciones
  - Usa llamadas recursivas a las funciones
- En LL(1):
  - En cada paso sólo se tiene una opción de producción
  - Requiere una gramática left-factor, en BNF, con la idea de eliminar prefijos comunes de múltiples producciones
  - Esta gramática se utiliza para construir una tabla de parseo
  - Todas las entradas que no tienen producción son errores
  - En lugar de llamadas recursivas usa un stack

## Tabla de análisis sintáctico

- La tabla contiene producciones y está indizada en las filas por No-terminales y en las columnas por tokens, incluyendo el $.
- Agregamos a la tabla M opciones de producción de acuerdo con las siguientes reglas:
  1. Si A→α es una opción de producción, y existe una derivación α ⇒* aβ, donde a es un token, entonces se agrega A→α a la entrada M[A,a].
  2. Si A→α es una opción de producción, y existen derivaciones α⇒* ε y S$⇒* βAaγ, donde S es el símbolo inicial y a es un token (o $), entonces se agrega A→α a la entrada M[A,a].

## Explicaciones de las reglas

- En la regla 1, dado un token a en la entrada, deseamos seleccionar un regla A→α si α puede producir una a para comparar.
- En la regla 2, si A deriva la cadena vacía (vía A→α), y si a es token que puede venir legalmente después de A en una derivación, entonces deseamos seleccionar A→α para hacer que A desaparezca. Un caso especial de la regla 2 ocurre cuando a=ε.

NOTA: Estas reglas son difíciles de implementar de manera directa pero existe un algoritmo que lo hace automáticamente usando los conjuntos FIRST y FOLLOW.

## Ejemplos

```
S → ( S ) S | ε
```

```
E → T+E | T
T → int | int * T | (E)
```

## Algoritmo Parseo Predictivo

```
Inicializar el stack = <S$> y next
repeat
  case stack of:
    <X, rest> : if M[X, *next] = Y1...Yn
               then stack ← < Y1...Yn rest>;
               else error();
    <t, rest> : if t == *next++
               then stack ← <rest>;
               else error();
until stack == <>
```

## ¿Cómo se hace la tabla?

1. Se tiene una gramática en BNF
2. Quitar recursión por la izquierda
3. Hacer left-factor para que sólo una producción inicie con un símbolo específico
4. Obtener el FIRST de cada símbolo de la nueva gramática.
5. Obtener el FOLLOW de cada símbolo de la nueva gramática.
6. Seguir el algoritmo para creación de la tabla.

## Quitar recursión izquierda y factorizar

```
E → TX
X → +E | ε
T → intY | (E)
Y → *T | ε
```

## Conjuntos FIRST y FOLLOW

- ¿Cómo construir fácilmente la tabla para LL(1)?
- Considere el no-terminal A, la producción A→α y el token t: hacemos M[A, t]=α en dos casos:
  - Si α →* tβ
    - α puede derivar a t en la primera posición
    - Decimos que t ∈ FIRST(α)
  - Si A→α, α→*ε y S→* βAtδ
    - Es útil si el stack tiene aA, la entrada es t y A no puede derivar a t
    - En este caso, sólo hay una opción para deshacerse de A (derivando ε)
    - Sólo puede ser si t puede seguir a A en al menos una derivación
    - Decimos que t ∈ FOLLOW(A)

## FIRST

- Definición: FIRST(X) = {t | X→*tα} ∪ {ε | X→* ε}
- Algoritmo:
  1. FIRST(t) = {t}, t es un terminal
  2. ε∈FIRST(X), X es un no-terminal
     - Si X→ε
     - Si X→A₁...Aₙ y ε∈FIRST(Aᵢ) para toda 1≤i≤n
  3. FIRST(α) ⊆ FIRST(X) si
     - X→A₁...Aₙα, y
     - ε∈FIRST(Aᵢ) para toda 1≤i≤n

## Para la gramática ejemplo modificada

```
E → TX
X → +E | ε
T → intY | (E)
Y → *T | ε
```

| Símbolo | FIRST | FOLLOW |
|---------|-------|--------|
| + | {+} | |
| * | {*} | |
| ( | {(} | |
| ) | {)} | |
| int | {int} | |
| E | {(, int} | |
| T | {(, int} | |
| X | {+, ε} | |
| Y | {*, ε} | |

## FOLLOW

- Definición: FOLLOW(X) = { t | S→* βXtδ }
- Intuición:
  - Si X → AB entonces FIRST(B) ⊆ FOLLOW(A) y FOLLOW(X) ⊆ FOLLOW(B)
    - Si B →* ε entonces FOLLOW(X) ⊆ FOLLOW(A)
  - Si S es el símbolo inicial entonces $ ∈ FOLLOW(S)
- Algoritmo:
  1. $ ∈ FOLLOW(S)
  2. FIRST(β) – {ε} ⊆ FOLLOW(X)
     - Para cada producción A→αXβ
  3. FOLLOW(A) ⊆ FOLLOW(X)
     - Para cada producción A→αXβ donde ε∈FIRST(β)

## Tabla de parseo a partir de FIRST y FOLLOW

- Objetivo: Construir una tabla M para una CFG G.
- Para cada producción A→α en G hacer:
  - Para cada terminal t ∈FIRST(α) hacer: M[A,t] = α
  - Si ε ∈ FIRST(α), para cada t ∈ FOLLOW(A) hacer: M[A,t] = α
  - Si ε ∈ FIRST(α) y $ ∈ FOLLOW(A) hacer: M[A,$] = α

## Bottom-up Parsing: Simple LR (SLR)

- Es más general y más eficiente que top-down parsing.
- Construido sobre las ideas de top-down parsing.
- Es el método preferido para hacer compiladores usando parser generator tools (e.g. YACC).
- No requiere gramáticas factorizadas a la izquierda.
- Usa una gramática más natural pero todavía se requiere que sea no ambigua.

## Gramática para los ejemplos

```
E → T+E | T
T → int * T | int | ( E )
```

## Reducciones

- Una reducción es la aplicación invertida de una producción.
- Bottom-Up Parsing hace reducciones sobre el string de entrada hasta llegar al símbolo de inicio, mediante la aplicación invertida de producciones.

## Fact #1

- Fact #1: Una propiedad importante es que si leemos las derivaciones aplicadas pero en sentido inverso al de su aplicación (de abajo hacia arriba) obtenemos una derivación de más a la derecha a la inversa.

## Shift-reduce parsing

- Es la estrategia general de todos los BUP.
- La propiedad de la derivación por la derecha tiene una consecuencia interesante:
  - Sea abw un paso del BUP
  - Asumimos que la siguiente reducción es X→β
  - Entonces, w es un string de terminales
  - Esto debido a que aXw→ abw es un paso de la derivación de más a la derecha

## Idea

- Dividir el string en 2 substrings:
  - Substring derecho, el cual todavía no es examinado por el parseo
  - Substring izquierdo, que contienen terminales y no terminales
  - El punto de división se marca con un pipe (|): aX|w, donde w es la entrada todavía no examinada
- Para implementar BUP sólo se requieren dos clases de acciones:
  - Movimientos Shift
  - Movimientos Reduce

## Movimientos Shift y Reduce

- Shift: mueve el pipe | un lugar a la derecha.
  - Pasa un terminal al string de la izquierda:  
    ABC | xyz ⇒ ABCx | yz
- Reduce: aplicar una producción inversa al final más a la derecha del string de la izquierda.
  - Si A→xy es una producción, entonces:  
    Cbxy | ijk ⇒ CbA | ijk

## Implementación

- Cada vez que hacemos un reduce generamos una parte del árbol.
- El string de la izquierda puede ser implementado por un stack:
  - El top del stack es |
  - Shift mete un terminal al stack
  - Reduce:
    - Saca 0 o más símbolos del stack (lado derecho de una producción)
    - Mete un no-terminal al stack (lado izquierdo de una producción)

## Conflictos

- En un estado dado, más de una acción (shift o reduce) puede llevarnos a un estado válido (lo cual no debe ser):
  - Si es un shift o reduce legal, hay un conflicto shift-reduce
    - No son buenos pero son fáciles de quitar
    - Posiblemente se requiera usar declaraciones de precedencia
  - Si es legal hacer un reduce por dos diferentes producciones es un conflicto reduce-reduce
    - Normalmente, indican alguna clase de problema grande con la gramática
    - La gramática debe ser revisada y modificada

## Handle

- Es otro concepto fundamental para los BUP.
- ¿Cómo decidimos cuando hacer shift o reduce?
  - Intuición: siempre queremos reducir sólo si el resultado puede seguirse reduciendo hasta el símbolo de inicio
- Si tenemos la derivación: S →* αXw → αβw
  - Decimos que αβ es un handle de αβw
  - Eso significa que esa reducción es correcta
- Los handles formalizan la intuición:
  - Un handle es una reducción que sólo permite reducciones hasta el símbolo de inicio
  - Sólo queremos reducir handles
  - ¿Cómo encuentro los handles?

## Fact #2

- Fact #2 sobre el bottom-up parsing:
  - En shift-reduce parsing, los handles sólo aparecen en el top de stack, nunca en medio.
- Los algoritmos de BUP se basan en reconocer handles.

## Reconociendo handles

- Malas noticias:
  - Hasta ahora, no existe ningún algoritmo eficiente para reconocer handles
- Buenas noticias:
  - Existen buenas heurísticas para pronosticar los handles
  - En algunos tipos de CFGs, las heurísticas siempre pronostican el correcto (e.g. gramáticas SLR(k))
- No es obvio cómo detectar handles
  - Recordar que en cada paso el parser sólo ve el stack, no la entrada completa

## Prefijo viable

- Definición: α es un prefijo viable si hay una w tal que α|w es un estado del parser shift-reduce.
  - α es el stack
  - w es el resto de la entrada.
- El parser sólo conoce un prefijo de w, generalmente un token
- ¿Qué significa un prefijo viable?
  - Un prefijo viable no extiende el pasado de la parte final del handle
  - Se llama prefijo viable porque es un prefijo del handle
  - Mientras el parser tenga prefijos viables en el stack no se detectará ningún error en el parseo

## Fact #3

- Fact #3 sobre el bottom-up parsing:
  - Para cualquier gramática, el conjunto de prefijos viables es un lenguaje regular
- Es un poco complicado de demostrar pero es la clave de los BUP.
  - Todas las herramientas de parseo están basadas en este hecho
  - Es decir, el conjunto de prefijos viables puede ser reconocido por un autómata finito

## Item

- Un ítem es una producción con un punto "." en algún lugar de su lado derecho.
- El único ítem para X→ε es X→.
- Los ítems son comúnmente llamados ítems LR(0).
- Ejemplo: Un ítem T→(E.) significa:
  - Hasta ahora hemos visto '(E' de esa producción y nos falta por ver ')'

## Organización del stack

- El stack puede tener muchos prefijos del lado derecho (rhs):
  Prefijo₁Prefijo₂ ... Prefijoₙ₋₁
- Sea Prefijoᵢ un prefijo del rhs de Xᵢ→αᵢ
  - El Prefijoᵢ eventualmente se reducirá a Xᵢ
  - La parte perdida de αᵢ₊₁ inicia con Xᵢ
    - Es decir, hay una producción Xᵢ₊₁ → Prefijoᵢ₊₁Xᵢβ para alguna β
- Recursivamente, Prefijo₁,Prefijo₂,...,Prefijoₙ eventualmente se reducirá a la parte perdida de α₀.

## Idea

- Para reconocer prefijos viables, debemos:
  - Reconocer una secuencia de lados derechos (rhs) parciales de las producciones
  - Cada rhs parcial puede, eventualmente, reducirse a parte del sufijo perdido de su predecesor

## Algoritmo reconocedor de prefijos viables

1. Agregar una producción dummy S'→S a G.
2. Los estados del NFA son los items de G. Incluyendo la producción extra
3. Para un ítem E→α.Xβ agregar la transición E → α . X β ⇒ₓ E → α X . β
4. Para un ítem E→α.Xβ y una producción X→γ agregar:
   E → α . X β ⇒ₑ X → . γ
5. Cada estado es un estado de aceptación.
6. El estado inicial es S'→.S

## Ejemplo: NFA

```
S' → E
E → T+E | T
T → int * T | int | ( E )
```

```
Producción agregada   Gramática original
   S'→E.
   S'→.E
           E→.T+E
           E→.T
```

## NFA completo

[Fuente: [3] 08-03-recognizing-viable-prefixes-annotated]

## DFA resultante

[Fuente: [3] 08-03-recognizing-viable-prefixes-annotated]

## SLR Parsing

- Significa Simple LR
- Mejora LR(0) asignando algunas heurísticas shift/reduce
  - Genera menos estados con conflictos
- Idea: Asume:
  - Stack contiene α
  - Siguiente entrada es t
  - DFA con la entrada α termina en el estado e (recorre todo el stack, desde el inicio hasta el top, esto es, de izquierda a derecha)
- Reduce por medio de X→β si
  - e contiene el ítem X→β.
  - t ∈ Follow(X) – Aprovecha la entrada
- Shift si
  - e contiene el ítem X→β.tw

## Gramática SLR

- Si hay un conflicto con las reglas anteriores entonces la gramática no es SLR.
- Las reglas equivalen a una heurística para detectar handles.
  - Las gramáticas SLR son aquellas donde las heurísticas detectan exactamente los handles.

## Ejemplo

- En el DFA del parser LR(0), los estados siguientes tienen conflictos shift-reduce:
  ```
  E→T.  E→T.+E
  T→int.  T→int.*T
  ```
- En el primero, usando FOLLOW(E) = {$, )}
  - Hace reduce si ya tenemos la entrada ($) o si el siguiente token en la entrada es )
  - Hará shift si el siguiente token en la entrada es +
  - En cualquier otra situación reportamos un parsing-error
- En el segundo igual:
  - Shift si el siguiente token es *
  - Reduce si la entrada está en el FOLLOW(T)={$, ), +}

## Algoritmo de parseo SLR

1. Sea M el DFA para prefijos viables de G
2. Sea |X₁ ... Xₙ $ la configuración inicial
3. Repetir hasta que la configuración sea S|$
   - Sea α|w la configuración actual
   - Recorrer M sobre el stack actual α
   - Si M rechaza α reportar parsing-error
     - El stack α no es un prefijo viable
   - Si M acepta α con el ítem I, sea a la siguiente entrada
     - Shift si X→β.αγ∈I
     - Reduce si X→β.∈I y a∈Follow(X)
     - Reportar parsing-error si ninguna aplica

## Ejemplo: DFA con números

[AA 2.22]

## Referencias

- A.V.Aho, M.S.Lam, R.Sethi, and J.D.Ullman. Compilers: Principles, Techniques, and Tools. 2nd Pearson (2012).
- K.C. Louden. Contrucción de Compiladores: principios y práctica. Thomson (2004).
- Alex Aiken. Compilers. Stanford Online (2018).
  - https://lagunita.stanford.edu/courses/Engineering/Compilers/Fall2014/about
