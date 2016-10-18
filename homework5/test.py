import yat.model
import yat.printer
import yat.folder

def example():
    pass
    """parent = Scope()
    parent["foo"] = yat.model.Function(('hello', 'world'),
                             [Print(yat.model.BinaryOperation(yat.model.Reference('hello'),
                                                    '+',
                                                    yat.model.Reference('world')))])
    parent["bar"] = yat.model.Number(10)
    scope = Scope(parent)
    assert 10 == scope["bar"].value
    scope["bar"] = yat.model.Number(20)
    assert scope["bar"].value == 20
    print('It should print 2: ', end=' ')
    a = yat.model.yat.model.FunctionCall(yat.model.Reference('foo'),
                 [yat.model.Number(5), yat.model.UnaryOperation('-', yat.model.Number(3))])
    a.evaluate(scope)
    ppt = yat.printer.PrettyPrinter()
    ppt.visit(a, 0)"""

def my_tests():
    pass
    """abacaba = Scope()
    a = yat.model.yat.model.FunctionDefinition("divisor", yat.model.Function(('n', 'i'), [yat.model.Conditional(yat.model.BinaryOperation(yat.model.BinaryOperation(yat.model.Reference('i'), '*', yat.model.Reference('i')), '>', yat.model.Reference('n')),
                                 [yat.model.Number(0)], [yat.model.Conditional(yat.model.BinaryOperation(yat.model.Reference('n'), '%', yat.model.Reference('i')), [yat.model.yat.model.FunctionCall(yat.model.Reference("divisor"), [yat.model.Reference('n'),
                                 yat.model.BinaryOperation(yat.model.Reference('i'), '+', yat.model.Number(1))])], [yat.model.Number(1)])])]))
    b = yat.model.yat.model.FunctionDefinition("next_prime", yat.model.Function(('n'), [a, yat.model.Conditional(yat.model.yat.model.FunctionCall(yat.model.Reference("divisor"), [yat.model.Reference('n'), yat.model.Number(2)]),
                                    [yat.model.yat.model.FunctionCall(yat.model.Reference("next_prime"), [yat.model.BinaryOperation(yat.model.Reference('n'), '+', yat.model.Number(1))])], [yat.model.Reference('n')])]))
    c = yat.model.yat.model.FunctionDefinition("main", yat.model.Function([], [b, Print(yat.model.yat.model.FunctionCall(yat.model.Reference("next_prime"), [Read("tmp")]))]))
    d = yat.model.yat.model.FunctionCall(c, [])
    #d.evaluate(abacaba)
    ppt = yat.printer.PrettyPrinter()
    print("\n")
    ppt.visit(d, 0)
    print()"""

def my_tests2():
    pass
    """z = yat.model.Conditional(yat.model.BinaryOperation(yat.model.Reference('a'), '==', yat.model.Number(0)), [yat.model.BinaryOperation(yat.model.Reference('a'), '*', yat.model.UnaryOperation('-', yat.model.Number(0)))], [])
    a = yat.model.yat.model.FunctionDefinition('ask', yat.model.Function(('a'), [z]))
    b = yat.model.yat.model.FunctionDefinition('func', yat.model.Function(('a'), [a, yat.model.yat.model.FunctionCall(yat.model.Reference('ask'), [yat.model.BinaryOperation(yat.model.Reference('a'), '-', yat.model.Reference('a'))])]))
    cf = yat.folder.ConstantFolder()
    pp = yat.printer.PrettyPrinter()
    c = cf.visit(b)
    #print(type(c))
    pp.visit(c, 0)"""

def my_tests3():
    a = [yat.model.Number(1)]
    for i in range(2, 5):
        a.append(yat.model.BinaryOperation(a[-1], '*', yat.model.Number(i)))
    for i in ['a', 'b']:
        a.append(yat.model.BinaryOperation(a[-1], '*', yat.model.Reference(i)))
    b = [yat.model.Number(1)]
    for i in range(2, 5):
        b.append(yat.model.BinaryOperation(b[-1], '+', yat.model.Number(i)))
    b.append(yat.model.BinaryOperation(b[-1], '+', yat.model.BinaryOperation(yat.model.Reference('a'), '*', yat.model.Number(1))))
    a.append(yat.model.BinaryOperation(a[-1], '+', b[-1]))
    a.append(yat.model.BinaryOperation(a[-1], '+', yat.model.BinaryOperation(yat.model.Reference('b'), '*', yat.model.Number(1))))
    c = yat.model.BinaryOperation(yat.model.Reference('a'), '*', yat.model.Number(0))
    d = yat.model.BinaryOperation(yat.model.Reference('b'), '*', yat.model.Number(0))
    a.append(yat.model.Print(yat.model.BinaryOperation(a[-1], '+', yat.model.BinaryOperation(c, '*', d))))
    z = yat.folder.ConstantFolder().visit(a[-1])
    yat.printer.PrettyPrinter().visit(z)

if __name__ == '__main__':
    example()
    my_tests()
    my_tests2()
    my_tests3()
