# Bosquejo gramática de Stókhos

```_
<entrada> -> <instrucción> | <expresión>
…
<expresión>
    -> <número>
    …
    -> <expresión> + <expresión>
```

---

## Para instrucciones

Una instrucción puede ser una definición o una asignación, diferenciándose en que una definición comienza con un identificador de tipo, al contrario de una asignación.

La sintaxis permite declarar variables de tipo numérico y booleano, además de arreglos de dichos tipos. También se permite la asignación después de definidas las variables, sin embargo, solamente se pueden reasignar elementos de un arreglo, mas no arreglos enteros.

Se puede acceder a los elementos de un arreglo colocando una expresión numérica entre corchetes al lado del identificador, cuya evaluación corresponde a un índice del arreglo.

```_
<instrucción> -> <definición>;  | <asignación>; | expresión

<definición> -> <tipo> <identificador> := <expresión>
    | [<tipo>] <identificador> := [<listaElems>]

<listaElems> -> (lambda)
    | <expresión>
    | <listaElems>, <expresión>

<asignación>  -> <identificador> := <expresión>
    | <identificador>[<expresion>] := <expresión>
```

## Para expresiones

Una expresión puede estar parentizada, acotada, ser numérica, booleana o una llamada a una función.

Como expresiones numéricas, es posible hacer operaciones entre expresiones que involucren literales y variables, estando permitidas la suma, resta, multiplicación, división, módulo y potenciación. Se incluyen también los operadores + y - prefijos.

Como expresiones booleanas, se permiten las disyuciones, conjunciones y comparaciones, además de la negación de expresiones enteras.

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

<comparación> -> <expresion> < <expresion>
    | <expresion> <= <expresion>
    | <expresion> > <expresion>
    | <expresion> >= <expresion>
    | <expresión> = <expresión>
    | <expresión> <> <expresión>

<función> -> <identificador> (<listaElems>)
```

## Terminales

```_
<identificador>  ->  <primCaracter> <idCola>

<primCaracter> -> (todos los caracteres posibles excepto un número)

<idCola> ->  <caracter> <idCola>
    | (lambda)

<caracter> -> (todos los caracteres posibles)

<número>  ->  <entero>
    | <entero> . <entero>
    | . <entero>
    | <entero> .
    
<digito> -> 0|1|2|3|4|5|6|7|8|9

<booleano> -> true
    | false

<tipo> -> num
    | bool
```
