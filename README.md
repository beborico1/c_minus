# Compilador C- a MIPS

Un compilador completo para el lenguaje C- que genera código ensamblador MIPS, desarrollado como proyecto académico para el curso de Diseño de Compiladores.

## Tabla de Contenidos
- [Descripción](#descripción)
- [Características](#características)
- [Requisitos](#requisitos)
- [Instalación](#instalación)
- [Uso](#uso)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Ejemplos](#ejemplos)
- [Pruebas](#pruebas)
- [Especificación del Lenguaje](#especificación-del-lenguaje)
- [Arquitectura](#arquitectura)
- [Contribuciones](#contribuciones)

## Descripción

Este proyecto implementa un compilador completo para C-, un subconjunto del lenguaje C. El compilador realiza análisis léxico, sintáctico y semántico, construye un Árbol Sintáctico Abstracto (AST) y genera código ensamblador MIPS que puede ejecutarse en simuladores como MARS o QtSpim.

**Curso**: Diseño de Compiladores  
**Profesor**: Dr. Víctor de la Cueva  
**Institución**: Tecnológico de Monterrey

## Características

- **Análisis Léxico**: Tokenización completa del código fuente
- **Análisis Sintáctico**: Parser recursivo descendente con recuperación de errores
- **Análisis Semántico**: Verificación de tipos y manejo de alcances
- **Generación de Código**: Traducción a ensamblador MIPS
- **Tabla de Símbolos**: Manejo de múltiples niveles de alcance
- **Soporte para**:
  - Declaraciones de variables (enteras y arreglos)
  - Funciones con parámetros y valores de retorno
  - Expresiones aritméticas (+, -, *, /)
  - Operadores relacionales (<, <=, >, >=, ==, !=)
  - Estructuras de control (if-else, while)
  - Llamadas recursivas
  - Funciones predefinidas (input/output)

## Requisitos

### Para ejecutar el compilador
- Python 3.x o superior
- Sistema operativo: Windows, macOS o Linux

### Para ejecutar el código generado
- [MARS (MIPS Assembler and Runtime Simulator)](https://github.com/dpetersanderson/MARS) versión 4.5 o superior
- Java Runtime Environment (JRE) para ejecutar MARS

## Instalación

1. Clonar el repositorio:
```bash
git clone https://github.com/[tu-usuario]/compilador-cminus.git
cd compilador-cminus
```

2. Verificar que Python esté instalado:
```bash
python --version
```

3. Descargar MARS desde el [repositorio oficial](https://github.com/dpetersanderson/MARS/releases)

## Uso

### Compilación básica

Para compilar un programa C- usando el script principal:

```bash
python main.py
```

Este comando compilará el archivo `sample.c-` y generará `file.s`.

### Compilación con archivo específico

Para compilar un archivo específico:

```bash
python compile.py nombre_archivo
```

Esto compilará `nombre_archivo.c-` y generará `nombre_archivo.s`.

### Ejecución del código MIPS generado

1. Abrir MARS
2. File → Open → Seleccionar el archivo `.s` generado
3. Run → Assemble (F3)
4. Run → Go (F5)

## Estructura del Proyecto

```
compilador-cminus/
├── globalTypes.py      # Definición de tipos y estructuras globales
├── lexer.py           # Analizador léxico
├── Parser.py          # Analizador sintáctico
├── semantic.py        # Analizador semántico
├── symtab.py          # Tabla de símbolos
├── cgen.py            # Generador de código MIPS
├── main.py            # Script principal
├── compile.py         # Script de compilación con opciones
├── sample.c-          # Programa de ejemplo
└── tests/             # Casos de prueba
    ├── factorial.c-
    ├── test00_simple.c-
    ├── test01_arithmetic.c-
    └── ...
```

## Ejemplos

### Ejemplo 1: Programa simple

**Archivo**: `sample.c-`
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

**Compilación**:
```bash
python main.py
```

**Salida esperada**: El programa imprimirá `30`

### Ejemplo 2: Factorial recursivo

**Archivo**: `factorial.c-`
```c
int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}

void main(void) {
    int x;
    int result;
    
    x = input();
    result = factorial(x);
    output(result);
}
```

## Pruebas

El directorio `tests/` contiene casos de prueba que cubren diferentes aspectos del lenguaje:

- `test00_simple.c-`: Programa básico con funciones
- `test01_arithmetic.c-`: Operaciones aritméticas
- `test02_globals.c-`: Variables globales
- `test03_locals.c-`: Variables locales
- `factorial.c-`: Recursión
- Y muchos más...

Para ejecutar una prueba específica:

```bash
python compile.py tests/test00_simple
```

## Especificación del Lenguaje

### Gramática C-

```
program → declaration-list
declaration-list → declaration { declaration }
declaration → var-declaration | fun-declaration
var-declaration → type-specifier ID ; | type-specifier ID [ NUM ] ;
type-specifier → int | void
fun-declaration → type-specifier ID ( params ) compound-stmt
params → param-list | void
param-list → param { , param }
param → type-specifier ID | type-specifier ID [ ]
compound-stmt → { local-declarations statement-list }
local-declarations → { var-declaration }
statement-list → { statement }
statement → expression-stmt | compound-stmt | selection-stmt 
          | iteration-stmt | return-stmt
expression-stmt → expression ; | ;
selection-stmt → if ( expression ) statement [ else statement ]
iteration-stmt → while ( expression ) statement
return-stmt → return ; | return expression ;
expression → var = expression | simple-expression
var → ID | ID [ expression ]
simple-expression → additive-expression [ relop additive-expression ]
relop → <= | < | > | >= | == | !=
additive-expression → term { addop term }
addop → + | -
term → factor { mulop factor }
mulop → * | /
factor → ( expression ) | var | call | NUM
call → ID ( args )
args → arg-list | ε
arg-list → expression { , expression }
```

### Palabras Reservadas
`else`, `if`, `int`, `return`, `void`, `while`

### Funciones Predefinidas
- `int input(void)`: Lee un entero del usuario
- `void output(int x)`: Imprime un entero seguido de salto de línea

## Arquitectura

### Fases del Compilador

1. **Análisis Léxico** (`lexer.py`)
   - Convierte el flujo de caracteres en tokens
   - Maneja comentarios /* */
   - Detecta errores léxicos

2. **Análisis Sintáctico** (`Parser.py`)
   - Construye el AST mediante análisis recursivo descendente
   - Implementa recuperación de errores
   - Genera estructura de árbol con nodos tipados

3. **Análisis Semántico** (`semantic.py`)
   - Construye la tabla de símbolos
   - Verifica tipos y compatibilidad
   - Valida el uso correcto de variables y funciones

4. **Generación de Código** (`cgen.py`)
   - Traduce el AST a ensamblador MIPS
   - Utiliza convenciones de llamada estándar
   - Maneja registros y memoria eficientemente

### Convenciones de Código MIPS

- **Acumulador**: `$a0`
- **Stack Pointer**: `$sp`
- **Frame Pointer**: `$fp`
- **Return Address**: `$ra`
- **Temporales**: `$t0-$t9`

## Contribuciones

Este es un proyecto académico desarrollado para el curso de Diseño de Compiladores. Para consultas o sugerencias, contactar al equipo de desarrollo.

## Licencia

Proyecto académico - Tecnológico de Monterrey
