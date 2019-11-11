from hir.BinaryExpression import BinaryExpression as BinExp
from hir.UnaryExpression import UnaryExpression as UnaExp
from hir.Operator import accessOperator, binaryOperator, unaryOperator
class AccessExpression(BinExp):
    """Access Expression works on any 
sequence with three args, lhs, op, rhs. 
Except for a differentiating class type, and 
operator from hir access operators group, 
instances hold same data as BinaryExpression 
instances."""
    def __init__(self, *args):
        lhs, op, rhs = args
        BinExp.__init__(self, lhs, op, rhs)

from hir.Identifier import Identifier

def AccessExpressionTest1():
    return AccessExpression(Identifier('a', None, False),
            accessOperator.DOT, Identifier('b', None, False))

def AccessExpressionTest2():
    return AccessExpression(Identifier('a', None, False),
            accessOperator.ARROW, Identifier('b', None, False))

def AccessExpressionTest3():
    una_exp1 = UnaExp(unaryOperator.DEREFERENCE,
            Identifier('b', None, False))
    una_exp1.setParens(True)
    binary_exp1 = BinExp(Identifier('a', None, False),
            binaryOperator.ADD,
            una_exp1)
    binary_exp1.setParens(True)
    return UnaExp(unaryOperator.DEREFERENCE,
            AccessExpression(binary_exp1,
                accessOperator.ARROW,
                Identifier('c', None, False)).setParens(True))

if __name__ == '__main__':
    print(AccessExpressionTest1())
    print(AccessExpressionTest2())
    print(AccessExpressionTest3())
