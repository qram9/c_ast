# A FUNCTION CALL TYPE IN ANSI C. Not supported for TcGen
from Expression import Expression

class InvalidTypeFunctionCallError(Exception):
	def __init__(self, value):
		self.value = value
	def __repr__(self):
		return 'Invalid type: (%s) for function call, expected (%s)' %(value, str(type(Expression)))

class InvalidTypeArgumentListError(Exception):
	def __init__(self, value):
		self.value = value
	def __repr__(self):
		return 'Invalid type: (%s) for Arguments, expected (%s)' %(value, str(type(list)))

class InvalidTypeArgumentError(Exception):
	def __init__(self, value):
		self.value = value
	def __repr__(self):
		return 'Invalid type: (%s) for Argument, expected (%s)' % (value, str(type(Expression)))

class FunctionCall(Expression):
	def __init__(self, expr, args = None):
		self.initialize()
		if not isinstance(expr, Expression):
			raise InvalidTypeFunctionCallError(str(type(expr)))
		if not args:
			self.setNumChildren(1)
			self.setChild(0, expr)
		else:
			if not isinstance(args, list):
				raise InvalidTypeArgumentListError(str(type(args)))
			else:
				self.setNumChildren(1+len(args))
				self.setChild(0, expr)
				r = 1
				for k in args:
					if not isinstance(k, Expression):
						raise InvalidTypeArgumentError(str(type(k)))
					else:
						self.setChild(r, k)
						r = r+1
	def __repr__(self):
		retval = repr(self.getChild(0)) + ' ('
		if self.getNumChildren() > 1:
			arglist = []
			for k in range(1,self.getNumChildren()):
				arglist.append(repr(self.getChild(k)))
			retval += ','.join(arglist)
		retval += ') '
		return retval
	__str__ = __repr__

def FunctionCallTest():
	from Identifier import Identifier
	k = FunctionCall(Identifier('fun'))
	print k
	args = [Identifier('a'), Identifier('b')]
	k = FunctionCall(Identifier('fun'), args)
	print k

if __name__ == '__main__':
	FunctionCallTest() 


