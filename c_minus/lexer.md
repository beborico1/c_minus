# Análisis Léxico
## Diseño de Compiladores
**Dr. Víctor de la Cueva**  
vcueva@tec.mx

## Lexer o Scanner

- **Programa fuente (texto) → TOKENS:**
  - Palabras de un lenguaje natural
  - Secuencia de caracteres → unidad de información:
    - Palabras reservadas
    - Identificadores
    - Símbolos especiales
    - Constantes
- **Métodos (algoritmos) principales (reconocimiento de patrones):**
  - Expresiones regulares
  - Autómatas finitos

## Tokens

- Son entidades lógicas que por lo general se definen como un tipo enumerado.
  - e.g. en C:
    ```c
    typedef enum
    {IF, THEN, ELSE, PLUS, MINUS, NUM, ID, ...}
    TokenType;
    ```
  - En Python: clase que hereda de la clase Enum (importar `from enum import Enum`).
  - Los tokens, como unidades lógicas, se deben distinguir claramente de las cadenas de caracteres (lexema) que representan.
    - IF representa a "if", PLUS representa a "+".

## Atributos

- Cualquier valor asociado con un token.
  - NUM:
    - Valor de cadena → "4537" (Lexema), Token = NUM
    - Valor numérico → 4537
  - PLUS
    - Valor de cadena → "+" (Lexema), Token = PLUS
    - Operador aritmético → +
- Es útil recolectar los atributos de un token en un registro (TokenRecord):
  ```c
  typedef struct {                typedef struct {
    TokenType tokenval;             TokenType tokenval;
    char * stringval;               union {
    int numval;                       char * stringval;
  } TokenRecord;                       int numval;
                                     } attribute;
                                   } TokenRecord;
  ```

## EXPRESIONES REGULARES

### Expresiones regulares

- Representan patrones de cadenas de caracteres, por lo que son una excelente herramienta para representar tokens de un tipo específico.
- r → L(r):
  - Σ → Alfabeto → Símbolos → Conjunto de caracteres
  - Normalmente ASCII
  - Metacaracteres: \ y ' (también son símbolos)

### Operaciones de ER

- **Tres operaciones básicas:**
  - Selección (entre alternativas): |
  - Concatenación: yuxtaposición
  - Repetición (cerradura): *
- **Extensiones:**
  - Al menos una vez: +
  - Cadena vacía: ε
  - Agrupamiento: ( )
  - Cualquier carácter: .
  - Intervalo (clases de caracteres): [a-z]
  - Cualquier carácter que no esté (not): ~a, ~(a|b|c) ≡ ^a, [^abc]
  - Opcionales: ? (+,-)?

### Concatenación i veces

- La única forma de representar una concatenación de i veces del mismo carácter es escribiendo el número completo:
  - E.g. concatenación de 4 veces el carácter b: bbbb
- Se puede ahorrar espacio usando un exponente: b⁴
- Esto puede llevar a algunas confusiones ya que algunas veces se puede usar como una variable:
  - E.g. bⁱ, se concatenan i caracteres b, por lo que se puede pensar que la expresión bⁱabⁱ es regular y ¡no lo es!

### ER para tokens en lenguajes

- Tienden a usarse por categorías:
  - Palabras reservadas
  - Símbolos especiales
  - Identificadores
  - Constantes o literales (numéricas o de cadena)

### Ambigüedad

- Algunas cadenas se puede definir con varias expresiones regulares:
  - then (identificador o palabra reservada)
  - <> (< o <>).
- Se deben establecer reglas de no ambigüedad:
  - Identificador o palabra reservada → palabra reservada
  - Principio de la subcadena más larga
  - Delimitadores de token (¿se eliminan o no?)

## AUTÓMATAS FINITOS

### Teoría de autómatas

- Es el estudio de los dispositivos computacionales abstractos (máquinas) especiales llamados máquinas de estados finitos.
- Antes de que hubiera computadoras, en los 30's, A. Turing estudió una máquina abstracta que tenía todas las capacidades de las computadoras actuales, al menos en cuanto a lo que podían computar (Máquina de Turing).
- En los 40s y 50s, los investigadores iniciaron el estudio de unas máquinas muy simples llamadas "Autómatas Finitos".
- Estos autómatas fueron propuestos originalmente para modelar el funcionamiento del cerebro, pero resultaron ser de gran utilidad en un gran número de problemas.

### Sistemas de estados finitos

- Un Autómata Finito (FA) es un modelo matemático de un sistema, con entradas y salidas discretas.
- El sistema puede estar en uno (cualquiera) de un número finito de configuraciones internas llamadas "estados".
- El estado del sistema resume la información concerniente a las entradas pasadas, que es necesaria para determinar el comportamiento del sistema para entradas subsecuentes.

### Definiciones básicas

- Un autómata finito (FA) consiste en un conjunto finito de estados y un conjunto de transiciones de un estado a otro que ocurren de acuerdo con símbolos de entrada seleccionados de un alfabeto Σ.
- Para cada símbolo de entrada hay exactamente una transición hacia afuera del estado (posiblemente de regreso al mismo estado).
- Un estado, usualmente denotado por q₀ (o simplemente 0), es el estado inicial, en el cual el autómata inicia su funcionamiento.
- Algunos estados son designados como estados finales o de aceptación.

### Autómatas finitos

- O máquinas de estados finitos, son una clase particular de algoritmos.
- Uso → proceso de reconocimiento de patrones en cadenas → construir analizadores léxicos.
- Fuerte relación entre FA y RE, de hecho, son equivalentes y representan lenguajes regulares.
- Como son algoritmos, son mucho más fáciles de implementar que las RE.

### Definición formal de FA

- Formalmente denotamos a un autómata finito por una 5-tupla (Q,Σ,δ,q₀,F), donde:
  - Q es el conjunto finito de estados
  - Σ es el alfabeto finito de entrada
  - q₀∈Q es el estado inicial
  - F⊆Q es el conjunto de estados finales
  - δ es la función de transición mapeando Q×Σ→Q, esto es, δ(q,a) es un estado para el estado actual q y un símbolo de entrada a

### Diagrama de Transición

- Un grafo dirigido, llamado diagrama de transición, es asociado con un autómata finito como sigue:
  - Los vértices del grafo corresponden a los estados de un FA.
  - Si existe una transición de un estado q a un estado p en una entrada a, entonces, hay un arco etiquetado con una a, del estado q al estado p en el diagrama de transición.
  - El FA acepta un string x si la secuencia de transiciones correspondiente a los símbolos de x lleva al FA de un estado de inicio a un estado de aceptación.
    - Si el string x no termina y el autómata ya no se puede mover, x se rechaza.
    - Si el string x termina, pero el autómata no queda en un estado final, x se rechaza.

### Resumen de nomenclatura gráfica

- Estados: círculos
- Estados finales: círculos dobles
- Transiciones: aristas dirigidas
- Estado inicial: con una arista sin círculo previo
- Etiquetas: en los estados o en las aristas

### Autómatas finitos y lenguajes regulares

- Anteriormente describimos lo que era un lenguaje regular.
- Estos lenguajes son exactamente los que pueden ser descritos usando autómatas finitos.
- Se puede decir que el autómata finito determinístico es un aceptador del lenguaje expresado por una RE.
- Otra forma de ver la relación entre los dos es que:
  - La RE sirve para definir el lenguaje.
  - El DFA sirve para implementar un reconocedor de strings que pertenecen al lenguaje.

### Aceptación de un string

- Un string x se dice aceptado por un autómata finito M=(Q,Σ,δ,q₀,F) si δ(q₀,x) = p para alguna p en F.
- El lenguaje aceptado por M, designado como L(M), es el conjunto {x|δ(q₀,x) está en F}.
- Un lenguaje es un conjunto regular (o sólo regular) si es un conjunto aceptado por algún autómata finito (el término regular viene de las expresiones regulares).
- Cuando se habla de algún lenguaje aceptado por un autómata finito M, nos referimos al conjunto específico L(M), no a todos los strings que sean aceptados por M.

### Un programa para aceptar o rechazar (membresía)

- En todos los autómatas, el proceso para decidir si se acepta o no un string dado es exactamente el mismo y se basa en la función de transición, representada por medio de una tabla de transición.
- Si la información se tiene en un archivo que contenga toda la definición de las 5 partes de un autómata, se puede hacer fácilmente un programa que lo lea, pida un string y conteste si se acepta o no.
- El programa que lee la tabla, la sigue y contesta, es exactamente el mismo para cualquier tabla.

### Ejemplo:

- Hacer una RE N que acepte el conjunto de strings sobre {a,b} que contenga el substring bb.  
  L(N)=(a|b)*bb(a|b)*.
- Hacer un DFA M que acepte el conjunto de strings sobre {a,b} que contenga el substring bb, es decir, que acepte strings que pertenecen al lenguaje definido como L(M)=(a|b)*bb(a|b)*.

### DFA

![DFA Example](https://ivanzuzak.info/noam/webapps/fsm_simulator/)
![DFA Example](https://rubenwardy.com/finite_automaton_sim/)

### Probando algunos strings en el DFA

**Se deben aceptar:**
- bb
- ababbab
- aaababbaa

**Se deben rechazar:**
- abab
- aaababa
- aaabbcaba

### Transiciones

- Las transiciones de un DFA se pueden definir matemáticamente con una función de transición o por medio de una tabla.
- Matemáticamente con una función de transición δ(qᵢ,a) = qⱼ:
  - δ(0,a) = 0     δ(0,b) = 1
  - δ(1,a) = 0     δ(1,b) = 2
  - δ(2,a) = 2     δ(2,b) = 2
- Veamos la tabla del más simple:

| Estado | a | b |
|--------|---|---|
| 0      | 0 | 1 |
| 1      | 0 | 2 |
| 2      | 2 | 2 |

### Implementando un reconocedor (un DFA)

- Hay dos formas clásicas de implementar un reconocedor (un DFA):
  - Usando solamente if's.
  - Usando una tabla de transición.
- **Tabla:**
  - Ventajas: 
    - Se puede guardar en un archivo y leerse al inicio cuando se arranca el programa.
    - Puede hacerse funcionar el mismo programa para varias tablas (motor de transición) con algunos parámetros adicionales.
  - Desventajas:
    - La lectura de la misma es lenta y su acceso es más lento que los if's (en programas simples no se nota ninguna de las dos).
- **If's:**
  - Ventajas:
    - Son más eficientes en velocidad.
  - Desventajas:
    - Para funciones muy grandes el número es muy grande y se puede hacer complejo debuguearlo.
    - Tiene que hacerse un programa para cada lenguaje.

### Código con IF's

```python
# Programa para implementar un reconocedor usando sólo IF's
def reconoce(w):
    estado = 0
    for c in w:
        if estado == 0:
            if c == 'a':
                estado = 0
            elif c == 'b':
                estado = 1
            else:
                return False
        elif estado == 1:
            if c == 'a':
                estado = 0
            elif c == 'b':
                estado = 2
            else:
                return False
        elif estado == 2:
            if c == '$':
                return True
            else:
                if c == 'a':
                    estado = 2
                elif c == 'b':
                    estado = 2
                else:
                    return False

w1 = "bb$"         # acepta
w2 = "ababbab$"    # acepta
w3 = "aaababa$"    # rechaza
w4 = "aaabbcaba$"  # rechaza
print(reconoce(w1))
print(reconoce(w2))
print(reconoce(w3))
print(reconoce(w4))
```

### Código con TABLA

```python
# Programa para implementar un reconocedor usando una TABLA
def reconoce(w):
    estado = inicial
    for c in w:
        if c in alfabeto:
            if c == '$':
                if estado in finales:
                    return True
                else:
                    return False
            estado = tabla[estado][dic[c]]
        else:
            return False
            
dic = {'a':0, 'b':1} # alfabeto X columnas
tabla = [[0, 1], [0, 2], [2, 2]] # tabla de transiciones
inicial = 0 # estado inicial
finales = [2] # estado finales
alfabeto = 'ab$' # alfabeto extendido con $

w1 = "bb$"         # acepta
w2 = "ababbab$"    # acepta
w3 = "aaababa$"    # rechaza
w4 = "aaabbcaba$"  # rechaza
print(reconoce(w1))
print(reconoce(w2))
print(reconoce(w3))
print(reconoce(w4))
```

### Ejemplo: programar este autómata

- Hacer un DFA que acepte strings sobre el alfabeto Σ={0,1}, que tengan un número par de ceros y un número par de unos y programarlo con tabla:

![DFA Example with states](images/diagram_par_impar.png)

## LEXER O SCANNER

### Aplicación de un DFA

- Una de las principales aplicaciones de un DFA es en la creación de la primera parte de un Compilador llamada Lexer o Scanner.
- Un lexer recibe como entrada una secuencia de caracteres y regresa los lexemas y los tokens.
  - Un lexema es un conjunto de caracteres que tiene sentido para un lenguaje (e.g. palabras reservadas, números, identificadores, símbolos especiales, etc.)
  - Un token es el tipo al que pertenece el lexema, es decir: palabra reservada, entero, real, identificador, suma, resta, etc.
  - Ejemplos (lexema, token): (123, ENTERO), (+, SUMA), (if, RESERVADA), (cont, ID), etc.

### De True y False a acciones

- Un DFA regresa normalmente True si un string pertenece a un lenguaje y False en caso contrario.
- Ahora requerimos que detecte token, para lo cual necesitamos que una vez encontrado uno, regrese al inicio del DFA y continúe buscando.
- Eso se puede lograr uniendo en el estado inicial a todos los DFA que detectan algún token para formar un solo DFA, y agregar acciones en los estados finales.

### Ejemplo: Lexer de lenguaje pequeño

- Hacer un lexer de un lenguaje que sume o reste números reales o enteros no negativos, con las siguientes condiciones:
  - Los números reales deben tener al menos un dígito antes del punto y uno después del punto.
  - Los reales no usan notación científica.
  - Los espacios en blanco se deben ignorar (espacios, EOL o TAB).
  - Todas las entradas terminan con el carácter $, que indica el fin de la entrada.
- Las operaciones permitidas son SUMA (+) y RESTA (-).
- Entonces, sólo detecta 4 tokens:
  - ENTERO, REAL, SUMA y RESTA
- Si el string contiene cualquier caracter que no cumpla con esas reglas, se detectará error.
- El Lexer debe contestar una tabla con parejas de Lexema y Token para todos los que detecte.

### Ejemplo de entrada y salida

- Si la entrada es: `25+31.4 - 123 +4$`.
- La salida es:

| Lexema | Token  |
|--------|--------|
| 25     | ENTERO |
| +      | SUMA   |
| 31.4   | REAL   |
| -      | RESTA  |
| 123    | ENTERO |
| +      | SUMA   |
| 4      | ENTERO |

### DFA y TABLA del Lexer

![DFA Lexer](diagram_lexer.png)

- Hay más transiciones a error, por ejemplo, de 1 a 8 con otro.
- b = blanco (espacio, EOL ($) o TAB).
- otro, es cualquier carácter que no sea ninguno de los del lenguaje.
- Se dejan los estados finales al final de la tabla para no tenerlos que poner.

| Estado | d | + | - | . | b | Otro |
|--------|---|---|---|---|---|------|
| 0      | 1 | 6 | 7 | 8 | 0 | 8    |
| 1      | 1 | 4 | 4 | 2 | 4 | 8    |
| 2      | 3 | 8 | 8 | 8 | 8 | 8    |
| 3      | 3 | 5 | 5 | 8 | 5 | 8    |

### Código

```python
tabla = [[1,6,7,0,0,8], [1,4,4,2,4,8], [3,8,8,8,8,8], [3,5,5,8,5,8]]
s = "25+23.56 + 97.042 +25$"
blanco = " \n\t$"
digito = "0123456789"

estado = 0
p = 0
lexema = ''
token = ''
while (p < len(s) and (s[p] != '$' and estado != 8)) and (estado != 8):
    c = s[p]
    if c in digito:
        col = 0
    elif c == '+':
        col = 1
    elif c == '-':
        col = 2
    elif c == '.':
        col = 3
    elif c in blanco:
        col = 4
    else:
        col = 5
    estado = tabla[estado][col]
    if estado == 4:
        token = 'ENTERO'
        print(lexema, token)
        lexema = ''
        estado = 0
    elif estado == 5:
        token = 'REAL'
        print(lexema, token)
        lexema = ''
        estado = 0
    elif estado == 6:
        token = 'SUMA'
        print('+', token)
        estado = 0
    elif estado == 7:
        token = 'RESTA'
        print('-', token)
        estado = 0
    elif estado == 8:
        print("ERROR")
        p += 1
    
    if estado != 0:
        lexema += c
    p += 1
    
    if estado == 0:
        lexema = c
```

### DFA para detectar números más complejos

- Hacer un autómata que reconozca si un string dado es un número o no.
- Un número puede ser:
  - Entero. 3569
  - Real: -12.45
  - Real con notación exponencial: 15.42E-12
- Pueden ser con signo (+ o -) o no
- Si el string contiene cualquier caracter que no cumpla con esas reglas, se detectará como rechazado.

### Autómata y tabla

![DFA Complex Numbers](images/diagram_complex_numbers.png)

| d | +,- | . | d | E,e | otro |
|---|-----|---|---|-----|------|
| 0 | 1   | 7 | 2 | 7   | 7    |
| 1 | 7   | 7 | 2 | 7   | 7    |
| 2 | 7   | 3 | 2 | 4   | 7    |
| 3 | 7   | 7 | 3 | 4   | 7    |
| 4 | 5   | 7 | 6 | 7   | 7    |
| 5 | 7   | 7 | 6 | 7   | 7    |
| 6 | 7   | 7 | 6 | 7   | 7    |
| 7 | 7   | 7 | 7 | 7   | 7    |

### DFA o NFA en código

- Existen varias formas.
- No todas son útiles para un analizador léxico.
- Ejemplo: identificadores

![DFA Identifiers](images/diagram_identifiers.png)

- Con anidación (recursión)
- Manteniendo el estado
- Tabla

### DFA y RE de comentarios

- No siempre es simple escribir una RE, p. ej. Los comentarios:
  - Si son de inicio hasta EOL, es simple: // esto es un comentario
  - Si son de dos símbolos, es complicado: /* este * también */
- Es mucho más simple hacer el DFA
  - Se puede pasar del DFA a RE
- La ventaja es que son prácticamente los mismos para todos los lenguajes de programación y ya están hechas
  - Se pueden buscar y consultar, sin olvidar poner la REFERENCIA.

### Herramientas adicionales

- ε-moves
- NFA
- Conversión de ER a NAF
- ε-closure
- Conversión de NFA a DFA

### Referencias

- A. V. Aho, M. S. Lam, R. Sethi, and J. D. Ullman. Compilers: Principles, Techniques, and Tools. 2nd Pearson (2012).
- K.C. Louden. Contrucción de Compiladores: principios y práctica. Thomson (2004).
- Alex Aiken. Compilers. Stanford Online (2018).
  - https://lagunita.stanford.edu/courses/Engineering/Compilers/Fall2014/about
