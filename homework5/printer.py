import yat.model

class PrettyPrinter:

    def __init__(self):
        self.b = False

    def visit(self, tree, tabs):
        b = self.b
        self.b = True
        name = tree.__class__.__name__
        fn = getattr(self, 'visit' + name)
        fn(tree, tabs)
        self.b = b
        if (not b):
            print(";")

    def visitNumber(self, num, tabs):
        print("\t" * tabs + str(num.value), end="")

    def visitFunctionDefinition(self, fun, tabs):
        print("\t" * tabs + "def " + fun.name + " (" + ", ".join(fun.function.args) + ") {")
        for var in fun.function.body:
            self.visit(var, tabs + 1)
            print(";")
        print("\t" * tabs, end="}")

    def visitConditional(self, cond, tabs):
        print("\t" * tabs, end = "if (")
        self.visit(cond.condition, 0)
        print(") {")
        for var in cond.if_true:
            self.visit(var, tabs + 1)
            print(";")
        if cond.if_false != None:
            print("\t" * tabs + "} else {")
            for var in cond.if_false:
                self.visit(var, tabs + 1)
                print(";")
        else:
            print(cond.if_false)
        print("\t" * tabs, end="}")

    def visitPrint(self, prt, tabs):
        print("\t" * tabs, end="print(")
        self.visit(prt.expr, 0)
        print(end=")")

    def visitRead(self, rd, tabs):
        print("\t" * tabs + "read(" + rd.name, end=")")

    def visitFunctionCall(self, fun, tabs):
        self.visit(fun.fun_expr, tabs)
        print(end="(")
        if len(fun.args):
            self.visit(fun.args[0], 0)
            for var in fun.args[1:]:
                 print(end=", ")
                 self.visit(var, 0)
        print(end=")")
        
    def visitReference(self, ref, tabs):
        print("\t"*tabs, end=ref.name)

    def visitBinaryOperation(self, bnr, tabs):
        print("\t"*tabs, end="(")
        self.visit(bnr.lhs, 0)
        print(") " + bnr.op ,end=" (")
        self.visit(bnr.rhs, 0)
        print(end=")")

    def visitUnaryOperation(self, unr, tabs):
        print(unr.op, end="(")
        self.visit(unr.expr, 0)
        print(end=")")

