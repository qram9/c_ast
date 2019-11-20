from hir.Statement import Statement
from hir.Loop import Loop
from hir.CharLiteral import CharLiteral
from hir.IntegerLiteral import IntegerLiteral
from hir.FloatLiteral import FloatLiteral
from hir.Identifier import Identifier as ID
from hir.IDExpression import IDExpression
from hir.Keyword import specifiers as spec
from hir.SymbolTable import SymbolTable
from hir.VariableDeclarator import VariableDeclarator as VARDTR
from hir.VariableDeclaration import VariableDeclaration as VARDCL
from hir.Declaration import Declaration
from hir.Declarator import Declarator
from hir.Specifier import Specifier
from hir.ParameterDeclarator import ParameterDeclarator
from hir.BinaryExpression import BinaryExpression
from hir.AccessExpression import AccessExpression
from hir.ConditionalExpression import ConditionalExpression as CONDEXP
from hir.UnaryExpression import UnaryExpression
from hir.Operator import binaryOperator, unaryOperator, assignmentOperator as ASNOP, conditionalOperator as CONDOP
from hir.AssignmentExpression import AssignmentExpression as ASNEXP
from hir.ArraySpecifier import ArraySpecifier
from hir.Statement import Statement
from hir.ExpressionStatement import ExpressionStatement as EXPSTM
from hir.DeclarationStatement import DeclarationStatement as DECLSTM
from hir.CompoundStatement import CompoundStatement as COMPSTM
from hir.IfStatement import IfStatement
from hir.FunctionCall import FunctionCall
from hir.ContinueStatement import ContinueStatement
from hir.DoLoop import DoLoop
from hir.ForLoop import ForLoop
from hir.Procedure import Procedure
from hir.Case import Case
from hir.Expression import Expression as EXP
from hir.BreakStatement import BreakStatement



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
