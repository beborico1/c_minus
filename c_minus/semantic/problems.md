# Problemas

## Programa 1 (sample.c-) errores 

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

Sí, los errores semánticos que se reportaron corresponden a este código. Analicemos estos errores y luego proveeré un código de C- corregido que pasaría el análisis semántico.

## Análisis de los errores reportados

1. **Operador 'EQ' aplicado a tipos no válidos (línea 5)**:
   En la línea `if (v == 0) return u;`, el analizador semántico espera que la comparación de igualdad sea entre tipos booleanos, pero está comparando un entero (`v`) con otro entero (`0`). Esto es un problema de la implementación del analizador semántico, no del código.

2. **Expresión de retorno debe ser de tipo entero (línea 5)**:
   En la línea `return u;`, el analizador está esperando que el valor retornado sea específicamente de tipo entero, pero está recibiendo un valor que tal vez no ha sido correctamente tipado.

3. **Operadores 'DIVIDE', 'TIMES', 'MINUS' aplicados a tipos no válidos (línea 6)**:
   En la expresión `u-u/v*v`, hay varios operadores aritméticos que el analizador espera que operen sobre tipos enteros, pero parece que no está reconociendo algunas variables como enteros.

4. **La condición del if debe ser booleana (línea 5)**:
   Relacionado con el primer error, el analizador espera que la condición del `if` sea un booleano, pero en C, las comparaciones como `v == 0` devuelven valores enteros (0 para falso, no-0 para verdadero).

5. **Errores en tipos de argumentos para funciones (líneas 6 y 13)**:
   Los argumentos pasados a `gcd` y a `output` no coinciden con los tipos esperados. Esto podría deberse a cómo se está interpretando el tipo de los parámetros.

## Razones de los errores

Estos errores parecen ser principalmente debido a:

1. **Diferencias en la semántica de tipos entre C- y la implementación del analizador**: Por ejemplo, en C, una comparación de igualdad devuelve un entero (0 para falso, 1 para verdadero), pero el analizador espera un tipo booleano explícito.

2. **Propagación de tipos**: Los tipos de algunas expresiones no están siendo correctamente propagados, causando que el análisis de tipos falle en expresiones complejas.

## Código corregido de C- que pasaría el análisis semántico

Aquí hay una versión modificada de tu código que probablemente pasaría el análisis semántico:

```c
/* Un programa para realizar el algoritmo
   de Euclides para calcular mcd. */

int gcd (int u, int v)
{ 
  if (v < 1) /* Usando < en vez de == para generar un booleano */
    return u;
  else {
    int temp;
    temp = u - (u/v)*v; /* Calculando el módulo de manera más explícita */
    return gcd(v, temp);
  }
}

void main(void)
{ 
  int x; 
  int y;
  x = input(); 
  y = input();
  output(gcd(x,y));
}
```

Las principales modificaciones son:

1. Cambiar la comparación `v == 0` a `v < 1` para generar un tipo booleano según lo esperado por el analizador.
2. Descomponer la expresión compleja `u-u/v*v` en pasos más simples usando una variable temporal.
3. Reorganizar el código para evitar expresiones anidadas complejas que pueden causar problemas con la propagación de tipos.

## Nota importante

Es relevante mencionar que el código original en C es perfectamente válido. Los errores que estás viendo son probablemente debido a limitaciones o características específicas de la implementación del analizador semántico, no a problemas reales en el código C-.

En un compilador de C completo y bien implementado, tu código original no debería generar estos errores semánticos. La implementación del analizador semántico puede tener reglas más estrictas o diferentes de lo que es común en C.

¿Te gustaría que explore más a fondo alguna de estas discrepancias o que te explique cómo podría mejorarse el analizador semántico para manejar correctamente el código original?

Analizando semántica...

Tabla de símbolos:
================================================================================
Ámbito  Nombre         Tipo      Líneas              Atributos                     
--------------------------------------------------------------------------------
0       gcd            int       4                   {'params': [<Parser.TreeNode object at 0x10665bf40>, <Parser.TreeNode object at 0x10668b250>]}
0       input          int       0                   {'params': []}                
0       main           void      10                  {'params': []}                
0       output         void      0                   {'params': [{'name': 'x', 'type': 'int', 'is_array': False}]}
1       u              int       4                   {'is_array': False}           
1       v              int       4                   {'is_array': False}           
2       x              int       11                  {'is_array': False, 'size': None}
2       y              int       11                  {'is_array': False, 'size': None}
================================================================================

Realizando verificación de tipos...
>>> Error semántico en línea 5: Operador 'EQ' aplicado a tipos no válidos
>>> Error semántico en línea 5: Expresión de retorno debe ser de tipo entero
>>> Error semántico en línea 6: Operador 'DIVIDE' aplicado a tipos no válidos
>>> Error semántico en línea 6: Operador 'TIMES' aplicado a tipos no válidos
>>> Error semántico en línea 6: Operador 'MINUS' aplicado a tipos no válidos
>>> Error semántico en línea 6: Tipo de argumento 1 no coincide con el parámetro de la función
>>> Error semántico en línea 5: La condición del if debe ser booleana
>>> Error semántico en línea 13: Tipo de argumento 1 no coincide con el parámetro de la función
>>> Error semántico en línea 13: Tipo de argumento 2 no coincide con el parámetro de la función

Se encontraron errores en la verificación de tipos.

## Programa 2 (sample2.c-) errores 

/* Un programa para realizar el algoritmo
   de Euclides para calcular mcd. */

int gcd (int u, int v)
{ 
  if (v < 1)
    return u;
  else {
    int temp;
    temp = u - (u/v)*v;
    return gcd(v, temp);
  }
}

void main(void)
{ 
  int x; 
  int y;
  x = input(); 
  y = input();
  output(gcd(x,y));
}

Veo que probaste el código corregido, y aunque la sintaxis ha sido analizada correctamente y la tabla de símbolos se construyó correctamente, sigues obteniendo errores semánticos similares a los que tenías con el código original.

Esto confirma que estos errores no son problemas con tu código C-, sino limitaciones o características específicas de la implementación del analizador semántico. Vamos a analizar por qué estos errores persisten:

## Análisis de los errores persistentes

1. **Operador 'LT' aplicado a tipos no válidos**: 
   ```
   >>> Error semántico en línea 6: Operador 'LT' aplicado a tipos no válidos
   ```
   A pesar de cambiar `==` por `<`, el analizador sigue reportando error porque espera que los operandos de comparación tengan algún tipo específico (quizás booleano), pero está recibiendo enteros.

2. **Errores de tipo de expresiones**:
   ```
   >>> Error semántico en línea 7: Expresión de retorno debe ser de tipo entero
   >>> Error semántico en línea 10: Operador 'DIVIDE'/'TIMES'/'MINUS' aplicado a tipos no válidos
   ```
   Estos errores sugieren que hay un problema fundamental en cómo el analizador semántico está infiriendo y propagando los tipos en las expresiones.

3. **Errores de tipo de argumento de función**:
   ```
   >>> Error semántico en línea 11: Tipo de argumento 1/2 no coincide con el parámetro de la función
   >>> Error semántico en línea 21: Tipo de argumento 1/2 no coincide con el parámetro de la función
   ```
   Estos errores indican que el analizador no está reconociendo correctamente los tipos de los argumentos pasados a las funciones.

## Problemas fundamentales del analizador semántico

El analizador semántico parece tener varias limitaciones importantes:

1. **Propagación de tipos incorrecta**: Puede que el analizador no esté propagando correctamente los tipos de las expresiones, lo que lleva a que muchas expresiones tengan tipos "desconocidos" o "inválidos".

2. **Reglas de tipo demasiado estrictas**: Las reglas de tipo parecen ser más estrictas o diferentes de lo que es común en C. Por ejemplo, puede estar esperando que las condiciones de `if` sean explícitamente booleanas, cuando en C cualquier expresión entera puede usarse como condición.

3. **Manejo incorrecto de funciones y parámetros**: Parece haber problemas en cómo se verifican los tipos de los argumentos en las llamadas a función.

## Posibles soluciones a nivel del analizador

Para hacer que el analizador acepte programas C- válidos, se necesitarían varios cambios en su implementación:

1. **Mejorar la inferencia de tipos**: El analizador debería reconocer que variables como `v`, `u`, `temp`, etc. son enteros y utilizar esa información para inferir los tipos de expresiones más complejas.

2. **Ajustar las reglas de tipo para comparaciones**: Debería reconocer que expresiones como `v < 1` o `v == 0` son válidas para condiciones de `if` y producen resultados booleanos implícitos.

3. **Corregir el chequeo de tipos para argumentos de función**: Debería verificar correctamente que los argumentos pasados a una función coincidan con los tipos de sus parámetros.

## ¿Es posible escribir un programa C- que pase el análisis semántico actual?

Dado los errores que vemos, parece difícil escribir un programa C- no trivial que pase el análisis semántico actual sin modificar el analizador. Sin embargo, podríamos intentar un programa muy simple:

```c
/* Programa simple que debería pasar el análisis semántico */

int simple_function(int x)
{
  return x;
}

void main(void)
{
  int z;
  z = input();
  output(simple_function(z));
}
```

Este programa es tan simple que podría tener menos probabilidades de desencadenar los errores de tipo, aunque no puedo garantizar que pase el análisis semántico con la implementación actual.

## Conclusión

El problema no está en tu código C-, sino en la implementación del analizador semántico. Un analizador semántico bien implementado para C- debería aceptar ambos códigos (el original y el corregido) sin errores semánticos.

La solución ideal sería modificar el analizador semántico para que maneje correctamente:
1. Inferencia de tipos para expresiones aritméticas
2. Condiciones en sentencias `if` y `while`
3. Verificación de tipos para argumentos de función
4. Expresiones de retorno

Esta tarea requeriría revisar y modificar las funciones en `analyze.py` responsables de verificar los tipos de expresiones, condiciones y argumentos de función.

¿Te gustaría que profundice en cómo podrían hacerse estas modificaciones al analizador semántico?

Analizando semántica...

Tabla de símbolos:
================================================================================
Ámbito  Nombre         Tipo      Líneas              Atributos                     
--------------------------------------------------------------------------------
0       gcd            int       4                   {'params': [<Parser.TreeNode object at 0x106b27f40>, <Parser.TreeNode object at 0x106b58250>]}
0       input          int       0                   {'params': []}                
0       main           void      15                  {'params': []}                
0       output         void      0                   {'params': [{'name': 'x', 'type': 'int', 'is_array': False}]}
1       u              int       4                   {'is_array': False}           
1       v              int       4                   {'is_array': False}           
2       temp           int       9                   {'is_array': False, 'size': None}
3       x              int       17                  {'is_array': False, 'size': None}
3       y              int       18                  {'is_array': False, 'size': None}
================================================================================

Realizando verificación de tipos...
>>> Error semántico en línea 6: Operador 'LT' aplicado a tipos no válidos
>>> Error semántico en línea 7: Expresión de retorno debe ser de tipo entero
>>> Error semántico en línea 10: Operador 'DIVIDE' aplicado a tipos no válidos
>>> Error semántico en línea 10: Operador 'TIMES' aplicado a tipos no válidos
>>> Error semántico en línea 10: Operador 'MINUS' aplicado a tipos no válidos
>>> Error semántico en línea 11: Tipo de argumento 1 no coincide con el parámetro de la función
>>> Error semántico en línea 11: Tipo de argumento 2 no coincide con el parámetro de la función
>>> Error semántico en línea 6: La condición del if debe ser booleana
>>> Error semántico en línea 21: Tipo de argumento 1 no coincide con el parámetro de la función
>>> Error semántico en línea 21: Tipo de argumento 2 no coincide con el parámetro de la función

Se encontraron errores en la verificación de tipos.


## Programa 3 (sample3.c-) errores 

/* Programa simple que debería pasar el análisis semántico */

int simplefunction(int x)
{
  return x;
}

Veo que la sintaxis del programa ha sido analizada correctamente, pero el analizador semántico aún encuentra dos errores:

1. **Error semántico en línea 5: Expresión de retorno debe ser de tipo entero**
   - Este error ocurre en la línea `return x;` dentro de la función `simplefunction`.
   - Aunque `x` está declarado como `int`, parece que el analizador no está reconociendo correctamente su tipo al retornarlo.

2. **Error semántico en línea 12: Tipo de argumento 1 no coincide con el parámetro de la función**
   - Este error ocurre en la línea `output(simplefunction(z));` cuando se pasa `z` a la función `simplefunction`.
   - Aunque `z` es un `int` y el parámetro `x` también es un `int`, el analizador está fallando al verificar la compatibilidad de tipos.

Estos errores confirman que hay problemas fundamentales en la implementación del analizador semántico, específicamente en:

1. **Verificación de tipos de expresiones de retorno**: El analizador no reconoce correctamente que `x` es de tipo entero al ser retornado.
2. **Verificación de tipos de argumentos de función**: El analizador no está verificando correctamente que el tipo del argumento coincida con el tipo del parámetro.

## Solución para el analizador semántico

Para solucionar estos problemas, sería necesario modificar el analizador semántico. Específicamente, necesitaríamos revisar las funciones en `analyze.py` responsables de:

1. Verificación de tipos de expresiones de retorno (función `checkStmt` para nodos `ReturnK`)
2. Verificación de tipos de argumentos de función (función `checkExp` para nodos `CallK`)

### Modificación propuesta para la verificación de retorno:

```python
# En analyze.py, dentro de la función checkStmt
elif t.stmt == StmtKind.ReturnK:
    # Verificar retorno
    if t.child[0] is None:
        # Retorno vacío, debe ser función void
        if function_return_type != ExpType.Void:
            error(t.lineno, "Retorno sin valor en función no void")
    else:
        # Retorno con valor
        if function_return_type == ExpType.Void:
            error(t.lineno, "Retorno con valor en función void")
        # MODIFICAR ESTA PARTE:
        # En lugar de verificar el tipo exacto, permitir cualquier tipo compatible
        # (entero o identificador que refiera a un entero)
        elif t.child[0].nodekind == NodeKind.ExpK and t.child[0].exp == ExpKind.IdK:
            # Si es un identificador, buscar su tipo en la tabla de símbolos
            sym = st_lookup(t.child[0].name)
            if sym is not None and sym.type_spec == "int":
                # Es un entero, todo bien
                pass
            else:
                error(t.lineno, "Expresión de retorno debe ser de tipo entero")
        elif t.child[0].type not in [ExpType.Integer, ExpType.Array]:
            error(t.lineno, "Expresión de retorno debe ser de tipo entero")
```

### Modificación propuesta para la verificación de argumentos de función:

```python
# En analyze.py, dentro de la función checkExp, la parte que verifica los argumentos de función
# Verificar tipos de argumentos
arg = t.child[0]
for i, param in enumerate(expected_params):
    if arg is None:
        break
    
    # MODIFICAR ESTA PARTE:
    # Verificar si param es un dict o un TreeNode
    if isinstance(param, dict):
        # Si es un dict, usar la clave 'type'
        param_type = param.get('type', 'int')
        expected_type = ExpType.Integer if param_type == 'int' else ExpType.Void
        is_array = param.get('is_array', False)
    else:
        # Si es un TreeNode, usar el atributo type
        expected_type = ExpType.Integer if param.type == ExpType.Integer else ExpType.Void
        is_array = param.is_array if hasattr(param, 'is_array') else False
    
    # Si el parámetro es un arreglo
    if is_array:
        if arg.exp != ExpKind.IdK:
            error(t.lineno, f"Argumento {i+1} debe ser un arreglo")
        else:
            arg_sym = st_lookup(arg.name)
            if arg_sym is None or not arg_sym.attr or not arg_sym.attr.get('is_array'):
                error(t.lineno, f"Argumento {i+1} debe ser un arreglo")
    
    # Verificar tipo
    # AQUÍ ESTÁ EL PROBLEMA: Modificar esta verificación para manejar identificadores
    elif arg.exp == ExpKind.IdK:
        # Si es un identificador, buscar su tipo en la tabla de símbolos
        arg_sym = st_lookup(arg.name)
        if arg_sym is not None:
            # Verificar compatibilidad de tipos basada en el tipo en la tabla de símbolos
            arg_type = ExpType.Integer if arg_sym.type_spec == "int" else ExpType.Void
            if arg_type != expected_type and arg_type != ExpType.Array:
                error(t.lineno, f"Tipo de argumento {i+1} no coincide con el parámetro de la función")
        else:
            error(t.lineno, f"Identificador '{arg.name}' no declarado")
    elif arg.type not in [expected_type, ExpType.Array]:
        error(t.lineno, f"Tipo de argumento {i+1} no coincide con el parámetro de la función")
    
    arg = arg.sibling
```

## Conclusión

El problema no está en tu código C-, sino en la implementación del analizador semántico que no maneja correctamente la verificación de tipos en ciertos contextos. Incluso con un programa muy simple, el analizador semántico actual tiene dificultades para verificar correctamente los tipos.

Las modificaciones propuestas anteriormente podrían ayudar a solucionar estos problemas, pero una solución completa probablemente requeriría una revisión más profunda del analizador semántico para asegurar que todos los tipos se infieran, propaguen y verifiquen correctamente en todos los contextos del programa.

Para un proyecto académico, podrías considerar estas limitaciones como parte del aprendizaje sobre los desafíos en la implementación de analizadores semánticos, y documentar estos problemas y posibles soluciones en tu informe o documentación.

void main(void)
{
  int z;
  z = input();
  output(simplefunction(z));
}

Analizando semántica...

Tabla de símbolos:
================================================================================
Ámbito  Nombre         Tipo      Líneas              Atributos                     
--------------------------------------------------------------------------------
0       input          int       0                   {'params': []}                
0       main           void      8                   {'params': []}                
0       output         void      0                   {'params': [{'name': 'x', 'type': 'int', 'is_array': False}]}
0       simplefunction int       3                   {'params': [<Parser.TreeNode object at 0x10ee92f40>]}
1       x              int       3                   {'is_array': False}           
2       z              int       10                  {'is_array': False, 'size': None}
================================================================================

Realizando verificación de tipos...
>>> Error semántico en línea 5: Expresión de retorno debe ser de tipo entero
>>> Error semántico en línea 12: Tipo de argumento 1 no coincide con el parámetro de la función

Se encontraron errores en la verificación de tipos.

Despues de implementar esa solucion todavía vemos:

Analizando semántica...

Tabla de símbolos:
================================================================================
Ámbito  Nombre         Tipo      Líneas              Atributos                     
--------------------------------------------------------------------------------
0       input          int       0                   {'params': []}                
0       main           void      8                   {'params': []}                
0       output         void      0                   {'params': [{'name': 'x', 'type': 'int', 'is_array': False}]}
0       simplefunction int       3                   {'params': [<Parser.TreeNode object at 0x101accf40>]}
1       x              int       3                   {'is_array': False}           
2       z              int       10                  {'is_array': False, 'size': None}
================================================================================

Realizando verificación de tipos...
>>> Error semántico en línea 5: Expresión de retorno debe ser de tipo entero
>>> Error semántico en línea 12: Tipo de argumento 1 no coincide con el parámetro de la función

Se encontraron errores en la verificación de tipos.