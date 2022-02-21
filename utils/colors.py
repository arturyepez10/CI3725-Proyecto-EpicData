"""
Colores para impresion de salida al usuario
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

# Lista de colores a utilizar para la impresion
BOLD = '\033[1m'
BLUE = '\033[94m'
RESET = '\033[0m'


def printResult(line: str) -> None:
    '''Imprime con un color en especifico los resultados de la REPL al usuario.

        Segun el enunciado, la salida standard de las respuestas de Stókhos debe ser en color azul.
        
        Retorna:
            Nada, dado que los resultados se imprimen al usuario.
    '''
    print(f'{BLUE}{line}{RESET}')