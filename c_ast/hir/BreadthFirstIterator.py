from hir.Traversable import Traversable
from hir.ForLoop import ForLoopTest2, bfs
from hir.IfStatement import IfStatementTest
from hir.Declarator import Declarator
from hir.Keyword import specifiers
from hir.Statement import Statement
from hir.Expression import Expression
from hir.ExpressionStatement import ExpressionStatementTest
from hir.AssignmentExpression import AssignmentExpression
from hir.AssignmentExpression import AssignmentExpressionTest
from hir.BinaryExpression import BinaryExpressionTest
from hir.UnaryExpression import UnaryExpressionTest


class BreadthFirstIteratorException(Exception):
    pass


class NotATraversableError(BreadthFirstIteratorException):
    pass


class PruneTypeError(Exception):
    pass


class BreadthFirstIterator(object):
    """Provides a breadth first iterator for a given HIR 
    object. Use the function "next" for the next 
    child. Also provides a prune feature, using which 
    we can a specific HIR object. """
    __slots__ = ('_prune_set', '_queue')

    def __init__(self, t):
        if not isinstance(t, Traversable):
            raise NotATraversableError(type(t))
        self._prune_set = []
        self._queue = []
        self._queue.append(t)

    def PruneOn(self, t):
        if not issubclass(t, Traversable):
            raise PruneTypeError(t.__name__)
        self._prune_set.append(t)

    def _getChildren(self, node):
        """Returns a list containing all child nodes 
of a Traversable type node. Returns empty list
when the node has no children. Used by BF/DF/Flat
iterative tree visitor functions."""
        try:
            k = node.getChildren()
            return k
        except:
            return []

    def __next__(self):
        """Yeilds the next object in a 
        Breadth first Iterator. First object 
        returned is the passed parameter. Following this
        the children of the object are returned followed by
        children's children... etc. all in breadth-first order.

        Maintains a queue containing children nodes of 
        a tree node. All children of the tree are visited 
        in breadth first order. The queue is used as a 
        FIFO implemention to acheive this breadth first
        visiting."""
        while len(self._queue):
            r = self._queue[0]
            if hasattr(self, '_prune_set') \
                    and len(self._prune_set):
                for k in self._prune_set:
                    if isinstance(r, k):
                        yield r
            else:
                yield r
            self._queue.remove(r)
            for k in self._getChildren(r):
                self._queue.append(k)


def reindent(s, numSpaces):
    """Useful for pretty printer, appends spaces in front of children nodes
    to visualize the breadth first hierarchy"""
    leading_space = numSpaces * ' '
    lines = [leading_space + line.strip()
             for line in s.splitlines()]
    return ''.join(lines)


if __name__ == '__main__':
    #    bfsitr = BreadthFirstIterator(bfstest)
    #    print 'The children of: ', bfstest
    #    print 'are'
    #    i = 1
    #    for k in bfsitr.next():
    #        print '%d:'%i, reindent(str(k), i)
    #        i += 1
    #    bfs(bfstest)
    #    bfstest = ForLoopTest()
    #    bfstest = ForLoopTest2()
    #    bfstest = ExpressionStatementTest()
    #    dec = DeclarationStatement(VariableDeclaration(specifiers.inT, VariableDeclarator(Identifier('a'))))
    #    as1 = AssignmentExpression(Identifier('a'), assignmentOperator.ADD, IntegerLiteral(1))
    #    exp_stmt = ExpressionStatement(as1)
    #    comp_stmt = CompoundStatement()
    #    comp_stmt.addStatement(dec)
    #    comp_stmt.addStatement(exp_stmt)
    ifst = IfStatementTest()
    from hir.Digrapher import Digrapher
    print(Digrapher(ifst, [Expression, Statement, Declarator]))
