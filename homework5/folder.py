import yat.model

class ConstantFolder:
    def visit(self, tree):
        name = tree.__class__.__name__
        fn = getattr(self, 'visit' + name)
        return fn(tree)

    def visitNumber(self, num):
        return num

    def visitFunctionDefinition(self, fun):
        body = [self.visit(var) for var in fun.function.body] 
        return yat.model.FunctionDefinition(fun.name, yat.model.Function(fun.function.args, body))

    def visitConditional(self, cond):
        condition = self.visit(cond.condition)
        if_true = [self.visit(var) for var in cond.if_true]
        if_false = ([self.visit(var) for var in cond.if_false] if (cond.if_false != None) else None)
        return yat.model.Conditional(condition, if_true, if_false)

    def visitPrint(self, prt):
        return yat.model.Print(self.visit(prt.expr))

    def visitRead(self, rd):
        return rd

    def visitFunctionCall(self, fun):
        fun_expr = self.visit(fun.fun_expr)
        args = [self.visit(var) for var in fun.args]
        return yat.model.FunctionCall(fun_expr, args)
        
    def visitReference(self, ref):
        return ref

    def visitBinaryOperation(self, bnr):
        lhs = self.visit(bnr.lhs)
        rhs = self.visit(bnr.rhs)
        if isinstance(lhs, yat.model.Number) and isinstance(rhs, yat.model.Number):
            return bnr.evaluate(Scope())
        if bnr.op == '*' and isinstance(lhs, yat.model.Number) and (not lhs.value) and isinstance(rhs, yat.model.Reference):
            return Number(0)
        if bnr.op == '*' and isinstance(rhs, yat.model.Number) and (not rhs.value) and isinstance(lhs, yat.model.Reference):
            return Number(0)
        if bnr.op == '-' and isinstance(lhs, yat.model.Reference) and isinstance(rhs, yat.model.Reference) and (lhs.name == rhs.name):
            return Number(0)
        return yat.model.BinaryOperation(lhs, bnr.op, rhs)

    def visitUnaryOperation(self, unr):
        expr = self.visit(unr.expr)
        if isinstance(expr, yat.model.Number):
            return unr.evaluate(Scope())
        return yat.model.UnaryOperation(unr.op, expr)
