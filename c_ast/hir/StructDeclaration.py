
from hir.Declaration import Declaration
from hir.DeclarationStatement import DeclarationStatement
from hir.VariableDeclaration import VariableDeclaration
from hir.Identifier import Identifier, NotAnIdentifierError
from hir.Specifier import Specifier


class IllegalFieldError(Exception):
    ''' Illegal Struct Field type'''

    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return 'Invalid type: (%s) for struct field' % (self.value)


class StructDeclaration(Declaration):
    __slots__ = ('_name', '_is_union')

    def __init__(self, idexp, is_union=False):

        Declaration.__init__(self)

        if not isinstance(idexp, Identifier):
            raise NotAnIdentifierError(str(type(idexp)))

        self._name = idexp
        self._is_union = is_union

    def get_name(self):
        return self._name

    def add_field(self, decl):
        if not isinstance(decl, DeclarationStatement):
            raise IllegalFieldError(str(type(decl)))
        self.setNumChildren(self.getNumChildren() + 1)
        children = self.getChildren()
        children.append(decl)
        decl.setParent(self)

    def __repr__(self):
        if self._is_union:
            struct = 'union'
        else:
            struct = 'struct'
        retval = struct + ' ' + repr(self._name)
        decs = '\n'.join(repr(ch) for ch in self.getChildren())
        if decs != '':
            retval += ' {\n' + decs + '\n}'
        return retval

    __str__ = __repr__

    def items(self):
        items = {}
        items['_name'] = self._name
        for base in StructDeclaration.__bases__:
            if hasattr(base, 'items'):
                supitems = base.items(self)
                for k, v in list(supitems.items()):
                    items[k] = v
        return dict(items)

    def __getstate__(self):
        return self.items()

    def __setstate__(self, statedict):
        for k, v in list(statedict.items()):
            setattr(self, k, v)

    def get_symbol(self):
        return self._name


def StructDeclarationTest():
    from hir.VariableDeclarator import VariableDeclarator
    from hir.VariableDeclaration import VariableDeclaration
    from hir.Keyword import specifiers

    k = VariableDeclaration(specifiers.int8,
                            VariableDeclarator(Identifier('y', None, False)))
    s = DeclarationStatement(k)
    id1 = Identifier('a', None, False)
    struct_dec = StructDeclaration(id1)
    struct_dec.add_field(s)
    k = VariableDeclaration(specifiers.int8,
                            VariableDeclarator(Identifier('x', None, False)))
    s = DeclarationStatement(k)
    struct_dec.add_field(s)

    print(struct_dec.getDeclaredSymbols())
    # id2 = Identifier('b', None, False)
    # struct_dec1 = StructDeclaration(id2)
    # struct_dec1.add_field(struct_dec)
    return struct_dec


if __name__ == '__main__':
    print(StructDeclarationTest())
