from yat import *

class ConstantFolder:
    def visit(self, tree):
        name = tree.__class__.__name__
        fn = getattr(self, 'visit' + name)
        return fn(tree)

    def visitNumber(self, num):
        return num

    def visitFunctionDefinition(self, fun):
        body = [self.visit(var) for var in fun.function.body] 
        return FunctionDefinition(fun.name, Function(fun.function.args, body))

    def visitConditional(self, cond):
        condition = self.visit(cond.condition)
        if_true = [self.visit(var) for var in cond.if_true]
        if_false = ([self.visit(var) for var in cond.if_false] if cond.if_false else None)
        return Conditional(condition, if_true, if_false)

    def visitPrint(self, prt):
        return Print(self.visit(prt.expr))

    def visitRead(self, rd):
        return rd

    def visitFunctionCall(self, fun):
        fun_expr = self.visit(fun.fun_expr)
        args = [self.visit(var) for var in fun.args]
        return FunctionCall(fun_expr, args)
        
    def visitReference(self, ref):
        return ref

    def visitBinaryOperation(self, bnr):
        lhs = self.visit(bnr.lhs)
        rhs = self.visit(bnr.rhs)
        n1 = lhs.__class__.__name__
        n2 = rhs.__class__.__name__
        if n1 ==  "Number" and n2 == "Number":
            return Number(bnr.d[bnr.op](lhs.value, rhs.balue))
        if bnr.op == '*' and n1 == "Number" and (not lhs.value) and n2 == "Reference":
            return Number(0)
        if bnr.op == '*' and n2 == "Number" and (not rhs.value) and n1 == "Reference":
            return Number(0)
        if bnr.op == '-' and n1 == "Reference" and n2 == "Reference" and (lhs.name == rhs.name):
            return Number(0)
        return BinaryOperation(lhs, bnr.op, rhs)

    def visitUnaryOperation(self, unr):
        expr = self.visit(unr.expr)
        nm = expr.__class__.__name__
        if nm == "Number":
            return Number(unr.d[unr.op](expr.value))
        return UnaryOperation(unr.op, expr)
