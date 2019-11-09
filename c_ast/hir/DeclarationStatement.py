from hir.Statement import Statement
from hir.Declaration import Declaration
class NotADeclarationError(Exception):
    pass
class DeclarationStatement(Statement):
    """Represents a declaration statement 
like 'int a;' or 'int proc_name (int).
VariableDeclarations can be directly
set here, but ProcedureDeclarators
need to be wrapped with a declaration.
Wraps a statement class around 
Declarations. __repr__ prints a ; after the 
VariableDeclaration."""
    def __init__(self, exp):
        """Instantiates a DeclarationStatement with a
given Declaration: can be either VariableDeclaration or
ProcedureDeclaration. Raises Exception if not either type"""
        Statement.__init__(self)
        self.setNumChildren(1)    
        if not isinstance(exp, Declaration):
            raise NotADeclarationError('Type: (%s)' % (type(exp)))
        self.setChild(0, exp)
        exp.setParent(self)
    def getDeclaration(self):
        """Returns the declaration associated with this
DeclarationStatement."""
        return self.getChild(0)
    def __repr__(self):
        retval = repr(self.getDeclaration()) + ';'
        return retval
    __str__ = __repr__

from hir.VariableDeclaration import VariableDeclaration
from hir.VariableDeclarator import VariableDeclarator
from hir.Identifier import Identifier
from hir.Keyword import specifiers

if __name__ == '__main__':
    k = VariableDeclaration(specifiers.int8, VariableDeclarator(Identifier('y')))
    s = DeclarationStatement(k)
    print((repr(s)))
