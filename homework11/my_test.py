from unittest.mock import *
from unittest import TestCase
from io import StringIO
import sys
import io
from model import *

@patch('sys.stdout', new_callable=StringIO)
def compare(expr, val, mock_print):
	scope = Scope()
	Print(expr).evaluate(scope)
	return mock_print.getvalue() == (str(val) + '\n')

class PrintTest(TestCase):
	def test_print(self):
		assert compare(Number(1), 1)
		
	def test_print1(self):
		assert compare(Number(3), 3)
	
class ReadTest(TestCase):
	def test_read(self):
		with patch('sys.stdin', new=io.StringIO('42')):
			r = Read('a')
			assert compare(r, 42)

class BinaryOperationTest(TestCase):
	def test_add(self):
		assert compare(BinaryOperation(Number(1), '+', Number(1)), 2)
	
	def test_sub(self):
		assert compare(BinaryOperation(Number(3), '-', Number(1)), 2)
	
	def test_mult(self):
		assert compare(BinaryOperation(Number(2), '*', Number(1)), 2)
		
	def test_eq(self):
		assert (not compare(BinaryOperation(Number(1), '==', Number(1)), False)) and (not compare(BinaryOperation(Number(1), '==', Number(1)), 0))
	
	def test_neq(self):
		assert compare(BinaryOperation(Number(1), '!=', Number(1)), False) or compare(BinaryOperation(Number(1), '!=', Number(1)), 0)

class UnaryOperationTest(TestCase):

	def test_neg(self):
		assert compare(UnaryOperation('-', Number(1)), -1)
	
	def test_not(self):
		assert compare(UnaryOperation('!', Number(2)), False)

class ConditionalTest(TestCase):

	def test_true(self):
		assert compare(Conditional(Number(1), [Number(2)], [Number(3)]), 2)
	
	def test_false(self):
		assert compare(Conditional(Number(0), [Number(2)], [Number(3)]), 3)
	
	def test_empty(self):
		assert compare(Conditional(Number(1), [Number(2)]), 2)

class ReferenceTest(TestCase):

	def test_ref(self):
		scope = Scope()
		scope['a'] = Number(3)
		assert compare(Reference('a').evaluate(scope), 3)

class ScopeTest(TestCase):

	def test_scope(self):
		par = Scope()
		par['a'] = Number(1)
		sc = Scope(par)
		sc['b'] = Number(2)
		assert compare(BinaryOperation(Reference('a'), '+', Reference('b')).evaluate(sc), 3)

class FunctionTest(TestCase):

	def test_func(self):
		#Example
		parent = Scope()
		parent["bar"] = Number(10)
		scope = Scope(parent)
		parent["foo"] = Function(('hello', 'world'), [BinaryOperation(Reference('hello'), '+', Reference('world'))])
		assert compare(FunctionCall(FunctionDefinition('foo', parent['foo']), [Number(2), UnaryOperation('-', Number(3))]).evaluate(scope), -1)

class AllTest(TestCase):

	def test_my(self):
		with patch('sys.stdin', new=io.StringIO('42')):
			abacaba = Scope()
			abacaba["divisor"] = Function(('n', 'i'), [Conditional(BinaryOperation(BinaryOperation(Reference('i'), '*', Reference('i')), '>', Reference('n')),
		                                 [Number(0)], [Conditional(BinaryOperation(Reference('n'), '%', Reference('i')), [FunctionCall(Reference("divisor"), [Reference('n'),
    	                                 BinaryOperation(Reference('i'), '+', Number(1))])], [Number(1)])])])
			abacaba["next_prime"] = Function(('n'), [Conditional(FunctionCall(Reference("divisor"), [Reference('n'), Number(2)]),
    	                                    [FunctionCall(Reference("next_prime"), [BinaryOperation(Reference('n'), '+', Number(1))])], [Reference('n')])])
			abacaba["main"] = Function([], [FunctionCall(Reference('next_prime'), [Read("tmp")])])
			assert compare(FunctionCall(Reference("main"), []).evaluate(abacaba), 43)

