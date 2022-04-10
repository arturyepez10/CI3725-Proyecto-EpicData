"""Validadores para subclases del AST de Stókhos.
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
from ..AST import *
from ..symtable import SymTable
from .helpers import ASTNodeVisitor


class ASTValidator(ASTNodeVisitor):
    '''Subclase que implementa el patrón de diseño de Visitor para visitar
    recursivamente todos los tipo nodos de AST, tranformando en cada paso
    los árboles (anotándolos con su tipo si es válida la expresión)
    '''
    def __init__(self, sym_table: SymTable):
        self.sym_table = sym_table

    # ---- CASOS BASE (TERMINALES) ----
    def visit_Number(self, ast: Number) -> Type:
        return NUM
    
    def visit_Boolean(self, ast: Boolean) -> Type:
        return BOOL

    def visit_Id(self, ast: Id) -> Type:
        # Verifica la existencia de la Id en la tabla de símbolos
        if self.sym_table.exists(ast.value):
            _type = self.sym_table.get_type(ast.value)
            ast.type = _type
            return _type
        
        raise SemanticError(f'Variable "{ast.value}" no definida '
            'anteriormente')

    # ---- NODOS RECURSIVOS ----

    # ---- OPERADORES ----
    def visit_BinOp(self, ast: BinOp) -> Type:
        # Verifica que los operandos sean del mismo tipo según el operador
        lhs_type = self.visit(ast.lhs)
        rhs_type = self.visit(ast.rhs)
        expected_type = BOOL if ast.op in ['&&', '||'] else NUM

        if lhs_type == expected_type and rhs_type == expected_type:
            ast.type = expected_type
            return expected_type
        
        raise SemanticError(f'"{ast.op}" no se puede aplicar a operandos '
            f'de tipo {lhs_type.type} y {rhs_type.type}')

    def visit_Comparison(self, ast: Comparison) -> Type:
        # Verifica que los operandos sean del mismo tipo según el operador
        lhs_type = self.visit(ast.lhs)
        rhs_type = self.visit(ast.rhs)
        
        if ast.op in ['<>', '=']:
            if lhs_type == rhs_type:
                if lhs_type in [NUM, BOOL]:
                    ast.type = BOOL
                    return BOOL
        else:
            if lhs_type == NUM and rhs_type == NUM:
                ast.type = BOOL
                return BOOL
        
        raise SemanticError(f'"{ast.op}" no se puede aplicar a operandos '
            f'de tipo {lhs_type.type} y {rhs_type.type}')            

    def visit_UnOp(self, ast: UnOp) -> Type:
        # Verifica que los operandos sean del tipo correcto según el operador
        term_type = self.visit(ast.term)
        expected_type = BOOL if ast.op == '!' else NUM

        if term_type == expected_type:
            ast.type = expected_type
            return expected_type

        raise SemanticError(f'"{ast.op} no se puede aplicar a operando '
            f'de tipo {term_type}')

    # ---- DEFINICIONES Y ASIGNACIONES ----
    def visit_SymDef(self, ast: SymDef) -> Type:
        # Verifica que no exista la variables en la tabla de símbolos
        if self.sym_table.exists(ast.id.value):
            raise SemanticError(f'Variable "{ast.id}" ya definida anteriormente')
        
        # Verifica que el tipo del lado derecho de la definición sea consistente
        expected_type = ast.type
        rhs_type = self.visit(ast.rhs)
        
        if rhs_type == expected_type:
            return VOID

        raise SemanticError(f'El tipo inferido es {rhs_type.type}, pero se '
            f'esperaba {expected_type.type}')
        

    def visit_Assign(self, ast: Assign):
        # Verifica que ya exista la variables en la tabla de símbolos
        expected_type = self.visit(ast.id)
        
        # Verifica que no se intente asignar a una función
        if self.sym_table.is_function(ast.id.value):
            raise SemanticError(f'Variable "{ast.id}" es una función '
                'precargada, no se puede asignar')

        # Verifica que el tipo del lado derecho de la asignación sea consistente
        rhs_type = self.visit(ast.rhs)

        if expected_type == rhs_type:
            # Se anota el arbol del lado derecho con el tipo asignado
            return VOID

        raise SemanticError(f'El tipo inferido es {rhs_type}, pero se '
            f'esperaba {expected_type}')
    
    def visit_AssignArrayElement(self, ast: AssignArrayElement) -> Type:
        # Verifica que el tipo del lado derecho de la asignación sea consistente
        array_type = self.visit(ast.array_access)
        rhs_type = self.visit(ast.rhs)

        if array_type == rhs_type:
            return VOID
        
        raise SemanticError(f'El tipo inferido es {rhs_type}, pero se '
            f'esperaba {array_type}')

    # ---- OTRAS EXPRESIONES ----
    def visit_Quoted(self, ast: Quoted) -> Type:
        _type = self.visit(ast.expr)
        ast.type = _type
        return _type

    def visit_Array(self, ast: Array) -> Type:
        # Si el arreglo es vacío puede ser de cualquier tipo
        if not ast:
            # Debe dar erro cuando se pide type([])
            ast.type = ANY_ARRAY
            return ANY_ARRAY

        expected_type = self.visit(ast[0])

        for el in ast:
            # Verifica que el tipo de cada elemento sea consistente# con el tipo
            # del primer elemento
            if type(el) == Array:
                raise SemanticError('Arreglos anidados no están permitidos')
            
            el_type = self.visit(el)
            if el_type != expected_type:
                raise SemanticError(f'El tipo de todos los elementos del '
                    f'arreglo debe ser {expected_type}, pero {el} es de tipo {el_type}')
        
        _type = NUM_ARRAY if expected_type == NUM else BOOL_ARRAY
        ast.type = _type
        return _type

    def visit_ArrayAccess(self, ast: ArrayAccess) -> Type:
        # Verifica que la Id corresponda a un arreglo
        id_type = self.visit(ast.expr)

        if not isinstance(id_type.type, TypedArray):
            raise SemanticError('No se permite el acceso a arreglo para '
                f'expresión de tipo {id_type}')

        index_type = self.visit(ast.index)
        if index_type == NUM:
            _type = Type(id_type.type.type)
            ast.type = _type
            return _type
        
        raise SemanticError(f'El tipo inferido del índice es '
            f'{index_type.type}, pero se esperaba num')

    def visit_FunctionCall(self, ast: FunctionCall):
        # Verifica que la id exista y sea una función
        return_type = self.visit(ast.id)
        
        if not self.sym_table.is_function(ast.id.value):
            raise SemanticError(f'Identificador "{ast.id}" no corresponde '
                'a una función')

        f_args = self.sym_table.get_args(ast.id.value)
        if ast.id.value in SPECIAL_FUNCTION_HANDLERS:
            _type = SPECIAL_FUNCTION_HANDLERS[ast.id.value](
                self,
                *[return_type, ast.args, f_args, ast.id.value]
            )
            
            ast.type = _type
            return _type

        # Si la lista de argumentos de la función no es vacía y la función tiene sobrecargas
        if f_args and isinstance(f_args[0], list):
            # Número de sobrecargas que tiene la función
            num_of_overloads = len(f_args)

            # Verifica si los argumentos hacen match con alguna 
            # de las sobrecargas
            for i, arg_list in enumerate(f_args):
                # Primero viendo el número de argumentos
                if len(arg_list) != len(ast.args):
                    if i + 1 == num_of_overloads:
                        raise SemanticError(f'La función "{ast.id}" esperaba '
                            f'{len(arg_list)} argumentos, pero se recibieron '
                            f'{len(ast.args)}')
                    continue

                # Luego viendo el tipo de cada argumento
                # Contador de argumentos con tipos consistentes
                matched_args = 0
                for j, expected_type in enumerate(arg_list):
                    arg_type = self.visit(ast.args[j])

                    if arg_type == expected_type:
                        matched_args += 1
                    else:
                        if i+1 == num_of_overloads:
                            raise SemanticError(f'El tipo del argumento #{i + 1} es '
                                f'{arg_type}, pero se esperaba {expected_type}')
                        break
                
                if matched_args == len(arg_list):
                    break

        # Si la función no tiene sobrecargas o es una lista vacía
        else:
            # Verifica si los argumentos hacen match
            # Primero por su número
            if len(f_args) != len(ast.args):
                raise SemanticError(f'La función "{ast.id}" esperaba '
                    f'{len(f_args)} argumentos, pero se recibieron '
                    f'{len(ast.args)}')

            # Luego por sus tipos
            for i, expected_type in enumerate(f_args):
                arg_type = self.visit(ast.args[i])
                if arg_type != expected_type:
                    raise SemanticError(f'El tipo del argumento #{i + 1} es '
                        f'{arg_type}, pero se esperaba {expected_type}')

        ast.type = return_type
        return return_type
                        
    def generic_visit(self, ast: AST):
        raise Exception(f'Validador de {type(ast).__name__} no implementado')

    def validate(self, ast: AST) -> Type:
        return self.visit(ast)

# Handlers de funciones especiales
def pass_handler(validator: ASTValidator, *args):
    # Valida igualmente cada argumento
    # (Número correcto y expresiones semánticamente válidas)
    if len(args[1]) != len(args[2]):
        raise SemanticError(f'La función "{args[3]}" esperaba '
            f'{len(args[2])} argumentos, pero se recibieron '
            f'{len(args[1])}')

    for arg in args[1]:
        validator.validate(arg)
    return args[0]

def if_handler(validator: ASTValidator, *args):
    if len(args[1]) != 3:
        raise SemanticError('La función "if" esperaba '
            f'3 argumentos, pero se recibieron {len(args[1])}')

    # Verifica que el primer argumento sea bool y los otros dos del mismo tipo
    condition_type = validator.visit(args[1][0])

    if condition_type != BOOL:
        raise SemanticError(f'El tipo del argumento #1 es '
            f'{condition_type}, pero se esperaba {BOOL}')

    exprT_type = validator.visit(args[1][1])
    exprF_type = validator.visit(args[1][2])
    
    if exprT_type == exprF_type:
        if exprT_type is ANY_ARRAY:
            return exprF_type
        return exprT_type
    
    raise SemanticError(f'El tipo del argumento #3 es '
        f'{exprF_type}, pero se esperaba {exprT_type}')

# Diccionario de handlers de funciones especiales
SPECIAL_FUNCTION_HANDLERS = {
    'type': pass_handler,
    'ltype': pass_handler,
    'reset': pass_handler,
    'if': if_handler,
}
