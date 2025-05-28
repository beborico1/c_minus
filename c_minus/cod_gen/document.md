# Proyecto 4: Generador de Código para Lenguaje C-

## Portada
**Nombre:** [Nombre del estudiante]  
**Matrícula:** [Número de matrícula]  
**Fecha:** [Fecha de entrega]  
**Materia:** Compiladores  
**Proyecto:** Generador de Código para Lenguaje C-  

---

## Introducción

### Tipo de Código Generado: MIPS Assembly

Para este proyecto se ha seleccionado la generación de código en **MIPS Assembly** por las siguientes razones:

1. **Simplicidad de la arquitectura**: MIPS es una arquitectura RISC (Reduced Instruction Set Computer) que cuenta con un conjunto de instrucciones simple y regular, lo que facilita la traducción desde el AST del lenguaje C-.

2. **Disponibilidad de herramientas**: SPIM es un simulador ampliamente utilizado y bien documentado para ejecutar código MIPS, proporcionando un entorno de pruebas accesible.

3. **Propósito educativo**: MIPS es comúnmente utilizado en cursos de arquitectura de computadoras y compiladores debido a su claridad conceptual.

4. **Correspondencia directa**: Las operaciones básicas del lenguaje C- (asignaciones, operaciones aritméticas, llamadas a funciones) tienen una traducción natural a instrucciones MIPS.

### Características del Generador de Código

El generador de código implementado en `cgen.py` traduce el Árbol Sintáctico Abstracto (AST) generado por el parser a código MIPS que puede ejecutarse en el simulador SPIM. Las características principales incluyen:

- **Manejo de variables globales y locales**
- **Implementación de funciones con parámetros**
- **Operaciones aritméticas básicas (+, -, *, /)**
- **Estructuras de control (condicionales, bucles)**
- **Llamadas a funciones predefinidas (input, output)**
- **Gestión de memoria y registros**

---

## Manual del Usuario

### Requisitos del Sistema

1. **Python 3.x** instalado en el sistema
2. **SPIM simulator** para ejecutar el código MIPS generado
3. Los siguientes archivos en el mismo directorio:
   - `globalTypes.py`
   - `Lexer.py`
   - `Parser.py`
   - `semantic.py`
   - `symtab.py`
   - `cgen.py`
   - `main.py`
   - `sample.c-` (archivo de prueba)

### Paso 1: Preparación del Archivo Fuente

Crear un archivo con extensión `.c-` que contenga el programa en lenguaje C-. Ejemplo (`sample.c-`):

```c
/* Programa de ejemplo */
int x;

int add(int a, int b) {
    return a + b;
}

void main(void) {
    int y;
    
    x = 10;
    y = 20;
    x = add(x, y);
    output(x);
}
```

**[SCREENSHOT 1: Editor de texto mostrando el contenido del archivo sample.c-]**
*Captura de pantalla del editor de texto (VS Code, Sublime, Notepad++, etc.) mostrando el código fuente del programa C- con sintaxis resaltada.*

### Paso 2: Compilación del Programa

**[SCREENSHOT 2: Terminal mostrando estructura de archivos]**
*Captura de pantalla del terminal ejecutando `ls -la` para mostrar todos los archivos del proyecto en el directorio actual.*

Ejecutar el compilador usando el script principal:

```bash
python main.py
```

**[SCREENSHOT 3: Terminal ejecutando python main.py]**
*Captura de pantalla del terminal mostrando el comando `python main.py` antes de ejecutarlo.*

**Salida esperada:**

**[SCREENSHOT 4: Salida completa de la compilación]**
*Captura de pantalla del terminal mostrando toda la salida del proceso de compilación, incluyendo:*

```
=== arbol Sintactico Abstracto (AST) ===

  Var Declaration: x
  Function Declaration: add
    Compound
      Return
        Op: PLUS
          Id: a
          Id: b
  Function Declaration: main
    Compound
      Var Declaration: y
      Assign to:
        Id: x
        Const: 10
      Assign to:
        Id: y
        Const: 20
      Assign to:
        Id: x
        Call: add
          Id: x
          Id: y
      Call: output
        Id: x

=== Iniciando análisis semántico ===

Tabla de simbolos:
================================================================================
ambito  Nombre         Tipo      Lineas              Atributos                     
--------------------------------------------------------------------------------
0       add            int       5                   {'params': [...], 'scope': 1}
0       input          int       0                   {'params': []}                
0       main           void      9                   {'params': [], 'scope': 2}    
0       output         void      0                   {'params': [...]}
0       x              int       3                   {'is_array': False, 'size': None}
1       a              int       5                   {'is_array': False}           
1       b              int       5                   {'is_array': False}           
2       y              int       10                  {'is_array': False, 'size': None}
================================================================================
Inferring Types...
Checking Types...
Type Checking Finished
=== Análisis semántico completado exitosamente ===
```

### Paso 3: Verificación del Código Generado

Después de la compilación exitosa, se genera el archivo `file.s` con el código MIPS:

```bash
ls -la file.s
```

**[SCREENSHOT 5: Verificación del archivo generado]**
*Captura de pantalla del terminal mostrando el comando `ls -la file.s` y confirmando que el archivo fue creado exitosamente.*

Para ver el contenido del código MIPS generado:

```bash
cat file.s
```

**[SCREENSHOT 6: Código MIPS generado]**
*Captura de pantalla mostrando el contenido completo del archivo `file.s` con el código MIPS assembly generado por el compilador.*

### Paso 4: Ejecución en SPIM

Para ejecutar el código generado en SPIM:

1. **Abrir SPIM**:
   ```bash
   spim
   ```

   **[SCREENSHOT 7: Inicio de SPIM]**
   *Captura de pantalla del terminal mostrando SPIM iniciándose y el prompt del simulador.*

2. **Cargar el archivo**:
   ```
   (spim) load "file.s"
   ```

   **[SCREENSHOT 8: Carga del archivo en SPIM]**
   *Captura de pantalla de SPIM mostrando el comando load y cualquier mensaje de confirmación o error.*

3. **Ejecutar el programa**:
   ```
   (spim) run
   ```

   **[SCREENSHOT 9: Ejecución del programa en SPIM]**
   *Captura de pantalla mostrando la ejecución del programa y la salida esperada (en este caso, el valor 30 que es la suma de 10 + 20).*

### Paso 5: Compilación con Archivo Personalizado

Para compilar un archivo diferente, usar el script `compile.py`:

```bash
python compile.py mi_programa
```

**[SCREENSHOT 10: Compilación con archivo personalizado]**
*Captura de pantalla del terminal mostrando la compilación de un archivo personalizado usando compile.py con un nombre específico.*

Esto compilará el archivo `mi_programa.c-` y generará `mi_programa.s`.

**[SCREENSHOT 11: Resultado de compilación personalizada]**
*Captura de pantalla mostrando la salida del proceso de compilación y la verificación de que se generó el archivo .s correspondiente.*

### Estructura de Archivos del Proyecto

```
cod_gen/
├── main.py              # Script principal según especificación
├── compile.py           # Compilador con opciones avanzadas
├── cgen.py              # Generador de código MIPS
├── Parser.py            # Analizador sintáctico
├── Lexer.py             # Analizador léxico
├── semantic.py          # Analizador semántico
├── symtab.py            # Tabla de símbolos
├── globalTypes.py       # Tipos y estructuras globales
├── sample.c-            # Archivo de prueba
├── sample.s             # Código MIPS de referencia
└── tests/               # Directorio con casos de prueba
    ├── test00_simple.c-
    ├── test00_simple.s
    └── ...
```

### Resolución de Problemas Comunes

1. **Error: "No module named 'X'"**
   - Verificar que todos los archivos estén en el mismo directorio
   - Verificar que los nombres de archivos coincidan exactamente

   **[SCREENSHOT 12: Error de módulo no encontrado]**
   *Captura de pantalla mostrando un error típico de módulo no encontrado y cómo se ve en la terminal.*

2. **Errores semánticos**
   - Revisar la sintaxis del programa C-
   - Verificar que las variables estén declaradas antes de su uso
   - Verificar que los tipos sean compatibles

   **[SCREENSHOT 13: Ejemplo de errores semánticos]**
   *Captura de pantalla mostrando un programa C- con errores semánticos y la salida del compilador indicando los errores específicos.*

3. **Error en SPIM**
   - Verificar que el archivo `.s` se haya generado correctamente
   - Verificar la sintaxis del código MIPS generado

   **[SCREENSHOT 14: Error en SPIM]**
   *Captura de pantalla de SPIM mostrando un error típico al cargar o ejecutar código MIPS mal formado.*

---

## Especificaciones Técnicas

### Función Principal: `codeGen(tree, file)`

**Parámetros:**
- `tree`: Árbol Sintáctico Abstracto generado por el parser
- `file`: Nombre del archivo de salida (incluyendo extensión `.s`)

**Funcionalidad:**
- Recorre el AST y genera código MIPS equivalente
- Utiliza la tabla de símbolos para resolver referencias
- Maneja registros y memoria de forma eficiente
- Genera código optimizado para SPIM

### Variables Globales Requeridas

```python
def globales(prog, pos, long):
    global programa
    global posicion  
    global progLong
    programa = prog
    posicion = pos
    progLong = long
```

### Script de Prueba Estándar

```python
from globalTypes import *
from Parser import *
from semantic import *
from cgen import *

f = open('sample.c-', 'r')
programa = f.read()
progLong = len(programa)
programa = programa + '$'
posicion = 0

globales(programa, posicion, progLong)
AST = parser(True)
semantica(AST, True)
codeGen(AST, "file.s")
```

---

## Apéndices

### Apéndice A: Proyecto 1 - Analizador Léxico (Lexer)

#### Descripción General
El analizador léxico es responsable de convertir el flujo de caracteres del programa fuente en una secuencia de tokens. Implementa un autómata finito determinista para reconocer los diferentes elementos léxicos del lenguaje C-.

#### Funciones Principales

**`getToken(imprime=True)`**
- **Propósito**: Función principal que obtiene el siguiente token del programa
- **Retorna**: Tupla (token, tokenString, lineno)
- **Implementación**: Utiliza un autómata finito con estados definidos en `StateType`

**`getChar()`**
- **Propósito**: Obtiene el siguiente carácter del programa fuente
- **Manejo**: Incrementa contadores de línea y posición automáticamente

**`ungetChar()`**
- **Propósito**: Retrocede un carácter en el flujo de entrada
- **Uso**: Permite lookahead de un carácter para la toma de decisiones

#### Estados del Autómata
```python
class StateType(Enum):
    START = 0       # Estado inicial
    INCOMMENT = 1   # Dentro de comentario
    INNUM = 2       # Reconociendo número
    INID = 3        # Reconociendo identificador
    INASSIGN = 4    # Reconociendo operador de asignación
    INLT = 5        # Reconociendo operador menor que
    INGT = 6        # Reconociendo operador mayor que
    INNOT = 7       # Reconociendo operador diferente
    DONE = 8        # Token completado
```

#### Tokens Reconocidos
- **Palabras reservadas**: `if`, `else`, `while`, `return`, `int`, `void`
- **Identificadores**: Secuencias alfanuméricas que comienzan con letra
- **Números**: Secuencias de dígitos
- **Operadores**: `+`, `-`, `*`, `/`, `<`, `<=`, `>`, `>=`, `==`, `!=`, `=`
- **Delimitadores**: `(`, `)`, `[`, `]`, `{`, `}`, `;`, `,`
- **Comentarios**: `/* ... */` (ignorados)

#### Características Especiales
- **Manejo de líneas**: Tracking automático de número de línea y posición
- **Recuperación de errores**: Caracteres no reconocidos se reportan como `ERROR`
- **Lookahead**: Soporte para retroceso de un carácter
- **Variables globales**: Integración con el sistema de variables globales del compilador

---

### Apéndice B: Proyecto 2 - Analizador Sintáctico (Parser)

#### Descripción General
El analizador sintáctico implementa un parser recursivo descendente que construye un Árbol Sintáctico Abstracto (AST) a partir de la secuencia de tokens proporcionada por el analizador léxico.

#### Estructura del AST
```python
class TreeNode:
    def __init__(self):
        self.child = [None] * MAXCHILDREN  # Máximo 3 hijos
        self.sibling = None                # Hermano en la lista
        self.lineno = 0                   # Número de línea
        self.nodekind = None              # NodeKind: StmtK, ExpK, DeclK
        self.stmt = None                  # StmtKind para sentencias
        self.exp = None                   # ExpKind para expresiones
        self.decl = None                  # DeclKind para declaraciones
        self.op = None                    # Operador (para ExpK.OpK)
        self.val = None                   # Valor (para ExpK.ConstK)
        self.name = None                  # Nombre (para ExpK.IdK)
        self.type = None                  # Tipo para verificación semántica
```

#### Funciones de Parsing Principales

**`parser(imprime=True)`**
- **Propósito**: Función principal de parsing
- **Retorna**: Tupla (AST, Error)
- **Función**: Inicia el análisis sintáctico llamando a `program()`

**`program()`**
- **Gramática**: `program → declaration-list`
- **Función**: Punto de entrada para el análisis del programa completo

**`declaration_list()`**
- **Gramática**: `declaration-list → declaration-list declaration | declaration`
- **Función**: Maneja la lista de declaraciones del programa

**`declaration()`**
- **Gramática**: `declaration → var-declaration | fun-declaration`
- **Función**: Distingue entre declaraciones de variables y funciones

#### Tipos de Nodos del AST

**Declaraciones (DeclK)**
- `VarK`: Declaración de variable
- `FunK`: Declaración de función
- `ParamK`: Parámetro de función

**Sentencias (StmtK)**
- `IfK`: Sentencia condicional
- `WhileK`: Sentencia de iteración
- `AssignK`: Sentencia de asignación
- `ReturnK`: Sentencia de retorno
- `CompoundK`: Sentencia compuesta

**Expresiones (ExpK)**
- `OpK`: Operación binaria
- `ConstK`: Constante numérica
- `IdK`: Identificador
- `CallK`: Llamada a función
- `SubscriptK`: Indexación de arreglo

#### Recuperación de Errores
- **Modo de recuperación**: Evita cascada de errores
- **Sincronización**: En tokens específicos como `;`, `}`, etc.
- **Continuación**: Permite completar el análisis tras encontrar errores

#### Características del Parser
- **Gramática LL(1)**: Parser recursivo descendente
- **Precedencia de operadores**: Implementada en la estructura de la gramática
- **Asociatividad**: Izquierda para operadores aritméticos y relacionales

---

### Apéndice C: Proyecto 3 - Analizador Semántico

#### Descripción General
El analizador semántico verifica la correctitud semántica del programa y construye la tabla de símbolos. Realiza verificación de tipos, alcance de variables, y correctitud de declaraciones y uso de funciones.

#### Funciones Principales

**`semantica(syntaxTree, imprime=True)`**
- **Propósito**: Función principal que coordina el análisis semántico
- **Proceso**: Construye tabla de símbolos, infiere tipos, y verifica tipos
- **Retorna**: `True` si no hay errores, `False` en caso contrario

**`buildSymtab(syntaxTree, imprime=True)`**
- **Propósito**: Construye la tabla de símbolos mediante recorrido del AST
- **Función**: Inserta declaraciones y verifica duplicados
- **Alcance**: Maneja múltiples niveles de alcance

**`typeCheck(syntaxTree)`**
- **Propósito**: Verifica la compatibilidad de tipos en el programa
- **Verificaciones**: Operaciones, asignaciones, llamadas a funciones, retornos

#### Tabla de Símbolos
```python
# Estructura de entrada en la tabla
{
    'name': str,           # Nombre del símbolo
    'type': str,           # Tipo (int, void)
    'lines': [int],        # Líneas donde aparece
    'scope': int,          # Nivel de alcance
    'is_array': bool,      # Si es arreglo
    'array_size': int,     # Tamaño del arreglo
    'params': list,        # Parámetros (para funciones)
    'is_function': bool    # Si es función
}
```

#### Verificaciones Semánticas

**Declaraciones**
- Variables no pueden redeclararse en el mismo alcance
- Funciones no pueden redeclararse
- Función `main` debe estar declarada como `void main(void)`
- Arreglos deben tener tamaño positivo

**Uso de Variables**
- Variables deben estar declaradas antes de su uso
- Variables locales tienen precedencia sobre globales
- Verificación de alcance correcto

**Verificación de Tipos**
- Operadores aritméticos requieren operandos enteros
- Operadores relacionales requieren operandos enteros
- Asignaciones deben ser de tipos compatibles
- Parámetros de funciones deben coincidir en tipo y cantidad

**Llamadas a Funciones**
- Función debe estar declarada
- Número correcto de argumentos
- Tipos de argumentos deben coincidir con parámetros
- Funciones `void` no pueden usarse en expresiones

#### Funciones Predefinidas
```python
# Funciones integradas del lenguaje C-
predefined_functions = {
    'input': {
        'type': 'int',
        'params': [],
        'returns': 'int'
    },
    'output': {
        'type': 'void', 
        'params': [{'type': 'int'}],
        'returns': 'void'
    }
}
```

#### Manejo de Errores
- **Errores semánticos**: Se reportan con número de línea
- **Advertencias**: Para casos ambiguos o potencialmente problemáticos
- **Continuación**: El análisis continúa después de encontrar errores
- **Contexto**: Los errores incluyen información contextual útil

---

### Apéndice D: Definición del Lenguaje C-

#### Gramática BNF del Lenguaje C-

```bnf
program → declaration-list

declaration-list → declaration-list declaration | declaration

declaration → var-declaration | fun-declaration

var-declaration → type-specifier ID ; | type-specifier ID [ NUM ] ;

type-specifier → int | void

fun-declaration → type-specifier ID ( params ) compound-stmt

params → param-list | void

param-list → param-list , param | param

param → type-specifier ID | type-specifier ID [ ]

compound-stmt → { local-declarations statement-list }

local-declarations → local-declarations var-declaration | empty

statement-list → statement-list statement | empty

statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt

expression-stmt → expression ; | ;

selection-stmt → if ( expression ) statement | if ( expression ) statement else statement

iteration-stmt → while ( expression ) statement

return-stmt → return ; | return expression ;

expression → var = expression | simple-expression

var → ID | ID [ expression ]

simple-expression → additive-expression relop additive-expression | additive-expression

relop → <= | < | > | >= | == | !=

additive-expression → additive-expression addop term | term

addop → + | -

term → term mulop factor | factor

mulop → * | /

factor → ( expression ) | var | call | NUM

call → ID ( args )

args → arg-list | empty

arg-list → arg-list , expression | expression
```

#### Tokens del Lenguaje

- **Palabras reservadas**: `if`, `else`, `while`, `return`, `int`, `void`
- **Símbolos especiales**: `+`, `-`, `*`, `/`, `<`, `<=`, `>`, `>=`, `==`, `!=`, `=`, `;`, `,`, `(`, `)`, `[`, `]`, `{`, `}`
- **Otros tokens**: `ID`, `NUM`, comentarios (`/* ... */`)

#### Funciones Predefinidas

- `int input(void)`: Lee un entero del usuario
- `void output(int x)`: Imprime un entero

---

## Conclusiones

El generador de código para el lenguaje C- ha sido implementado exitosamente, proporcionando una traducción completa desde el AST hasta código MIPS ejecutable. El sistema integra todos los componentes desarrollados en proyectos anteriores (analizador léxico, sintáctico y semántico) para crear un compilador funcional.

La arquitectura modular del proyecto permite fácil mantenimiento y extensión de funcionalidades. El uso de MIPS como arquitectura objetivo proporciona un balance adecuado entre simplicidad de implementación y valor educativo.