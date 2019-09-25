from Declaration import Declaration
from Declarator import Declarator
class ParameterDeclaratorException(Exception): pass
class ParameterNotADeclarationError(Exception): pass

class ParameterDeclarator(Declarator):
	""" Represents a parameter list that is used by 
Procedure declarations. 
For example (int x, int y, int z[])"""
	def __init__(self, params=[]):
		"""Initializes a ParameterDeclaration from a
list type argument 'params'. Sets the number of 
Children of this Traversable
type to the the len(iterable). Requires that each 
argument be of Declaration type"""
		self.initialize()
		self.setNumChildren(len(params))
		r = 0
		for k in params:
			if not isinstance(k, Declaration):
				raise ParameterNotADeclarationError, type(k)
			self.setChild(r, k)
			r+=1

	def getParameter(self, which):
		"""Returns a specified Declaration"""
		return self.getChild(which)

	def __repr__(self):
		"""Returns a AnsiC string representation of the 
parameter list, for ex. (int a, int b)"""
		retval = ''
		retval += ' ('
		substr = []
		for k in range(0, self.getNumChildren()):
			substr.append(repr(self.getChild(k)))
		retval += ', '.join(substr)
		retval += ') '
		return retval

	__str__ = __repr__

def ParameterDeclaratorTest():
	from keyword import specifiers
	from VariableDeclaration import VariableDeclaration
	from VariableDeclarator import VariableDeclarator
	from Identifier import Identifier
	k = VariableDeclaration(specifiers.chaR, VariableDeclarator(Identifier('a')))
	l = VariableDeclaration(specifiers.chaR, VariableDeclarator(Identifier('b')))
	r = ParameterDeclarator([k,l])
	return r

if __name__ == '__main__':
	print ParameterDeclaratorTest()
