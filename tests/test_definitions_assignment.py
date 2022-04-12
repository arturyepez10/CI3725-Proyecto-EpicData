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
    
    # Crear x de tipo num
    process_command(VM, 'num x := 2;')
    # Comprobar existencia de x, y su valor
    assert VM.symbol_table.lookup('x')
    assert eq_SymVar(VM.symbol_table.lookup('x'), SymVar(NUM, Number(2)))


    # Crear y de tipo bool
    process_command(VM, 'bool y := false;')
    # Comprobar existencia de y, y su valor
    assert VM.symbol_table.lookup('y')
    assert eq_SymVar(VM.symbol_table.lookup('y'), SymVar(BOOL, Boolean(False)))


    # Crear arrX de tipo [num]
    process_command(VM, '[num] arrX := [1,2,3];') 
    # Comprobar existencia de arrX, y su valor
    assert VM.symbol_table.lookup('arrX')
    assert eq_SymVar(VM.symbol_table.lookup('arrX'), SymVar(NUM_ARRAY, Array([Number(1), Number(2), Number(3)])))


    # Crear arrY de tipo [bool]
    process_command(VM, '[bool] arrY := [true, false, true];') 
    # Comprobar existencia de arrY, y su valor    
    assert VM.symbol_table.lookup('arrY')
    assert eq_SymVar(VM.symbol_table.lookup('arrY'), SymVar(BOOL_ARRAY, Array([Boolean(True), Boolean(False), Boolean(True)])))


    # Todas las variables fueron creadas y su valor es el indicado, se cambia su valor con asignaciones que las usan a ellas mismas

    # Aumentar x
    process_command(VM, 'x := x^2 + 2;')
    # Comprobar existencia de x, y su valor
    assert VM.symbol_table.lookup('x')
    assert eq_SymVar(VM.symbol_table.lookup('x'), SymVar(NUM, Number(6)))

    # Negar y
    process_command(VM, 'y := !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!y;')
    # Comprobar existencia de y, y su valor
    assert VM.symbol_table.lookup('y')
    assert eq_SymVar(VM.symbol_table.lookup('y'), SymVar(BOOL, Boolean(True)))

    # Modificar todos los valores de arrX
    process_command(VM, 'arrX[0] := +(arrX[0]*1) - 1;')
    process_command(VM, 'arrX[1] := +(arrX[1]*1) - 2;')
    process_command(VM, 'arrX[2] := +(arrX[2]*1) - 3;')
    # Comprobar existencia de arrX, y sus nuevos valores
    assert VM.symbol_table.lookup('arrX')
    assert eq_SymVar(VM.symbol_table.lookup('arrX'), SymVar(NUM_ARRAY, Array([Number(0), Number(0), Number(0)])))

    # Negar todos los valores de arrY
    process_command(VM, 'arrY[0] := !!!arrY[0];')
    process_command(VM, 'arrY[1] := !!!!!arrY[1];')
    process_command(VM, 'arrY[2] := !arrY[2] || !(arrY[0] || !arrY[0]);')
    # Comprobar existencia de arrY, y sus nuevos valores
    assert VM.symbol_table.lookup('arrY')
    assert eq_SymVar(VM.symbol_table.lookup('arrY'), SymVar(BOOL_ARRAY, Array([Boolean(False), Boolean(True), Boolean(False)])))

    # Resetar la VM y comprobar que todas las variables creadas ya no existen
    process_command(VM, 'reset()')
    try:
        VM.symbol_table.lookup('x')
        assert False
    except UndefinedSymbolError:
        pass
    try:
        VM.symbol_table.lookup('y')
        assert False
    except UndefinedSymbolError:
        pass
    try:
        VM.symbol_table.lookup('arrX')
        assert False
    except UndefinedSymbolError:
        pass
    try:
        VM.symbol_table.lookup('arrY')
        assert False
    except UndefinedSymbolError:
        pass


def process_command(VM, command:str):
    out = VM.process(command)

    if out.startswith("ERROR: "):        
        assert False, f'{out}'

def eq_SymVar(one, another):
    if isinstance(another, SymVar):
        return one.type == another.type and one.value == another.value
    else:
        raise TypeError
    