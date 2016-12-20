from unittest.mock import *
from io import StringIO
import sys
import io
from model import *

@patch('sys.stdout', new_callable=StringIO)
def compare(expr, val, mock_print):
	scope = Scope()
	Print(expr).evaluate(scope)
	assert mock_print.getvalue() == (str(val) + '\n')

def test_print():
	compare(Number(1), 1)

def test_read():
	with patch('sys.stdin', new=io.StringIO('42')):
		r = Read('a')
		compare(r, 42)

def test_bo():
	compare(BinaryOperation(Number(1), '+', Number(1)), 2)
	compare(BinaryOperation(Number(3), '-', Number(1)), 2)
	compare(BinaryOperation(Number(2), '*', Number(1)), 2)
	compare(BinaryOperation(Number(1), '==', Number(1)), True)
	compare(BinaryOperation(Number(1), '!=', Number(1)), False)

def test_uo():
	compare(UnaryOperation('-', Number(1)), -1)
	compare(UnaryOperation('!', Number(2)), False)

def test_cond():
	compare(Conditional(Number(1), [Number(2)], [Number(3)]), 2)
	compare(Conditional(Number(0), [Number(2)], [Number(3)]), 3)
	compare(Conditional(Number(1), [Number(2)]), 2)

def test_ref():
	scope = Scope()
	scope['a'] = Number(3)
	compare(Reference('a').evaluate(scope), 3)

def test_scope():
	par = Scope()
	par['a'] = Number(1)
	sc = Scope(par)
	sc['b'] = Number(2)
	compare(BinaryOperation(Reference('a'), '+', Reference('b')).evaluate(sc), 3)

def test_func():
	#Example
	parent = Scope()
	parent["bar"] = Number(10)
	scope = Scope(parent)
	parent["foo"] = Function(('hello', 'world'), [BinaryOperation(Reference('hello'), '+', Reference('world'))])
	compare(FunctionCall(FunctionDefinition('foo', parent['foo']), [Number(2), UnaryOperation('-', Number(3))]).evaluate(scope), -1)

def test_my():
	with patch('sys.stdin', new=io.StringIO('42')):
		abacaba = Scope()
		abacaba["divisor"] = Function(('n', 'i'), [Conditional(BinaryOperation(BinaryOperation(Reference('i'), '*', Reference('i')), '>', Reference('n')),
	    	                         [Number(0)], [Conditional(BinaryOperation(Reference('n'), '%', Reference('i')), [FunctionCall(Reference("divisor"), [Reference('n'),
        	                         BinaryOperation(Reference('i'), '+', Number(1))])], [Number(1)])])])
		abacaba["next_prime"] = Function(('n'), [Conditional(FunctionCall(Reference("divisor"), [Reference('n'), Number(2)]),
        	                            [FunctionCall(Reference("next_prime"), [BinaryOperation(Reference('n'), '+', Number(1))])], [Reference('n')])])
		abacaba["main"] = Function([], [FunctionCall(Reference('next_prime'), [Read("tmp")])])
		compare(FunctionCall(Reference("main"), []).evaluate(abacaba), 43)



if (__name__ == "__main__"):
	test_bo()
	test_uo()
	test_func()
	test_scope()
	test_cond()
	test_read()
	test_my()
	test_ref()
	test_print()
