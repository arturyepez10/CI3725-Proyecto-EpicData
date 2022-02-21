"""
REPL para la VM del lenguaje Stókhos
    Copyright (C) 2022 Arturo Yepez - Jesus Bandez - Christopher Gómez
    CI3725 - Traductores e Interpretadores

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
# Libreria principal para construir REPL
from cmd import Cmd
# Libreria de Virtual Machine de Stokhos
from StokhosVM import StokhosVM as SVM

# Utilidades miscelaneas del proyecto
from utils.colors import *
import os

class StokhosCMD(Cmd):
    """
    Clase StokhosCMD
        extiende:
            Cmd:
                Superclase que hereda con los metodos iniciales del CMD/REPL de nuestro
                lenguaje de programacion. Se utilza de la libreria de 'cmd'

        atributos:
            vm:
                Instancia de la Virtual Machine creada para manipular Stókhos
        
        descripcion:
            Esta clase es donde se van a aplicar los metodos principales para crear la REPL del
            lenguaje de programacion 'Stókhos'. Utiliza de base los metodos ofrecidos de la
            libreria 'cmd' con una capa de customizacion para el actual proyecto.
    """

    # Instancia de VM de Stókhos
    vm = SVM()

    # El prompt por defecto del REPL
    prompt = f'{RESET}< Stókhos > {BOLD}'
    # Mensaje de introduccion al REPL de Stókhos
    intro = '¡Bienvenido! Utiliza "?" para mostrar los comandos disponibles'
    # Encabezado documentacion de comandos
    doc_header = 'Lista de comandos basicos (escribe `help <nombre>` para informacion detallada)'
    misc_header = 'Lista de funciones disponibles (escribe `help <nombre>` para informacion detallada)'

    # ---------------------------------------------- #
    # METODOS DE LA VIRTUAL MACHINE
    # ---------------------------------------------- #
    def send_lexer(self, line: str) -> None:
        '''Envia un comando en especifico al analizador lexicografico de Stókhos

            El analizador se encarga de procesar la entrada para construir un arreglo de tokens segun el comando
            y luego poder imprimir en pantalla.

            Retorna:
                Nada, dado que los resultados se imprimen al usuario.
        '''
        # Entrada es cortada para verificar si hay mas contenido luego de '.lex' y enviar a la VM acorde a eso
        input_splitted = line.split('.lex ')
        vm_input = line.split('.lex ')[1] if input_splitted[0] != '.lex' else ''

        # Entrada analizada lexicograficamente por la VM
        processed_input = self.vm.lextest(vm_input)

        # Se imprime al usuario el resultado final
        printResult(processed_input)

    def send_process(self, line: str) -> None:
        '''Envia un comando en especifico al procesador de Stókhos

            Transforma el comando en un arbol abstracto, evalúa expresiones y las
            ejecuta en el contexto de las variables existentes en memoria.

            Retorna:
                Nada, dado que los resultados se imprimen al usuario.
        '''
        # Entrada procesada de la VM
        processed_input = self.vm.process(line)

        # Se imprime al usuario el resultado final
        printResult(processed_input)

    # ---------------------------------------------- #
    # DOCUMENTACION DE COMANDOS DISPONIBLES
    # ---------------------------------------------- #
    def help_lexer(self) -> None:
        print('''
        Aplica el analizador lexicográfico de Stókhos a un comando en particular.

        El analizador se encarga de procesar la entrada para construir un arreglo de tokens segun el comando
        que se le envie y luego imprime en pantalla esa lista. En caso de error, se le notifica al usuario
        cual token presenta un error.

        Su ejecucion se realiza mediante:
            >>> .lex <comando>
        ''')

    # ---------------------------------------------- #
    # METODOS BASICOS
    # ---------------------------------------------- #
    def do_exit(self, line: str) -> bool:
        '''
        Finaliza el CMD/REPL de Stókhos.
        
        Se puede ejecutar de dos maneras:
            >>> exit
            >>> .
        '''
        return True

    def do_clear(self, line: str) -> None:
        '''Limpia la pantalla de la terminal de los comandos anteriores'''
        comando = 'clear'

        # Si el SO es Windows, cambia el comando
        if os.name in ('nt', 'dos'):
            comando = 'cls'
        os.system(comando)

    def emptyline(self) -> bool:
        '''Procesador de lineas en blanco. El comportamiendo por defecto es no hacer nada.'''
        return False

    def default(self, line: str) -> bool or None:
        '''Procesador de entrada por defecto.

            Dada la implementacion, si la entrada posee alguno de los comandos reservados o funciones magicas se 
            pide su ejecucion especial a la VM. Estos comandos tienen la forma de:
                >>> .lex <comando>
                >>> .load <archivo>
                >>> .failed
                >>> .reset
            
            En el caso contrario, envia la entrada al procesador regular de la VM.

            Retorna:
                Caso 1: booleano, en caso de que se quiera terminar la ejecucion de la VM.
                Caso 2: nada, cuando se interpreta un comando se imprime su salida al usuario.
        '''
        
        if line == ".":
            return self.do_exit(line)
        elif line.startswith('.lex ') or line.startswith('.lex'):
            return self.send_lexer(line)
        else:
            return self.send_process(line)

# Se implementa ciclo principal del REPL
StokhosCMD().cmdloop()