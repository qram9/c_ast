#TODO
"""Represents an Ansi C function prototype
declarator. Use for TcGen is not foreseen.
Will not be supported until further notice"""

from Declarator import Declarator
from Declaration import Declaration
from Identifier import Identifier
from Specifier import Specifier

class NameNotAnIdentifier(Exception):
	def __init__(self, value=''):
		self.value = value
	def __str__(self):
		return 'Invalid type:(%s), in place of Identifier' % (value)

class ParameterNotSupportedError(Exception):
	def __init__(self, value=''):
		self.value = value
	def __str__(self):
		return 'Invalid type:(%s), in place of Identifier' % (value)

class ProcedureDeclarator(Declarator):
	__slots__ = ['lead', 'trail']
	def __init__(self, name, lead=[], params=[]):
		self.lead = []
		self.trail = []
		if not isinstance(name, Identifier):
			raise NameNotAnIdentifier(str(type(name)))
		self.initialize()
		self.setNumChildren(1)
		self.setChild(0, name)
		for k in lead:
			if not isinstance(k, Specifier):
				raise LeadingSpecNotASpecifierError(str(type(k)))
			self.lead.append(k)
		for k in params:
			if isinstance(k, Declaration):
				self.trail.append(k)
			elif isinstance(k, Specifier):
				self.trail.append(k)
			else:
				raise ParameterNotSupportedError(str(type(k)))
	def getSymbol(self):
		return self.getChild(0)

	def __repr__(self):
		retval = ''
		retval = ' '.join([str(k) for k in self.lead])
		retval += ' ' + repr(self.getChild(0))
		retval += '('
		retval += ','.join([str(k) for k in self.trail])
		retval += ')'
		return retval
	__str__ = __repr__
	def items(self):
		items = {}
		items['lead'] = self.lead
		items['trail'] = self.trail
		for k in ProcedureDeclarator.__bases__:
			if hasattr(k, 'items'):
				supitems = k.items(self)
				for k,v in supitems.items():
					items[k] = v
		print 'items for ProcedureDeclarator <%s>:' % self, items
		return dict(items)
	def __getstate__(self):
		return self.items()
	def __setstate__(self, statedict):
		print 'New set state for ProcedureDeclarator'
		for k,v in statedict.items():
			setattr(self, k, v)

if __name__ == '__main__':
	from Identifier import Identifier
	from keyword import specifiers
	from VariableDeclaration import VariableDeclaration
	from VariableDeclarator import VariableDeclarator
	k = ProcedureDeclarator(Identifier('proc_name'), [specifiers.int8], \
		[VariableDeclaration(specifiers.int8, VariableDeclarator(Identifier('x'))), specifiers.inT])
	print k
	from Declaration import Declaration
	l = Declaration()
	l.setChild(0,k)
	print l
	from DeclarationStatement import DeclarationStatement
	print DeclarationStatement(l)
