# Ejemplo de creación de tabla de símbolos y chequeo de tipos

## Diseño de Compiladores
**Dr. Víctor de la Cueva**  
vcueva@tec.mx

## Código de ejemplo

```c
/* Un programa para encontrar el mínimo de 
   un arreglo de máximo 20 elementos. */

int x[20];

int minimo ( int a[], int high )
{ int i; int x; int k;
  k = 0;
  x = a[0];
  i = 1;
  while (i < high)
   { if (a[i] < x)
      { x = a[i];
        k = i; }
     i = i + 1;
   }
  return k;
}

void main(void)
{ int i; int high;
  i = 0;
  high = input(); /* pide el número de elementos en el arreglo < 20 */
  while (i < high)
   { x[i] = input();
     i = i + 1;}
  output(minimo(x, high));
}
```

## Proceso de creación de la Tabla de Símbolos

### 1. Inicialización
- **Scope 0**: Se inicializa el scope a 0
- **Current Scope**: Se actualiza el puntero al current scope

### 2. Declaración de variable global
Al encontrar `int x[20];`:
- Se agrega la variable arreglo `x` al current scope
- Entrada: `x | int | arr | 20`

### 3. Declaración de función `minimo`
Al encontrar `int minimo ( int a[], int high )`:
- Se agrega el símbolo `minimo` al current scope con su tipo y sus argumentos (pendientes de actualizar)
- Entrada: `minimo | int | args`

### 4. Nuevo scope para función
- Se inicializa **Scope 1**
- Se mueve el current scope al Scope 1

### 5. Actualización de argumentos
- Se actualizan los argumentos del símbolo `minimo` buscándolo hasta donde se encuentre
- Actualización: `minimo | int | int|int`

### 6. Agregar parámetros al scope local
Se agregan los argumentos de `minimo` al current scope:
- `a | int | arr | void`
- `high | int`

### 7. Declaraciones locales
Se encuentran las declaraciones locales y se agregan al current scope:
- `i | int`
- `x | int`
- `k | int`

### 8. Procesamiento del cuerpo
Durante el procesamiento del cuerpo de la función:
- Se buscan los símbolos cuando se referencian
- Para estructuras de control (while, if) no se crean nuevos scopes en este lenguaje
- Se verifica que cada símbolo esté declarado en el scope actual o en scopes padre

### 9. Búsqueda de símbolos
Cuando se encuentra una referencia a un símbolo:
1. Se busca primero en el current scope
2. Si no se encuentra, se busca en el scope padre
3. Se continúa hasta encontrarlo o llegar al scope 0
4. Si no se encuentra en ningún scope, se marca ERROR

### 10. Cierre de scope
Al terminar la función:
- Se cierra el Scope 1
- Se regresa el current scope a 0

### 11. Declaración de función `main`
Al encontrar `void main(void)`:
- Se agrega el símbolo `main` al Scope 0
- Entrada: `main | void | args`
- Se crea un nuevo **Scope 2**
- Se actualiza: `main | void | void`

### 12. Variables locales de main
Se agregan las variables locales:
- `i | int`
- `high | int`

### 13. Búsqueda de símbolos globales
Cuando `main` referencia a `x`:
- No se encuentra en Scope 2
- Se busca en Scope 0 y se encuentra

### 14. Llamada a función
Cuando se encuentra `minimo(x, high)`:
- Se busca `minimo` en el current scope
- Como no se encuentra, se busca en scopes padre hasta encontrarlo

### 15. Finalización
- Se cierra el Scope 2
- Se regresa al Scope 0
- Se cierra el Scope 0

## Estructura final de la Tabla de Símbolos

### Scope 0 (Global)
| Símbolo | Tipo | Información adicional |
|---------|------|----------------------|
| x | int | arr, 20 |
| minimo | int | int\|int |
| main | void | void |

### Scope 1 (función minimo)
| Símbolo | Tipo | Información adicional |
|---------|------|----------------------|
| a | int | arr, void |
| high | int | - |
| i | int | - |
| x | int | - |
| k | int | - |

### Scope 2 (función main)
| Símbolo | Tipo | Información adicional |
|---------|------|----------------------|
| i | int | - |
| high | int | - |

## Referencias

- Alan G. Labouseur. http://labouseur.com/courses/compilers/AST-and-Symbol-Table.pdf (consultado el 24-oct-2018)