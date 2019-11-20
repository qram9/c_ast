from hir.Statement import Statement
from hir.Traversable import Traversable
from hir.Declarator import Declarator
from hir.Traversable import ChildNotCorrectType, ParentNotCorrectType
from hir.Traversable import get_symbols
from hir.Identifier import Identifier


class Declaration(Traversable):
    """Represents a base type 
for a VariableDeclaration. ProcedureDeclarator
are wrapped with a Declaration and used
in DeclarationStatements.

Subclassed by VariableDeclaration and Procedure.
When super-class variable declarations are added 
to Compound statements, the compound statement 
analyzes the declarations and automatically adds 
symbol table entries. This class maybe revisited
as this is somewhat brain melting.
"""

    def __init__(self, size=1):
        Traversable.__init__(self)
        self.setNumChildren(size)

    def _catchChildNotCorrectType(self, t):
        """Allowed types for children are 
1: Declaration for Declarations containing nested declarations
2: Declarator: either the ProcedureDeclarator or VariableDeclarator, for ex. 'int a' or 'int proc_name (int, char)'
and 
3: Statement: For the CompoundStatement representing  
procedures body. Procedures declarations 
need to subclass Declaration as they represent 
symbol table entries in a source file (also called 
'Translation unit').
"""
        if not isinstance(t, (Declaration, Declarator, Statement)):
            raise ChildNotCorrectType(str(type(t)))

    def setChild(self, which, t):
        """Overrides the Traversable setChild to catch
unsupported child nodes"""
        self._catchChildNotCorrectType(t)
        Traversable.setChild(self, which, t)

    def removeChild(self, t):
        """Overrides the Traversable removeChild to 
catch unsupported referenced nodes"""
        self._catchChildNotCorrectType(t)
        Traversable.removeChild(self, t)

    def _catchParentNotCorrectType(self, t):
        """Allowed types for declaration parents are 
1: Declaration for Declarations containing nested declarations
2: Declarator: either the ProcedureDeclarator or VariableDeclarator, for ex. 'int a' or 'int proc_name (int, char)'
and 
3: Statement: For the CompoundStatement representing  
procedures body. Procedures declarations 
need to subclass Declaration as they represent 
symbol table entries in a source file (also called 
'Translation unit').
"""
        if not isinstance(t, (Declaration,
                              Declarator, Statement)):
            raise ParentNotCorrectType(str(type(t)))

    def setParent(self, t):
        """Overrides the setParent in Traversable to
catch unsupported parent node"""
        self._catchParentNotCorrectType(t)
        Traversable.setParent(self, t)

    def __repr__(self):
        retval = repr(self.getChild(0))
        return retval
    __str__ = __repr__

# TODO: RETHINK THIS FUNCTION

    def getDeclaredSymbols(self):
        allsym = []
        get_symbols(self, allsym)
        return allsym
