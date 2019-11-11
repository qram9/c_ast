from hir.Statement import Statement
from hir.Expression import Expression

class ExpressionStatement(Statement):
    __slots__ = ('_expr')

    def __init__(self, expr):
        """Represents a Ansi C expression statement, 
for example, a = b; a = b+c; or b++;. Traversable
type has 1 child that holds the 'expr' argument. 
There is an 'expr' attr in __slots__. 
The Traversable children based system may come into 
rethink if experiments indicate difficulty in usage"""
        Statement.__init__(self)
        self.setNumChildren(1)
        expr.setParent(self)
        expr.setParens(False)
        self._expr = expr
        self.setChild(0, expr)

    def getExpression(self):
        """Returns the __slots__.expr attribute"""
        return self._expr

    def __repr__(self):
        return repr(self.getExpression()) + ';'

    __str__ = __repr__

    def items(self):
        """Returns items dict when called from hir.etstate. 
Adds __slots__ entry "_expr" to items dict.
Recurses into base classes and collects items from hir.here too."""
        items = {}
        items['_expr'] = self._expr
        for k in ExpressionStatement.__bases__:
            if hasattr(k, 'items'):
                supitems = k.items(self)
                for k,v in list(supitems.items()):
                    items[k] = v
        return dict(items)

    def __getstate__(self):
        """Returns a dict representing the contents of 
this ExpressionStatement object and its base classes 
instances' contents. Uses the items() function.
Contents added here is _expr"""
        return dict(self.items())

    def __setstate__(self, statedict):
        """Blindly calls setattr with entried from hir. 
__getstate__ like string->attr dict"""
        for k,v in list(statedict.items()):
            setattr(self, k, v)

from hir.AssignmentExpression import AssignmentExpression
from hir.Identifier import Identifier
from hir.Operator import assignmentOperator

def ExpressionStatementTest():
    return ExpressionStatement(
            AssignmentExpression(Identifier('a', None, False),
                assignmentOperator.ADD, Identifier('b', None, False)))

from hir.BinaryExpression import BinaryExpression
from hir.Operator import binaryOperator
from hir.Identifier import Identifier

if __name__ == '__main__':
    id1 = Identifier('a', None, False)
    id2 = Identifier('b', None, False)
    binexp = BinaryExpression(id1, binaryOperator.ADD, id2)
    expstmt = ExpressionStatement(binexp)
    print (expstmt)
