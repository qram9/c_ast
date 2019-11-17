from hir.Specifier import Specifier

class PointerSpecifierException(Exception):
    def __init__(self, value):
        self.value = value

class PointerSpecifier(Specifier):
    'Pointer Specifier'
    __slots__ = ('qualifiers')
    
    def __init__(self,qual):
        self.qualifiers = []
        for k in qual:
            self.qualifiers.append(k)

    def __str__(self):
        retval = '*'
        jj = ' '.join([str(k) for k in self.qualifiers])
        if jj != '':
            retval += ' ' + jj
        return retval

    __repr__ = __str__

    def items(self):
        """Returns the 'dimensions' list of ints"""
        items = {}
        items['qualifiers'] = self.qualifiers
        for k in PointerSpecifier.__bases__:
            if hasattr(k, 'items'):
                supitems = k.items(self)
                for k,v in list(supitems.items()):
                    items[k] = v
        return dict(items)

    def __getstate__(self):
        """Returns the 'qualifier' list of ints. Calls items directly"""
        return dict(self.items())

    def __setstate__(self, statedict):
        """Blindly sets the state of this object, using a statedict"""
        for k,v in list(statedict.items()):
            setattr(self, k, v)

def PointerSpecifierTest():
    from hir.Keyword import CONST, VOLATILE, RESTRICT
    k = PointerSpecifier([CONST])
    print(k)
    k = PointerSpecifier([CONST, VOLATILE])
    print(k)
    k = PointerSpecifier([CONST, RESTRICT])
    print(k)
    k = PointerSpecifier([CONST, RESTRICT, VOLATILE])
    print(k)

if __name__ == '__main__':
    PointerSpecifierTest()


