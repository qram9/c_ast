# TODO: getParentTables()
# TODO: addDeclaration()
# TODO: addDeclarationBefore()
# TODO: addDeclarationAfter()
class NotADeclarationError(Exception):
	def __init__(self, value=''):
		self.value = value
	def __str__(self):
		print(('Invalid type: (%s) to add to symbol table', self.value))
class SymbolTableException(Exception): pass
class SymbolNotFound(SymbolTableException): pass
class DuplicateSymbolInsertionError(SymbolTableException): pass

from hir.odict import odict
from hir.Declaration import Declaration
class SymbolTable(object):
	"""Represents a symbol table type in the HIR
Used by CompoundStatements, Procedures, TranslationUnits (files)
to create lexical scopes in the program. A symbols declared in
a scope is stored in an ordered dict type: odict from hir.he Python
cook book. Symbols can be added with a addDeclaration. Declarations
must be of type Declaration. Declarations are stored by using the 
repr(identifier), where identifier is usually of type Identifier,
and repr is the string representation of it. I use repr instead of the 
object because that conveniently lets me use different objects with the 
same name and finding a match nonetheless"""
	__slots__ = ['symbolTable']
	def __init__(self):
		"""Initializes SymbolTable with a new odict type"""
		self.symbolTable = odict({})
	def findSymbol(self, exp):
		"""Looks up a symbol using repr(arg0) and returns it. Throws
exception when not found. CompoundStatement or Procedure must catch
these errors and process these errors."""
		return self.symbolTable[repr(exp)]
	def _catchNotADeclarationError(self, decl):
		if not isinstance(decl, Declaration):
			raise NotADeclarationError(str(type(decl)))
	def addDeclaration(self, name, decl):
		"""Adds a declaration type to symbol table. If this a duplicate,
raises DuplicateSymbolInsertionError exception"""
		self._catchNotADeclarationError(decl)
		if repr(name) in self.symbolTable:
                    raise DuplicateSymbolInsertionError(
                            'Symbol Table has an entry with'
                            ' same representation:<%s:%s>'
                            % (repr(name), repr(self.symbolTable[repr(name)])))
		self.symbolTable[repr(name)] = decl
	def __repr__(self):
		return repr(self.symbolTable)
	def items(self):
		"""Returns the symbolTable __slots__ entry in an
ordered dict for getstate"""
		items = {}
		items['symbolTable'] = self.symbolTable
		return dict(items)
	def __getstate__(self):
		"""Returns the state, i.e. __slots__.symbolTable to pickle or copy"""		
		return dict(self.items())
	def __setstate__(self, statedict):
		"""Blindly sets the given statedict into a new object of this class"""
		for k,v in list(statedict.items()):
			setattr(self, k, v)
if __name__ == '__main__':
	sym = SymbolTable()
	from hir.import_all import *
	sym.addDeclaration('p', VariableDeclaration(specifiers.int16, VariableDeclarator(Identifier('k'))))
	sym.addDeclaration('l', VariableDeclaration(specifiers.int16, VariableDeclarator(Identifier('m'))))
