from hir.Expression import Expression
from hir.Operator import binaryOperator
from hir.Operator import getBinaryOperatorList, getAssignmentOperatorList, getConditionalOperatorList

class BinaryExpressionException(Exception): pass
class InvalidBinaryOperatorTypeError(BinaryExpressionException): pass
#class InvalidBinaryExpressionError(BinaryExpressionException): pass

class BinaryExpression(Expression):
    """Subclass of Expression, contains _op to hold binaryOperator"""
    __slots__ = ['_op']
    def _catchNotBinaryOperatorError(self, uop):
        """Catches Error when binary expression instantiated 
with an unknown type for operator. Passed operator 
must be present in one of the lists returned by 
getBinaryOperatorList(), getAssignmentOperatorList(). 
Care must be taken here if you have made a copy 
of an individual operator type."""
        bops = getBinaryOperatorList()
        aops = getAssignmentOperatorList()
        cops = getConditionalOperatorList()
        bops.extend(aops)
        bops.extend(cops)
        allops = bops
        for anop in allops:
            if anop == uop:
                return
        else:
            print((uop, type(uop), id(uop)))
            raise InvalidBinaryOperatorTypeError( type(uop), id(uop))

    def __init__(self, *args):
        """Binary Expression initialized with a sequence with lhs, uop, rhs"""
        Expression.__init__(self)
        lhs, uop, rhs = args
        self.setOperator(uop)
        lhs.setParent(self)
        rhs.setParent(self)
        self.setNumChildren(2)
        self.setLHS(lhs)
        self.setRHS(rhs)
        self.setParens(False)

#    def setExpression(self, expr):
#        """Set the contents: lhs, operator, rhs of binary expression from hir.nother expression"""
#        if not isinstance(expr, BinaryExpression):
#            raise InvalidBinaryExpressionError, type(expr)
#        self.setParent(expr.getParent())
#        self.setLHS(expr.getLHS())
#        self.setRHS(expr.getRHS())
#        self.setOperator(expr.getOperator())

    def getOperator(self):
        """Returns the operator __slots__ entry: _op"""
        return self._op
    def getRHS(self):
        """Returns the right side child of the binary expression"""
        return self.getChild(1)
    def getLHS(self):
        """Returns the left side child of the binary expression"""
        return self.getChild(0)

    def setRHS(self, expr):
        """Sets the right side child of the binary expression"""
        self.setChild(1, expr)
    def setLHS(self, expr):
        """Sets the left side child of the binary expression"""
        self.setChild(0, expr)
    def setOperator(self, uop):
        """Sets the operator __slots__ entry:_op"""
        self._catchNotBinaryOperatorError(uop)
        self._op = uop

    def __repr__(self):
        """Returns a string representation of the contents 
of the binary expression object (with enclosing () if 
necessary). Currently the returned string is in AnsiC. 
Change this function to return different a representation."""
        if self.getParens():
            retval = '(' + repr(self.getLHS()) + repr(self._op) + repr(self.getRHS()) + ')'
        else:
            retval = repr(self.getLHS()) + repr(self._op) + repr(self.getRHS())
        return retval
    __str__ = __repr__

    def items(self):
        """Returns items dict when called from hir.etstate. 
Adds __slots__ entry "_op" to items dict.
Recurses into base classes and collects items from hir.here too."""
        items = {}
        name = self.getOperator()
        items['_op'] = getattr(self,'_op')
        for k in BinaryExpression.__bases__:
            if hasattr(k, 'items'):
                supitems = k.items(self)
                for k,v in list(supitems.items()):
                    items[k] = v
        return dict(items)
    def __getstate__(self):
        """Returns a dict representing the contents of 
this Binary Expression object and its base classes 
instances' contents. Uses the items() function.
Contents added here is _op"""
        return dict(self.items())
    def __setstate__(self, statedict):
        """Blindly calls setattr with entried from hir. 
__getstate__ like string->attr dict"""
        for k,v in list(statedict.items()):
            setattr(self, k, v)

from hir.Operator import binaryOperator
from hir.Identifier import Identifier
def BinaryExpressionTest():
    return BinaryExpression(Identifier('a'), binaryOperator.SUBTRACT, Identifier('b'))

from hir.Operator import binaryOperator
from hir.Identifier import Identifier
import pickle
from hir.bfs import bfsItr
if __name__ == '__main__':
    binary_exp1 = BinaryExpression(Identifier('a'), binaryOperator.SUBTRACT, Identifier('b'))
    binary_exp1.setParens(True)
    binary_exp2 = BinaryExpression(Identifier('a'), binaryOperator.SUBTRACT, Identifier('b'))
    binary_exp2.setParens(False)
    binary_exp3 = BinaryExpression(binary_exp1, binaryOperator.ADD, binary_exp2)
    print((repr(binary_exp3)))
    binary_exp3.setParens(True)
    print ('for pickle r')
    r = pickle.loads(pickle.dumps(binary_exp3,2))
    for k in bfsItr(r):
        print(('next: <%d,%s,%s>' % (id(k), str(type(k)), k)))
    print ('for copy l of pickle r')
    import copy
    l = copy.deepcopy(r)
    for k in bfsItr(l):
        print(('next: <%d,%s,%s>' % (id(k), str(type(k)), k)))
    print ('for original binexp3')
    for k in bfsItr(binary_exp3):
        print(('next: <%d,%s,%s>' % (id(k), str(type(k)), k)))

