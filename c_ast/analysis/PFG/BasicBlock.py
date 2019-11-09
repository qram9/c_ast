#TODO: add comments, add getstate, items, setstate modules
from hir.Statement import Statement
class BasicBlockException(Exception): pass
class NotABasicBlockError(BasicBlockException): pass
class BasicBlock(object):
    __slots__ = ('_statements', '_preds', '_succs', '_visited', 'name')
    def __init__(self, name):
        self._statements = []
        self._preds = []
        self._succs = []
        self._visited = False
        self.name = name
    def getName(self):
        return self.name
    def addPredecessor(self, bb):
        if not isinstance(bb, BasicBlock):
            raise NotABasicBlockError(type(bb))
        self._preds.append(bb)
    def addSuccessor(self, bb):
        if not isinstance(bb, BasicBlock):
            raise NotABasicBlockError(type(bb))
        self._succs.append(bb)
    def addStatement(self, stmt):
        if not isinstance(stmt, Statement): 
            raise NotAStatementError(type(stmt)) 
        self._statements.append(stmt)
    def getStatements(self):
        return self._statements
    def getSuccs(self):
        return self._succs
    def getPreds(self):
        return self._preds    
    def __repr__(self):
        return self.name
