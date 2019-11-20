from hir.Identifier import Identifier
from hir.BinaryExpression import BinaryExpression
from hir.Operator import conditionalOperator


class ConditionalExpression(BinaryExpression):
    """Conditional Expression works on any 
sequence with three args, true_expr, uop, false_expr. 
Except for a differentiating class type, and 
operator from hir.he conditional operators group, 
instances hold same data as BinaryExpression 
instances."""

    def __init__(self, *args):
        true_expr, uop, false_expr = args
        BinaryExpression.__init__(self, true_expr,
                                  uop, false_expr)


if __name__ == '__main__':
    exp1 = Identifier('a', None, False)
    exp2 = Identifier('b', None, False)
    cond_exp = ConditionalExpression(
        exp1, conditionalOperator.COMPARE_EQ, exp2)
    print((repr(cond_exp)))
