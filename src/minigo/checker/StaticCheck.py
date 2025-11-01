"""
* @author nhphung
"""

from AST import *
from Visitor import *
from Utils import Utils
from StaticError import *
from functools import reduce


class MType:
    def __init__(self, partype, rettype):
        self.partype = partype
        self.rettype = rettype

    def __str__(self):
        return (
            "MType(["
            + ",".join(str(x) for x in self.partype)
            + "],"
            + str(self.rettype)
            + ")"
        )


class Symbol:
    def __init__(self, name, mtype, value=None):
        self.name = name
        self.mtype = mtype
        self.value = value

    def __str__(self):
        return (
            "Symbol("
            + str(self.name)
            + ","
            + str(self.mtype)
            + ("" if self.value is None else "," + str(self.value))
            + ")"
        )


class StaticChecker(BaseVisitor, Utils):
    def __init__(self, ast):
        self.ast = ast
        self.struct_names = {}
        self.type_list: List[StructType | InterfaceType] = []
        self.func_list: List[FuncDecl] = [
            FuncDecl("getInt", [], IntType(), Block([])),
            FuncDecl("putInt", [ParamDecl("i", IntType())], VoidType(), Block([])),
            FuncDecl("putIntLn", [ParamDecl("i", IntType())], VoidType(), Block([])),
            FuncDecl("getFloat", [], FloatType(), Block([])),
            FuncDecl("putFloat", [ParamDecl("f", FloatType())], VoidType(), Block([])),
            FuncDecl(
                "putFloatLn", [ParamDecl("f", FloatType())], VoidType(), Block([])
            ),
            FuncDecl("getBool", [], BoolType(), Block([])),
            FuncDecl("putBool", [ParamDecl("b", BoolType())], VoidType(), Block([])),
            FuncDecl("putBoolLn", [ParamDecl("b", BoolType())], VoidType(), Block([])),
            FuncDecl("getString", [], StringType(), Block([])),
            FuncDecl(
                "putString", [ParamDecl("s", StringType())], VoidType(), Block([])
            ),
            FuncDecl(
                "putStringLn", [ParamDecl("s", StringType())], VoidType(), Block([])
            ),
            FuncDecl("putLn", [], VoidType(), Block([])),
        ]
        self.global_env = [
            [
                Symbol("getInt", MType([], IntType())),
                Symbol("putInt", MType([IntType()], VoidType())),
                Symbol("putIntLn", MType([IntType()], VoidType())),
                Symbol("getFloat", MType([], FloatType())),
                Symbol("putFloat", MType([FloatType()], VoidType())),
                Symbol("putFloatLn", MType([FloatType()], VoidType())),
                Symbol("getBool", MType([], BoolType())),
                Symbol("putBool", MType([BoolType()], VoidType())),
                Symbol("putBoolLn", MType([BoolType()], VoidType())),
                Symbol("getString", MType([], StringType())),
                Symbol("putString", MType([StringType()], VoidType())),
                Symbol("putStringLn", MType([StringType()], VoidType())),
                Symbol("putLn", MType([], VoidType())),
            ]
        ]
        self.current_func: FuncDecl = None
        self.current_struct: StructType = None

    def compareType(
        self,
        lhs_type,
        rhs_type,
        convertable_type_sets=[],
        c=None,
    ) -> bool:
        def check_struct_implementation(interface_type, struct_type):
            def match_method(prototype, method):
                return (
                    prototype.name == method.fun.name
                    and len(prototype.params) == len(method.fun.params)
                    and (
                        prototype.retType.name
                        if isinstance(prototype.retType, Id)
                        else type(prototype.retType)
                    )
                    == (
                        method.fun.retType.name
                        if isinstance(method.fun.retType, Id)
                        else type(method.fun.retType)
                    )
                    and all(
                        type(prop_arg) == type(meth_arg.parType)
                        for prop_arg, meth_arg in zip(
                            prototype.params, method.fun.params
                        )
                    )
                )

            return all(
                any(match_method(prototype, method) for method in struct_type.methods)
                for prototype in interface_type.methods
            )

        def check_array_type(lhs_type, rhs_type):
            if len(lhs_type.dimens) != len(rhs_type.dimens):
                return False
            if not all(
                (self.derive_value(lhs_dim, c) == self.derive_value(rhs_dim, c))
                for lhs_dim, rhs_dim in zip(lhs_type.dimens, rhs_type.dimens)
            ):
                return False
            if type(lhs_type.eleType) != type(rhs_type.eleType):
                if (
                    type(lhs_type.eleType),
                    type(rhs_type.eleType),
                ) in convertable_type_sets:
                    return True
                return False
            elif isinstance(lhs_type.eleType, Id) and isinstance(rhs_type.eleType, Id):
                return lhs_type.eleType.name == rhs_type.eleType.name
            return True

        lhs_type = (
            self.lookup(lhs_type.name, self.type_list, lambda x: x.name)
            if isinstance(lhs_type, Id)
            else lhs_type
        )
        rhs_type = (
            self.lookup(rhs_type.name, self.type_list, lambda x: x.name)
            if isinstance(rhs_type, Id)
            else rhs_type
        )

        if isinstance(rhs_type, StructType) and rhs_type.name == "":
            return isinstance(lhs_type, (StructType, InterfaceType))

        if (type(lhs_type), type(rhs_type)) in convertable_type_sets:
            if isinstance(lhs_type, InterfaceType) and isinstance(rhs_type, StructType):
                return check_struct_implementation(lhs_type, rhs_type)
            return True

        if type(lhs_type) == type(rhs_type) and isinstance(
            lhs_type, (StructType, InterfaceType)
        ):
            return lhs_type.name == rhs_type.name

        if isinstance(lhs_type, ArrayType) and isinstance(rhs_type, ArrayType):
            return check_array_type(lhs_type, rhs_type)

        return type(lhs_type) == type(rhs_type)

    def derive_value(self, ast, c):
        if isinstance(ast, IntLiteral):
            return ast.value

        if isinstance(ast, Id):
            symbol = next(
                filter(
                    lambda symbol: symbol.name == ast.name,
                    reduce(lambda acc, ele: acc + ele, c, []),
                ),
                None,
            )
            if symbol is not None:
                return symbol.value

        if isinstance(ast, BinaryOp) and isinstance(self.visit(ast, c), IntType):
            lhs_val = self.derive_value(ast.left, c)
            rhs_val = self.derive_value(ast.right, c)
            if ast.op == "+":
                return int(lhs_val + rhs_val)
            elif ast.op == "-":
                return int(lhs_val - rhs_val)
            elif ast.op == "*":
                return int(lhs_val * rhs_val)
            elif ast.op == "/":
                if rhs_val == 0:
                    raise ZeroDivisionError()  # TODO: check if this scenario is possible
                return int(lhs_val / rhs_val)
            elif ast.op == "%":
                if rhs_val == 0:
                    raise ZeroDivisionError()
                return int(lhs_val % rhs_val)

        if isinstance(ast, UnaryOp) and isinstance(self.visit(ast, c), IntType):
            return -self.derive_value(ast.body, c)

        return 0

    def check(self):
        return self.visit(self.ast, self.global_env)

    def visitProgram(self, ast: Program, c):
        global_names = list(
            map(
                lambda symbol: symbol.name,
                reduce(lambda acc, ele: acc + ele, self.global_env, []),
            )
        )

        for decl in ast.decl:
            if isinstance(decl, (StructType, InterfaceType)):
                if decl.name in global_names:
                    raise Redeclared(Type(), decl.name)
                global_names.append(decl.name)
                self.type_list = [decl] + self.type_list
            elif isinstance(decl, FuncDecl):
                if decl.name in global_names:
                    raise Redeclared(Function(), decl.name)
                global_names.append(decl.name)
                self.func_list = [decl] + self.func_list
            elif isinstance(decl, ConstDecl):
                if decl.conName in global_names:
                    raise Redeclared(Constant(), decl.conName)
                global_names.append(decl.conName)
            elif isinstance(decl, VarDecl):
                if decl.varName in global_names:
                    raise Redeclared(Variable(), decl.varName)
                global_names.append(decl.varName)

        def add_method(ast: MethodDecl, c):
            found = self.lookup(ast.fun.name, c.methods, lambda x: x.fun.name)
            if found is not None:
                raise Redeclared(Method(), ast.fun.name)
            if ast.fun.name in self.struct_names[c.name]:
                raise Redeclared(Method(), ast.fun.name)
            c.methods.append(ast)
            self.struct_names[c.name].append(ast.fun.name)

        self.struct_names = {
            struct.name: []
            for struct in self.type_list
            if isinstance(struct, StructType)
        }

        reduce(
            lambda acc, type: [self.visit(type, acc)] + acc,
            list(
                filter(
                    lambda decl: isinstance(decl, (InterfaceType, StructType)), ast.decl
                )
            ),
            [],
        )

        list(
            map(
                lambda method_decl: add_method(
                    method_decl,
                    self.lookup(
                        method_decl.recType.name, self.type_list, lambda type: type.name
                    ),
                ),
                list(filter(lambda decl: isinstance(decl, MethodDecl), ast.decl)),
            )
        )

        reduce(
            lambda acc, ele: [
                (
                    [symbol] + acc[0]
                    if isinstance(symbol := self.visit(ele, acc), Symbol)
                    else acc[0]
                )
            ]
            + acc[1:],
            list(filter(lambda decl: isinstance(decl, Decl), ast.decl)),
            self.global_env,
        )

        return c

    def visitParamDecl(self, ast: ParamDecl, c) -> Symbol:
        if c:
            found_param = self.lookup(ast.parName, c, lambda x: x.name)
            if found_param:
                raise Redeclared(Parameter(), ast.parName)
        return [Symbol(ast.parName, ast.parType, None)] + c

    def visitVarDecl(self, ast: VarDecl, c) -> Symbol:
        if self.lookup(ast.varName, c[0], lambda x: x.name):
            raise Redeclared(Variable(), ast.varName)

        var_type = ast.varType if ast.varType else None
        init_type = self.visit(ast.varInit, c) if ast.varInit else None
        init_val = self.derive_value(ast.varInit, c) if ast.varInit else None

        if var_type is None:
            return Symbol(ast.varName, init_type, init_val)

        elif init_type is None:
            return Symbol(ast.varName, var_type, None)

        elif self.compareType(
            var_type, init_type, [(FloatType, IntType), (InterfaceType, StructType)], c
        ):
            if isinstance(ast.varType, NilLiteral):
                return Symbol(ast.varName, NilLiteral(), None)
            return Symbol(ast.varName, var_type, init_val)

        raise TypeMismatch(ast)

    def visitConstDecl(self, ast: ConstDecl, c) -> Symbol:
        if self.lookup(ast.conName, c[0], lambda x: x.name) is not None:
            raise Redeclared(Constant(), ast.conName)
        init_type = self.visit(ast.iniExpr, c)
        init_val = self.derive_value(ast.iniExpr, c)
        return Symbol(ast.conName, init_type, init_val)

    def visitFuncDecl(self, ast: FuncDecl, c) -> Symbol:
        if self.lookup(ast.name, c[0], lambda x: x.name) is not None:
            raise Redeclared(Function(), ast.name)
        params = reduce(lambda acc, param: self.visit(param, acc), ast.params, [])
        self.current_func = ast
        self.visit(ast.body, [params] + c)
        return Symbol(
            ast.name,
            MType(
                list(reduce(lambda acc, param: [param.mtype] + acc, params, [])),
                ast.retType,
            ),
            None,
        )

    def visitStructType(self, ast: StructType, c) -> StructType:
        def visitField(ast, c, struct):
            if ast[0] in self.struct_names[struct.name]:
                raise Redeclared(Field(), ast[0])
            else:
                self.struct_names[struct.name].append(ast[0])
            if c:
                if self.lookup(ast[0], c, lambda x: x[0]) is not None:
                    raise Redeclared(Field(), ast[0])
            return c + [ast]

        reduce(lambda acc, field: visitField(field, acc, ast), ast.elements, [])
        return ast

    def visitMethodDecl(self, ast: MethodDecl, c) -> None:
        params = reduce(
            lambda acc, param: self.visit(param, acc),
            ast.fun.params,
            [],
        )
        self.current_func = ast.fun
        self.current_struct = ast.recType
        self.visit(
            ast.fun.body, [params] + [[Symbol(ast.receiver, ast.recType, None)]] + c
        )

    def visitPrototype(self, ast: Prototype, c) -> Prototype:
        if self.lookup(ast.name, c, lambda x: x.name) is not None:
            raise Redeclared(Prototype(), ast.name)
        return ast

    def visitInterfaceType(self, ast: InterfaceType, c) -> InterfaceType:
        if self.lookup(ast.name, c, lambda x: x.name) is not None:
            raise Redeclared(Type(), ast.name)
        reduce(lambda acc, ele: [self.visit(ele, acc)] + acc, ast.methods, [])
        return ast

    def visitForBasic(self, ast: ForBasic, c) -> None:
        if not isinstance(self.visit(ast.cond, c), BoolType):
            raise TypeMismatch(ast)
        self.visit(Block(ast.loop.member), c)

    def visitForStep(self, ast: ForStep, c) -> None:
        init = self.visit(ast.init, [[]] + c)
        if not isinstance(self.visit(ast.cond, [[init]] + c), BoolType):
            raise TypeMismatch(ast)
        self.visit(Block([ast.init] + [ast.upda] + ast.loop.member), [[init]] + c)

    def visitForEach(self, ast: ForEach, c) -> None:
        arr_type = self.visit(ast.arr, c)
        if not isinstance(arr_type, ArrayType):
            raise TypeMismatch(ast)

        for_idx_type = self.visit(ast.idx, c)
        for_value_type = self.visit(ast.value, c)

        if not self.compareType(for_idx_type, IntType()):
            raise TypeMismatch(ast)

        if isinstance(for_value_type, ArrayType):
            if not self.compareType(
                for_value_type, ArrayType(arr_type.dimens[1:], arr_type.eleType)
            ):
                raise TypeMismatch(ast)
        elif not self.compareType(for_value_type, arr_type.eleType):
            raise TypeMismatch(ast)

        self.visit(Block(ast.loop.member), c)

    def visitBlock(self, ast: Block, c) -> None:
        reduce(
            lambda acc, ele: [
                (
                    [result] + acc[0]
                    if isinstance(
                        result := (
                            self.visit(ele, (acc, True))
                            if isinstance(ele, (MethCall, FuncCall))
                            else self.visit(ele, acc)
                        ),
                        Symbol,
                    )
                    else acc[0]
                )
            ]
            + acc[1:],
            ast.member,
            [[]] + c,
        )

    def visitIf(self, ast: If, c):
        if not isinstance(self.visit(ast.expr, c), BoolType):
            raise TypeMismatch(ast)
        self.visit(Block(ast.thenStmt.member), c)
        if ast.elseStmt:
            self.visit(ast.elseStmt, c)

    def visitIntType(self, ast, c) -> Type:
        return IntType()

    def visitFloatType(self, ast, c) -> Type:
        return FloatType()

    def visitBoolType(self, ast, c) -> Type:
        return BoolType()

    def visitStringType(self, ast, c) -> Type:
        return StringType()

    def visitVoidType(self, ast, c) -> Type:
        return VoidType()

    def visitArrayType(self, ast: ArrayType, c) -> Type:
        list(map(lambda ele: self.derive_value(self.visit(ele, c)), ast.dimens))
        return ast

    def visitAssign(self, ast: Assign, c):
        if isinstance(ast.lhs, Id):
            if (
                next(
                    filter(
                        lambda symbol: symbol.name == ast.lhs.name,
                        reduce(lambda acc, ele: acc + ele, c, []),
                    ),
                    None,
                )
                is None
            ):
                return Symbol(ast.lhs.name, self.visit(ast.rhs, c), None)

        lhs_type = self.visit(ast.lhs, c)
        rhs_type = self.visit(ast.rhs, c)

        if not self.compareType(
            lhs_type, rhs_type, [(FloatType, IntType), (InterfaceType, StructType)], c
        ):
            raise TypeMismatch(ast)

    def visitContinue(self, ast, c):
        return ast

    def visitBreak(self, ast, c):
        return ast

    def visitReturn(self, ast: Return, c):
        if not self.compareType(
            self.current_func.retType,
            self.visit(ast.expr, c) if ast.expr else VoidType(),
        ):
            raise TypeMismatch(ast)

    def visitBinaryOp(self, ast: BinaryOp, c) -> Type:
        lhs_type = self.visit(ast.left, c)
        rhs_type = self.visit(ast.right, c)

        if ast.op == "+":
            if self.compareType(
                lhs_type, rhs_type, [(FloatType, IntType), (IntType, FloatType)]
            ):
                if isinstance(lhs_type, StringType):
                    return StringType()
                elif isinstance(lhs_type, IntType) and isinstance(rhs_type, IntType):
                    return IntType()
                elif isinstance(lhs_type, FloatType) or isinstance(rhs_type, FloatType):
                    return FloatType()
        elif ast.op in ("-", "*", "/"):
            if self.compareType(
                lhs_type, rhs_type, [(FloatType, IntType), (IntType, FloatType)]
            ):
                if isinstance(lhs_type, IntType) and isinstance(rhs_type, IntType):
                    return IntType()
                elif isinstance(lhs_type, FloatType) or isinstance(rhs_type, FloatType):
                    return FloatType()
        elif ast.op == "%":
            if self.compareType(lhs_type, rhs_type):
                if isinstance(lhs_type, IntType) and isinstance(rhs_type, IntType):
                    return IntType()

        elif ast.op in ("==", "!=", "<", ">", "<=", ">="):
            if self.compareType(lhs_type, rhs_type):
                if isinstance(lhs_type, (IntType, FloatType, StringType)):
                    return BoolType()

        elif ast.op in ("&&", "||"):
            if self.compareType(lhs_type, rhs_type):
                if isinstance(lhs_type, BoolType):
                    return BoolType()

        raise TypeMismatch(ast)

    def visitUnaryOp(self, ast: UnaryOp, c) -> Type:
        exp_type = self.visit(ast.body, c)

        if ast.op == "-":
            if isinstance(exp_type, IntType):
                return IntType()
            if isinstance(exp_type, FloatType):
                return FloatType()

        elif ast.op == "!":
            if isinstance(exp_type, BoolType):
                return BoolType()

        raise TypeMismatch(ast)

    def visitFuncCall(self, ast: FuncCall, c) -> Type:
        stmt = False
        if isinstance(c, tuple):
            c, stmt = c

        func = None
        for symbol in reduce(lambda acc, ele: acc + ele, c, []):
            if symbol.name == ast.funName:
                if not isinstance(symbol.mtype, MType):
                    raise Undeclared(Function(), ast.funName)
        func = self.lookup(ast.funName, self.func_list, lambda x: x.name)

        if func:
            if len(ast.args) != len(func.params):
                raise TypeMismatch(ast)
            if (stmt and not isinstance(func.retType, VoidType)) or (
                not stmt and isinstance(func.retType, VoidType)
            ):
                raise TypeMismatch(ast)

            for arg, param in zip(ast.args, func.params):
                param_type = (
                    param
                    if isinstance(param, ArrayType)
                    else (
                        self.lookup(
                            param.parType.name, self.type_list, lambda x: x.name
                        )
                        if isinstance(param.parType, Id)
                        else param.parType
                    )
                )
                arg_type = self.visit(arg, c)

                if (
                    isinstance(arg_type, (StructType, InterfaceType))
                    and arg_type.name == ""
                ):
                    continue

                if not self.compareType(param_type, arg_type, [], c):
                    raise TypeMismatch(ast)
            return func.retType

        raise Undeclared(Function(), ast.funName)

    def visitMethCall(self, ast: MethCall, c) -> Type:
        stmt = False
        if isinstance(c, tuple):
            c, stmt = c

        recType = self.visit(ast.receiver, c)
        if isinstance(recType, Id):
            recType = self.lookup(recType.name, self.type_list, lambda x: x.name)

        if not isinstance(recType, (StructType, InterfaceType)):
            raise TypeMismatch(ast)

        if isinstance(recType, StructType):
            found_method = self.lookup(
                ast.metName, recType.methods, lambda x: x.fun.name
            )
        else:
            found_method = self.lookup(ast.metName, recType.methods, lambda x: x.name)

        if found_method:
            if isinstance(recType, StructType):
                found_method = found_method.fun
            if len(ast.args) != len(found_method.params):
                raise TypeMismatch(ast)
            if (stmt and not isinstance(found_method.retType, VoidType)) or (
                not stmt and isinstance(found_method.retType, VoidType)
            ):
                raise TypeMismatch(ast)
            for arg, param in zip(ast.args, found_method.params):
                param_type = (
                    param
                    if isinstance(param, ArrayType)
                    else (
                        self.lookup(
                            param.parType.name, self.type_list, lambda x: x.name
                        )
                        if isinstance(param.parType, Id)
                        else param.parType
                    )
                )
                arg_type = self.visit(arg, c)
                if (
                    isinstance(arg_type, (StructType, InterfaceType))
                    and arg_type.name == ""
                ):
                    continue
                if not self.compareType(param_type, arg_type, [], c):
                    raise TypeMismatch(ast)

            return found_method.retType

        raise Undeclared(Method(), ast.metName)

    def visitId(self, ast: Id, c):
        symbol = next(
            filter(
                lambda symbol: symbol.name == ast.name,
                reduce(lambda acc, ele: acc + ele, c, []),
            ),
            None,
        )

        if symbol is None:
            raise Undeclared(Identifier(), ast.name)

        if isinstance(symbol.mtype, Id):
            return next(
                filter(lambda type: type.name == symbol.mtype.name, self.type_list),
                None,
            )
        else:
            return symbol.mtype

    def visitArrayCell(self, ast: ArrayCell, c):
        array_type = self.visit(ast.arr, c)
        if not isinstance(array_type, ArrayType):
            raise TypeMismatch(ast)

        if not all(
            map(lambda ele: self.compareType(self.visit(ele, c), IntType()), ast.idx)
        ):
            raise TypeMismatch(ast)

        if len(array_type.dimens) == len(ast.idx):
            return array_type.eleType
        elif len(array_type.dimens) > len(ast.idx):
            return ArrayType(array_type.dimens[len(ast.idx) :], array_type.eleType)

        raise TypeMismatch(ast)

    def visitFieldAccess(self, ast: FieldAccess, c) -> Type:
        recType = self.visit(ast.receiver, c)

        if isinstance(recType, Id):
            recType = self.lookup(recType.name, self.type_list, lambda x: x.name)

        if not isinstance(recType, StructType):
            raise TypeMismatch(ast)

        field = self.lookup(ast.field, recType.elements, lambda x: x[0])
        if field is None:
            raise Undeclared(Field(), ast.field)

        return field[1]

    def visitIntLiteral(self, ast: IntLiteral, c):
        return IntType()

    def visitFloatLiteral(self, ast: FloatLiteral, c):
        return FloatType()

    def visitBooleanLiteral(self, ast: BooleanLiteral, c):
        return BoolType()

    def visitStringLiteral(self, ast: StringLiteral, c):
        return StringType()

    def visitArrayLiteral(self, ast: ArrayLiteral, c):
        def visit_array_element(ele, c):
            if isinstance(ele, list):
                list(map(lambda e: visit_array_element(e, c), ele))
            else:
                self.visit(ele, c)

        visit_array_element(ast.value, c)
        return ArrayType(ast.dimens, ast.eleType)

    def visitStructLiteral(self, ast: StructLiteral, c):
        found = self.lookup(
            ast.name,
            filter(lambda type: isinstance(type, StructType), self.type_list),
            lambda x: x.name,
        )
        if not found:
            raise Undeclared(Type(), ast.name)
        list(map(lambda value: self.visit(value[1], c), ast.elements))
        return found

    def visitNilLiteral(self, ast: NilLiteral, c) -> Type:
        return StructType("", [], [])
