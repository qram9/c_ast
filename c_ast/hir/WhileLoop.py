from hir.Statement import Statement
from hir.Loop import Loop
from hir.AstBuild import *


class WhileLoop(Statement, Loop):
    """Ansi C while loop. Requires a ConditionalExpression,
and a compound statement for a body"""

    def __init__(self, *args):
        """WhileLoop works on any sequence type containing 
2 elements. Initializes 2 children in the traversable 
class. Tests if the specified 'condition' argument
is of type EXP. Secondly, tests if
the specified 'body' is of type CompoundStatement"""
        condition, body = args
        self.initialize()
        self.setNumChildren(2)
        if not isinstance(condition, EXP):
            raise InvalidCondtionException(type(condition))
        self.setChild(0, condition)
        if not isinstance(body, COMPSTM):
            raise InvalidBodyException(type(body))
        self.setChild(1, body)

    def __repr__(self):
        """Returns a string representation of the contents 
of the do loop object (Example: 'while (...) {...}
). Currently the returned string is in AnsiC. 
Change this function to return different a representation."""
        retval = 'while ('
        retval += repr(self.getChild(0)) + ')'
        retval += repr(self.getChild(1))
        return retval


if __name__ == '__main__':
    control = CONDEXP(ID('a', None, False),
                      CONDOP.COMPARE_EQ, ID('a', None, False))
    body = COMPSTM()
    assignexp1 = ASNEXP(ID('a', body, False),
                        ASNOP.ADD, ID('b', body, False))
    assignStmt = EXPSTM(assignexp1)
    decl1 = DECLSTM(VARDCL(
        spec.int8, VARDTR(ID('y', body, False))))
    body.addStatement(decl1)
    body.addStatement(assignStmt)
    whileloop = WhileLoop(control, body)
    print(whileloop)
