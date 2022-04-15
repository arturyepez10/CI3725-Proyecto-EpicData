"""Implementaciones de las funciones predefinidas de Stókhos.

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

from math import floor, log, exp, sin, cos
from random import uniform
from time import time

from ..AST import *
from ..utils.constants import *


def stk_uniform() -> Number:
    '''Retorna un número aleatorio entre 0 y 1.
    '''
    return Number(uniform(0, 1))

def stk_floor(x: Number) -> Number:
    '''Retorna el máximo entero menor o igual a x.
    
    Args:
        x: Número a redondear.
    '''
    return floor(x)

def stk_length(a: Array) -> Number:
    '''Retorna el tamaño de una lista.
    
    Args:
        l: Lista a evaluar.
    '''
    return Number(len(a))

def stk_sum(a: Array) -> Number:
    '''Retorna la suma de los elementos de un arreglo de Number
    
    Args:
        l: Arreglo a evaluar.
    '''
    return sum(a, Number(0))

def stk_avg(a: Array) -> Number:
    '''Retorna la media de los elementos de un arreglo de Number, o 0 si el
    arreglo está vacío.
    
    Args:
        a: Arreglo a evaluar.
    '''
    return stk_sum(a) / stk_length(a) if a else 0

def stk_pi() -> Number:
    '''Retorna el valor de pi en formato de doble precisión (IEEE754).'''
    return Number(3.141592653589793)

def stk_now() -> Number:
    '''Retorna un Number correspondiente al los milisegundos transcurridos
    desde un punto de referencia en el tiempo.
    
    La implementación interna es la de currentmillis.com sugerida para Python.
    '''
    return Number(int(round(time() * 1000)))

def stk_ln(x: Number) -> Number:
    '''Retorna el logaritmo natural de x.
    
    Args:
        x: Número a evaluar.
    '''
    try:
        res = Number(log(x.value))
    except ValueError:
        raise StkRuntimeError('El logaritmo natural de un número negativo o '
            'nulo no existe')
    return res

def stk_exp(x: Number) -> Number:
    '''Retorna e elevado a x.
    
    Args:
        x: Número a evaluar.
    '''
    return Number(exp(x.value))

def stk_sin(x: Number) -> Number:
    '''Retorna el seno de x.
    
    Args:
        x: Número a evaluar.
    '''
    return Number(sin(x.value))

def stk_cos(x: Number) -> Number:
    '''Retorna el coseno de x.
    
    Args:
        x: Número a evaluar.
    '''
    return Number(cos(x.value))
