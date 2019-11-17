import copy
from hir.IfStatement import IfStatementTest
from hir.Statement import Statement
from hir.CompoundStatement import CompoundStatement
from hir.Loop import Loop
from hir.Expression import Expression
from hir.BinaryExpression import BinaryExpression
from hir.ConditionalExpression import ConditionalExpression
from hir.UnaryExpression import UnaryExpression
from hir.Operator import binaryOperator, unaryOperator, assignmentOperator, conditionalOperator
from hir.Identifier import Identifier
from hir.ExpressionStatement import ExpressionStatement
from hir.VariableDeclaration import VariableDeclaration
from hir.DeclarationStatement import DeclarationStatement
from hir.Keyword import specifiers
from hir.VariableDeclarator import VariableDeclarator
from hir.AssignmentExpression import AssignmentExpression
from hir.IntegerLiteral import IntegerLiteral
from hir.FloatLiteral import FloatLiteral
from hir.CompoundStatement import CompoundStatement


class ForLoopException(Exception):
    pass


class InvalidBodyTypeError(ForLoopException):
    def __init__(self, value=''):
        self.value = value

    def __repr__(self):
        return 'Invalid type for Body:(%s), expecting Statement or CompoundStatement' % value


class InvalidTypeForIndexExpressionError(ForLoopException):
    def __init__(self, value=''):
        self.value = value

    def __repr__(self):
        return 'Invalid type for loop index expression: (%s), expecting expression type' % value


class BodyNotSetError(ForLoopException):
    pass


class ForLoop(Statement, Loop):
    """Represents a Counting based FOR Loop 
for use in functional like programs.
Currently, the supported 
syntax expects 3 HIR Expressions and a 
CompoundStatement type for Loop body. ForLoop
subclasses Loop (other than Statement), for 
some less obvious reasons. It is convenient to have a
Loop class for Pruning tree visitor function, which 
iterate over all Loops, either ForLoop, DoLoop, WhileLoops."""

    def __init__(self, *args):
        """Initializes a ForLoop in HIR from hir.ny 
iterable sequence. The first three arguments are
init, condition, step values. The last value is the 
CompoundStatement holding statements in the loop body"""
        init, condition, step, body = args
        self.initialize()
        self.setNumChildren(4)
        self.setInit(init)
        self.setCondition(condition)
        self.setStep(step)
        self.setBody(body)

#    def addDeclaration(self, decl):
#        """Provides a direct entry into the symbol table of the
# CompoundStatement"""
#        self.getChild(3).addDeclaration(decl)

    def setInit(self, expr):
        """Sets the init expression for the ForLoop.
Expects a HIR Expression type here."""
        if not isinstance(expr, Expression):
            raise InvalidTypeForIndexExpressionError(
                str(type(expr))+':'+repr(expr))
        self.setChild(0, expr)

    def setCondition(self, expr):
        """Sets the exit-condition expression for the ForLoop.
Expects a HIR Expression type here."""
        if not isinstance(expr, Expression):
            raise InvalidTypeForIndexExpressionError(
                str(type(expr))+':'+repr(expr))
        self.setChild(1, expr)

    def setStep(self, expr):
        """Sets the step expression for the ForLoop.
Expects a HIR Expression type here."""
        if not isinstance(expr, Expression):
            raise InvalidTypeForIndexExpressionError(
                str(type(expr))+':'+repr(expr))
        self.setChild(2, expr)

    def setBody(self, stmt):
        """Sets the body of the ForLoop to either a
passed CompoundStatement or a new CompoundStatement that 
wraps a passed Statement type"""
        if isinstance(stmt, CompoundStatement):
            self.setChild(3, stmt)
        elif isinstance(stmt, Statement):
            self.setChild(3, CompoundStatement().addStatement(stmt))
        else:
            raise InvalidBodyTypeError(str(type(stmt)))

    def getInit(self):
        """Returns the Init expression"""
        return self.getChild(0)

    def getCondition(self):
        """Returns the exit-Condition expression"""
        return self.getChild(1)

    def getStep(self):
        """Returns the step expression"""
        return self.getChild(2)

    def getBody(self):
        """Returns the body CompoundStatement"""
        return self.getChild(3)

    def __repr__(self):
        """Returns a string representation of the contents 
of the for loop object (Example: 'for (...,...,...) {...}' 
). Currently the returned string is in AnsiC. 
Change this function to return different a representation."""
        retval = 'for'
        retval += ' (%s; %s; %s) ' % (repr(self.getInit()),
                                      repr(self.getCondition()), repr(self.getStep()))
        retval += repr(self.getBody())
        return retval


def ForLoopTest(parent=None):
    doTest = False
    if parent is not None:
        doTest = True
# i = 0
    init = AssignmentExpression(Identifier('i', parent, doTest),
                                assignmentOperator.EQUAL, IntegerLiteral(0))
# i++
    step = UnaryExpression(unaryOperator.POST_INCREMENT,
                           Identifier('i', parent, False))
# i < 100
    condition = ConditionalExpression(Identifier('i', parent, doTest),
                                      conditionalOperator.COMPARE_LE, IntegerLiteral(100))
# A body for the for loop
    body = CompoundStatement()
# a variable declaration: inT y
    decl1 = DeclarationStatement(VariableDeclaration(specifiers.inT,
                                                     VariableDeclarator(Identifier('y', body, doTest))))
    body.addStatement(decl1)
# identifiers a, b
    id1 = Identifier('a', parent, doTest)
    id2 = Identifier('y', parent, doTest)
# assignment expression, a += b, a = b, a %= b
    args1 = id1, assignmentOperator.ADD, id2
    args2 = copy.deepcopy(id1), assignmentOperator.EQUAL, copy.deepcopy(id2)
    args3 = copy.deepcopy(id1), assignmentOperator.MODULUS, copy.deepcopy(id2)
    args4 = copy.deepcopy(args3)
    assignments = [AssignmentExpression(*k)
                   for k in [args1, args2, args3, args4]]
    r = list(map(ExpressionStatement, assignments))
# adding the statements to the body of the ForLoop
    list(map(body.addStatement, r))
    body.addStatement(IfStatementTest())
    forloop = ForLoop(init, condition, step, body)
    return forloop


def ForLoopTest2(symtab):
    # i = 0
    init = AssignmentExpression(Identifier('i', None, False),
                                assignmentOperator.EQUAL, IntegerLiteral(0))
# i++
    step = UnaryExpression(unaryOperator.POST_INCREMENT,
                           Identifier('i', None, False))
# i < 100
    condition = ConditionalExpression(Identifier('i', None, False),
                                      conditionalOperator.COMPARE_LE, IntegerLiteral(100))
# A body for the for loop
    body = CompoundStatement()
# a variable declaration: inT y
    decl1 = DeclarationStatement(VariableDeclaration(specifiers.inT,
                                                     VariableDeclarator(Identifier('y', None, False, None, False))))
    body.addStatement(decl1)
# identifiers a, b
    id1 = Identifier('a', None, False)
    id2 = Identifier('y', None, False)
    as1 = ExpressionStatement(AssignmentExpression(id2,
                                                   assignmentOperator.EQUAL, Identifier('i', None, False)))
    as2 = ExpressionStatement(AssignmentExpression(copy.deepcopy(id1),
                                                   assignmentOperator.EQUAL, id2))
    body.addStatement(as1)
    body.addStatement(as2)
    forloop = ForLoop(init, condition, step, body)
    return forloop

# a reindenter for pretty printing


def reindent(s, numSpaces):
    leading_space = numSpaces * ' '
    lines = [leading_space + line.strip()
             for line in s.splitlines()]
    return ''.join(lines)


def bfs(IRNode):
    from hir.fs import bfsItr
    i = 1
    for k in bfsItr(IRNode):
        print(('%d:' % (i), reindent(str(k), i)))
        i += 1


if __name__ == '__main__':
    forloop = ForLoopTest()
    print(forloop)
