

class ConstantFolder:
    def visit(self, tree):
        name = tree.__class__.__name__
        fn = getattr(self, 'visit' + name)
        return fn(tree)

    def visitNumber(self, num):
        return num

    def visitFunctionDefinition(self, fun):
        body = [self.visit(var) for var in fun.function.body] 
        return model.FunctionDefinition(fun.name, model.Function(fun.function.args, body))

    def visitConditional(self, cond):
        condition = self.visit(cond.condition)
        if_true = [self.visit(var) for var in cond.if_true]
        if_false = ([self.visit(var) for var in cond.if_false] if (cond.if_false != None) else None)
        return model.Conditional(condition, if_true, if_false)

    def visitPrint(self, prt):
        return model.Print(self.visit(prt.expr))

    def visitRead(self, rd):
        return rd

    def visitFunctionCall(self, fun):
        fun_expr = self.visit(fun.fun_expr)
        args = [self.visit(var) for var in fun.args]
        return model.FunctionCall(fun_expr, args)
        
    def visitReference(self, ref):
        return ref

    def visitBinaryOperation(self, bnr):
        lhs = self.visit(bnr.lhs)
        rhs = self.visit(bnr.rhs)
        if isinstance(lhs, model.Number) and isinstance(rhs, model.Number):
            return bnr.evaluate(Scope())
        if bnr.op == '*' and isinstance(lhs, model.Number) and (not lhs.value) and isinstance(rhs, model.Reference):
            return Number(0)
        if bnr.op == '*' and isinstance(rhs, model.Number) and (not rhs.value) and isinstance(lhs, model.Reference):
            return Number(0)
        if bnr.op == '-' and isinstance(lhs, model.Reference) and isinstance(rhs, model.Reference) and (lhs.name == rhs.name):
            return Number(0)
        return model.BinaryOperation(lhs, bnr.op, rhs)

    def visitUnaryOperation(self, unr):
        expr = self.visit(unr.expr)
        if isinstance(expr, model.Number):
            return unr.evaluate(Scope())
        return model.UnaryOperation(unr.op, expr)
