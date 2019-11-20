
from hir.Keyword import *
from hir.Declarator import Declarator
from hir.Traversable import ChildNotCorrectType


class NestedDeclarator(Declarator):
    __slots__ = ('_has_param', '_trail', '_lead')

    def __init__(self, nested_decl, lead=None, trail=None, params=None):

        Declarator.__init__(self)
        children = self.getChildren()

        if not isinstance(nested_decl, Declarator):
            raise ChildNotCorrectType(str(type(nested_decl)))

        children.append(nested_decl)

        self._lead = []
        self._trail = []

        if params is not None:
            for pa in params:
                children = self.getChildren()
                self.setNumChildren(self.getNumChildren() + 1)
                children.append(pa)
                pa.setParent(self)
            self._has_param = True
        else:
            self._has_param = False

        if trail is not None:
            for tr in trail:
                self._trail.append(tr)

        if lead is not None:
            for ld in lead:
                self._lead.append(ld)

    def __repr__(self):

        retval_le = ' '.join([repr(le) for le in self._lead])

        children = self.getChildren()

        retval_de = '(' + repr(children[0]) + ')'

        retval_pa = ''
        if self._has_param:
            retval_pa = '(' + ', '.join(
                [repr(ch) for ch in children[1:]]) + ')'

        retval_tr = ' '.join(repr(tr) for tr in self._trail)

        retval = ''
        if retval_le != '':
            retval += retval_le + ' '
        retval += retval_de
        if retval_tr != '':
            retval += ' ' + retval_tr
        if retval_pa != '':
            retval += ' ' + retval_pa
        return retval

    __str__ = __repr__

    def items(self):

        items = {}

        if hasattr(self._lead):
            items['_lead'] = self._lead

        if hasattr(self, "_trail_spec"):
            items["_trail_spec"] = self._trail_spec

        for ke in NestedDeclarator.__bases__:
            if hasattr(ke, 'items'):
                supitems = ke.items(self)
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
        return self.getChildren()[0].get_symbol()


def NestedDeclaratorTest():
    from hir.Identifier import Identifier
    from hir.PointerSpecifier import PointerSpecifier
    from hir.ArraySpecifier import ArraySpecifier
    from hir.VariableDeclarator import VariableDeclarator
    from hir.ParameterDeclarator import ParameterDeclaratorTest
    from hir.VariableDeclaration import VariableDeclaration
    from hir.DeclarationStatement import DeclarationStatement

    ns = VariableDeclarator(Identifier('a', None, False), None,
                            PointerSpecifier([CONST]))

    k = VariableDeclaration(DOUBLE,
                            VariableDeclarator(Identifier('xyz', None, False)))

    ns = NestedDeclarator(ns, None, None, [k])
    ns = VariableDeclarator(ns, ArraySpecifier([3]))
    ns = VariableDeclarator(ns, None, PointerSpecifier())
    ns = DeclarationStatement(VariableDeclaration(INT, ns))
    return ns


if __name__ == '__main__':
    print(NestedDeclaratorTest())
