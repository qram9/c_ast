from hir.IDExpression import IDExpression


class IdentifierException(Exception):
    pass


class InvalidNameTypeError(IdentifierException):
    pass


class MissingImmediateParentError(IdentifierException):
    pass


class NotAnIdentifierError(IdentifierException):
    def __init__(self, value=''):
        self.value = value

    def __str__(self):
        return 'Invalid type:(%s), in place of Identifier' % (value)


class SymbolTableError(IdentifierException):
    pass


class Identifier(IDExpression):
    """Represents a variable type in AnsiC.
    Has an Associated _name __slots__ parameter.
    Use the _name entry to look up in the symbol table
    hierarchy to find a corresponding Declaration. Subclasses
    IDExpression"""

    __slots__ = ['_name', '_parent']

    def __init__(self, name, parent, test=True,
                 isGlobal=False, isTypename=False):
        """Initializes an Identifier from given arguments.
        Expect name to be type python <str>. isGlobal, isTypename..."""
        if not isinstance(name, str):
            raise InvalidNameTypeError(type(name))
        self._name = name
        IDExpression.__init__(self, isGlobal, isTypename)
        if test:
            self.findSymbol()

    def setName(self, name):
        """Sets the name __slots__ entry to a
        given <str>"""
        if not isinstance(name, str):
            raise InvalidNameTypeError(type(name))
        self._name = name

    def getName(self):
        """Returns the string __slots__ entry for name"""
        return self._name

    def findSymbol(self):
        """Looks up this identifier in the parent hierarchy and gets
        the SymbolTable entry for it"""
        if self.getParent() == None:
            raise MissingImmediateParentError(
                'Expression does not have parent')
        p = self.getParent()
        while p:
            if hasattr(p, 'symbolTable'):
                return p.findSymbol(self)
            else:
                p = p.getParent()
        raise SymbolTableError(repr(self))

    def __repr__(self):
        # return 'Identifier(%s)' % (self.getName())
        return self.getName()

    def __str__(self):
        return self.getName()

    def items(self):
        """Returns items dict when called from hir.etstate.
        Adds __slots__ entry "_name" to items dict.
        Recurses into base classes and collects items
        from hir.here too."""
        items = {}
        items['_name'] = getattr(self, '_name')
        for k in Identifier.__bases__:
            if hasattr(k, 'items'):
                supitems = k.items(self)
                for k, v in list(supitems.items()):
                    items[k] = v
        return dict(items)

    def __getstate__(self):
        """Returns a dict representing the contents of
        this Identifier object and its base classes
        instances' contents. Uses the items() function.
        Contents added here is _needs_parens, by calling
        'items' function"""
        return dict(self.items())

    def __setstate__(self, statedict):
        """Blindly calls setattr with entried from hir.
        __getstate__ like string->attr dict"""
        for k, v in statedict.items():
            setattr(self, k, v)

    def __eq__(self, other):
        if isinstance(other, Identifier):
            return repr(self) == repr(other)
        else:
            return False

    def __hash__(self):
        return hash(repr(self.getName()))

    def get_symbol(self):
        return self


if __name__ == '__main__':
    z = Identifier('z', None, False)
    r = Identifier('z', None, False)
