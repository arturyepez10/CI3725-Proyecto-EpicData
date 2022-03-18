# Stókhos by EpicData

## CI3725 - Traductores e Interpretadores | Enero - Marzo 2022

### Arturo Yepez - Jesus Bandez - Christopher Gómez
### Copyright (C) 2022

## Descripcion general 📃

**Stókhos** (del griego στόχος) es un lenguaje interactivo orientado a simulaciones estocásticas.

En base al lenguaje original, la implementacion realizada en este periodo de tiempo constituye a una versión simplificada del lenguaje, detallado en una sección posterior.

La interacción con el lenguaje se realizará principalmente mediante un REPL (Read-Evaluate-Print-Loop) encargado de enviar a la VM (Virtual Machine) las instrucciones ingresadas por el usuario. El REPL imita el comportamiento de otros lenguajes de programación mas conocidos (Python, NodeJS, etc.).

## Comenzando 🔧

Para comenzar a programar en Stókhos:

1. Clona el repositorio.
2. Abre la linea de comandos y navega hasta la raiz del proyecto.
3. Utiliza el shell interactivo del lenguaje, para ello escribe:
    ```
    python Stokhos.py
    ```

4. ¡Listo! Disfruta programar en Stókhos.

## Comandos

Hay una lista de comandos y acciones pre-definidas por defecto en Stókhos. Estos son:

* `?` o `help`: Da acceso en la linea de comando a la lista de "funciones magicas" y funcionalidades de la CMD/REPL disponibles.
* `? <comando>` o `help <comando>`: donde `<comando>` es una de las funciones disponibles de la lista. Muestra detalladamente la definicion y/o uso del comando que se esta consultando.
* `exit` o `.`: finaliza la ejecucion del REPL.
* `clear`: limpia la consola de comandos del historial de comandos y resultados.
* `.load <direccion>`: Carga un archivo y ejecuta los comandos en cada uno de sus lineas.
* `.lexer <comando>`: envia el `<comando>` al analizador lexicográfico de Stókhos.
* `.failed`: retorna a la salida estandar la lista de errores que se han generado sobre anteriores ejecuciones.
* `.reset`: por el momento, limpia deja vacia la lista de errores almacenadas.
* `.ast <comando>`: envia el `<comando>` al analizador sintáctico de Stókhos.

## Implementación

La implementación corresponde a una versión simplificada de un lenguaje, en la que principalmente se puede notar que no se permiten definiciones de funciones, dado que es un tópico propio de otra cadena de asignaturas.

La estructura principal del proyecto opta por modularizar las distintas funcionalidades del **Interpretador de Stókhos** con el proposito de lograr mejor mantenibilidad y legibilidad.

La implementación actual está basada en Python. Las librerias que dan soporte a la construcción del interpretador corresponden a:

- [**PLY (Python Lex-Yacc)**](https://github.com/dabeaz/ply): Lexer y parser de utilidad para el interpretador.
- [**cmd**](https://docs.python.org/3/library/cmd.html): Soporte para intérpretes de línea de comandos, usada para la implementacion del REPL.

### Estructura de la Implementacion

El archivo base para probar Stókhos desde su linea de comandos es **Stokhos.py**

Actualmente, los archivos y directorios principales del proyecto son los siguiente:

- **Stokhos.py**: Convergencia de distintos módulos para la ejecución del proyecto. Archivo ejecutable (indicado en la seccion de **Comenzando 🔧**).
- **VM.py**: Declaración de la clase que implementa la VM (Virtual Machine) que servirá de intérprete del lenguaje Stókhos.
- **REPL.py**: Declaración de clase que implementa el shell interactivo de Stókhos y su conexión directa a la VM.
- **tokenrules.py**: Módulo que define las reglas para el tokenizer de Stókhos.
- **tests** (diretorio): Todas las pruebas unitarias que existen sobre los distintos modulos de la implementacion de Stókhos.
- **utils** (directorio): Distintas funciones de objetivos misceláneos para el contexto del proyecto.
  - **constants.py**: Módulo con métodos y variables para todo el proyecto.

## Pruebas

Para el correcto flujo de pruebas de todos los modulos del proyecto, se diseñaron un conjunto de pruebas unitarias para probar y asertar las distintas funcionalidades y acciones disponibles de Stókhos.

Esta implementacion se hizo utilizando una libreria o herramienta de construccion de pruebas: [**pytest**](https://docs.pytest.org/en/7.1.x/). Para hacer uso de esta libreria y correr las pruebas disponibles realizamos los siguientes pasos:

1. Se debe instalar la libreria, y para ello:
    ```
      pip install -r requirements.txt
    ```
2. Ejecutamos la libreria, usando el siguiente comando:
    ```
      pytest
    ```
3. Los resultados de las pruebas se mostraran en la salida estandar.
    * A su vez, podra ver las pruebas que se generan en el archivo que se genera automaticamente `parser.out`.

## Manejo de Errores

En la implementacion de Stókhos se tuvo que tomar la decision de como manejar los distintos errores que pudiesen presentarse durante la analisis y/o ejecucion de comandos ingresados por el usuario.

Se definio, que existirian 2 tipos de errores:
* **Errores Fatales**: aquellos que deben tener la ejecucion del comando o archivo cargado de forma inmediata sin intentar recuperarse de este. 
    * Actualmente, estos errores solo pueden ocurrir cuando son errores que se generan desde el REPL, es decir, los errores derivados de la carga de archivos o los errores por reconocer comandos de implementaciones no culminadas.
* **Errores Simples**: aquellos errores donde la ejecucion de comandos posteriores o de la terminacion de la accion en si no se vea afectada y no sea necesario terminarse, por lo que se puede notificar despues de que se culminen.
    * Actualmente, los errores de la ejecucion de `.lex <comando>` pueden arrojar errores que no bloquean la ejecucion de comandos posteriores (en el caso de que se carguen archivos).