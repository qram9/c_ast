from Declaration import Declaration
from Declarator import Declarator
from Specifier import Specifier
class NotAValidDeclaratorError(Exception):
	def __init__(self, value=''):
		self.value = value
	def __str__(self):
		return 'Invalid type for Declarator:(%s) for VariableDeclaration' % self.value

class NotAValidSpecifierError(Exception):
	def __init__(self, value=''):
		self.value = value
	def __str__(self):
		return 'Invalid type for Specifier:(%s) for VariableDeclaration' % self.value

class VariableDeclaration(Declaration):
	"""Represents a VariableDeclaration type in Ansi C. Requires
specifier type arguments and declaration type arguments. _spec
is a list of Specifiers, for ex. int or static int (unsupported)
and decl is a list of Declarators which in turn contain Identifiers
(and may contain ArraySpecifier).
"""
	__slots__ = ['_spec']

	def _processDecl(self, decl):
		"""Process the VariableDeclarator(s) declared in
this VariableDeclaration object. A VariableDeclarator
is added to the children of this VariableDeclaration object"""
		if not decl:
			pass
		elif isinstance(decl, list):
			self.setNumChildren(len(decl))
			count = 0
			for k in decl:
				if isinstance(k, Declarator):
					self.setChild(count,k)
				else:
					raise NotAValidDeclaratorError(str(type(k)))
				count +=1
		elif isinstance(decl, Declarator):
			self.setNumChildren(1)
			self.setChild(0,decl)
		else:
			raise NotAValidDeclaratorError(str(type(decl)))

	def _processSpec(self, spec):
		"""The specifier(s) associated with this VariableDeclaration
is added to the _spec __slots__ list. For example, specifiers like 
int or char"""
		if isinstance(spec, list):
			for k in spec:
				if isinstance(k, Specifier):
					self._spec.append(k)
				else:
					raise NotAValidSpecifierError(str(type(k)))
		elif isinstance(spec, Specifier):
			self._spec.append(spec)
		else:
			raise NotAValidSpecifierError(str(type(spec)))

	def __init__(self, spec, decl=None):
		"""Initializes VariableDeclaration class with 
a list or singleton of leading specifiers, and a list or
singleton of VariableDeclarators. Specifiers are
stored in __slots__._spec while the 
Declarators are set as the Traversable's 
children."""
		self._spec = []
		self.initialize()
		self._processDecl(decl)
		self._processSpec(spec)

	def getDeclaredSymbols(self):
		"""Returns for example: [a, b] for a VariableDeclaration int a,b"""
		return self.getChildren()
			
	def __repr__(self):
		"""Returns the  Ansi C representation of this object, for example
int a,b"""
		retval = ''
		for k in self._spec:
			retval += '%s ' % k
		retval += ','.join([repr(k) for k in self.getChildren()])
		return retval
	__str__ = __repr__

	def items(self):
		"""Used by pickle or copy to get the state
associated with the class. The returned items 
dict contains _spec object from this 
class and the contents of the __slots__ of the 
bases of this class"""
		items = {}
		items['_spec'] = self._spec
		for k in VariableDeclaration.__bases__:
			if hasattr(k, 'items'):
				supitems = k.items(self)
				for k,v in supitems.items():
					items[k] = v
		return dict(items)
	def __getstate__(self):
		"""Returns the results of self.items() call 
when called by pickle or copy"""
		return self.items()
	def __setstate__(self, statedict):
		"""Blindly sets state based on the items like statedict"""
		for k,v in statedict.items():
			setattr(self, k, v)

if __name__ == '__main__':
	from VariableDeclarator import VariableDeclarator
	from Identifier import Identifier
	from keyword import specifiers
#Test1: (meant to work)
	decl = VariableDeclarator(Identifier('x'))
	spec = specifiers.int16
	vardecl = VariableDeclaration(spec, decl)
	print 'test1: ' + repr(vardecl)
#Test2: (meant to work):
#decl = decl
#spec = list of Specifier
	decl = VariableDeclarator(Identifier('y'))
	spec = [specifiers.Global, specifiers.int16]
	vardecl = VariableDeclaration(spec, decl)
	print 'test 2: ' + repr(vardecl)
#Test3: (meant to work)
# decl == list of declarator
# spec == Specifier
	spec = specifiers.int16
	decl = [VariableDeclarator(Identifier('z')), VariableDeclarator(Identifier('w'))]
	vardecl = VariableDeclaration(spec, decl)
	print 'test 3: ' + repr(vardecl)
	print vardecl.getDeclaredSymbols()
#Test4: (not meant to work)
	try:
		vardecl = VariableDeclaration()
	except TypeError:
		print 'failed test4, OK'
#Test5: (not meant to work)
#decl == list of many stuff
#spec = Specifier or List
	decl.append(1)
	try:
		vardecl = VariableDeclaration(spec, decl)
	except NotAValidDeclaratorError:
		print 'failed test5, OK'
#Test6: (not meant to work)
#decl == list of Declarator or Declarator
#spec == Declarator or any type
	decl.pop()
	try:
		vardecl = VariableDeclaration(decl, decl)
	except NotAValidSpecifierError:
		print 'failed Test6, OK'

# TEST: 
# spec == NULL, decl == List of Declarator
# spec == NULL, decl == Declarator
# spec == List of Specifier, decl == List of Declarator
# spec == List of Specifier, decl == Declarator
# spec == Specifier, decl == List of Declarator
# spec == Specifier, decl == Declarator
