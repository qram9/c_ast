#TODO: add comments, add getstate, items, setstate modules
from BasicBlock import BasicBlock, NotABasicBlockError
class ProcBasicBlockException(Exception): pass
class ProcBasicBlock(BasicBlock):
    __slots__ = ('entryBB', 'exitBB', 'name')
    def __init__(self,name):
        self.entryBB = BasicBlock("%s_ENTRY"%name)
        self.exitBB = BasicBlock("%s_EXIT"%name)
        self.name = name
    def addPredecessor(self, bb):
        if not isinstance(bb, BasicBlock):
            raise NotABasicBlockError, type(bb)
        self.entryBB.addPredecessor(bb)
    def addSuccessor(self, bb):
        if not isinstance(bb, BasicBlock):
            raise NotABasicBlockError, type(bb)
        self.exitBB.addSuccessor(bb)
