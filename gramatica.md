# Gramática de Stókhos

## Para instrucciones

Una instrucción puede ser una definición o una asignación, diferenciándose en que una definición comienza con un identificador de tipo, al contrario de una asignación.

La sintaxis permite declarar variables de tipo numérico y booleano, además de arreglos de dichos tipos. También se permite la asignación después de definidas las variables, sin embargo, solamente se pueden reasignar elementos de un arreglo, mas no arreglos enteros.

Se puede acceder a los elementos de un arreglo colocando una expresión numérica entre corchetes al lado del identificador, cuya evaluación corresponde a un índice del arreglo.

```_
<instrucción> -> <definición>; | <asignación>; | <expresión>

<definición> -> <tipo> <identificador> := <expresión>

<asignación> -> <identificador> := <expresión>
    | <acceso_arreglo> := <expresión>

<tipo> -> <tipo_primitivo> | <tipo_arreglo>
<tipo_arreglo> -> [<tipo_primitivo>]

```

## Para expresiones

Una expresión puede estar parentizada, acotada, ser numérica, booleana o una llamada a una función.

Como expresiones numéricas, es posible hacer operaciones entre expresiones que involucren literales y variables, estando permitidas la suma, resta, multiplicación, división, módulo y potenciación. Se incluyen también los operadores + y - prefijos.

Como expresiones booleanas, se permiten las disyuciones, conjunciones y comparaciones, además de la negación de expresiones enteras.

La tabla de precedencia de las operaciones es la siguiente, listada desde los operadores de mayor precedencia hasta los de menor:

| Operador(es) | Descripción | Asociatividad |
| --- | --- | --- |
| ( ), ' ', [ ], { } | Agrupación, acotación y acceso a arreglos | no asociativo |
| ^ | Elevación a potencia | Derecha |
| !, +, - | Negación lógica, más y menos unarios | no asociativo |
| *, /, % | Multiplicación, división y módulo | izquierda |
| +, - | Suma y resta | izquierda |
| <, >, <=, >=, | Desigualdad numérica | no asociativo |
| ==, <> | Comparación | no asociativo |
| && | Conjunción lógica | izquierda |
| \|\| | Disyunción lógica | izquierda |
| := | Asignación | no asociativo |

```_
<expresión> -> (<expresión>)
    | '<expresión>'
    | <número>
    | <booleano>
    | <identificador>
    | -<expresión>
    | +<expresión>
    | <expresión> + <expresión>
    | <expresión> - <expresión>
    | <expresión> * <expresión>
    | <expresión> / <expresión>
    | <expresión> % <expresión>
    | <expresión> ^ <expresión>
    | !<expresión>
    | <expresión> && <expresión>
    | <expresión> || <expresión>
    | <comparación>
    | <función>
    | <arreglo>
    | <acceso_arreglo>

<arreglo> -> [<lista_elementos>]

<listaElems> -> (lambda)
    | <expresión>
    | <listaElems>, <expresión>

<comparación> -> <expresion> < <expresion>
    | <expresion> <= <expresion>
    | <expresion> > <expresion>
    | <expresion> >= <expresion>
    | <expresión> = <expresión>
    | <expresión> <> <expresión>

<función> -> <identificador> (<expresion>)
<acceso_arreglo> -> <identificador> [<expresión>]
```

## Terminales

```_
<identificador> -> <primCaracter> <idCola>

<primCaracter> -> [A-za-z_] <idCola>
<idCola> -> [A-za-z_0-9]*

<número> -> <entero>
    | <entero> . <entero>
    | . <entero>
    | <entero> .
    
<entero> -> [0-9]+

<booleano> -> true
    | false

<tipo_primitivo> -> num
    | bool
```
