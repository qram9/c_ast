from hir.Procedure import Procedure
from hir.Traversable import Traversable
from hir.BreadthFirstIterator import BreadthFirstIterator
from analysis.PFG.ControlFlowGraph import ControlFlowGraph
class ProgramFlowGraphException(Exception): pass
class ProgramFlowGraph(object):
    __slots__ = ('progMap',)
    def __init__(self, t):
        if not isinstance(t, Traversable):
            raise ProgramFlowGraphException, \
                "Invalid type for ProgramFlowGraph, init", type(t)
        self.progMap = {}
        bit = BreadthFirstIterator(t)
        bit.PruneOn(Procedure)
        for p in bit.next():
            k = ControlFlowGraph(p)
            k.graphIt()
if __name__ == '__main__':
    from hir.Procedure import procedureTest
    k = ProgramFlowGraph(procedureTest())
