# Analizador Semántico
## Análisis Semántico

- Es la fase del compilador que calcula la información adicional necesaria (para la compilación) una vez que se conoce la estructura sintáctica de un programa.
- Involucra el cálculo de información que rebasa las capacidades de las FCG.
- Como el análisis que realiza un compilador es estático por definición (tiene lugar antes de la ejecución), dicho análisis semántico también se conoce como Análisis Semántico Estático (ASE).

## ¿Qué verifica?

Dependiendo del lenguaje de programación de que se trate puede verificar cosas como:

- Que todos los identificadores estén declarados
- Tipos
- Que las relaciones de herencia tengan sentido
- Que las clases sólo sean definidas una vez
- Que las variables sólo estén declaradas una vez en el mismo scope
- Que los métodos en las clases sean definidos sólo una vez
- Que los identificadores reservados no estén mal usados
- Y muchos otros...

## ¿Qué involucra?

En un lenguaje típico estáticamente tipado (e.g. C), el análisis semántico involucra:

- La construcción de una tabla de símbolos (ST, por sus siglas en inglés) para mantenerse al tanto de los significados de nombres establecidos en declaraciones, e
- Inferir tipos y verificarlos en expresiones y sentencias con el fin de determinar su exactitud dentro de las reglas de tipos del lenguaje.

## División

El Análisis Semántico se puede dividir en dos categorías:

- El análisis de un programa que requiere las reglas del lenguaje de programación para establecer su exactitud y garantizar una ejecución adecuada.
  - E.g. verificación de tipos estáticos
- El análisis realizado por un compilador para mejorar la eficiencia de ejecución del programa traducido
  - Por lo general se incluye en el análisis de optimización o técnicas de mejoramiento de código
  - Las dos categorías no son mutuamente excluyentes.

## Herramientas

El ASE involucra tanto la descripción de los análisis a realizar como la implementación de los análisis utilizando los algoritmos adecuados.

- Es similar al léxico (RE y FA) o sintaxis (FCG y Gradiente descendente o LL(1))
- En ASE la situación no es tan clara:
  - En parte porque no hay un método estándar que permita especificar la semántica estática de un lenguaje, y
  - En parte porque la cantidad y categoría del ASE varía demasiado de un lenguaje a otro

## Un método muy usado

Un método para describir el análisis semántico que los escritores de compiladores usan muy a menudo con buenos efectos, es la identificación de atributos, o propiedades, de entidades del lenguaje que deben calcularse, y escribir ecuaciones de atributos o reglas semánticas, que expresan la forma en la que el cálculo de tales atributos está relacionado con las reglas gramaticales del lenguaje.

Un conjunto así de atributos y ecuaciones se denomina gramática con atributos (GCA).

- Las GCA son más útiles para los lenguajes que obedecen al principio de la semántica dirigida por la sintaxis

## Semántica dirigida por sintaxis

- Asegura que el contenido semántico de un programa se encuentra estrechamente relacionado con su sintaxis.
- Todos los lenguajes modernos tienen esta propiedad.
- Desafortunadamente, el escritor de compiladores casi siempre debe construir una GCA a mano, a partir del manual del lenguaje, ya que rara vez es proporcionada por el diseñador del lenguaje.

## Gramática con atributos

En la Gramática Dirigida por Sintaxis, los atributos están directamente asociados con los símbolos gramaticales del lenguaje (terminales y no terminales).

Si X es un símbolo gramatical y a es un atributo de X, entonces escribimos X.a para el valor de a asociado con X.

Una forma típica de implementar cálculos de atributo es colocar valores de atributo (o miembros de una struct) en los nodos de un AST utilizando campos de registro.

Cada relación de atributos de la forma:

X → X₁ X₂ ... Xₙ

(si el mismo símbolo X₁ aparece más de una vez en una regla, entonces cada aparición debe distinguirse con una subindización adecuada) está especificada por una ecuación de atributo o regla semántica de la forma:

Xₖ.aᵢ = fₖᵢ(X₀.a₁, ..., X₀.aₙ, X₁.a₁, ..., X₁.aₙ ... Xₙ.a₁, ..., Xₙ.aₙ)

donde fₖᵢ es una función matemática.

## Forma de gramática con atributos

Por lo general las gramáticas con atributo se escriben en forma tabular, con cada regla gramatical enumerada con el conjunto de valores de atributo, o reglas semánticas asociadas con esa regla (o producción).

## Ejemplo 1: número con un dígito

Consideremos la siguiente gramática simple para números sin signo:

- número → número dígito | dígito
- dígito → 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9

El atributo más importante de un número es su valor al que nos podemos referir con el nombre val.

Si un número contiene un solo dígito, se deriva de la regla:

- número → dígito

y su valor está determinado con la ecuación de atributo:

- número.val = dígito.val

## Ejemplo 2: número con varios dígitos

Si un número contiene varios dígitos, se deriva de la producción:
- número → número dígito

Y debemos expresar el valor del símbolo del lado izquierdo de la producción en función de los valores de los símbolos del lado derecho.

Vea que las dos ocurrencias del no terminal número deben distinguirse porque sus valores no son iguales, por lo que reescribimos la regla gramatical como:

- número₁ → número₂ dígito

Debido a que los dígitos tienen un valor referente a su posición, la ecuación del atributo valor queda así:

- número₁.val → número₂.val * 10 + dígito.val

## Gramática para val

Una gramática con atributos completa para el atributo val es:

1. número → dígito
   - número.val = dígito.val
2. número₁ → número₂ dígito
   - número₁.val = número₂.val * 10 + dígito.val
3. dígito → 0
   - dígito.val = 0
4. dígito → 1
   - dígito.val = 1
   
...y así para todos los dígitos...

## Significado de las ecuaciones

El significado de las ecuaciones de atributo para una cadena particular puede visualizarse utilizando el árbol de análisis gramatical para la cadena.

## Ejemplo 3: gramática para expresiones

Considere la gramática para expresiones aritméticas simples:

```
expr → expr + term | expr - term | term
term → term * factor | term / factor | factor
factor → ( expr ) | numero | id
```

Y su gramática con atributos:

```
expr → expr₁ + term
  expr.val = expr₁.val + term.val
expr → expr₁ - term
  expr.val = expr₁.val - term.val
expr → term
  expr.val = term.val
...
```

NOTA: de la misma forma se deben escribir ecuaciones para todos los atributos como: tipo, base (binaria, octal, hexadecimal o decimal), etc.

## Algoritmos de implementación

Los algoritmos para la implementación del análisis semántico tampoco son claramente expresables (como los algoritmos de análisis sintáctico).

De nuevo, esto se debe a los mismos problemas respecto a la especificación del análisis semántico.

Si el ASE se puede suspender hasta que todo el análisis sintáctico (y la construcción de un AST) esté completo, entonces la tarea de implementar el ASE se vuelve considerablemente más fácil.

## ASE después del AST

Consiste, en esencia, en la especificación de orden para un recorrido del AST, junto con los cálculos a realizar cada vez que se encuentra un nodo en el recorrido.

Esto implica que el compilador debe ser de pasos múltiples.

Afortunadamente, la práctica moderna permite cada vez más al escritor de compiladores utilizar pasos múltiples para simplificar los procesos de ASE y Generación de Código (CG).

## Funciones principales del ASE

Las dos áreas principales del ASE son:
- Tabla de símbolos
- Verificación de tipos

NOTA: No existe alguna herramienta de amplio uso para generar en forma automática los ASE.

# VERIFICACIÓN DE TIPOS (TYPE CHECKING)

## Formalismo apropiado

El formalismo apropiado en la verificación de tipos son las reglas lógicas de inferencia (logical rules of inference):

- Tiene la forma:
  - if hipótesis == true, then conclusión == true
- La verificación de tipos se hace vía razonamiento:
  - if E1 y E2 tienen cierto tipo, then E3 tiene cierto tipo
- Las reglas de inferencia son una notación compacta para estatutos if-then
  - Son estatutos de implicación donde alguna hipótesis implica alguna conclusión

## Notación

- Su notación es fácil de leer con la práctica.
- Inicia con un sistema simplificado y gradualmente le agrega características.
- Building blocks:
  - El símbolo ∧ es "and"
  - El símbolo ⇒ es "if-then"
  - x:T significa "x tiene el tipo T"

## Formato

Una regla de inferencia se escribe así:
- Hipótesis₁ ∧ ... ∧ Hipótesisₙ ⇒ Conclusión

Por tradición, estas reglas se escriben como:

⊢Hipótesis₁ ...⊢Hipótesisₙ  
⊢Conclusión

Donde ⊢ se lee, "se puede probar que..."

Significa, si se puede probar que la hipótesis 1 es verdadera y que, así sucesivamente, hasta la hipótesis n es verdadera, entonces se puede probar que la conclusión es verdadera.

Las reglas de tipo de los lenguajes tienen hipótesis y una conclusión del tipo ⊢ e:T

## Reglas simples de tipos

Para una constante entera:
```
⊢n:Int [Int]
```

Para la suma:
```
⊢e₁:Int ⊢e₂:Int
⊢e₁+e₂:Int [Add]
```

Estas reglas son como templates que describen cómo tipar (poner tipos) enteros y expresiones de suma.

Llenando los templates podemos producir un tipado completo para las expresiones.

## Condición de corrección (correctness)

Una propiedad importante de cualquier sistema de tipos es que debe ser sano (sound).

Un sistema de tipos es sound si:
- Siempre que ⊢ e:T
- Entonces e se evalúa a un valor de tipo T

Sólo queremos reglas que sean sound.
- Pero algunas reglas sound son mejores que otras.

## AST y las pruebas

La verificación de tipos prueba hechos e:T
- La prueba está en la estructura del AST
- La prueba tiene la misma estructura que el AST
- Se usa una regla de tipo por cada nodo del AST

En la regla de tipo usada para el nodo e:
- Las hipótesis son las pruebas de los tipos de las subexpresiones de e
- La conclusión es el tipo de e

Los tipos son calculados en una pasada bottom-up (posorden) del AST.

Hay una correspondencia directa entre la estructura de una prueba y la forma del AST.

## Regla para una variable

Hasta ahora podemos definir de una forma muy directa, reglas de tipos razonables para cualquier constructor.

Pero se presenta un problema: ¿cuál es el tipo de una referencia a una variable?

```
⊢x:? [Var]
```

La regla no tiene suficiente información para dar el tipo de x.

La solución es simple:
- ¡Poner más información en la regla!

## Ambientes de tipos (type environments)

Un type environment proporciona los tipos para las variables libres (free variables).
- Un type environmente es una función de identificadores (nombres de variables) a tipos

Una variable es libre en una expresión si no está definida dentro de la expresión.

## Función id → tipos

Sea Γ una función de identificadores a tipos:
- La sentencia Γ ⊢ e:T se lee:
  - Bajo la asunción de que las variables libres tienen los tipos dados por Γ, se puede probar que la expresión e tiene tipo T
- Es decir, si me dices el tipo de las variables libres en una expresión, te puedo decir el tipo de la expresión

A Γ se les conoce como ambiente de tipos.

## Γ como el ambiente

Si la expresión e tiene variables libres, tenemos que ver la función Γ para que nos dé su tipo.

Ahora nuestro problema con las variables libres se convierte en un problema sencillo y podemos escribir nuevas reglas:

```
Γ x:T
Γ⊢x:T [Var]
```

Para saber el tipo de x simplemente lo veo en mi ambiente de objetos.

## Instrucción let

Podemos tener ahora una regla para la instrucción let:

```
Γ ⊢e₁:T₁
Γ[T₁|x] ⊢e₂:T₂
Γ⊢let x:T₁ in e₂:T₂
```

Γ[T|x] es la función Γ modificada en el único punto x para regresar T:
- Γ[T|x](x) = T al aplicarle x a la función regresa T
- Γ[T|x](y) = Γ(y) ya tenía definida a y

Se puede observar que Γ se implementa con una ST.

## ¿Cómo se implementa?

La función Γ se implementa como la tabla de símbolos:
- Una o varias dependiendo de los bloques
- Una tabla por cada bloque.
- Si son varias se requerirá una pila de tablas de símbolos

Tendremos una función recursiva llamada typecheck que toma dos argumentos:
- Un type environment (ST) y una expresión

El código se verá muy parecido a la lectura de la regla trasladada a código y esa es una de las principales ventajas de la notación de los type systems.

## Ejemplo función typecheck

```
Typecheck(environment, e1+e2) {
    T1 = typecheck(environment, e1);
    T2 = typecheck(environment, e2);
    check T1 == T2 == Int;
    return Int; 
}

Typecheck(environment, let x:T ¬ e0 in e1) {
    T0 = typecheck(environment, e0);
    T1 = typecheck(environment.add(x:T), e1);
    check subtype(T0, T1);
    return T1; 
}
```

## Recomendación en la implementación

Recorre el árbol en posorden (de abajo hacia arriba), iniciando en la raíz.

Verifica qué tipo de nodo estás analizando:
- Dependiendo del nodo, llama a la función typecheck o verifícalo directamente en el código usando la tabla de símbolos (o el stack de la tabla de símbolos), para cada uno de sus hijos.
- Asigna el tipo encontrado al nodo analizado.

## En resumen

- El ambiente de tipos proporciona los tipos para las variables libres.
- El ambiente de tipos se pasa como parámetro al ASE.
- El ambiente de tipos (tabla de símbolos) se calcula a partir del AST de la raíz hacia las hojas (preorden)
- Los tipos son calculados en el AST de las hojas a la raíz (posorden).

# Tabla de símbolos

## Tabla de símbolos (ST, por sus siglas en inglés)

- Es común hacer que el parser de un compilador construya y mantenga la tabla de símbolos, aunque muchas veces es más simple si se hace en el analizador semántico.
- La tabla de símbolos almacena información acerca de los tokens del programa fuente, principalmente de los identificadores.
- La tabla de símbolos es un componente fundamental en la interface entre el análisis semántico y sintáctico.

## ST como una estructura de datos

- Mantener una ST bien organizada es una de las tareas más importantes de un compilador.
- Conforme un compilador traduce programa fuente, debe ser capaz de colocar nueva información o actualizar la existente en la ST en forma eficiente.
- El enfoque es:
  - Crear el diseño conceptual de una ST.
  - Desarrollar una implementación en un lenguaje de programación que represente el diseño.

## Información en la ST

- Durante el proceso de traducción, el compilador crea y actualiza entradas en la ST para que guarde información importante de ciertos tokens del programa fuente.
- Cada entrada tiene un nombre, el cual es el string del token.
  - La entrada también contiene otra información acerca del identificador.
  - A medida que se traduce el programa fuente, el compilador busca y actualiza dicha información.

## Operaciones básicas de la ST

¿Qué información debe contener la ST?
- Cualquier información que sea útil

Por ejemplo, una entrada de la ST para un identificador contiene típicamente:
- Su tipo
- Estructura
- Y cómo está definido

Sin importar cuál información se guarda en la ST, las operaciones básicas que debe soportar son:
- Introducir nueva información (altas)
- Buscar información existente (consultas)
- Actualizar información existente (actualizaciones)

## Bloques en los lenguajes

La mayor parte de los lenguajes modernos están formados por módulos:
- {...}
- begin ... end
- Funciones, procedimientos, métodos, etc.
- Tipos: estructuras, registros, etc.
- Clases

Cada bloque:
- Tiene declarados variables, constantes, otros bloques, etc.
- Define un alcance (scope) local para los identificadores.

## ST: bloques, declaraciones y AST

En el AST:
- Los nodos que inician un bloque están bien definidos (function-return, program-end, {...}, begin-end, class, etc.).
- Los nodos que inician declaraciones también (var, int, float, type, lista de parámetros, etc.)
- Si no hay parte declarativa, cada vez que se encuentre un identificador se considera que se está declarando (revisar reglas del lenguaje)

Cada vez que se encuentre un bloque:
- Se debe crear una nueva ST (local), a la que se le deberán agregar los identificadores que se encuentren dentro del bloque, si es que estos están declarados ahí.
- Se insertarán TODOS los elementos que estén declarados en dicho bloque.

## El stack de STs

Si un lenguaje está compuesto de sólo una secuencia de instrucciones (statements o estatutos, e.g. Basic, Fortran o TINY), bastará sólo una ST.

Si el programa es estructurado en bloques (e.g. Pascal, C, C++, Java o C-), se requerirán múltiples STs:
- Una ST global, para el programa principal
- Una ST local, para cada procedimiento, función, estructura o clase.

Debido a que estas estructuras pueden estar anidadas, se requerirá un STACK de ST:
- La ST en el top contendrá información sobre el programa o función que se esté parsenado en ese momento.

## Una entrada de la ST

Cada entrada de la ST contiene información acerca de un token:
- Típicamente un identificador
  - Nombre de la entrada
  - Información del token en forma de atributos

Una ST busca las entradas usando los nombres como claves de búsqueda.

## Diseño conceptual y estructura de datos (DS)

Del diseño conceptual sólo se debe entender:
- Cuáles son los principales componente de una ST
- Cuáles son sus roles
- Cómo se relacionan unos con otros

Es importante entender los conceptos anteriores para decidir cuál es la mejor estructura de datos (DS) que se puede utilizar en su implementación.

## Generalización de la ST

Aún y cuando haya sólo una ST en el programa, es conveniente implementarla como un stack con las siguientes operaciones:
- Enter: introduce una nueva entrada en la ST local, la cual se encuentra en el top del stack
- Local look up: buscar una entrada sólo en la tabla local
- Global look up: buscar una entrada en todas las ST del stack

Una vez que la entrada ha sido encontrada se puede actualizar (update) su contenido.

## Ejercicio

Usando el AST entregado por su parser haga una función que, cada vez que se encuentre un identificador, le agrega a su ST global, su número de línea.
- Por el momento no importa si el identificador aparece dentro de una función (en cuyo caso se tendría que crear una nueva ST local)

Al final, imprimir la ST global creada.

Ejemplo:
```
Identificador Números de línea
abc          31 33
epsilon      4 33
newton       7 14 16 17 19
```

## Comentario sobre la creación de la ST

Es posible crear las ST desde el léxico y el parseo.
- Es más simple si se hace después, es decir, en al AST.

Si alguien quiere modificar su léxico o parser para ir creando la ST lo puede hacer.

# Ejemplo de creación de tabla de símbolos y chequeo de tipos

El documento presenta un ejemplo detallado de cómo se construye una tabla de símbolos y se realiza el chequeo de tipos para un programa que encuentra el mínimo de un arreglo. El proceso muestra paso a paso cómo:

1. Se inicializa el scope (ámbito)
2. Se agregan símbolos a la tabla (variables, funciones)
3. Se manejan diferentes scopes para funciones
4. Se buscan símbolos en los scopes apropiados
5. Se realizan verificaciones de tipos
6. Se cierran los scopes al terminar bloques

El ejemplo muestra los estados de la tabla de símbolos en cada paso del análisis semántico, mostrando cómo:
- Se crea la tabla de símbolos para el scope global
- Se crean tablas de símbolos para funciones (scope local)
- Se gestionan las relaciones entre scopes anidados
- Se buscan identificadores desde el scope actual hacia el exterior

## Referencias

- A.V. Aho, M. S. Lam, R. Sethi, and J. D. Ullman. Compilers: Principles, Techniques, and Tools. 2nd Pearson (2012).
- K.C. Louden. Contrucción de Compiladores: principios y práctica. Thomson (2004).
- Alex Aiken. Compilers. Stanford Online (2018).
  - https://lagunita.stanford.edu/courses/Engineering/Compilers/Fall2014/about
- R. Mak,. Writing Compilers and Interpreters: A Software Engineering Aproach. 3rd ed, Wiley (2009).
- Alan G. Labouseur. http://labouseur.com/courses/compilers/AST-and-Symbol-Table.pdf. (consultado el 24-oct-2018)