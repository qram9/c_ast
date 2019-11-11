class DoLoopException(Exception): pass

class InvalidConditionException(DoLoopException): pass

class InvalidBodyException(DoLoopException): pass

from hir.Statement import Statement
from hir.Loop import Loop
from hir.Expression import Expression

class DoLoop(Statement, Loop):
    """Ansi C do/while loop. Requires a ConditionalExpression,
and a compound statement for a body"""
    def __init__(self, *args): 
        """DoLoop works on any sequence type containing 
2 elements. Initializes 2 children in the traversable 
class. Tests if the specified 'condition' argument
is of type Expression. Secondly, tests if
the specified 'body' is of type CompoundStatement"""

        condition, body = args
        self.initialize()
        self.setNumChildren(2)
        if not isinstance(condition, Expression):
            raise InvalidConditionException(type(condition))
        self.setChild(0, condition)
        if not isinstance(body, CompoundStatement):
            raise InvalidBodyException(type(body))
        self.setChild(1, body) 

    def __repr__(self):
        """Returns a string representation of the contents 
of the do loop object (Example: 'do {...} while(...)' 
). Currently the returned string is in AnsiC. 
Change this function to return different a representation."""

        retval = 'do ' + repr(self.getChild(1)) + ' while ('
        retval += repr(self.getChild(0)) + ')'
        return retval

from hir.AstBuild import *

if __name__ == '__main__':
    control = ConditionalExpression(Identifier('a', None, False),
            conditionalOperator.COMPARE_EQ, Identifier('a', None, False))
    assignexp1 = AssignmentExpression(Identifier('a', None, False),
            assignmentOperator.ADD, Identifier('b', None, False))
    assignStmt = ExpressionStatement(assignexp1)
    decl1 = DeclarationStatement(VariableDeclaration(specifiers.int8,
            VariableDeclarator(Identifier('y', None, False))))
    body = CompoundStatement()
    body.addStatement(decl1)
    body.addStatement(assignStmt)
    doloop = DoLoop(control, body)
    print(doloop)

