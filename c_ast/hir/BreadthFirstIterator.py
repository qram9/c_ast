class BreadthFirstIteratorException(Exception): pass
class NotATraversableError(BreadthFirstIteratorException): pass
from Traversable import Traversable
class PruneTypeError(Exception): pass
class BreadthFirstIterator(object):
    """Provides a breadth first iterator for a given HIR 
    object. Use the function "next" for the next 
    child. Also provides a prune feature, using which 
    we can a specific HIR object. """
    __slots__ = ('_prune_set', '_queue')
    def __init__(self, t):
        if not isinstance(t, Traversable):
            raise NotATraversableError, type(t)
        self._prune_set = []
        self._queue = []
        self._queue.append(t)
    def PruneOn(self, t):
        if not issubclass(t, Traversable):
            raise PruneTypeError, t.__name__
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
    def next(self):
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
    lines = [leading_space + line.strip( )
              for line in s.splitlines( ) ]
    return ''.join(lines)

if __name__ == '__main__':
    from ForLoop import ForLoopTest2, bfs
    from UnaryExpression import UnaryExpressionTest
    from UnaryExpression import UnaryExpressionTest
    from BinaryExpression import BinaryExpressionTest
    from AssignmentExpression import AssignmentExpressionTest
    from AssignmentExpression import AssignmentExpression
    from ExpressionStatement import ExpressionStatementTest
    from Expression import Expression
    from Statement import Statement
    from keyword import specifiers
    from Declarator import Declarator
    #	bfsitr = BreadthFirstIterator(bfstest)
    #	print 'The children of: ', bfstest
    #	print 'are'
    #	i = 1
    #	for k in bfsitr.next():
    #		print '%d:'%i, reindent(str(k), i)
    #		i += 1
    #	bfs(bfstest)
    #	bfstest = ForLoopTest()
    #	bfstest = ForLoopTest2()
    #	bfstest = ExpressionStatementTest()
    #	dec = DeclarationStatement(VariableDeclaration(specifiers.inT, VariableDeclarator(Identifier('a'))))
    #	as1 = AssignmentExpression(Identifier('a'), assignmentOperator.ADD, IntegerLiteral(1))
    #	exp_stmt = ExpressionStatement(as1)
    #	comp_stmt = CompoundStatement()
    #	comp_stmt.addStatement(dec)
    #	comp_stmt.addStatement(exp_stmt)
    from IfStatement import IfStatementTest
    from Digrapher import Digrapher
    ifst = IfStatementTest()
    print Digrapher(ifst, [Expression,Statement,Declarator])
