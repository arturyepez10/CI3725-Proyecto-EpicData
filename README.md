# Interpretador de Stókhos
## CI3725 - Traductores e Interpretadores | Enero - Marzo 2022

### Autores:
### Arturo Yepez, Jesus Bandez, Christopher Gómez
### Copyright (C) 2022
## Descripcion General

**Stókhos** (del griego στόχος) es un lenguaje interactivo orientado a simulaciones estocásticas.

En base al lenguaje original, la implementacion realizada en este periodo de tiempo constituye a una version simplificada del lenguaje, que sera detallado en una seccion a posterior.

La interaccion con el lenguaje se realizara mediante una REPL encargada de hacerle llegar a la VM (Virtual Machine) los comandos ingresados por el usuario. La REPL imita el comportamiento de otros lenguajes de programacion mas conocidos (Python, NodeJS, etc).

## USO

Para poder correr el proyecto, se necesita:
1. Clonar el repositorio.
2. Abrir linea de comandos en la raiz del proyecto.
3. Para iniciar la ejecucion de la REPL del proyecto, se utiliza:
```
python Stokhos.py
```
4. ¡Listo! Disfrute codear en Stókhos.

## IMPLEMENTACION

Como fue mencionado en la primera seccion, esta implementacion corresponde a una version simplificada donde principalmente se puede notar que no se permiten definiciones de funciones, dado que es un topico propio de otra cadena de asignaturas.

Para estructura principal del proyecto se decidio modularizar las distintas funcionalidades del **Interpretador de Stókhos** con el proposito de lograr mejor mantenibilidad y legibilidad.

Para implementacion, al momento actual se decanto por utilizar librerias de soporte para la construccion del interpretador. Estas librerias corresponden a:
- **ply**, para el interpretador.
- **cmd**, para la implementacion del REPL. 

Los desarrolladores optaron de forma temporal la siguiente estructura de proyecto:

- **Stokhos.py**: Convergencia de distintos modulos para la ejecucion del proyecto. Archivo "ejecutable" (indicado en la seccion de **USO**).
- **StokhosVM.py**: Declaracion de clase cuya implementacion consiste en la VM (Virtual Machine) de nuestro lenguaje de programacion.
- **REPL.py**: Declaracion de clase con la implementacion de la cmd de Stókhos y su conexion directa a la VM.
- **tokenrules.py**: Reglas para el tokenizer de Stókhos.
- **lexer.test.py**: Archivo con pruebas unitarias para el analizador lexicografico de Stókhos.
- **utils** (directorio): Distintas funciones de objetivos miscelaneos para el contexto de la aplicacion.
    - **colors.py**: Metodos y variables para output segun especificaciones.