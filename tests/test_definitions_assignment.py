"""Modulo de pruebas para el chequeo de tipos"""
import os
import sys
import pytest



sys.path.insert(1, os.path.abspath('.'))

from stokhos.symtable import SymVar
from stokhos.AST import *
from stokhos.VM import StokhosVM as SVM

NUM_UN_OPS = ['+', '-']
BOOL_UN_OPS = ['!']
NUM_BIN_OPS = ['^', '+', '-', '*', '%', '/']
BOOL_BIN_OPS = ['&&', '||']
COMPARISONS = ['<', '<=', '>', '>=', '=', '<>']
ALL_BIN_OPS = NUM_BIN_OPS + BOOL_BIN_OPS + COMPARISONS

# -------------- Pruebas de asignaciones ----------




def test_definitions_assignments():
    # Crear VM
    VM = SVM()

    # Tabla de simbolos simulada
    simulated_symbol_table = []

    # Crear x de tipo num
    command_process(VM, 'num x := 2;')
    # Comprobar existencia de x, y su valor
    assert VM.symbol_table.lookup('x')
    assert eq_SymVar(VM.symbol_table.lookup('x'), SymVar(NUM, Number(2)))
    # Agregar x la simulacion
    simulated_symbol_table.append(('x', SymVar(NUM, Number(2))))


    # Crear y de tipo bool
    command_process(VM, 'bool y := false;')
    # Comprobar existencia de y, y su valor
    assert VM.symbol_table.lookup('y')
    assert eq_SymVar(VM.symbol_table.lookup('y'), SymVar(BOOL, Boolean(False)))
    # Agregar y la simulacion
    simulated_symbol_table.append(('y', SymVar(BOOL, Boolean(False))))


    # Crear arrX de tipo [num]
    command_process(VM, '[num] arrX := [1,2,3];') 
    # Comprobar existencia de arrX, y su valor
    assert VM.symbol_table.lookup('arrX')
    assert eq_SymVar(VM.symbol_table.lookup('arrX'), SymVar(NUM_ARRAY, Array([Number(1), Number(2), Number(3)])))
    # Agregar arrX la simulacion
    simulated_symbol_table.append(('arrX', SymVar(NUM_ARRAY, Array([Number(1), Number(2), Number(3)]))))


    # Crear arrY de tipo [bool]
    command_process(VM, '[bool] arrY := [true, false, true];') 
    # Comprobar existencia de arrY, y su valor    
    assert VM.symbol_table.lookup('arrY')
    assert eq_SymVar(VM.symbol_table.lookup('arrY'), SymVar(BOOL_ARRAY, Array([Boolean(True), Boolean(False), Boolean(True)])))
    # Agregar arrY la simulacion
    simulated_symbol_table.append(('arrY', SymVar(BOOL_ARRAY, Array([Boolean(True), Boolean(False), Boolean(True)]))))


    

    
def command_process(VM, command:str):
    out = VM.process(command)

    if out.startswith("ERROR: "):        
        assert False, f'{out}'

def eq_SymVar(one, another):
    if isinstance(another, SymVar):
        return one.type == another.type and one.value == another.value
    else:
        raise TypeError
    