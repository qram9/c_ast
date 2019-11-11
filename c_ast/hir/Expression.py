from hir.Traversable import Traversable
import sys
# TODO: add clone, swapWith like Cetus: For Later
# TODO: Fix the repr printing
class ExpressionException(Exception): pass
class InvalidTypeNeedsParensError(ExpressionException): pass

class ChildNotAnExpressionError(ExpressionException):
    """Exception to be raised when an non-Expression type child is specified"""
    def __init__(self, value=''):
        self.value = value
    def __str__(self):
        return 'Invalid type:(%s) for expression child, must be Expression type' % (self.value)

class Expression(Traversable):
    """Represents an abstract base type for all 
expression types in this HIR"""
    __slots__ = ['_needs_parens']
    def __init__(self):
        """Expression type is somewhat of an C++/Java abstract type, 
__init__ must only be called by a subclass. 
Sets _needs_parens to False. User may set it 
to true in a subclass to add a parenthesis expression"""
        self._needs_parens = False
        Traversable.__init__(self)

    def setChild(self, which, t):
        """Overrides Traversable's setChild to 
enforce the rule that a child of an Expression must be 
type Expression"""
        if isinstance(t, Expression):
            Traversable.setChild(self, which, t)
        else:
            raise ChildNotAnExpressionError(str(type(t)))
        return self

    def __repr__(self):
        """Returns a string representation of the contents 
of the expression object (with enclosing () if necessary). 
Currently the returned string is in AnsiC. 
Change this function to return different a representation."""
        retval = '' 
#        retval = 'parent(%s)' % (str(id(self._parent)))
        if self._needs_parens:
            retval += '('
            for k in self.getChildren():
                retval += repr(k)
#                if k != self._children[-1]:
#                    retval += ' '    
            retval += ')'
        else:
            for k in self.getChildren():
                retval += repr(k)
#                if k != self._children[-1]:
#                    retval += ' '    
        return retval
    __str__ = __repr__

    def getParens(self):
        """Returns true if __ slots__ entry _needs_parens is set"""
        return self._needs_parens

    def setParens(self, f):
        """Sets __slots__ entry _needs_parens to true or false. If true, 
printing will return the contents of the expression enclosed in ()"""
        if not isinstance(f, bool):
            raise InvalidTypeNeedsParensError( type(f))
        self._needs_parens = f
        return self

    def items(self):
        """Returns items dict when called from hir.etstate. 
Adds __slots__ entry "_needs_parens" to items dict.
Recurses into base classes and collects items from hir.here too."""
        items = {}
        name = '_needs_parens'
        items[name] = getattr(self,name)
        for k in Expression.__bases__:
            if hasattr(k, 'items'):
                supitems = k.items(self)
                for k,v in list(supitems.items()):
                    items[k] = v
        return dict(items)

    def __getstate__(self):
        """Returns a dict representing the contents of 
this Expression object and its base classes 
instances' contents. Uses the items() function.
Contents added here is _needs_parens, by calling
'items' function"""
        return dict(self.items())

    def __setstate__(self, statedict):
        """Blindly calls setattr with entried from hir. 
__getstate__ like string->attr dict"""
        for k,v in list(statedict.items()):
            setattr(self, k, v)

if __name__ == '__main__':
    exp = Expression()
#    exp.testIfNoChild()
#    exp.testIfNoParent()
    tra = Traversable()
    exp.setParens(True)
    exp.setParent(tra)
    exp.setNumChildren(2)
    chi1 = Expression()
    chi2 = Expression()
    exp.setChild(0,chi1)
    exp.setChild(1,chi2)
#    exp.getChild(100)
#    exp.setChild(1,1)
#    exp.setChild(100,chi1)
    print((repr(exp)))
#    exp.setParent(1)
