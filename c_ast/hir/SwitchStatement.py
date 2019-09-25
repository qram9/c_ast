from Statement import Statement
from Expression import Expression
from CompoundStatement import CompoundStatement

class SwitchException(Exception): pass
class InvalidTypeForSwitchExpressionError(SwitchException): pass
class InvalidTypeForSwitchBodyError(SwitchException): pass

class SwitchStatement(Statement):
	"""Represents an Ansi C switch statement, for ex switch(expr) {...}
Is represented independent of case statements. We need to have the 
'case:', 'default:' cases for the control flow graph to look meaningful.
It is upto the User or the parser to get this set up 
correctly for the input C code"""
	def __init__(self, expr, body):
		"""Initializes an Expression type for the switch condition and 
a CompoundStatement body type for the body of the switch type. 
Both values are added to the children of the underlying Traversable
type"""
		self.initialize()
		self.setNumChildren(2)
		if not isinstance(expr, Expression):
			raise InvalidTypeForSwitchExpressionError, type(expr)
		self.setChild(0, expr)
		if not isinstance(body, CompoundStatement):
			raise InvalidTypeForSwitchBodyError, type(body)
		self.setChild(1, body)

	def __repr__(self):
		"""Returns Ansi C switch statement for example 
switch (...) {...}. Change this function to get a 
different string."""
		retval = 'switch (' + repr(self.getChild(0)) + ')'
		retval += repr(self.getChild(1))
		return retval

	__str__ = __repr__

from Imports import *
def SwitchTest():
	from CompoundStatement import CompoundStatementTest
	body = CompoundStatementTest()
	condition = ConditionalExpression(Identifier('a'), \
conditionalOperator.COMPARE_LE, Identifier('b'))
	return SwitchStatement(condition, body)

if __name__ == '__main__':
	print SwitchTest()	

