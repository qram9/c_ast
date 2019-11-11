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

from hir.Declaration import Declaration
from hir.Traversable import Traversable
class SymbolTable(Traversable):
    """Represents a symbol table type in the HIR
Used by CompoundStatements, Procedures, TranslationUnits (files)
to create lexical scopes in the program. A symbols declared in
a scope is stored in an ordered dict type: dict.
Symbols can be added with an addDeclaration. Declarations
must be of type Declaration. Declarations are stored by using the 
str(identifier), where identifier is usually of type Identifier,
and str is the string representation of it. I use str instead of the 
object because that conveniently lets me use different objects with the 
same name and finding a match nonetheless."""
    __slots__ = ['currSyms']

    def __init__(self):
        """Initializes SymbolTable with a new dict type"""
        self.currSyms = {}
        Traversable.__init__(self)

    def findSymbol(self, exp):
        """Looks up a symbol using str(arg0) and returns it. Throws
exception when not found. CompoundStatement or Procedure must catch
these errors and process these errors."""
        k = str(exp)
        try:
            return self.currSyms[k]
        except KeyError:
            raise SymbolNotFound('Identifier not found:<%s>' % (k))

    def _catchNotADeclarationError(self, decl):
        if not isinstance(decl, Declaration):
            raise NotADeclarationError(str(type(decl)))

    def addDeclaration(self, name, decl):
        """Adds a declaration type to symbol table.
If this a duplicate, raises DuplicateSymbolInsertionError exception"""
        self._catchNotADeclarationError(decl)
        if str(name) in self.currSyms:
            raise DuplicateSymbolInsertionError(
                    'Symbol Table has an entry with'
                    ' same representation:<%s:%s>'
                    % (str(name), str(self.currSyms[str(name)])))
        self.currSyms[str(name)] = decl

    def __repr__(self):
        return repr(self.currSyms)

    def __str__(self):
        return repr(self)

    def items(self):
        """Returns the symbolTable __slots__ entry in an dict for getstate"""
        items = {}
        items['currSyms'] = self.currSyms
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
    sym.addDeclaration('p', VariableDeclaration(specifiers.int16,
        VariableDeclarator(Identifier('k', None, False))))
    sym.addDeclaration('l', VariableDeclaration(specifiers.int16,
        VariableDeclarator(Identifier('m', None, False))))
