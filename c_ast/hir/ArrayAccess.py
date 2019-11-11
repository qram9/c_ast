from hir.Expression import Expression
class ArrayAccessException(Exception):
    def __init__(self, value):
        self.value = value
class InvalidIndexTypeError(ArrayAccessException):
    def __repr__(self):
        return 'Invalid type:(%s) for index, expected Expression or list of expressions' % (value)
class InvalidArrayTypeError(ArrayAccessException):
    def __repr__(self):
        return 'Invalid type: (%s) for Array name, expected Expression' %(value)

class ArrayAccess(Expression):
    """Represents an Array Access expression in C. For example, a[i] or a[i+s]"""
    def _catchIndexError(self, indices):
        """Helper function that check if indices specified by 
the ArrayAccess are either a list of expressions or single 
expressions"""
        if not isinstance(indices, list):
            if not isinstance(indices, Expression):
                raise InvalidIndexTypeError(str(type(indices)))
        else:
            for k in indices:
                if not isinstance(k, Expression):
                    raise InvalidIndexTypeError(str(type(k)))
    def _addNodes(self,array, indices):
        """Adds the specified array name and indices
to create a new ArrayAccess subtree"""
        if isinstance(indices, list):
            self.setNumChildren(1+len(indices))
            self.setChild(0, array)
            r = 1
            for k in indices:
                self.setChild(r, k)
                r = r+1
        else:
            self.setNumChildren(2)
            self.setChild(0, array)
            self.setChild(1, indices)

    def __init__(self, array, indices):
        """Initializes an ArrayAccess object with an 
Expression type for Array_name, and either a list 
of expressions or a single expression for the 
address location"""
        if not isinstance(array, Expression):
            raise InvalidArrayTypeError(str(type(array)))
        self._catchIndexError(indices)
        Expression.__init__(self)
        self.initialize()
        self._addNodes(array, indices)

    def __repr__(self):
        """Returns a string representation of the contents 
of the array access object. Currently the 
returned string is in AnsiC. 
Change this function to return different a representation."""
        retval = repr(self.getChild(0))
        for k in range(1,self.getNumChildren()):
            retval += '[' + repr(self.getChild(k)) + ']'
        return retval
    __str__ = __repr__

from hir.Identifier import Identifier
def ArrayAccessTest():
    a = ArrayAccess(Identifier('k', None, False),
            [Identifier(k, None, False) for k in ['a', 'b','c']])
    print(a)
    b = ArrayAccess(Identifier('k', None, False), Identifier('i', None, False))
    print(b)
    return b

if __name__ == '__main__':
    ArrayAccessTest()
