from Expression import Expression
from Statement import Statement

class InvalidTypeExpressionForCase(Exception):
	def __init__(self, value):
		self.value = value
	def __repr__(self):
		return 'Invalid type: (%s) for Case statement, expected: (%s)' % (value, str(type(Expression)))

class Case(Statement):
	"""Represents the case statement in Ansi C.
The supported form requires an expression to be 
specified for the case statement. Raises 
exception if non-expressions are specified.
The IR for case is not contained in the 
switch IR, and care to be taken where the case
is inserted. As in Ansi C cases do not create 
a new scope."""
	def __init__(self, expr):
		if not isinstance(expr, Expression):
			raise InvalidTypeExpressionForCase(str(type(expr)))
		self.initialize()
		self.setNumChildren(1)
		self.setChild(0, expr)
	def __repr__(self):
		return 'case ' + repr(self.getChild(0)) + ':'
	__str__ = __repr__

def CaseTest():
	from Identifier import Identifier
	c = Case(Identifier('a'))
	return c

if __name__ == '__main__':
	print CaseTest()
