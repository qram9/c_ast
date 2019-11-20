from hir.Declarator import Declarator
from hir.PointerSpecifier import PointerSpecifier
from hir.ArraySpecifier import ArraySpecifier
from hir.Identifier import Identifier
from hir.Identifier import NotAnIdentifierError


class VariableDeclaratorException(Exception):
    pass


class UnsupportedTrailingSpecifierError(VariableDeclaratorException):
    pass


class UnsupportedLeadSpecifierError(VariableDeclaratorException):
    pass


class VariableDeclarator(Declarator):
    """Represents the name of a declared Identifier 
(and ArraySpecifiers if any. Array specifiers
are in the __slots__ entry, _trail_spec"""

    __slots__ = ("_lead_spec", "_trail_spec")

    def __init__(self, decl, trail_spec=None, lead_spec=None):
        """Initializes VariableDeclarator with a given
Identifier type and an ArraySpecifier set, if passed
as trail_spec argument. Identifiers are also refered to as 
symbols elsewhere in this document. 
Requires declarator name to be 
Identifier type and trail_spec to be ArraySpecifier."""
        if not isinstance(decl, Identifier):
            if not isinstance(decl, Declarator):
                raise NotAnIdentifierError(str(type(decl)))
        self.initialize()
        self.setNumChildren(1)
        self.setChild(0, decl)
        if trail_spec:
            if not isinstance(trail_spec, ArraySpecifier):
                raise UnsupportedTrailingSpecifierError(type(trail_spec))
            self._trail_spec = trail_spec
        if lead_spec:
            if not isinstance(lead_spec, PointerSpecifier):
                raise UnsupportedLeadSpecifierError(type(lead_spec))
            self._lead_spec = lead_spec

    def __repr__(self):
        """Returns Ansi C string value corresponding to 
the variable declarator. For ex. a[10][20]"""

        ret_val = ''

        if hasattr(self, "_lead_spec"):
            ret_val = repr(self._lead_spec) + ' '

        ret_val += repr(self.getChild(0))

        if hasattr(self, "_trail_spec"):
            ret_val += repr(self._trail_spec)

        return ret_val

    __str__ = __repr__

    def items(self):
        """Used by pickle or copy to get the state
associated with the class. The returned items 
dict contains _trail_spec object from hir.his 
class and the contents of the __slots__ of the 
bases of this class"""

        items = {}

        if hasattr(self, "_lead_spec"):
            items["_lead_spec"] = self._lead_spec

        if hasattr(self, "_trail_spec"):
            items["_trail_spec"] = self._trail_spec

        for k in VariableDeclarator.__bases__:
            if hasattr(k, 'items'):
                supitems = k.items(self)
                for k, v in list(supitems.items()):
                    items[k] = v
        return dict(items)

    def __getstate__(self):
        """Returns the results of self.items() call 
when called by pickle or copy"""
        return dict(self.items())

    def __setstate__(self, statedict):
        """Blindly sets state based on the items like statedict"""
        for k, v in list(statedict.items()):
            setattr(self, k, v)

    def get_symbol(self):
        ch = self.getChildren()
        return ch[0].get_symbol()


if __name__ == '__main__':
    from hir.Identifier import Identifier
    from hir.ArraySpecifier import ArraySpecifierTest
    from hir.Keyword import CONST, VOLATILE, RESTRICT
    print((VariableDeclarator(Identifier('a', None, False),
                              ArraySpecifierTest())))
    print((VariableDeclarator(Identifier('a', None, False),
                              ArraySpecifierTest(),
                              PointerSpecifier([CONST,
                                                RESTRICT, VOLATILE]))))
