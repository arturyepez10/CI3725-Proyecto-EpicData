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
3. Utiliza el shell interactivo del lenguaje, escribe:
```
python Stokhos.py
```
4. ¡Listo! Disfruta programar en Stókhos.

## Implementación 

La implementación corresponde a una versión simplificada de un lenguaje, en la que principalmente se puede notar que no se permiten definiciones de funciones, dado que es un tópico propio de otra cadena de asignaturas.

Para la estructura principal del proyecto se decidio modularizar las distintas funcionalidades del **Interpretador de Stókhos** con el proposito de lograr mejor mantenibilidad y legibilidad.

La implementación actual está basada en Python. Al momento actual se decantó por utilizar librerias de soporte para la construcción del interpretador. Estas librerias corresponden a:

- [**PLY (Python Lex-Yacc)**](https://github.com/dabeaz/ply): Lexer y parser de utilidad para el interpretador.
- [**cmd**](https://docs.python.org/3/library/cmd.html): Soporte para intérpretes de línea de comandos, usada para la implementacion del REPL. 

Actualmente, la estructura de proyecto es la siguiente:

- **Stokhos.py**: Convergencia de distintos modulos para la ejecución del proyecto. Archivo "ejecutable" (indicado en la seccion de **Comenzando 🔧**).
- **StokhosVM.py**: Declaración de la clase que implementa la VM (Virtual Machine) que servirá de intérprete del lenguaje Stókhos.
- **REPL.py**: Declaración de clase que implementa el shell interactivo de Stókhos y su conexión directa a la VM.
- **tokenrules.py**: Módulo que define las reglas para el tokenizer de Stókhos.
- **lexer.test.py**: Archivo con pruebas unitarias para el analizador lexicográfico de Stókhos.
- **utils** (directorio): Distintas funciones de objetivos misceláneos para el contexto del proyecto.
    - **colors.py**: Módulo con métodos y variables para el formateo de strings en la salida estándar.
