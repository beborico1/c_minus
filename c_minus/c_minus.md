# C- (C-minus)
## Un lenguaje para un proyecto de compilador
(Lauden, 2004)

- Es un subconjunto considerablemente restringido de C.
- Contiene:
  - Enteros
  - Arreglos de enteros
  - Funciones (con tipo o void)
  - Declaraciones (estáticas) locales y globales
  - Funciones recursivas (simples)
  - Condicional if-else
  - Ciclo while
  - Función input() que lee desde el teclado
  - Función output() que escribe a la pantalla
- Un programa se compone de una secuencia de declaraciones de variables y funciones.
- Al final debe declararse una función main.
- La ejecución inicia con una llamada a main.

## Léxico de C-

1. Las palabras clave o reservadas del lenguaje son las siguientes:

```
else if int return void while
```

Todas las palabras reservadas o clave están reservadas, y deben ser escritas en minúsculas.

2. Los símbolos especiales son los siguientes:

```
+ - * / < <= > >= == != = ; , ( ) [ ] { } /* */
```

3. Otros tokens son `ID` y `NUM`, definidos mediante las siguientes expresiones regulares:

```
ID = letra letra*
NUM = digito digito*
letra = a|..|z|A|..|Z
digito = 0|..|9
```

Se distingue entre letras minúsculas y mayúsculas.

4. Los espacios en blanco se componen de blancos, retornos de línea y tabulaciones. El espacio en blanco es ignorado, excepto cuando deba separar `ID`, `NUM` y palabras reservadas.

5. Los comentarios están encerrados entre las anotaciones habituales del lenguaje C `/*...*/`. Los comentarios se pueden colocar en cualquier lugar donde pueda aparecer un espacio en blanco (es decir, los comentarios no pueden ser colocados dentro de los token) y pueden incluir más de una línea. Los comentarios no pueden estar anidados.

## Sintaxis de C-

Una gramática BNF para C- es como se describe a continuación:

1. program → declaration-list
2. declaration-list → declaration-list declaration | declaration
3. declaration → var-declaration | fun-declaration
4. var-declaration → type-specifier ID ; | type-specifier ID [ NUM ] ;
5. type-specifier → int | void
6. fun-declaration → type-specifier ID ( params ) compound-stmt
7. params → param-list | void
8. param-list → param-list , param | param
9. param → type-specifier ID | type-specifier ID [ ]
10. compound-stmt → { local-declarations statement-list }
11. local-declarations → local-declarations var-declaration | empty
12. statement-list → statement-list statement | empty
13. statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt
14. expression-stmt → expression ; | ;
15. selection-stmt → if ( expression ) statement | if ( expression ) statement else statement
16. iteration-stmt → while ( expression ) statement
17. return-stmt → return ; | return expression ;
18. expression → var = expression | simple-expression
19. var → ID | ID [ expression ]
20. simple-expression → additive-expression relop additive-expression | additive-expression
21. relop → <= | < | > | >= | == | !=
22. additive-expression → additive-expression addop term | term
23. addop → + | -
24. term → term mulop factor | factor
25. mulop → * | /
26. factor → ( expression ) | var | call | NUM
27. call → ID ( args )
28. args → arg-list | empty
29. arg-list → arg-list , expression | expression

## Semántica de C-

1. program → declaration-list
2. declaration-list → declaration-list declaration | declaration
3. declaration → var-declaration | fun-declaration

Un programa (program) se compone de una lista (o secuencia) de declaraciones (declaration-list), las cuales pueden ser declaraciones de variable o función, en cualquier orden. Debe haber al menos una declaración. Las restricciones semánticas son como sigue (éstas no se presentan en C). Todas las variables y funciones deben ser declaradas antes de utilizarlas (esto evita las referencias de retroajuste). La última declaración en un programa debe ser una declaración de función con el nombre main. Advierta que C- carece de prototipos, de manera que no se hace una distinción entre declaraciones y definiciones (como en el lenguaje C).

4. var-declaration → type-specifier ID ; | type-specifier ID [ NUM ] ;
5. type-specifier → int | void

Una declaración de variable declara una variable simple de tipo entero o una variable de arreglo cuyo tipo base es entero, y cuyos índices abarcan desde 0...NUM-1. Observe que en C- los únicos tipos básicos son entero y vacío ("void"). En una declaración de variable sólo se puede utilizar el especificador de tipo int. Void es para declaraciones de función (véase más adelante). Advierta también que sólo se puede declarar una variable por cada declaración.

6. fun-declaration → type-specifier ID ( params ) compound-stmt
7. params → param-list | void
8. param-list → param-list , param | param
9. param → type-specifier ID | type-specifier ID [ ]

Una declaración de función consta de un especificador de tipo (type-specifier) de retorno, un identificador y una lista de parámetros separados por comas dentro de paréntesis, seguida por una sentencia compuesta con el código para la función. Si el tipo de retorno de la función es void, entonces la función no devuelve valor alguno (es decir, es un procedimiento). Los parámetros de una función pueden ser void (es decir, sin parámetros) o una lista que representa los parámetros de la función. Los parámetros seguidos por corchetes son parámetros de arreglo cuyo tamaño puede variar. Los parámetros enteros simples son pasados por valor. Los parámetros de arreglo son pasados por referencia (es decir, como apuntadores) y deben ser igualados mediante una variable de arreglo durante una llamada. Advierta que no hay parámetros de tipo "función". Los parámetros de una función tienen un ámbito igual a la sentencia compuesta de la declaración de función, y cada invocación de una función tiene un conjunto separado de parámetros. Las funciones pueden ser recursivas (hasta el punto en que la declaración antes del uso lo permita).

10. compound-stmt → { local-declarations statement-list }

Una sentencia compuesta se compone de llaves que encierran un conjunto de declaraciones y sentencias. Una sentencia compuesta se realiza al ejecutar la secuencia de sentencias en el orden dado. Las declaraciones locales tienen un ámbito igual al de la lista de sentencias de la sentencia compuesta y reemplazan cualquier declaración global.

11. local-declarations → local-declarations var-declaration | empty
12. statement-list → statement-list statement | empty

Advierta que tanto la lista de declaraciones como la lista de sentencias pueden estar vacías. (El no terminal empty representa la cadena vacía, que se describe en ocasiones como ε.)

13. statement → expression-stmt | compound-stmt | selection-stmt | iteration-stmt | return-stmt
14. expression-stmt → expression ; | ;

Una sentencia de expresión tiene una expresión opcional seguida por un signo de punto y coma. Tales expresiones por lo regular son evaluadas por sus efectos colaterales. Por consiguiente, esta sentencia se utiliza para asignaciones y llamadas de función.

15. selection-stmt → if ( expression ) statement | if ( expression ) statement else statement

La sentencia if tiene la semántica habitual: la expresión es evaluada; un valor distinto de cero provoca la ejecución de la primera sentencia; un valor de cero ocasiona la ejecución de la segunda sentencia, si es que existe. Esta regla produce la ambigüedad clásica del else ambiguo, la cual se resuelve de la manera estándar: la parte else siempre se analiza sintácticamente de manera inmediata como una subestructura del if actual (la regla de eliminación de ambigüedad "de anidación más cercana").

16. iteration-stmt → while ( expression ) statement

La sentencia while es la única sentencia de iteración en el lenguaje C-. Se ejecuta al evaluar de manera repetida la expresión y al ejecutar entonces la sentencia si la expresión evalúa un valor distinto de cero, finalizando cuando la expresión se evalúa a 0.

17. return-stmt → return ; | return expression ;

Una sentencia de retorno puede o no devolver un valor. Las funciones no declaradas como void deben devolver valores. Las funciones declaradas void no deben devolver valores. Un retorno provoca la transferencia del control de regreso al elemento que llama (o la terminación del programa si está dentro de main).

18. expression → var = expression | simple-expression
19. var → ID | ID [ expression ]

Una expresión es una referencia de variable seguida por un símbolo de asignación (signo de igualdad) y una expresión, o solamente una expresión simple. La asignación tiene la semántica de almacenamiento habitual: se encuentra la localidad de la variable representada por var, luego se evalúa la subexpresión a la derecha de la asignación, y se almacena el valor de la subexpresión en la localidad dada. Este valor también es devuelto como el valor de la expresión completa. Una var es una variable (entera) simple o bien una variable de arreglo subindizada. Un subíndice negativo provoca que el programa se detenga (a diferencia de C). Sin embargo, no se verifican los límites superiores de los subíndices.

20. simple-expression → additive-expression relop additive-expression | additive-expression
21. relop → <= | < | > | >= | == | !=

Una expresión simple se compone de operadores relacionales que no se asocian (es decir, una expresión sin paréntesis puede tener solamente un operador relacional). El valor de una expresión simple es el valor de su expresión aditiva si no contiene operadores relacionales, o bien, 1 si el operador relacional se evalúa como verdadero, o 0 si se evalúa como falso.

22. additive-expression → additive-expression addop term | term
23. addop → + | -
24. term → term mulop factor | factor
25. mulop → * | /

Los términos y expresiones aditivas representan la asociatividad y precedencia típicas de los operadores aritméticos. El símbolo / representa la división entera; es decir, cualquier residuo es truncado.

26. factor → ( expression ) | var | call | NUM

Un factor es una expresión encerrada entre paréntesis, una variable, que evalúa el valor de su variable; una llamada de una función, que evalúa el valor devuelto de la función; o un NUM, cuyo valor es calculado por el analizador léxico. Una variable de arreglo debe estar subindizada, excepto en el caso de una expresión compuesta por una ID simple y empleada en una llamada de función con un parámetro de arreglo (véase a continuación).

27. call → ID ( args )
28. args → arg-list | empty
29. arg-list → arg-list , expression | expression

Una llamada de función consta de un ID (el nombre de la función), seguido por sus argumentos encerrados entre paréntesis. Los argumentos pueden estar vacíos o estar compuestos por una lista de expresiones separadas mediante comas, que representan los valores que se asignarán a los parámetros durante una llamada. Las funciones deben ser declaradas antes de llamarlas, y el número de parámetros en una declaración debe ser igual al número de argumentos en una llamada. Un parámetro de arreglo en una declaración de función debe coincidir con una expresión compuesta de un identificador simple que representa una variable de arreglo.

Finalmente, las reglas anteriores no proporcionan sentencia de entrada o salida. Debemos incluir tales funciones en la definición de C-, puesto que a diferencia del lenguaje C, C- no tiene facilidades de ligado o compilación por separado. Por lo tanto, consideraremos dos funciones por ser predefinidas en el ambiente global, como si tuvieran las declaraciones indicadas:

```c
int input(void) { ... }
void output(int x) { ... }
```

La función input no tiene parámetros y devuelve un valor entero desde el dispositivo de entrada estándar (por lo regular el teclado). La función output toma un parámetro entero, cuyo valor imprime a la salida estándar (por lo regular la pantalla), junto con un retorno de línea.

## Ejemplos de programas en C-

El siguiente es un programa que introduce dos enteros, calcula su máximo común divisor y lo imprime:

```c
/* Un programa para realizar el algoritmo
   de Euclides para calcular mcd. */

int gcd (int u, int v)
{ if (v == 0) return u ;
  else return gcd(v,u-u/v*v);
  /* u-u/v*v == u mod v */
}

void main(void)
{ int x; int y;
  x = input(); y = input();
  output(gcd(x,y));
}
```

A continuación tenemos un programa que introduce una lista de 10 enteros, los clasifica por orden de selección, y los exhibe otra vez:

```c
/* Un programa para realizar ordenación por
   selección en un arreglo de 10 elementos. */

int x[10];

int minloc ( int a[], int low, int high )
{ int i; int x; int k;
  k = low;
  x = a[low];
  i = low + 1;
  while (i < high)
    { if (a[i] < x)
        { x = a[i];
          k = i; }
      i = i + 1;
    }
  return k;
}

void sort( int a[], int low, int high)
{ int i; int k;
  i = low;
  while (i < high-1)
    { int t;
      k = minloc(a,i,high);
      t = a[k];
      a[k] = a[i];
      a[i] = t;
      i = i + 1;
    }
}

void main(void)
{ int i;
  i = 0;
  while (i < 10)
    { x[i] = input();
      i = i + 1; }
  sort(x,0,10);
  i = 0;
  while (i < 10)
    { output(x[i]);
      i = i + 1; }
}
```
