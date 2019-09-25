from Statement import Statement
from Expression import Expression
class ExpressionStatement(Statement):
	__slots__ = ['_expr']
	def __init__(self, expr):
		"""Represents a Ansi C expression statement, 
for example, a = b; a = b+c; or b++;. Traversable
type has 1 child that holds the 'expr' argument. 
There is an 'expr' attr in __slots__. 
The Traversable children based system may come into 
rethink if experiments indicate difficulty in usage"""
		Statement.__init__(self)
		self.setNumChildren(1)
		expr.setParent(self)
		expr.setParens(False)
		self._expr = expr
		self.setChild(0, expr)
	def getExpression(self):
		"""Returns the __slots__.expr attribute"""
		return self._expr
	def __repr__(self):
		return repr(self.getExpression()) + ';'
	__str__ = __repr__
	def items(self):
		"""Returns items dict when called from setstate. 
Adds __slots__ entry "_expr" to items dict.
Recurses into base classes and collects items from there too."""
		items = {}
		items['_expr'] = self._expr
		for k in ExpressionStatement.__bases__:
			if hasattr(k, 'items'):
				supitems = k.items(self)
				for k,v in supitems.items():
					items[k] = v
		return dict(items)
	def __getstate__(self):
		"""Returns a dict representing the contents of 
this ExpressionStatement object and its base classes 
instances' contents. Uses the items() function.
Contents added here is _expr"""
		return self.items()
	def __setstate__(self, statedict):
		"""Blindly calls setattr with entried from a 
__getstate__ like string->attr dict"""
		for k,v in statedict.items():
			setattr(self, k, v)
def ExpressionStatementTest():
	from AssignmentExpression import AssignmentExpression
	from Identifier import Identifier
	from operator import assignmentOperator
	return ExpressionStatement(AssignmentExpression(Identifier('a'), assignmentOperator.ADD, Identifier('b')))

if __name__ == '__main__':
	from BinaryExpression import BinaryExpression
	from operator import binaryOperator
	from Identifier import Identifier
	id1 = Identifier('a')
	id2 = Identifier('b')
	binexp = BinaryExpression(id1, binaryOperator.ADD, id2)
	expstmt = ExpressionStatement(binexp)
	print expstmt
