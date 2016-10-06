class Scope:

    def __init__(self, parent=None):
        if (parent == None):
            self.d = dict()
        else:
            self.d = parent.d
        self.parent = parent

    def __getitem__(self, key):

        if (not key in self.d):
            return None
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
        if (self.condition.evaluate(scope).value):
            tmp = None
            for var in self.if_true:
                tmp = var.evaluate(scope)
            return tmp
        else:
            tmp = None
            for var in self.if_false:
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
        for var in self.args:
            lst.append(var.evaluate(scope))
        if len(lst) != len(function.args):
            print("wrong number of args")
            exit(0)
        for i in range(len(lst)):
            call_scope[function.args[i]] = lst[i]
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

    def evaluate(self, scope):
        lhs = self.lhs.evaluate(scope)
        rhs = self.rhs.evaluate(scope)
        if self.op == '+':
            return Number(lhs.value + rhs.value)
        if self.op == '*':
            return Number(lhs.value * rhs.value)
        if self.op == '-':
            return Number(lhs.value - rhs.value)
        if self.op == '/':
            return Number(lhs.value // rhs.value)
        if self.op == '%':
            return Number(lhs.value % rhs.value)
        if self.op == '==':
            return Number(lhs.value == rhs.value)
        if self.op == '!=':
            return Number(lhs.value != rhs.value)
        if self.op == '<':
            return Number(lhs.value < rhs.value)
        if self.op == '<=':
            return Number(lhs.value <= rhs.value)
        if self.op == '>=':
            return Number(lhs.value >= rhs.value)
        if self.op == '&&':
            return Number(lhs.value and rhs.value)
        if self.op == '||':
            return Number(lhs.value or rhs.value)
        if self.op == '>':
            return Number(lhs.value > rhs.value)


class UnaryOperation:

    
    def __init__(self, op, expr):
        self.op = op
        self.expr = expr

    def evaluate(self, scope):
        expr = self.expr.evaluate(scope)
        if (self.op == '-'):
            return Number(-expr.value)
        if (self.op == '!'):
            return Number(not expr.value)


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
    FunctionCall(Reference('foo'),
                 [Number(5), UnaryOperation('-', Number(3))]).evaluate(scope)

def my_tests():
    abacaba = Scope()
    abacaba["divisor"] = Function(('n', 'i'), [Conditional(BinaryOperation(BinaryOperation(Reference('i'), '*', Reference('i')), '>', Reference('n')),
                                 [Number(0)], [Conditional(BinaryOperation(Reference('n'), '%', Reference('i')), [FunctionCall(Reference("divisor"), [Reference('n'),
                                 BinaryOperation(Reference('i'), '+', Number(1))])], [Number(1)])])])
    abacaba["next_prime"] = Function(('n'), [Conditional(FunctionCall(Reference("divisor"), [Reference('n'), Number(2)]),
                                    [FunctionCall(Reference("next_prime"), [BinaryOperation(Reference('n'), '+', Number(1))])], [Reference('n')])])
    abacaba["main"] = Function([], [Print(FunctionCall(Reference('next_prime'), [Read("tmp")]))])
    FunctionCall(Reference("main"), []).evaluate(abacaba)

if __name__ == '__main__':
    example()
    my_tests()
