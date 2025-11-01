"""
*   @author Nguyen Hua Phung
*   @version 1.0
*   23/10/2015
*   This file provides a simple version of code generator
*
"""

from Utils import *
from StaticCheck import *
from StaticError import *
from Emitter import Emitter
from Frame import Frame
from abc import ABC, abstractmethod
from functools import reduce


class Val(ABC):
    pass


class Index(Val):
    def __init__(self, value):
        # value: Int

        self.value = value


class CName(Val):
    def __init__(self, value, isStatic=True):
        # value: String
        self.isStatic = isStatic
        self.value = value


class ClassType(Type):
    def __init__(self, name):
        # value: Id
        self.name = name


class CodeGenerator(BaseVisitor, Utils):
    def __init__(self):
        self.className = "MiniGoClass"
        self.astTree = None
        self.path = None
        self.emit = None
        self.current_func: FuncDecl = None
        self.current_arr_cell_type = None
        self.current_type: StructType = None
        self.type_list = {}

        self.function_list = []

    def init(self):
        mem = [
            Symbol("getInt", MType([], IntType()), CName("io", True)),
            Symbol("putInt", MType([IntType()], VoidType()), CName("io", True)),
            Symbol("putIntLn", MType([IntType()], VoidType()), CName("io", True)),
            Symbol("getFloat", MType([], FloatType()), CName("io", True)),
            Symbol("putFloat", MType([FloatType()], VoidType()), CName("io", True)),
            Symbol("putFloatLn", MType([FloatType()], VoidType()), CName("io", True)),
            Symbol("getBool", MType([], BoolType()), CName("io", True)),
            Symbol("putBool", MType([BoolType()], VoidType()), CName("io", True)),
            Symbol("putBoolLn", MType([BoolType()], VoidType()), CName("io", True)),
            Symbol("getString", MType([], StringType()), CName("io", True)),
            Symbol("putString", MType([StringType()], VoidType()), CName("io", True)),
            Symbol("putStringLn", MType([StringType()], VoidType()), CName("io", True)),
            Symbol("putLn", MType([], VoidType()), CName("io", True)),
        ]
        return mem

    def gen(self, ast, dir_):
        gl = self.init()
        self.astTree = ast
        self.path = dir_
        self.emit = Emitter(dir_ + "/" + self.className + ".j")
        self.visit(ast, gl)

    def emitObjectInit(self):
        frame = Frame("<init>", VoidType())
        self.emit.printout(
            self.emit.emitMETHOD("<init>", MType([], VoidType()), False, False, frame)
        )  # Bắt đầu định nghĩa phương thức <init>
        frame.enterScope(True)
        self.emit.printout(
            self.emit.emitVAR(
                frame.getNewIndex(),
                "this",
                ClassType(self.className),
                frame.getStartLabel(),
                frame.getEndLabel(),
                frame,
            )
        )  # Tạo biến "this" trong phương thức <init>

        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        self.emit.printout(
            self.emit.emitREADVAR("this", ClassType(self.className), 0, frame)
        )
        self.emit.printout(self.emit.emitINVOKESPECIAL(frame))
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()

    def emitObjectCInit(self, ast, o):
        frame = Frame("<clinit>", VoidType())
        self.emit.printout(
            self.emit.emitMETHOD("<clinit>", MType([], VoidType()), True, False, frame)
        )
        frame.enterScope(True)
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        o["frame"] = frame
        self.visit(
            Block(
                [
                    (
                        Assign(Id(decl.varName), decl.varInit)
                        if isinstance(decl, VarDecl)
                        else Assign(Id(decl.conName), decl.iniExpr)
                    )
                    for decl in ast.decl
                    if isinstance(decl, (VarDecl, ConstDecl))
                ]
            ),
            o,
        )

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()

    def visitProgram(self, ast, c):
        self.type_list = {
            type_decl.name: type_decl
            for type_decl in list(
                filter(
                    lambda decl: isinstance(decl, (StructType, InterfaceType)), ast.decl
                )
            )
        }
        [
            self.type_list[m.recType.name].methods.append(m)
            for m in ast.decl
            if isinstance(m, MethodDecl)
        ]
        self.function_list = c + [
            Symbol(
                decl.name,
                MType(list(map(lambda x: x.parType, decl.params)), decl.retType),
                CName(ClassType(self.className)),
            )
            for decl in ast.decl
            if isinstance(decl, FuncDecl)
        ]
        env = {}
        env["env"] = [c]
        self.emit.printout(self.emit.emitPROLOG(self.className, "java.lang.Object"))
        env = reduce(
            lambda a, x: self.visit(x, a) if isinstance(x, (VarDecl, ConstDecl)) else a,
            ast.decl,
            env,
        )
        glob = env["env"][0]
        env["env"] = [[]]
        for decl in ast.decl:
            if isinstance(decl, (VarDecl)):
                symbol = self.lookup(decl.varName, glob, lambda x: x.name)
                env["env"][0] = env["env"][0] + [symbol]
            if isinstance(decl, (ConstDecl)):
                symbol = self.lookup(decl.conName, glob, lambda x: x.name)
                env["env"][0] = env["env"][0] + [symbol]
            if isinstance(decl, FuncDecl):
                self.visit(decl, env)
        self.emitObjectInit()
        self.emitObjectCInit(ast, env)
        self.emit.printout(self.emit.emitEPILOG())
        for type in self.type_list.values():
            self.current_type = type
            self.emit = Emitter(self.path + "/" + type.name + ".j")
            if isinstance(self.current_type, StructType):
                type_o = {"env": env["env"], "frame": Frame("struct", VoidType())}
            else:
                type_o = {"env": env["env"]}
            self.visit(type, type_o)

        return env

    # ----------------------------------------------- #
    # =-=-=-=-=-=-=-=-= Declaration =-=-=-=-=-=-=-=-= #
    # ----------------------------------------------- #

    def visitVarDecl(self, ast, o):
        def default_init(var_type, o):
            if isinstance(var_type, IntType):
                return IntLiteral(0)
            elif isinstance(var_type, FloatType):
                return FloatLiteral(0.0)
            elif isinstance(var_type, StringType):
                return StringLiteral('""')
            elif isinstance(var_type, BoolType):
                return BooleanLiteral("false")

        if not ast.varInit:
            if isinstance(ast.varType, ArrayType):
                var_init = ArrayLiteral(
                    ast.varType.dimens, ast.varType.eleType, ast.varType
                )
            elif isinstance(ast.varType, Id):
                var_init = StructLiteral(ast.varType.name, [])
            else:
                var_init = default_init(ast.varType, o)
            ast.varInit = var_init

        env = o.copy()
        env["frame"] = Frame("var_decl", VoidType())
        right_code, right_type = self.visit(ast.varInit, env)

        if not ast.varType:
            ast.varType = right_type

        if "frame" not in o:  # global var
            o["env"][0] = [
                Symbol(ast.varName, ast.varType, CName(ClassType(self.className)))
            ] + o["env"][0]
            self.emit.printout(
                self.emit.emitATTRIBUTE(
                    ast.varName,
                    ast.varType,
                    True,
                    False,
                    None,
                )
            )
        else:
            right_code, right_type = self.visit(ast.varInit, o)
            index = o["frame"].getNewIndex()
            o["env"][0] = [Symbol(ast.varName, ast.varType, Index(index))] + o["env"][0]
            self.emit.printout(
                self.emit.emitVAR(
                    index,
                    ast.varName,
                    ast.varType,
                    o["frame"].getStartLabel(),
                    o["frame"].getEndLabel(),
                    o["frame"],
                )
            )
            if isinstance(ast.varType, FloatType) and isinstance(right_type, IntType):
                right_code = right_code + self.emit.emitI2F(o["frame"])
            elif isinstance(ast.varType, IntType) and isinstance(right_type, FloatType):
                right_code = self.emit.emitI2F(o["frame"]) + right_code
            self.emit.printout(right_code)
            self.emit.printout(
                self.emit.emitWRITEVAR(ast.varName, ast.varType, index, o["frame"])
            )
        return o

    def visitParamDecl(self, ast, o):
        frame = o["frame"]
        index = frame.getNewIndex()
        o["env"][0].append(Symbol(ast.parName, ast.parType, Index(index)))
        self.emit.printout(
            self.emit.emitVAR(
                index,
                ast.parName,
                ast.parType,
                frame.getStartLabel(),
                frame.getEndLabel(),
                frame,
            )
        )
        return o

    def visitConstDecl(self, ast, o):
        return self.visit(VarDecl(ast.conName, ast.conType, ast.iniExpr), o)

    def visitFuncDecl(self, ast, o):
        self.current_func = ast

        isMain = ast.name == "main"
        if isMain:
            func_type = MType([ArrayType([None], StringType())], VoidType())
        else:
            func_type = MType([param.parType for param in ast.params], ast.retType)

        o["env"][0] += [Symbol(ast.name, func_type, CName(ClassType(self.className)))]

        frame = Frame(ast.name, ast.retType)
        env = o.copy()
        env["frame"] = frame
        self.emit.printout(
            self.emit.emitMETHOD(ast.name, func_type, True, False, frame)
        )

        frame.enterScope(True)
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))
        env["env"] = [[]] + env["env"]

        if isMain:
            self.emit.printout(
                self.emit.emitVAR(
                    frame.getNewIndex(),
                    "args",
                    ArrayType([None], StringType()),
                    frame.getStartLabel(),
                    frame.getEndLabel(),
                    frame,
                )
            )
        else:
            env = reduce(lambda acc, e: self.visit(e, acc), ast.params, env)

        self.visit(ast.body, env)
        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if type(ast.retType) is VoidType:
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))
        frame.exitScope()
        return o

    def visitMethodDecl(self, ast, o):
        index = 0
        for decl in self.astTree.decl:
            if isinstance(decl, MethodDecl) and decl.fun.name == ast.fun.name:
                break
            if isinstance(decl, (VarDecl, ConstDecl)):
                index += 1

        glob = o["env"][0]
        env = o.copy()
        frame = Frame(ast.fun.name, ast.fun.retType)
        env["frame"] = frame
        env["env"] = [[]] + [glob[:index]]

        self.current_func = ast.fun
        func_type = MType([param.parType for param in ast.fun.params], ast.fun.retType)

        self.emit.printout(
            self.emit.emitMETHOD(ast.fun.name, func_type, False, False, frame)
        )

        frame.enterScope(True)
        self.emit.printout(
            self.emit.emitVAR(
                frame.getNewIndex(),
                "this",
                Id(self.current_type.name),
                frame.getStartLabel(),
                frame.getEndLabel(),
                frame,
            )
        )
        self.emit.printout(self.emit.emitLABEL(frame.getStartLabel(), frame))

        if ast.receiver is None:
            for type in self.type_list.values():
                rec_name = type.name if ast in type.methods else ""

            self.emit.printout(self.emit.emitREADVAR("this", Id(rec_name), 0, frame))
            self.emit.printout(self.emit.emitINVOKESPECIAL(frame))

        env["env"] = [[]] + env["env"]
        env = reduce(lambda acc, e: self.visit(e, acc), ast.fun.params, env)

        self.visit(ast.fun.body, env)

        self.emit.printout(self.emit.emitLABEL(frame.getEndLabel(), frame))
        if isinstance(ast.fun.retType, VoidType):
            self.emit.printout(self.emit.emitRETURN(VoidType(), frame))
        self.emit.printout(self.emit.emitENDMETHOD(frame))

        frame.exitScope()
        return o

    def visitStructType(self, ast, o):
        self.emit.printout(self.emit.emitPROLOG(ast.name, "java.lang.Object", False))
        for interface in self.type_list.values():
            if isinstance(interface, InterfaceType) and compare_type(
                interface, ast, [(InterfaceType, StructType)]
            ):
                self.emit.printout(self.emit.emitIMPLEMENTS(interface.name))

        for field_name, field_type in ast.elements:
            self.emit.printout(
                self.emit.emitATTRIBUTE(field_name, field_type, False, False, False)
            )
        self.current_type = ast
        self.visit(
            MethodDecl(
                None,
                None,
                FuncDecl(
                    "<init>",
                    [
                        ParamDecl(field_name, field_type)
                        for field_name, field_type in ast.elements
                    ],
                    VoidType(),
                    Block(
                        [
                            Assign(FieldAccess(Id("this"), field_name), Id(field_name))
                            for field_name, _ in ast.elements
                        ]
                    ),
                ),
            ),
            o,
        )
        self.visit(
            MethodDecl(
                None,
                None,
                FuncDecl("<init>", [], VoidType(), Block([])),
            ),
            o,
        )

        for method in ast.methods:
            self.visit(method, o)

        self.emit.printout(self.emit.emitEPILOG())
        self.current_type = None

    def visitInterfaceType(self, ast, o):
        self.emit.printout(self.emit.emitPROLOG(ast.name, "java.lang.Object", True))
        for method in ast.methods:
            self.emit.printout(
                self.emit.emitMETHOD(
                    method.name,
                    MType([param for param in method.params], method.retType),
                    False,
                    True,
                    None,
                )
            )
            self.emit.printout(self.emit.emitENDMETHOD(None))
        self.emit.printout(self.emit.emitEPILOG())

    # ----------------------------------------------- #
    # =-=-=-=-=-=-=-=-=- Statement -=-=-=-=-=-=-=-=-= #
    # ----------------------------------------------- #

    def visitBlock(self, ast, o):
        env = o.copy()
        env["env"] = [[]] + env["env"]
        env["frame"].enterScope(False)

        self.emit.printout(
            self.emit.emitLABEL(env["frame"].getStartLabel(), env["frame"])
        )

        for stmt in ast.member:
            if isinstance(stmt, (FuncCall, MethCall)):
                env["stmt"] = True
            env = self.visit(stmt, env)

        self.emit.printout(
            self.emit.emitLABEL(env["frame"].getEndLabel(), env["frame"])
        )
        env["frame"].exitScope()
        return o

    def visitAssign(self, ast, o):
        if isinstance(ast.lhs, Id) and not next(
            filter(
                lambda s: s.name == ast.lhs.name,
                [sym for scope in o["env"] for sym in scope],
            ),
            None,
        ):
            return self.visit(VarDecl(ast.lhs.name, None, ast.rhs), o)

        if isinstance(ast.lhs, FieldAccess):
            left_code, left_type = self.visit(ast.lhs.receiver, o)
            type = self.type_list[left_type.name]
            field_name, field_type = next(
                filter(lambda field: field[0] == ast.lhs.field, type.elements), None
            )
            right_code, right_type = self.visit(ast.rhs, o)

            if isinstance(field_type, IntType) and isinstance(right_type, FloatType):
                left_code = left_code + self.emit.emitI2F(o["frame"])
            elif isinstance(field_type, FloatType) and isinstance(right_type, IntType):
                right_code = right_code + self.emit.emitI2F(o["frame"])

            self.emit.printout(left_code)
            self.emit.printout(right_code)
            self.emit.printout(
                self.emit.emitPUTFIELD(
                    type.name + "/" + field_name, field_type, o["frame"]
                )
            )

        elif isinstance(ast.lhs, Id) and not next(
            filter(
                lambda s: s.name == ast.lhs.name,
                [sym for scope in o["env"] for sym in scope],
            ),
            None,
        ):
            return self.visit(VarDecl(ast.lhs.name, None, ast.rhs), o)

        elif isinstance(ast.lhs, ArrayCell):
            o["isLeft"] = True
            left_code, left_type = self.visit(ast.lhs, o)
            o["isLeft"] = False
            right_code, right_type = self.visit(ast.rhs, o)

            if isinstance(left_type, IntType) and isinstance(right_type, FloatType):
                left_code = left_code + self.emit.emitI2F(o["frame"])
            elif isinstance(left_type, FloatType) and isinstance(right_type, IntType):
                right_code = right_code + self.emit.emitI2F(o["frame"])
            self.emit.printout(left_code)
            self.emit.printout(right_code)
            self.emit.printout(
                self.emit.emitASTORE(self.current_arr_cell_type, o["frame"])
            )
        else:
            right_code, right_type = self.visit(ast.rhs, o)
            o["isLeft"] = True
            left_code, left_type = self.visit(ast.lhs, o)
            o["isLeft"] = False
            if isinstance(left_type, IntType) and isinstance(right_type, FloatType):
                left_code = left_code + self.emit.emitI2F(o["frame"])
            elif isinstance(left_type, FloatType) and isinstance(right_type, IntType):
                right_code = right_code + self.emit.emitI2F(o["frame"])
            self.emit.printout(right_code)
            self.emit.printout(left_code)

        return o

    def visitFuncCall(self, ast, o):
        sym = next(filter(lambda x: x.name == ast.funName, self.function_list), None)
        if o.get("stmt"):
            o["stmt"] = False
            [self.emit.printout(self.visit(x, o)[0]) for x in ast.args]
            self.emit.printout(
                self.emit.emitINVOKESTATIC(
                    f"{sym.value.value if not isinstance(sym.value.value, ClassType) else sym.value.value.name}/{ast.funName}",
                    sym.mtype,
                    o["frame"],
                )
            )
            return o
        else:
            code = "".join([str(self.visit(x, o)[0]) for x in ast.args])
            code += self.emit.emitINVOKESTATIC(
                f"{sym.value.value if not isinstance(sym.value.value, ClassType) else sym.value.value.name}/{ast.funName}",
                sym.mtype,
                o["frame"],
            )
            return code, sym.mtype.rettype

    def visitMethCall(self, ast, o):
        code = list()
        rec_code, rec_type = self.visit(ast.receiver, o)
        code.append(rec_code)

        if isinstance(rec_type, Id):
            rec_type = self.type_list[rec_type.name]

        is_stmt = o.get("stmt", False)

        for arg in ast.args:
            code.append(self.visit(arg, o)[0])

        ret_type = None

        if isinstance(rec_type, StructType):
            method = next(
                (
                    method.fun
                    for method in self.type_list[rec_type.name].methods
                    if method.fun.name == ast.metName
                ),
                None,
            )
            ret_type = method.retType
            mtype = MType([param.parType for param in method.params], ret_type)
            code.append(
                self.emit.emitINVOKEVIRTUAL(
                    rec_type.name + "/" + ast.metName, mtype, o["frame"]
                )
            )

        elif isinstance(rec_type, InterfaceType):
            method = next(
                method
                for method in self.type_list[rec_type.name].methods
                if method.name == ast.metName
            )

            ret_type = method.retType
            mtype = MType([param for param in method.params], ret_type)
            code.append(
                self.emit.emitINVOKEINTERFACE(
                    rec_type.name + "/" + ast.metName,
                    mtype,
                    1 + len(method.params),
                    o["frame"],
                )
            )

        if is_stmt:
            o["stmt"] = False
            self.emit.printout("".join(code))
            return o
        else:
            return "".join(code), ret_type

    def visitIf(self, ast, o):
        exit_label = o["frame"].getNewLabel()
        false_label = o["frame"].getNewLabel()
        cond_code, _ = self.visit(ast.expr, o)
        self.emit.printout(cond_code)
        self.emit.printout(self.emit.emitIFFALSE(false_label, o["frame"]))
        self.visit(ast.thenStmt, o)
        self.emit.printout(self.emit.emitGOTO(exit_label, o["frame"]))
        self.emit.printout(self.emit.emitLABEL(false_label, o["frame"]))
        if ast.elseStmt is not None:
            self.visit(ast.elseStmt, o)
        self.emit.printout(self.emit.emitLABEL(exit_label, o["frame"]))
        return o

    def visitForBasic(self, ast, o):
        env = o.copy()
        env["env"] = [[]] + o["env"]
        env["frame"].enterLoop()
        cont_label = env["frame"].getContinueLabel()
        break_label = env["frame"].brkLabel[-1]
        self.emit.printout(self.emit.emitLABEL(cont_label, env["frame"]))
        self.emit.printout(self.visit(ast.cond, o)[0])
        self.emit.printout(self.emit.emitIFFALSE(break_label, env["frame"]))
        self.visit(ast.loop, env)
        self.emit.printout(self.emit.emitGOTO(cont_label, env["frame"]))
        self.emit.printout(self.emit.emitLABEL(break_label, env["frame"]))
        env["frame"].exitLoop()
        return o

    def visitForStep(self, ast, o):
        env = o.copy()
        env["env"] = [[]] + o["env"]
        env["frame"].enterLoop()
        cont_label = env["frame"].getContinueLabel()
        break_label = env["frame"].brkLabel[-1]
        cond_label = env["frame"].getNewLabel()
        self.visit(ast.init, env)
        self.emit.printout(self.emit.emitLABEL(cond_label, env["frame"]))
        self.emit.printout(self.visit(ast.cond, env)[0])
        self.emit.printout(self.emit.emitIFFALSE(break_label, env["frame"]))
        self.visit(ast.loop, env)
        self.emit.printout(self.emit.emitLABEL(cont_label, env["frame"]))
        self.visit(ast.upda, env)
        self.emit.printout(self.emit.emitGOTO(cond_label, env["frame"]))
        self.emit.printout(self.emit.emitLABEL(break_label, env["frame"]))
        env["frame"].exitLoop()
        return o

    def visitForEach(self, ast, o):
        return o

    def visitContinue(self, ast, o):
        self.emit.printout(
            self.emit.emitGOTO(o["frame"].getContinueLabel(), o["frame"])
        )
        return o

    def visitReturn(self, ast, o):
        if ast.expr:
            self.emit.printout(self.visit(ast.expr, o)[0])
        self.emit.printout(self.emit.emitRETURN(self.current_func.retType, o["frame"]))
        return o

    def visitBreak(self, ast, o):
        self.emit.printout(self.emit.emitGOTO(o["frame"].getBreakLabel(), o["frame"]))
        return o

    # ----------------------------------------------- #
    # =-=-=-=-=-=-=-=-=-= Literal =-=-=-=-=-=-=-=-=-= #
    # ----------------------------------------------- #

    def visitIntLiteral(self, ast, o):
        return self.emit.emitPUSHICONST(ast.value, o["frame"]), IntType()

    def visitFloatLiteral(self, ast, o):
        return self.emit.emitPUSHFCONST(str(ast.value), o["frame"]), FloatType()

    def visitBooleanLiteral(self, ast, o):
        return self.emit.emitPUSHICONST(ast.value, o["frame"]), BoolType()

    def visitStringLiteral(self, ast, o):
        return (
            self.emit.emitPUSHCONST(str(ast.value), StringType(), o["frame"]),
            StringType(),
        )

    def visitArrayLiteral(self, ast, o):
        def visitNestedList(item, o):
            if not isinstance(item, list):
                return self.visit(item, o)

            code = list()
            code.append(self.emit.emitPUSHCONST(len(item), IntType(), o["frame"]))

            if not isinstance(item[0], list):  # 1-dimensional array
                ele_type = self.visit(item[0], o)[1]
                code.append(self.emit.emitNEWARRAY(ele_type, o["frame"]))
                for idx, ele in enumerate(item):
                    code.append((self.emit.emitDUP(o["frame"])))
                    code.append(self.emit.emitPUSHICONST(idx, o["frame"]))
                    code.append(self.visit(ele, o)[0])
                    code.append(self.emit.emitASTORE(ele_type, o["frame"]))
                return "".join(code), ArrayType([len(item)], ele_type)
            else:  # multi-dimensional array
                ele_type = visitNestedList(item[0], o)[1]  # type = ArrayType
                code.append(self.emit.emitANEWARRAY(ele_type.eleType, o["frame"]))
                for idx, ele in enumerate(item):
                    code.append(self.emit.emitDUP(o["frame"]))
                    code.append(self.emit.emitPUSHICONST(idx, o["frame"]))
                    code.append(visitNestedList(ele, o)[0])
                    code.append(self.emit.emitASTORE(ele_type, o["frame"]))
                return "".join(code), ArrayType([len(item)], ele_type)

        if isinstance(ast.value, ArrayType):
            return self.visit(ast.value, o)

        return visitNestedList(ast.value, o)

    def visitStructLiteral(self, ast, o):
        code = list()
        code.append(self.emit.emitNEW(ast.name, o["frame"]))
        code.append(self.emit.emitDUP(o["frame"]))

        ele_types = []
        for ele in ast.elements:
            ele_code, ele_type = self.visit(ele[1], o)
            code.append(ele_code)
            ele_types.append(ele_type)

        # type = (
        #     MType(ele_types, Id(ast.name))
        #     if len(ast.elements)
        #     else MType([], VoidType())
        # )
        type = MType(ele_types, VoidType())
        code.append(self.emit.emitINVOKESPECIAL(o["frame"], f"{ast.name}/<init>", type))
        return "".join(code), Id(ast.name)

    def visitNilLiteral(self, ast, o):
        return self.emit.emitPUSHNULL(o["frame"]), Id("")

    # ----------------------------------------------- #
    # =-=-=-=-=-=-=-=-= Expressions =-=-=-=-=-=-=-=-= #
    # ----------------------------------------------- #

    def visitBinaryOp(self, ast, o):
        left_code, left_type = self.visit(ast.left, o)
        right_code, right_type = self.visit(ast.right, o)

        if ast.op in {"+", "-"} and isinstance(left_type, (FloatType, IntType)):
            code = left_code + right_code
            ret_type = (
                IntType()
                if not any(
                    isinstance(type, FloatType) for type in [left_type, right_type]
                )
                else FloatType()
            )
            if isinstance(left_type, IntType) and isinstance(right_type, FloatType):
                code = left_code + self.emit.emitI2F(o["frame"]) + right_code
                ret_type = FloatType()
            elif isinstance(left_type, FloatType) and isinstance(right_type, IntType):
                code = left_code + right_code + self.emit.emitI2F(o["frame"])
                ret_type = FloatType()
            return code + self.emit.emitADDOP(ast.op, ret_type, o["frame"]), ret_type

        if ast.op == "+" and isinstance(left_type, StringType):
            return (
                left_code
                + right_code
                + self.emit.emitINVOKEVIRTUAL(
                    "java/lang/String/concat",
                    MType(
                        [
                            StringType(),
                        ],
                        StringType(),
                    ),
                    o["frame"],
                ),
                StringType(),
            )

        elif ast.op in {"*", "/"}:
            code = left_code + right_code
            ret_type = (
                IntType()
                if not any(
                    isinstance(type, FloatType) for type in [left_type, right_type]
                )
                else FloatType()
            )
            if isinstance(left_type, IntType) and isinstance(right_type, FloatType):
                code = left_code + self.emit.emitI2F(o["frame"]) + right_code
                ret_type = FloatType()
            elif isinstance(left_type, FloatType) and isinstance(right_type, IntType):
                code = left_code + right_code + self.emit.emitI2F(o["frame"])
                ret_type = FloatType()
            return code + self.emit.emitMULOP(ast.op, ret_type, o["frame"]), ret_type

        elif ast.op == "%":
            return (
                left_code + right_code + self.emit.emitMOD(o["frame"]),
                IntType(),
            )

        elif ast.op in {"==", "!=", "<", "<=", ">", ">="} and isinstance(
            left_type, (FloatType, IntType)
        ):
            return (
                left_code
                + right_code
                + self.emit.emitREOP(ast.op, left_type, o["frame"])
            ), BoolType()
        elif ast.op in {"==", "!=", "<", "<=", ">", ">="} and isinstance(
            left_type, StringType
        ):
            return (
                left_code
                + right_code
                + self.emit.emitINVOKEVIRTUAL(
                    "java/lang/String/compareTo",
                    MType(
                        [StringType()],
                        IntType(),
                    ),
                    o["frame"],
                )
                + self.emit.emitPUSHICONST(0, o["frame"])
                + self.emit.emitREOP(ast.op, IntType(), o["frame"])
            ), BoolType()

        elif ast.op == "||":
            return (
                left_code + right_code + self.emit.emitOROP(o["frame"]),
                BoolType(),
            )
        elif ast.op == "&&":
            return (
                left_code + right_code + self.emit.emitANDOP(o["frame"]),
                BoolType(),
            )

    def visitUnaryOp(self, ast, o):
        code, ret_type = self.visit(ast.body, o)
        if ast.op == "!":
            return code + self.emit.emitNOT(BoolType(), o["frame"]), BoolType()
        elif ast.op == "-":
            return code + self.emit.emitNEGOP(ret_type, o["frame"]), ret_type

    def visitArrayCell(self, ast, o):
        env = o.copy()
        env["isLeft"] = False
        code = list()
        arr_code, arr_type = self.visit(ast.arr, env)
        code.append(arr_code)

        for ele in ast.idx[:-1]:
            ele_code, ele_type = self.visit(ele, env)
            code.append(ele_code)
            code.append(self.emit.emitALOAD(arr_type, o["frame"]))
        code.append(self.visit(ast.idx[-1], env)[0])

        if o.get("isLeft"):
            self.current_arr_cell_type = (
                arr_type.eleType if len(arr_type.dimens) == len(ast.idx) else arr_type
            )
            return "".join(code), arr_type.eleType
        else:
            code.append(self.emit.emitALOAD(arr_type.eleType, o["frame"]))
            return "".join(code), arr_type.eleType

    def visitId(self, ast, o):
        symbol = None
        for scope in o["env"]:
            symbol = self.lookup(ast.name, scope, lambda x: x.name)
            if symbol is not None:
                break

        if symbol is None:
            if o.get("isLeft"):
                return (
                    self.emit.emitWRITEVAR(
                        "this", Id(self.current_type.name), 0, o["frame"]
                    ),
                    self.current_type,
                )
            return (
                self.emit.emitREADVAR(
                    "this", Id(self.current_type.name), 0, o["frame"]
                ),
                self.current_type,
            )

        if o.get("isLeft"):
            if isinstance(symbol.value, Index):
                return (
                    self.emit.emitWRITEVAR(
                        ast.name, symbol.mtype, symbol.value.value, o["frame"]
                    ),
                    symbol.mtype,
                )
            else:
                return (
                    self.emit.emitPUTSTATIC(
                        self.className + "/" + symbol.name,
                        symbol.mtype,
                        o["frame"],
                    ),
                    symbol.mtype,
                )

        else:
            if isinstance(symbol.value, Index):
                return (
                    self.emit.emitREADVAR(
                        ast.name, symbol.mtype, symbol.value.value, o["frame"]
                    ),
                    symbol.mtype,
                )
            else:
                return (
                    self.emit.emitGETSTATIC(
                        self.className + "/" + symbol.name,
                        symbol.mtype,
                        o["frame"],
                    ),
                    symbol.mtype,
                )

    def visitFieldAccess(self, ast, o):
        code, rec_type = self.visit(ast.receiver, o)
        type = self.type_list[rec_type.name]
        field_name, field_type = next(
            filter(lambda field: field[0] == ast.field, type.elements), None
        )
        if o.get("isLeft"):
            return code, field_type
        else:
            return (
                code
                + self.emit.emitGETFIELD(
                    rec_type.name + "/" + field_name, field_type, o["frame"]
                ),
                field_type,
            )

    # ----------------------------------------------- #
    # =-=-=-=-=-=-=-=-=-=- Types -=-=-=-=-=-=-=-=-=-= #
    # ----------------------------------------------- #
    def visitArrayType(self, ast, o):
        code = list()
        for dimen in ast.dimens:
            code.append(self.visit(dimen, o)[0])
        code.append(self.emit.emitMULTIANEWARRAY(ast, o["frame"]))
        return "".join(code), ArrayType


def compare_type(
    left_type,
    right_type,
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
                    for prop_arg, meth_arg in zip(prototype.params, method.fun.params)
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
            (lhs_dim.value == rhs_dim.value)
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

    if isinstance(right_type, StructType) and right_type.name == "":
        return isinstance(left_type, (StructType, InterfaceType))

    left_type = (
        self.lookup(left_type.name, self.type_list.keys(), lambda x: x.name)
        if isinstance(left_type, Id)
        else left_type
    )
    right_type = (
        self.lookup(right_type.name, self.type_list.keys(), lambda x: x.name)
        if isinstance(right_type, Id)
        else right_type
    )

    if (type(left_type), type(right_type)) in convertable_type_sets:
        if isinstance(left_type, InterfaceType) and isinstance(right_type, StructType):
            return check_struct_implementation(left_type, right_type)
        return True

    if type(left_type) == type(right_type) and isinstance(
        left_type, (StructType, InterfaceType)
    ):
        return left_type.name == right_type.name

    if isinstance(left_type, ArrayType) and isinstance(right_type, ArrayType):
        return check_array_type(left_type, right_type)

    return type(left_type) == type(right_type)
