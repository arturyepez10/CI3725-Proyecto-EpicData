"""Constantes de utilidad para el proyecto.
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

from stokhos.AST import Type, PrimitiveType, TypeArray


VERSION = '0.1.3'

# Lista de colores a utilizar para la impresión
BOLD = '\033[1m'
BLUE = '\033[94m'
RESET = '\033[0m'
RED = '\033[91m'

# Abreviaturas para los tipos de datos
NUM = Type(PrimitiveType('num'))
BOOL = Type(PrimitiveType('bool'))
VOID = Type(PrimitiveType('void'))
NUM_ARRAY = Type(TypeArray(PrimitiveType('num')))
BOOL_ARRAY = Type(TypeArray(PrimitiveType('bool')))