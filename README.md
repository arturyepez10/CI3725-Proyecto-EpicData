# Stókhos by EpicData

## CI3725 - Traductores e Interpretadores | Enero - Marzo 2022

### Arturo Yepez - Jesus Bandez - Christopher Gómez

### Copyright (C) 2022

## Descripcion general 📃

**Stókhos** (del griego στόχος) es un lenguaje interactivo orientado a simulaciones estocásticas.

En base al lenguaje original, la implementación realizada en este periodo de tiempo constituye a una versión simplificada del lenguaje, detallado en una sección posterior.

La interacción con el lenguaje se realizará principalmente mediante un REPL (Read-Evaluate-Print-Loop) encargado de enviar a la VM (Virtual Machine) las instrucciones ingresadas por el usuario. El REPL imita el comportamiento de otros lenguajes de programación mas conocidos (Python, NodeJS, etc.).

## Comenzando 🔧

Para comenzar a programar en Stókhos:

1. Clone el repositorio.
2. Abra la linea de comandos y navega hasta la raiz del proyecto.
3. Utilice el shell interactivo del lenguaje, para ello escriba:

    ```_
    python Stokhos.py
    ```

4. ¡Listo! Disfrute programar en Stókhos.

## Comandos

Hay una lista de comandos y acciones pre-definidas por defecto en el REPL de Stókhos. Estos son:

* `?` o `help`: Da acceso en la linea de comando a la lista de "funciones magicas" y funcionalidades de la CMD/REPL disponibles.
* `? <comando>` o `help <comando>`, donde `<comando>` es una de las funciones disponibles de la lista: Muestra detalladamente la definicion y/o uso del comando que se esta consultando.
* `exit` o `.`: Finaliza la ejecucion del REPL.
* `clear`: Limpia la consola de comandos del historial de comandos y resultados.
* `.load <direccion>`: Carga un archivo y ejecuta los comandos de cada una de sus lineas de forma secuencial, de la misma manera que si el usuario los fuera escrito manualmente en el REPL.
* `.lexer <comando>`: Envía el `<comando>` al analizador lexicográfico de Stókhos, e imprime la lista de tokens obtenidos del comando.
* `.failed`: Retorna a la salida estandar una lista de errores que se han generado sobre anteriores ejecuciones.
* `.reset`: Por el momento, limpia deja vacia la lista de errores almacenadas.
* `.ast <comando>`: Envía el `<comando>` al analizador sintáctico de Stókhos e imprime el Árbol de Sintaxis Abstracta retornado por él como una cadena de caracteres.

## Implementación

La implementación corresponde a una versión simplificada de un lenguaje, en la que principalmente se puede notar que no se permiten definiciones de funciones, dado que es un tópico propio de otra cadena de asignaturas.

La estructura principal del proyecto opta por modularizar las distintas funcionalidades del **Interpretador de Stókhos** con el proposito de lograr mejor mantenibilidad y legibilidad.

La implementación actual está basada en Python. Las librerias que dan soporte a la construcción del interpretador corresponden a:

* [**PLY (Python Lex-Yacc)**](https://github.com/dabeaz/ply): Lexer y parser de utilidad para el interpretador.
* [**cmd**](https://docs.python.org/3/library/cmd.html): Soporte para intérpretes de línea de comandos, usada para la implementacion del REPL.

### Estructura de la implementacion

El archivo base para probar Stókhos desde su linea de comandos es **Stokhos.py**

Actualmente, los archivos y directorios principales del proyecto son los siguiente:

* **Stokhos.py**: Convergencia de distintos módulos para la ejecución del proyecto. Archivo ejecutable (indicado en la seccion de **Comenzando 🔧**).
* **VM.py**: Declaración de la clase que implementa la VM (Virtual Machine) que servirá de intérprete del lenguaje Stókhos.
* **REPL.py**: Declaración de clase que implementa el shell interactivo de Stókhos y su conexión directa a la VM.
* **tokenrules.py**: Módulo que define las reglas para el tokenizer de Stókhos.
* **grammar.py**: Módulo que define la gramática para el parser de Stókhos, este hace uso del tokenizer.
* **AST.py**: Declaración de la clase AST que implementa el Árbol de Sintaxis Abstracta de Stókhos, y de todas sus subclases.
* **gramatica.md**: Archivo de marcado que contiene una descripción sencilla de la gramática del lenguaje Stókhos.
* **ply**: Librería utilizada con la implementación del tokenizer y parser.
* **tests** (diretorio): Todas las pruebas unitarias que existen sobre los distintos modulos de la implementacion de Stókhos.
* **utils** (directorio): Distintos scripts de objetivos misceláneos para el contexto del proyecto.
  * **constants.py**: Módulo con constantes útiles para el proyecto.
  * **custom_exceptions.py**: Módulo donde se declaran excepciones personalizadas.
  * **helpers.py**: Módulo con funciones y clases de utilidad.
  * **err_strings.py**: Módulo donde se definen todas las strings de error mostradas en el REPL.

## Pruebas

Para el correcto flujo de pruebas de todos los modulos del proyecto, se diseñó un conjunto de pruebas unitarias para probar y asertar las distintas funcionalidades y acciones disponibles de Stókhos (las implementadas hasta el momento).

Esta implementación se hizo utilizando una librería o herramienta de construcción de pruebas [**pytest**](https://docs.pytest.org/en/7.1.x/). Usted puede correr las pruebas de Stókhos de la siguiente manera:

1. Instale la librería, escribiendo en la linea de comandos:

    ```_
      pip install -r requirements.txt
    ```

2. Ejecute las pruebas, usando el siguiente comando:

    ```_
      pytest
    ```

3. Los resultados de las pruebas se mostraran en la salida estándar.

## Manejo de errores

En la implementación de Stókhos se tomó la decisión de manejar dos tipos distintos de errores que pueden presentarse durante la analisis y/o ejecución de comandos ingresados por el usuario, estos son:

* **Errores fatales**: Estos detienen la ejecución del comando y hacen que se deje de leer el archivo cargado que se está leyendo de forma inmediata sin intentar recuperarse de este.
  * Actualmente, estos errores solamente son los derivados de la carga de archivos, bien sea por la detección de posibles dependencias circulares de archivos cargados o por la introducción de rutas inexistentes a un archivo.
* **Errores simples**: En estos la ejecución de comandos posteriores no se ve afectada.
