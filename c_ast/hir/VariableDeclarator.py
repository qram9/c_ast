class VariableDeclaratorException(Exception): pass

class NotAnIdentifierError(VariableDeclaratorException):
    def __init__(self, value=''):
        self.value = value
    def __str__(self):
        return 'Invalid type:(%s), in place of Identifier' % (value)

class UnsupportedTrailingSpecifierError(VariableDeclaratorException): pass
    
from hir.Declarator import Declarator
from hir.Identifier import Identifier
from hir.ArraySpecifier import ArraySpecifier

class VariableDeclarator(Declarator):
    """Represents the name of a declared Identifier 
(and ArraySpecifiers if any. Array specifiers
are in the __slots__ entry, _trail_spec"""

    __slots__ = ("_trail_spec")

    def __init__(self, decl, trail_spec=None):
        """Initializes VariableDeclarator with a given
Identifier type and an ArraySpecifier set, if passed
as trail_spec argument. Identifiers are also refered to as 
symbols elsewhere in this document. 
Requires declarator name to be 
Identifier type and trail_spec to be ArraySpecifier."""
        if not isinstance(decl, Identifier):
            raise NotAnIdentifierError(str(type(decl)))
        self.initialize()
        self.setNumChildren(1)
        self.setChild(0,decl)
        if trail_spec:
            if not isinstance(trail_spec, ArraySpecifier):
                raise UnsupportedTrailingSpecifierError( type(trail_spec))
            self._trail_spec = trail_spec

    def getSymbol(self):
        """Returns the symbol or the identifier 
associated with this VariableDeclarator.
The declarator's Identifier type is also refered to as 
the declarator's symbol, here and elsewhere"""
        return self.getChild(0)

    def __repr__(self):
        """Returns Ansi C string value corresponding to 
the variable declarator. For ex. a[10][20]"""
        if hasattr(self, "_trail_spec"):
            return repr(self.getChild(0)) + repr(self._trail_spec)
        else:
            return repr(self.getChild(0))

    __str__ = __repr__

    def items(self):
        """Used by pickle or copy to get the state
associated with the class. The returned items 
dict contains _trail_spec object from hir.his 
class and the contents of the __slots__ of the 
bases of this class"""
        items = {}
        if hasattr(self, "_trail_spec"):
            items["_trail_spec"] = self._trail_spec
        for k in VariableDeclarator.__bases__:
            if hasattr(k, 'items'):
                supitems = k.items(self)
                for k,v in list(supitems.items()):
                    items[k] = v
        return dict(items)

    def __getstate__(self):
        """Returns the results of self.items() call 
when called by pickle or copy"""
        return dict(self.items())

    def __setstate__(self, statedict):
        """Blindly sets state based on the items like statedict"""
        for k,v in list(statedict.items()):
            setattr(self, k, v)

if __name__ == '__main__':
    from hir.Identifier import Identifier
    from hir.ArraySpecifier import ArraySpecifierTest
    print((VariableDeclarator(Identifier('a', None, False),
            ArraySpecifierTest())))

