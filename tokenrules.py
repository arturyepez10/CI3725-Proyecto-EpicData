"""Definiciones de reglas para el tokenizer de Stókhos.

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

from ply.lex import LexToken, lex
import re

# Palabras reservadas del lenguaje
reserved = {
    'bool' : 'TkBool',
    'num' : 'TkNum',   
    'true' : 'TkTrue',
    'false' : 'TkFalse',
}

# Definicion de los tokens
tokens = [
    'TkOpenPar', 'TkClosePar','TkOpenBracket','TkCloseBracket', 'TkOpenBrace',
    'TkCloseBrace', 'TkNot', 'TkPower', 'TkMult', 'TkDiv', 'TkMod', 'TkPlus',
    'TkMinus','TkLT', 'TkLE', 'TkGE', 'TkGT', 'TkEq', 'TkNE', 'TkAnd', 'TkOr',
    'TkQuote', 'TkComma', 'TkAssign', 'TkSemicolon', 'TkColon', 'TkId',
    'TkNumber',
] + list(reserved.values())

# Se debe ignorar todo tipo de espacio en blanco
t_ignore = ' \t'

# Regex para obtener cada token de operadores y símbolos de agrupación
t_TkOpenPar = r'\('
t_TkClosePar = r'\)'
t_TkOpenBracket = r'\['
t_TkCloseBracket = r'\]'
t_TkOpenBrace = r'\{'
t_TkCloseBrace = r'\}'
t_TkNot = r'!'
t_TkPower = r'\^'
t_TkMult = r'\*'
t_TkDiv = r'/'
t_TkMod = r'%'
t_TkPlus = r'\+'
t_TkMinus = r'-'
t_TkLT = r'<'
t_TkLE = r'<='
t_TkGE = r'>='
t_TkGT = r'>'
t_TkEq = r'='
t_TkNE = r'<>'
t_TkAnd = r'&&'
t_TkOr = r'\|\|'
t_TkQuote = r'\''
t_TkComma = r','
t_TkAssign = r':='
t_TkSemicolon = r';'
t_TkColon = r':'

# Regex para los caracteres, digitos y puntos
def t_TkId(t: LexToken) -> LexToken:
    r'[_0-9a-zA-Z_\.][a-zA-Z_0-9\.]*'

    # Comprobar si la string completa es un numero
    if re.match(r'^(\.[0-9]+|[0-9]+\.?[0-9]*)$', t.value):
        # En caso de serlo, se le asigna el tipo Number y el valor
        t.type = 'TkNumber'
        try:
            t.value = int(t.value)
        except ValueError:
            t.value = float(t.value)

    # Se filtran los nombres ilegales
    # Si el ID comienza con un digito o contiene un '.', se retorna un token de tipo 
    # 'IllegalID'
    elif re.match(r"\d", t.value[0]) or '.' in t.value:
        t.type = 'IllegalID'
        
    else:
        # En caso de que se haya conseguido una palabra reservada del lenguaje,
        # se le asigna su respectivo tipo al token. En cualquier otro caso, el
        # el tipo del token es 'TkId'
        t.type = reserved.get(t.value,'TkId')   # Chequea palabras reservadas

    return t

# Maneja caracteres ilegales
def t_error(t: LexToken):
    t.type = 'IllegalCharacter'
    t.value = t.value[0]

    # Salta el caracter ilegal
    t.lexer.skip(1)
    return t