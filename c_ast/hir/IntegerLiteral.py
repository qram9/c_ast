from hir.Literal import Literal


class InvalidTypeIntegerLiteralError(Exception):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return 'Invalid type: (%s) for integer literal, expected: (%s)' % (value, str(type(int)))


class IntegerLiteral(Literal):
    """Represents a Integer literal lexical token.
Subclasses Literal type. Sets the given character
value to a __slots__ entry 'value'."""
    __slots__ = ['value']

    def __init__(self, value):
        """Initializes a Ansi C Integer Literal object. Tests
if given character is of type python <int> (Sorry, not 
Ansi C yet. But the size of the current implementation. Sets the
__slots__.value parameter"""
        if not isinstance(value, int):
            raise InvalidTypeIntegerLiteralError(str(type(int)))
        self.initialize()
        Literal.__init__(self)
        self.value = value

    def __repr__(self):
        """Returns the integral number"""
        return str(self.value)
    __str__ = __repr__

    def items(self):
        """Returns items dict when called from hir.etstate. 
Adds __slots__ entry "value" to items dict.
Recurses into base classes and collects items from hir.here too."""
        items = {}
        items['value'] = self.value
        for k in IntegerLiteral.__bases__:
            if hasattr(k, 'items'):
                supitems = k.items(self)
                for k, v in list(supitems.items()):
                    items[k] = v
        return dict(items)

    def __getstate__(self):
        """Returns current state for 'pickling' or 'copy'. 
Adds __slots__ entry "value" to items dict."""
        return dict(self.items())

    def __setstate__(self, statedict):
        """Blindly sets state from hir. given statedict"""
        for k, v in list(statedict.items()):
            setattr(self, k, v)


def IntegerLiteralTest():
    l = IntegerLiteral(0x12)
    return l


if __name__ == '__main__':
    print(IntegerLiteralTest())
