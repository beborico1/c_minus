# Implementación de un Analizador Sintáctico con AST

Hola, jóvenes. En nuestra última clase no pudimos terminar por completo el código de la gramática pequeña que estábamos programando para construir el Abstract Syntax Tree (AST). Hoy haré esta explicación de manera más detallada para que puedan revisarla tranquilamente la próxima semana.

## Antecedentes: La Gramática y EBNF

Recordarán que teníamos una gramática que debíamos programar, pero necesitábamos hacer transformaciones porque tenía recursión por la izquierda. Específicamente, en las reglas `exp` y `term` encontramos recursión por la izquierda, lo cual requería conversiones.

Los expertos en gramáticas descubrieron que es mejor convertirla a una forma especial conocida como EBNF (Extended Backus-Naur Form), que nos ahorra muchos problemas y se parece mucho a la forma en que vamos a codificarla. En esta notación:

- Las **llaves `{}`** indican un ciclo (Kleene Star), que se programa con un `while`
- Los **corchetes `[]`** indican una parte opcional, que se programa con un `if`

El token siguiente es el que nos indica si debemos entrar al ciclo o no. Por ejemplo:
- Para entrar al ciclo en `exp`, necesitamos que el siguiente token sea `OpSuma` (+ o -)
- Para entrar al ciclo en `factor`, necesitamos que el siguiente token sea `OpMult` (*)
- En el caso de `if-else`, la parte opcional se ejecuta si el siguiente token es `ELSE`

## Preparando el Código

Abriré un nuevo archivo en Python y lo guardaré como "parser_AST_simple.py" para que lo recuerden. Comenzaremos colocando la gramática en EBNF como comentario:

```
# Gramática en EBNF:
# exp -> term {(+ | -) term}
# term -> factor {* factor}
# factor -> NUM | ( exp )
```

Observen que no es necesario programar `OpSuma` y `OpMult` como reglas separadas. `OpSuma` se sustituye directamente por los símbolos + o -, y `OpMult` por el símbolo *.

## Estructura del Analizador

Lo que queremos ahora es que nuestro parser devuelva un AST, no simplemente un valor booleano como antes. Vamos a seguir la estructura recomendada por el autor del libro.

Primero, importamos la biblioteca `enum` de Python para hacer enumeraciones:

```python
from enum import Enum
```

### Definición del Tipo de Expresión

Creamos una enumeración para los tipos de expresiones:

```python
class TipoExpresion(Enum):
    OP = 0    # Operador (+, -, *) con dos operandos (hijos)
    CONST = 1 # Constante numérica (sin hijos)
```

En esta gramática simple solo tenemos dos tipos de expresiones:
1. **Operadores:** como +, -, * que tienen dos operandos (hijo izquierdo y derecho)
2. **Constantes:** que son los números, sin hijos

Aunque procesaremos paréntesis que abren y cierran, estos no forman parte del AST final, ya que su función es solo modificar la precedencia de operaciones.

### Definición del Nodo del Árbol

Necesitamos crear una clase para los nodos del árbol:

```python
class NodoArbol:
    def __init__(self):
        self.hijoIzquierdo = None  # Hijo izquierdo (operando izquierdo)
        self.hijoDerecho = None    # Hijo derecho (operando derecho)
        self.exp = None            # Tipo de expresión (OP o CONST)
        self.op = None             # Operador (+, -, *) si es tipo OP
        self.val = None            # Valor numérico si es tipo CONST
```

Un nodo puede tener solo dos hijos porque los operadores de nuestra gramática (suma, resta, multiplicación) son binarios. Para estructuras más complejas como un `if` (que tendría tres hijos: condición, acciones verdadero, acciones falso), necesitaríamos más hijos o implementarlos como un arreglo.

### Función para Crear Nuevos Nodos

Creamos una función que nos facilite crear nuevos nodos:

```python
def nuevoNodo(tipo):
    t = NodoArbol()
    if t is None:
        print("Error: sin memoria disponible")
        return None
    else:
        t.exp = tipo  # Asignamos el tipo de expresión
        return t
```

### Función para Manejar Errores de Sintaxis

También necesitamos una función para manejar errores de sintaxis:

```python
def errorSintaxis(mensaje):
    print("---> Error de sintaxis:", mensaje)
```

## Funciones Principales del Parser

### Función Match

Esta función verifica si el token actual coincide con el esperado y avanza al siguiente:

```python
def match(tok):
    global token, posicion
    
    if token == tok:
        posicion += 1
        if posicion == len(cadena):
            token = '$'  # Fin de la entrada
        else:
            token = cadena[posicion]
    else:
        errorSintaxis("Token no esperado")
```

### Función para Expresiones

La función `exp` implementa la regla `exp -> term {(+ | -) term}`:

```python
def exp():
    # Procesar el primer término
    t = term()
    
    # Ciclo para procesar operadores de suma/resta y términos adicionales
    while token in ['+', '-']:
        # Crear nodo para el operador
        p = nuevoNodo(TipoExpresion.OP)
        p.hijoIzquierdo = t  # El término procesado es hijo izquierdo
        p.op = token         # Guardar el operador (+ o -)
        
        # Avanzar al siguiente token
        match(token)
        
        # Procesar término derecho
        p.hijoDerecho = term()
        
        # Actualizar t para mantener la construcción del árbol
        t = p
    
    return t
```

### Función para Términos

La función `term` implementa la regla `term -> factor {* factor}`:

```python
def term():
    # Procesar el primer factor
    t = factor()
    
    # Ciclo para procesar operadores de multiplicación y factores adicionales
    while token in ['*']:
        # Crear nodo para el operador
        p = nuevoNodo(TipoExpresion.OP)
        p.hijoIzquierdo = t  # El factor procesado es hijo izquierdo
        p.op = token         # Guardar el operador (*)
        
        # Avanzar al siguiente token
        match(token)
        
        # Procesar factor derecho
        p.hijoDerecho = factor()
        
        # Actualizar t para mantener la construcción del árbol
        t = p
    
    return t
```

### Función para Factores

La función `factor` implementa la regla `factor -> NUM | ( exp )`:

```python
def factor():
    # Caso 1: El factor es un número
    if token in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
        t = nuevoNodo(TipoExpresion.CONST)
        t.val = token  # Guardar el valor numérico
        match(token)
        return t
    
    # Caso 2: El factor es una expresión entre paréntesis
    elif token == '(':
        match('(')  # Consumir el paréntesis de apertura
        t = exp()   # Procesar la expresión dentro de los paréntesis
        match(')')  # Consumir el paréntesis de cierre
        return t
    
    # Caso de error: token inesperado
    else:
        errorSintaxis("Token no esperado")
        return None
```

## Funciones para Imprimir el Árbol

Para visualizar el AST generado, necesitamos funciones que lo impriman:

```python
indentacion = 0  # Variable global para la indentación

def imprimeEspacios():
    print(" " * indentacion, end="")

def imprimeAST(arbol):
    global indentacion
    
    if arbol is not None:
        # Aumentar indentación para este nivel
        indentacion += 2
        
        # Imprimir espacios según nivel de indentación
        imprimeEspacios()
        
        # Imprimir según tipo de nodo
        if arbol.exp == TipoExpresion.OP:
            print("Operador:", arbol.op)
        elif arbol.exp == TipoExpresion.CONST:
            print("Constante:", arbol.val)
        else:
            print("ExpNode de tipo desconocido")
        
        # Imprimir recursivamente los hijos
        imprimeAST(arbol.hijoIzquierdo)
        imprimeAST(arbol.hijoDerecho)
        
        # Disminuir indentación al volver
        indentacion -= 2
```

## Programa Principal

Finalmente, nuestro programa principal:

```python
# Inicialización
cadena = input("Dame la cadena que quieres que procese: ")
posicion = 0
token = cadena[posicion]

# Construir el AST
ast = exp()

# Verificar que se consumió toda la entrada
if token != '$' and posicion < len(cadena):
    errorSintaxis("El código termina antes que el archivo")
else:
    # Imprimir el AST
    imprimeAST(ast)
```

## Ejemplos de Ejecución

Probemos el código con algunos ejemplos:

1. **Ejemplo: `5+2*7`**
   - Raíz: Operador +
     - Hijo izquierdo: Constante 5
     - Hijo derecho: Operador *
       - Hijo izquierdo: Constante 2
       - Hijo derecho: Constante 7

2. **Ejemplo: `(2+5)*7`**
   - Raíz: Operador *
     - Hijo izquierdo: Operador +
       - Hijo izquierdo: Constante 2
       - Hijo derecho: Constante 5
     - Hijo derecho: Constante 7

3. **Ejemplo: `(2+4)*(3-7)`**
   - Raíz: Operador *
     - Hijo izquierdo: Operador +
       - Hijo izquierdo: Constante 2
       - Hijo derecho: Constante 4
     - Hijo derecho: Operador -
       - Hijo izquierdo: Constante 3
       - Hijo derecho: Constante 7

## Consideraciones Finales

Es importante recordar que en una implementación real, los tokens no se extraen directamente de un string como hicimos aquí por simplicidad. En un compilador completo, los tokens son proporcionados por el analizador léxico (lexer). Cada vez que necesitamos un token, lo solicitamos al lexer.

He compartido en Canvas el código completo del parser de Tiny, que muestra cómo interactúa con el lexer. Lo revisaremos después de las vacaciones.

¡Gracias por su atención! Que tengan unas buenas vacaciones y nos vemos pronto.
