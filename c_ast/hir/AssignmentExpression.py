from hir.BinaryExpression import BinaryExpression
from hir.Operator import assignmentOperator

class AssignmentExpression(BinaryExpression):
    """Assignment Expression works on any 
sequence with three args, lhs, op, rhs. 
Except for a differentiating class type, and 
operator from hir.he assignment operators group, 
instances hold same data as BinaryExpression 
instances."""
    def __init__(self, *args):
        lhs, op, rhs = args
        BinaryExpression.__init__(self, lhs, op, rhs)

from hir.Identifier import Identifier

def AssignmentExpressionTest():
    return AssignmentExpression(Identifier('a', None, False),
            assignmentOperator.ADD, Identifier('b', None, False))

if __name__ == '__main__':
    print(AssignmentExpressionTest())
