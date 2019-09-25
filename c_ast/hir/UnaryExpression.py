from Expression import Expression
from operator import unaryOperator, getUnaryOperatorList

class UnaryExpressionException(Exception): pass
class InvalidUnaryOperatorTypeError(UnaryExpressionException): pass

class UnaryExpression(Expression):
	"""Subclass of Expression, contains _op to hold unaryOperator"""
	__slots__ = ['_op']
	def _catchNotUnaryOperatorError(self, uop):
		"""Catches Error when unary expression instantiated 
with an unknown type for operator. Passed operator 
must be present in the lists returned by 
getUnaryOperatorList(). Care must be taken here 
if you have made a copy of a operator type."""
		uops = getUnaryOperatorList()
		if uop not in uops:
			print uop, type(uop), id(uop)
			raise InvalidUnaryOperatorTypeError, type(uop), id(uop)
	def __init__(self, *args):
		"""UnaryExpression initialized with sequence with uop, child"""
		Expression.__init__(self)
		uop, expr = args
		self.setOperator(uop)
		self.setNumChildren(1)
		self.setChild(0, expr)
		self.setParens(False)

	def getOperator(self):
		"""Returns the operator __slots__ entry: _op"""
		return self._op
	def setOperator(self, uop):
		"""Set an Unary Operator as the _op member 
of the UnaryExpression object"""
		self._catchNotUnaryOperatorError(uop)
		self._op = uop

#	def setExpression(self, expr):
#		self.setParent(expr.getParent())
#		self.setChild(0, expr.getChild(0))
#		self.setOperator(expr.getOperator())

	def items(self):
		"""Returns items dict when called from setstate. 
Adds __slots__ entry "_op" to items dict.
Recurses into base classes and collects items from there too."""
		items = {}
		items['_op'] = self._op
		for k in UnaryExpression.__bases__:
			if hasattr(k, 'items'):
				supitems = k.items(self)
				for k,v in supitems.items():
					items[k] = v
		return dict(items)
	def __getstate__(self):
		"""Returns a dict representing the contents of 
this Unary Expression object and its base classes 
instances' contents. Uses the items() function.
Contents added here is _op"""
		return self.items()
	def __setstate__(self, statedict):
		"""Blindly calls setattr with entried from a 
__getstate__ like string->attr dict"""
		for k,v in statedict.items():
			setattr(self, k, v)

	def __repr__(self):
		"""Call to print the UnaryExpression Infix. 
() are added if specified.
Except for unaryOperator.POST_INCREMENT 
and unaryOperator.POST_DECREMENT, 
the rest of the unary operators 
precede the expression child."""
		if (self._op == unaryOperator.POST_INCREMENT) or (self._op == unaryOperator.POST_DECREMENT):
			retval = repr(self.getChild(0)) + repr(self._op) 
		else:
			retval = repr(self._op) + repr(self.getChild(0))	
		if self.getParens():
			retval = '(' + retval + ')'
		return retval 
	__str__ = __repr__

def UnaryExpressionTest():
	from operator import unaryOperator
	from Identifier import Identifier
	a = Identifier('a')
	b = UnaryExpression(unaryOperator.POST_DECREMENT, a)
	return b

if __name__ == '__main__':
	from Identifier import Identifier
	exp = Identifier('a')
	unary_exp = UnaryExpression(unaryOperator.POST_DECREMENT, exp)
	print repr(unary_exp)

