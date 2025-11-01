from typing import get_type_hints
from antlr4 import TerminalNode
from MiniGoVisitor import MiniGoVisitor
from MiniGoParser import MiniGoParser
from AST import *
from functools import reduce


##! continue update
class ASTGeneration(MiniGoVisitor):
    # Visit a parse tree produced by MiniGoParser#varType.
    def visitVarType(self, ctx: MiniGoParser.VarTypeContext):
        if ctx.primType():
            return self.visit(ctx.primType())
        elif ctx.ID():
            return Id(ctx.ID().getText())
        else:
            return self.visit(ctx.arrayType())

    def visitPrimType(self, ctx: MiniGoParser.PrimTypeContext):
        if ctx.INT():
            return IntType()
        elif ctx.FLOAT():
            return FloatType()
        elif ctx.STRING():
            return StringType()
        else:  # ctx.BOOL():
            return BoolType()

    # Visit a parse tree produced by MiniGoParser#dimsType.
    def visitDimsType(self, ctx: MiniGoParser.DimsTypeContext):
        return [self.visit(exp) for exp in ctx.exp()]

    # Visit a parse tree produced by MiniGoParser#arrayType.
    def visitArrayType(self, ctx: MiniGoParser.ArrayTypeContext):
        dimens = self.visit(ctx.dimsLit())
        if ctx.INT():
            eleType = IntType()
        elif ctx.FLOAT():
            eleType = FloatType()
        elif ctx.STRING():
            eleType = StringType()
        elif ctx.BOOL():
            eleType = BoolType()
        else:  # ctx.ID():
            eleType = Id(ctx.ID().getText())

        return ArrayType(dimens, eleType)

    # Visit a parse tree produced by MiniGoParser#seminl.
    def visitSeminl(self, ctx: MiniGoParser.SeminlContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by MiniGoParser#arrVal.
    def visitArrVal(self, ctx: MiniGoParser.ArrValContext):
        if ctx.primitiveLit():
            return self.visit(ctx.primitiveLit())
        elif ctx.structLit():
            return self.visit(ctx.structLit())
        elif ctx.NIL_LIT():
            return NilLiteral()
        else:
            return Id(ctx.ID().getText())

    # Visit a parse tree produced by MiniGoParser#arrInitVal.
    def visitArrInitVal(self, ctx: MiniGoParser.ArrInitValContext):
        if ctx.arrVal():
            return self.visit(ctx.arrVal())
        else:
            return self.visit(ctx.arrInit())

    # Visit a parse tree produced by MiniGoParser#arrInit.
    def visitArrInit(self, ctx: MiniGoParser.ArrInitContext):
        if ctx.arrInit():
            return [self.visit(ctx.arrInitVal())] + self.visit(ctx.arrInit())
        return [self.visit(ctx.arrInitVal())]

    # Visit a parse tree produced by MiniGoParser#dimsLit.
    def visitDimsLit(self, ctx: MiniGoParser.DimsLitContext):
        ele = []
        for child in ctx.children:
            if child.getSymbol().type == MiniGoParser.INT_LIT:
                ele.append(IntLiteral(child.getText()))
            elif child.getSymbol().type == MiniGoParser.ID:
                ele.append(Id(child.getText()))
        return ele

    # Visit a parse tree produced by MiniGoParser#arrayLit.
    def visitArrayLit(self, ctx: MiniGoParser.ArrayLitContext):
        array_type = self.visit(ctx.arrayType())
        dimens = array_type.dimens
        eleType = array_type.eleType
        value = self.visit(ctx.arrInit())

        return ArrayLiteral(dimens, eleType, value)

    # Visit a parse tree produced by MiniGoParser#structField.
    def visitStructField(self, ctx: MiniGoParser.StructFieldContext):
        # elements: List[Tuple[str,Expr]] # [] if there is no elements
        fieldName = ctx.ID().getText()
        fieldType = self.visit(ctx.exp())
        return (fieldName, fieldType)

    # Visit a parse tree produced by MiniGoParser#structFieldList.
    def visitStructFieldList(self, ctx: MiniGoParser.StructFieldListContext):
        if ctx.structFieldList():
            return [self.visit(ctx.structField())] + self.visit(ctx.structFieldList())
        return [self.visit(ctx.structField())]

    # Visit a parse tree produced by MiniGoParser#structLit.
    def visitStructLit(self, ctx: MiniGoParser.StructLitContext):
        name = ctx.ID().getText()
        elements = []
        if ctx.structFieldList():
            elements = self.visit(ctx.structFieldList())

        return StructLiteral(name, elements)

    # Visit a parse tree produced by MiniGoParser#funcCall.
    def visitFuncCall(self, ctx: MiniGoParser.FuncCallContext):
        # funName:str
        # args:List[Expr] # [] if there is no arg

        funName = ctx.ID().getText()
        args = []
        if ctx.expList():
            args = self.visit(ctx.expList())

        return FuncCall(funName, args)

    # Visit a parse tree produced by MiniGoParser#expList.
    def visitExpList(self, ctx: MiniGoParser.ExpListContext):
        if ctx.expList():
            return [self.visit(ctx.exp())] + self.visit(ctx.expList())
        return [self.visit(ctx.exp())]

    # Visit a parse tree produced by MiniGoParser#exp.
    def visitExp(self, ctx: MiniGoParser.ExpContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        op = ctx.getChild(1).getText()
        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        return BinaryOp(op, left, right)

    # Visit a parse tree produced by MiniGoParser#andExp.
    def visitAndExp(self, ctx: MiniGoParser.AndExpContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        op = ctx.getChild(1).getText()
        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        return BinaryOp(op, left, right)

    # Visit a parse tree produced by MiniGoParser#relExp.
    def visitRelExp(self, ctx: MiniGoParser.RelExpContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        op = ctx.getChild(1).getText()
        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        return BinaryOp(op, left, right)

    # Visit a parse tree produced by MiniGoParser#plusMinusExp.
    def visitPlusMinusExp(self, ctx: MiniGoParser.PlusMinusExpContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        op = ctx.getChild(1).getText()
        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        return BinaryOp(op, left, right)

    # Visit a parse tree produced by MiniGoParser#mulDivModExp.
    def visitMulDivModExp(self, ctx: MiniGoParser.MulDivModExpContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        op = ctx.getChild(1).getText()
        left = self.visit(ctx.getChild(0))
        right = self.visit(ctx.getChild(2))
        return BinaryOp(op, left, right)

    # Visit a parse tree produced by MiniGoParser#notNegExp.
    def visitNotNegExp(self, ctx: MiniGoParser.NotNegExpContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))
        op = ctx.getChild(0).getText()
        body = self.visit(ctx.getChild(1))
        return UnaryOp(op, body)

    # Visit a parse tree produced by MiniGoParser#arrStructExp.
    def visitArrStructExp(self, ctx: MiniGoParser.ArrStructExpContext):
        if ctx.getChildCount() == 1:
            return self.visit(ctx.getChild(0))

        elif ctx.getChild(1).getText() == "[":
            arr = self.visit(ctx.getChild(0))
            idx = [self.visit(ctx.getChild(2))]

            if isinstance(arr, ArrayCell):
                lastArr = arr
                arr = lastArr.arr
                idx = lastArr.idx + idx
                # print(f"\n\n\nINDEX: {idx}\n\n\narr: {arr}")

            return ArrayCell(arr, idx)

        elif ctx.LP():
            receiver = self.visit(ctx.getChild(0))
            metName = ctx.ID().getText()
            args = []
            if ctx.expList():
                args = self.visit(ctx.expList())
            return MethCall(receiver, metName, args)

        else:
            receiver = self.visit(ctx.getChild(0))
            field = ctx.ID().getText()
            return FieldAccess(receiver, field)

    # Visit a parse tree produced by MiniGoParser#literalExp.
    def visitLiteralExp(self, ctx: MiniGoParser.LiteralExpContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        elif ctx.primitiveLit():
            return self.visit(ctx.primitiveLit())
        elif ctx.arrayLit():
            return self.visit(ctx.arrayLit())
        elif ctx.structLit():
            return self.visit(ctx.structLit())
        elif ctx.funcCall():
            return self.visit(ctx.funcCall())
        elif ctx.NIL_LIT():
            return NilLiteral()
        else:
            return self.visit(ctx.exp())

    # Visit a parse tree produced by MiniGoParser#primitiveLit.
    def visitPrimitiveLit(self, ctx: MiniGoParser.PrimitiveLitContext):
        if ctx.INT_LIT():
            return IntLiteral(ctx.INT_LIT().getText())
        elif ctx.FLOAT_LIT():
            return FloatLiteral(ctx.FLOAT_LIT().getText())
        elif ctx.STRING_LIT():
            return StringLiteral(ctx.STRING_LIT().getText())
        elif ctx.BOOL_LIT():
            return BooleanLiteral(ctx.BOOL_LIT().getText() == "true")

    # Visit a parse tree produced by MiniGoParser#program.
    def visitProgram(self, ctx: MiniGoParser.ProgramContext):
        decls = self.visit(ctx.declList())
        return Program(decls)

    # Visit a parse tree produced by MiniGoParser#declList.
    def visitDeclList(self, ctx: MiniGoParser.DeclListContext):
        if ctx.declList():
            return self.visit(ctx.declList()) + [self.visit(ctx.decl())]
            # return [self.visit(ctx.decl())] + self.visit(ctx.declList())
        return [self.visit(ctx.decl())]

    # Visit a parse tree produced by MiniGoParser#decl.
    def visitDecl(self, ctx: MiniGoParser.DeclContext):
        return self.visit(ctx.getChild(0))

    # Visit a parse tree produced by MiniGoParser#varDecl.
    def visitVarDecl(self, ctx: MiniGoParser.VarDeclContext):
        varName = ctx.ID().getText()
        varType = None
        varInit = None

        if ctx.varType():
            varType = self.visit(ctx.varType())
        if ctx.varInit():
            varInit = self.visit(ctx.varInit())

        return VarDecl(varName, varType, varInit)

    # Visit a parse tree produced by MiniGoParser#varInit.
    def visitVarInit(self, ctx: MiniGoParser.VarInitContext):
        return self.visit(ctx.exp())

    # Visit a parse tree produced by MiniGoParser#constDecl.
    def visitConstDecl(self, ctx: MiniGoParser.ConstDeclContext):
        conName = ctx.ID().getText()
        conType = None
        iniExpr = self.visit(ctx.exp())

        return ConstDecl(conName, conType, iniExpr)

    # Visit a parse tree produced by MiniGoParser#idList.
    def visitIdList(self, ctx: MiniGoParser.IdListContext):
        if ctx.idList():
            return [ctx.ID().getText()] + self.visit(ctx.idList())
        return [ctx.ID().getText()]

    # Visit a parse tree produced by MiniGoParser#param.
    def visitParam(self, ctx: MiniGoParser.ParamContext):
        parType = self.visit(ctx.varType())

        if ctx.ID():
            parName = ctx.ID().getText()
            return [(parName, parType)]

        idList = self.visit(ctx.idList())
        paramList = [(parName, parType) for parName in idList]
        return paramList

    # Visit a parse tree produced by MiniGoParser#paramList.
    def visitParamList(self, ctx: MiniGoParser.ParamListContext):
        if ctx.paramList():
            return self.visit(ctx.param()) + self.visit(ctx.paramList())
        return self.visit(ctx.param())

    # Visit a parse tree produced by MiniGoParser#receiver.
    def visitReceiver(self, ctx: MiniGoParser.ReceiverContext):
        return (ctx.ID(0).getText(), Id(ctx.ID(1).getText()))

    # Visit a parse tree produced by MiniGoParser#funcFragment.
    def visitFuncFragment(self, ctx: MiniGoParser.FuncFragmentContext):
        name = ctx.ID().getText()
        params = []
        retType = VoidType()
        body = self.visit(ctx.blockStmt())

        if ctx.paramList():
            params = self.visit(ctx.paramList())
            params = [ParamDecl(parName, parType) for parName, parType in params]
        if ctx.varType():
            retType = self.visit(ctx.varType())

        return name, params, retType, body

    # Visit a parse tree produced by MiniGoParser#funcDecl.
    def visitFuncDecl(self, ctx: MiniGoParser.FuncDeclContext):
        # name: str
        # params: List[ParamDecl]
        # retType: Type # VoidType if there is no return type
        # body: Block

        name, params, retType, body = self.visit(ctx.funcFragment())
        return FuncDecl(name, params, retType, body)

    # Visit a parse tree produced by MiniGoParser#methodDecl.
    def visitMethodDecl(self, ctx: MiniGoParser.MethodDeclContext):
        name, params, retType, body = self.visit(ctx.funcFragment())
        fun = FuncDecl(name, params, retType, body)
        receiver, recType = self.visit(ctx.receiver())
        return MethodDecl(receiver, recType, fun)

    # Visit a parse tree produced by MiniGoParser#field.
    def visitField(self, ctx: MiniGoParser.FieldContext):
        fieldName = ctx.ID().getText()
        fieldType = self.visit(ctx.varType())
        return (fieldName, fieldType)

    # Visit a parse tree produced by MiniGoParser#fieldList.
    def visitFieldList(self, ctx: MiniGoParser.FieldListContext):
        if ctx.fieldList():
            return [self.visit(ctx.field())] + self.visit(ctx.fieldList())
        return [self.visit(ctx.field())]

    # Visit a parse tree produced by MiniGoParser#structDecl.
    def visitStructDecl(self, ctx: MiniGoParser.StructDeclContext):
        # name: str
        # elements:List[Tuple[str,Type]]
        # methods:List[MethodDecl]

        name = ctx.ID().getText()
        elements = self.visit(ctx.fieldList())
        methods = []

        return StructType(name, elements, methods)

    # Visit a parse tree produced by MiniGoParser#method.
    def visitMethod(self, ctx: MiniGoParser.MethodContext):
        name = ctx.ID().getText()
        params = []
        retType = VoidType()

        if ctx.paramList():
            params = self.visit(ctx.paramList())
            params = [parType for _, parType in params]
        if ctx.varType():
            retType = self.visit(ctx.varType())

        return Prototype(name, params, retType)

    # Visit a parse tree produced by MiniGoParser#methodList.
    def visitMethodList(self, ctx: MiniGoParser.MethodListContext):
        if ctx.methodList():
            return [self.visit(ctx.method())] + self.visit(ctx.methodList())
        return [self.visit(ctx.method())]

    # Visit a parse tree produced by MiniGoParser#interfaceDecl.
    def visitInterfaceDecl(self, ctx: MiniGoParser.InterfaceDeclContext):
        name = ctx.ID().getText()
        methods = self.visit(ctx.methodList())
        return InterfaceType(name, methods)

    # Visit a parse tree produced by MiniGoParser#stmt.
    def visitStmt(self, ctx: MiniGoParser.StmtContext):
        return self.visit(ctx.getChild(0))

    # Visit a parse tree produced by MiniGoParser#stmtList.
    def visitStmtList(self, ctx: MiniGoParser.StmtListContext):
        if ctx.stmtList():
            return [self.visit(ctx.stmt())] + self.visit(ctx.stmtList())
        return [self.visit(ctx.stmt())]

    # Visit a parse tree produced by MiniGoParser#blockStmt.
    def visitBlockStmt(self, ctx: MiniGoParser.BlockStmtContext):
        stmts = []
        if ctx.stmtList():
            stmts = self.visit(ctx.stmtList())

        return Block(stmts)

    # Visit a parse tree produced by MiniGoParser#declStmt.
    def visitDeclStmt(self, ctx: MiniGoParser.DeclStmtContext):
        return self.visit(ctx.getChild(0))

    # Visit a parse tree produced by MiniGoParser#assignOp.
    def visitAssignOp(self, ctx: MiniGoParser.AssignOpContext):
        return ctx.getChild(0).getText()

    # Visit a parse tree produced by MiniGoParser#lhsDims.
    def visitLhsDims(self, ctx: MiniGoParser.LhsDimsContext):
        # children = [
        #     child for child in ctx.getChildren() if child.getText() not in ["[", "]"]
        # ]
        # indices = []
        # for child in children:
        #     if isinstance(child, MiniGoParser.TerminalNode):
        #         if child.getSymbol().type == MiniGoParser.ID:
        #             indices.append(Id(child.getText()))
        #         elif child.getSymbol().type == MiniGoParser.INT_LIT:
        #             indices.append(IntLiteral(child.getText()))
        #     else:
        #         indices.append(self.visit(child))

        indices = []

        for child in ctx.getChildren():
            text = child.getText()

            if text in ["[", "]"]:
                continue  # Skip brackets

            if isinstance(child, TerminalNode):  # Terminal nodes (INT_LIT, ID)
                if child.getSymbol().type == MiniGoParser.ID:
                    indices.append(Id(text))
                elif child.getSymbol().type == MiniGoParser.INT_LIT:
                    indices.append(IntLiteral(text))
            else:  # Expression nodes
                indices.append(self.visit(child))

        return indices

    # Visit a parse tree produced by MiniGoParser#lhs.
    def visitLhs(self, ctx: MiniGoParser.LhsContext):
        base = Id(ctx.ID(0).getText())
        i = 1
        while i < ctx.getChildCount():
            if isinstance(ctx.getChild(i), MiniGoParser.LhsDimsContext):
                dims = self.visit(ctx.getChild(i))
                # for ele in dims:
                #     base = ArrayCell(base, [ele])
                base = ArrayCell(base, dims)
                # print(f"\n\n\n{base}")
            else:
                base = FieldAccess(base, ctx.getChild(i + 1).getText())
                i += 1
            i += 1
        return base

    # Visit a parse tree produced by MiniGoParser#assignStmt.
    def visitAssignStmt(self, ctx: MiniGoParser.AssignStmtContext):
        lhs = self.visit(ctx.lhs())
        rhs = self.visit(ctx.exp())
        op = ctx.assignOp().getText()

        if op == ":=":
            return Assign(lhs, rhs)
        else:
            op = op[0]
            rhs = BinaryOp(op, lhs, rhs)
            return Assign(lhs, rhs)

    # Visit a parse tree produced by MiniGoParser#condBlock.
    def visitCondBlock(self, ctx: MiniGoParser.CondBlockContext):
        expr = self.visit(ctx.exp())
        block = self.visit(ctx.blockStmt())
        return expr, block

    # Visit a parse tree produced by MiniGoParser#elifClause.
    def visitElifClause(self, ctx: MiniGoParser.ElifClauseContext):
        return self.visit(ctx.condBlock())

    # Visit a parse tree produced by MiniGoParser#elseClause.
    def visitElseClause(self, ctx: MiniGoParser.ElseClauseContext):
        return self.visit(ctx.blockStmt())

    # Visit a parse tree produced by MiniGoParser#ifStmt.
    def visitIfStmt(self, ctx: MiniGoParser.IfStmtContext):
        # expr:Expr
        # thenStmt:Block
        # elseStmt:Block # None if there is no else

        expr, thenStmt = self.visit(ctx.condBlock())
        elifStmt = []
        elseStmt = None

        if ctx.elifClause():
            elifStmt = [self.visit(elifClause) for elifClause in ctx.elifClause()]

        def elifClause(elifs, elseStmt):
            if len(elifs) == 0:
                return elseStmt
            expr, thenStmt = elifs[0]
            return If(expr, thenStmt, elifClause(elifs[1:], elseStmt))

        if ctx.elseClause():
            elseStmt = self.visit(ctx.elseClause())

        return If(expr, thenStmt, elifClause(elifStmt, elseStmt))

    # Visit a parse tree produced by MiniGoParser#basicFor.
    def visitBasicFor(self, ctx: MiniGoParser.BasicForContext):
        cond = self.visit(ctx.exp())
        loop = self.visit(ctx.blockStmt())
        return ForBasic(cond, loop)

    # Visit a parse tree produced by MiniGoParser#forInit.
    def visitForInit(self, ctx: MiniGoParser.ForInitContext):
        if ctx.assignOp():
            lhs = Id(ctx.ID().getText())
            rhs = self.visit(ctx.exp())
            op = ctx.assignOp().getText()
            if op == ":=":
                return Assign(lhs, rhs)
            else:
                op = op[0]
                rhs = BinaryOp(op, lhs, rhs)
                return Assign(lhs, rhs)

        else:
            varName = ctx.ID().getText()
            varType = None
            varInit = self.visit(ctx.exp())

            if ctx.varType():
                varType = self.visit(ctx.varType())

            return VarDecl(varName, varType, varInit)

    # Visit a parse tree produced by MiniGoParser#forUpdate.
    def visitForUpdate(self, ctx: MiniGoParser.ForUpdateContext):
        lhs = Id(ctx.ID().getText())
        rhs = self.visit(ctx.exp())
        op = ctx.assignOp().getText()

        if op == "=" or op == ":=":
            return Assign(lhs, rhs)
        else:
            op = op[0]
            rhs = BinaryOp(op, lhs, rhs)
            return Assign(lhs, rhs)

    # Visit a parse tree produced by MiniGoParser#complexFor.
    def visitComplexFor(self, ctx: MiniGoParser.ComplexForContext):
        # init:Stmt
        # cond:Expr
        # upda:Assign
        # loop:Block

        init = self.visit(ctx.forInit())
        cond = self.visit(ctx.exp())
        upda = self.visit(ctx.forUpdate())
        loop = self.visit(ctx.blockStmt())

        return ForStep(init, cond, upda, loop)

    # Visit a parse tree produced by MiniGoParser#rangeFor.
    def visitRangeFor(self, ctx: MiniGoParser.RangeForContext):
        # idx: Id
        # value: Id
        # arr: Expr
        # loop:Block

        idx = Id(ctx.ID(0).getText())
        value = Id(ctx.ID(1).getText())
        arr = self.visit(ctx.exp())
        loop = self.visit(ctx.blockStmt())

        return ForEach(idx, value, arr, loop)

    # Visit a parse tree produced by MiniGoParser#forStmt.
    def visitForStmt(self, ctx: MiniGoParser.ForStmtContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by MiniGoParser#breakStmt.
    def visitBreakStmt(self, ctx: MiniGoParser.BreakStmtContext):
        return Break()

    # Visit a parse tree produced by MiniGoParser#contStmt.
    def visitContStmt(self, ctx: MiniGoParser.ContStmtContext):
        return Continue()

    # Visit a parse tree produced by MiniGoParser#callBaseVal.
    def visitCallBaseVal(self, ctx: MiniGoParser.CallBaseValContext):
        if ctx.ID():
            return Id(ctx.ID().getText())
        return self.visit(ctx.funcCall(()))

    # Visit a parse tree produced by MiniGoParser#callBase.
    def visitCallBase(self, ctx: MiniGoParser.CallBaseContext):
        if ctx.dimsType():
            dims = self.visit(ctx.dimsType())
            arr = self.visit(ctx.callBase())
            return ArrayCell(arr, dims)
        elif ctx.DOT():
            receiver = self.visit(ctx.callBase())
            baseVal = self.visit(ctx.callBaseVal())
            if isinstance(baseVal, FuncCall):
                metName = baseVal.funName
                args = baseVal.args
                return MethCall(receiver, metName, args)
            else:
                field = baseVal.name
                return FieldAccess(receiver, field)

        else:
            return self.visit(ctx.callBaseVal())

    # Visit a parse tree produced by MiniGoParser#callStmt.
    def visitCallStmt(self, ctx: MiniGoParser.CallStmtContext):
        func = self.visit(ctx.funcCall())
        if ctx.callBase():
            receiver = self.visit(ctx.callBase())
            metName = func.funName
            args = func.args

            return MethCall(receiver, metName, args)
        else:
            return func

    # # Visit a parse tree produced by MiniGoParser#callBase.
    # def visitCallBase(self, ctx: MiniGoParser.CallBaseContext):
    #     if ctx.dimsType():
    #         arr = Id(ctx.ID().getText())
    #         idx = self.visit(ctx.dimsType())
    #         return ArrayCell(arr, idx)
    #     else:
    #         return ctx.ID().getText()
    #
    # # Visit a parse tree produced by MiniGoParser#callBaseList.
    # def visitCallBaseList(self, ctx: MiniGoParser.CallBaseListContext):
    #     if ctx.callBaseList():
    #         return [self.visit(ctx.callBase())] + self.visit(ctx.callBaseList())
    #     return [self.visit(ctx.callBase())]
    #
    # # Visit a parse tree produced by MiniGoParser#callStmt.
    # def visitCallStmt(self, ctx: MiniGoParser.CallStmtContext):
    #     if ctx.callBaseList():
    #         baseList = self.visit(ctx.callBaseList())
    #         # print(f"\n\n\n{baseList}\n\n\n")
    #
    #         receiver = baseList[0]
    #         if isinstance(receiver, str):
    #             receiver = Id(receiver)
    #
    #         for base in baseList[1:]:
    #             if isinstance(base, str):
    #                 receiver = FieldAccess(receiver, base)
    #             elif isinstance(base, ArrayCell):
    #                 receiver = ArrayCell(FieldAccess(receiver, base.arr.name), base.idx)
    #         metName = ctx.ID().getText()
    #         args = []
    #         if ctx.expList():
    #             args = self.visit(ctx.expList())
    #         return MethCall(receiver, metName, args)
    #     else:
    #         funName = ctx.ID().getText()
    #         args = []
    #         if ctx.expList():
    #             args = self.visit(ctx.expList())
    #         return FuncCall(funName, args)

    # Visit a parse tree produced by MiniGoParser#returnStmt.
    def visitReturnStmt(self, ctx: MiniGoParser.ReturnStmtContext):
        if ctx.exp():
            return Return(self.visit(ctx.exp()))
        return Return(None)
