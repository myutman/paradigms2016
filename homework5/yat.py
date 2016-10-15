import printer
import folder

class Scope:

    def __init__(self, parent=None):
        self.d = dict()
        self.parent = parent

    def __getitem__(self, key):

        if (not key in self.d):
            return self.parent[key] if self.parent != None else None
        return self.d[key]    

    def __setitem__(self, key, value):
        self.d[key] = value 

class Number:

    def __init__(self, value):
        self.value = value

    def evaluate(self, scope):
        return self


class Function:

   
    def __init__(self, args, body):
        self.args = args
        self.body = body

    def evaluate(self, scope):
        tmp = None
        for var in self.body:
            tmp = var.evaluate(scope)
        return tmp


class FunctionDefinition:

    
    def __init__(self, name, function):
        self.name = name
        self.function = function

    def evaluate(self, scope):
        scope[self.name] = self.function
        return self.function


class Conditional:

    

    def __init__(self, condition, if_true, if_false=None):
        self.condition = condition
        self.if_true = if_true
        self.if_false = if_false

    def evaluate(self, scope):
        branch = self.if_true if self.condition.evaluate(scope).value else self.if_false
        tmp = None
        for var in branch:
            tmp = var.evaluate(scope)
        return tmp


class Print:

    
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, scope):
        print(self.expr.evaluate(scope).value)


class Read:

    

    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        tmp = Number(int(input()))
        scope[self.name] = tmp
        return tmp


class FunctionCall:

    

    def __init__(self, fun_expr, args):
        self.fun_expr = fun_expr
        self.args = args

    def evaluate(self, scope):
        function = self.fun_expr.evaluate(scope)
        call_scope = Scope(scope)
        lst = [] 
        for name, arg in zip(function.args, self.args):
            call_scope[name] = arg.evaluate(scope)
        return function.evaluate(call_scope)



class Reference:

    
    def __init__(self, name):
        self.name = name

    def evaluate(self, scope):
        return scope[self.name]


class BinaryOperation:

    

    def __init__(self, lhs, op, rhs):
        self.lhs = lhs
        self.op = op
        self.rhs = rhs
        self.d = {'+': (lambda x,y: x + y), '*': (lambda x,y: x * y), '-': (lambda x,y: x - y), '/': (lambda x,y: x // y),
                  '%': (lambda x,y: x % y), '==': (lambda x,y: x == y), '!=': (lambda x,y: x != y), '<': (lambda x,y: x < y),
                  '>': (lambda x,y: x > y), '<=': (lambda x,y: x <= y), '>=': (lambda x,y: x >= y), '&&': (lambda x,y: x and y), '||': (lambda x,y: x or y)}

    def evaluate(self, scope):
        lhs = self.lhs.evaluate(scope)
        rhs = self.rhs.evaluate(scope)
        return Number(self.d[self.op](lhs.value, rhs.value))


class UnaryOperation:

    
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr
        self.d = {'-': (lambda x: -x), '!': (lambda x: not x)}

    def evaluate(self, scope):
        expr = self.expr.evaluate(scope)
        return Number(self.d[self.op](expr.value))
       



def example():
    parent = Scope()
    parent["foo"] = Function(('hello', 'world'),
                             [Print(BinaryOperation(Reference('hello'),
                                                    '+',
                                                    Reference('world')))])
    parent["bar"] = Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    a = FunctionCall(Reference('foo'),
                 [Number(5), UnaryOperation('-', Number(3))])
    a.evaluate(scope)
    ppt = printer.PrettyPrinter()
    ppt.visit(a, 0)

def my_tests():
    abacaba = Scope()
    a = FunctionDefinition("divisor", Function(('n', 'i'), [Conditional(BinaryOperation(BinaryOperation(Reference('i'), '*', Reference('i')), '>', Reference('n')),
                                 [Number(0)], [Conditional(BinaryOperation(Reference('n'), '%', Reference('i')), [FunctionCall(Reference("divisor"), [Reference('n'),
                                 BinaryOperation(Reference('i'), '+', Number(1))])], [Number(1)])])]))
    b = FunctionDefinition("next_prime", Function(('n'), [a, Conditional(FunctionCall(Reference("divisor"), [Reference('n'), Number(2)]),
                                    [FunctionCall(Reference("next_prime"), [BinaryOperation(Reference('n'), '+', Number(1))])], [Reference('n')])]))
    c = FunctionDefinition("main", Function([], [b, Print(FunctionCall(Reference("next_prime"), [Read("tmp")]))]))
    d = FunctionCall(c, [])
    #d.evaluate(abacaba)
    ppt = printer.PrettyPrinter()
    print("\n")
    ppt.visit(d, 0)
    print()

def my_tests2():
    z = Conditional(BinaryOperation(Reference('a'), '==', Number(0)), [BinaryOperation(Reference('a'), '*', UnaryOperation('-', Number(0)))], None)
    a = FunctionDefinition('ask', Function(('a'), [z]))
    b = FunctionDefinition('func', Function(('a'), [a, FunctionCall(Reference('ask'), [BinaryOperation(Reference('a'), '-', Reference('a'))])]))
    cf = folder.ConstantFolder()
    pp = printer.PrettyPrinter()
    c = cf.visit(b)
    #print(type(c))
    pp.visit(c, 0)

if __name__ == '__main__':
    example()
    my_tests()
    my_tests2()
