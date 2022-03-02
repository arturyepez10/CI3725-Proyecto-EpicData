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
<instrucción> -> <definición>  | <asignación>

<definición> -> <tipo> <identificador> := <expresión>;
    | [<tipo>] <identificador> := [<listaElems>];

<listaElems> -> <expresión>
    | <listaElems>, <expresión>

<asignación>  -> <identificador> := <expresión>;
    | <identificador>[<numExpr>] := <expresión>;
```

## Para expresiones

Una expresión puede estar parentizada, acotada, ser numérica, booleana o una llamada a una función.

Como expresiones numéricas, es posible hacer operaciones entre expresiones que involucren literales y variables, estando permitidas la suma, resta, multiplicación, división, módulo y potenciación. Se incluyen también los operadores + y - prefijos.

Como expresiones booleanas, se permiten las disyuciones, conjunciones y comparaciones, además de la negación de expresiones enteras.

```_
<expresión> -> (<expresión>)
    | '<expresión>'
    | <numExpr>
    | <boolExpr>
    | <función>(<listaElems>)

<numExpr> -> <número>
    | <identificador>
    | (<numExpr>)
    | -<numExpr>
    | +<numExpr>
    | <numExpr> + <numExpr>
    | <numExpr> - <numExpr>
    | <numExpr> * <numExpr>
    | <numExpr> / <numExpr>
    | <numExpr> % <numExpr>
    | <numExpr> ^ <numExpr>


<boolExpr> -> <booleano>
    | <identificador>
    | <comparación>
    | (<boolExpr>)
    | !<boolExpr>
    | <boolExpr> && <boolExpr>
    | <boolExpr> || <boolExpr>

<comparación> -> <numExpr> < <numExpr>
    | <numExpr> <= <numExpr>
    | <numExpr> > <numExpr>
    | <numExpr> >= <numExpr>
    | <expresión> = <expresión>
    | <expresión> <> <expresión>
```
