"""Funciones de ayuda para los demás módulos del proyecto.
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

import re

def match_magic_command(name: str, line: str) -> bool:
    '''Retorna un booleano indicando si la línea contiene un comando magico
    
    Argumentos:
        name: Nombre del comando magico
        line: Línea a analizar
    '''
    return bool(re.match(r'\.' + f'{name}($| )', line))

class NullLogger():
    '''Logger sustituto para no mostrar las warnings de PLY'''
    
    def debug(self, msg, *args, **kwargs):
        pass
    
    def warning(self, msg, *args, **kwargs):
        pass

    def error(self, msg, *args, **kwargs):
        pass

    info = debug
    critical = debug