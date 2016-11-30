from unittest.mock import MagicMock
from model import *

def read():
	r = Read('a')
	s = Scope()
	assert BinaryOperation(r, '-', Reference('a')).evaluate(s).value == 0

def test_bo():
	s = Scope()
	assert BinaryOperation(Number(1), '+', Number(1)).evaluate(s).value == 2
	assert BinaryOperation(Number(1), '==', Number(1)).evaluate(s).value == 1
	assert BinaryOperation(Number(1), '!=', Number(1)).evaluate(s).value == 0

def test_cond():
	s = Scope()
	assert Conditional(BinaryOperation(Number(1), '+', Number(1)), [Number(2)], [Number(3)]).evaluate(s).value == 2
	assert Conditional(BinaryOperation(Number(1), '-', Number(1)), [Number(2)], [Number(3)]).evaluate(s).value == 3
	assert Conditional(BinaryOperation(Number(1), '-', Number(1)), [Number(2)]).evaluate(s) == None

def test_scope():
	par = Scope()
	par['a'] = Number(1)
	sc = Scope(par)
	par['b'] = Number(2)
	assert BinaryOperation(Reference('a'), '+', Reference('b')).evaluate(sc).value == 3
	#assert BinaryOperation(Reference('a'), '+', Reference('c')).evaluate(sc).value == 3

if (__name__ == "__main__"):
	test()
	test_bo()
	test_scope()
	test_cond()
	#read()

