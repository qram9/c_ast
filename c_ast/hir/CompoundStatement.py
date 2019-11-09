from hir.Statement import Statement
from hir.SymbolTable import SymbolTable
from hir.Declaration import Declaration
from hir.DeclarationStatement import DeclarationStatement

class CompoundStatementException(Exception): pass
class NotAStatementError(CompoundStatementException): pass
class StatementNotFoundError(CompoundStatementException): pass
class SymbolNotFoundError(CompoundStatementException): pass

class CompoundStatement(Statement):
    """Represents a block structure statement i.e. stuff between {} in C.
Creates a new scope. A SymbolTable is provided to hold local declarations. 
Functions addStatement, addStatementBefore, addStatementAfter are provided to 
add statements to the compound statement object. Care must be taken by the user 
to maintain the required order. This class *does not* impose any ordering on 
the given statements, viz. for example, declaration must precede all expression 
statements in AnsiC. This class is dumb and does not check these kinds of requirements."""
    __slots__ = ['symbolTable']
    def __init__(self):
        """Set up CompoundStatement with an SymbolTable object"""
        Statement.__init__(self)
        self.symbolTable = SymbolTable()

    def _catchNotAStatementError(self, stmt):
        """Tests this: A Referenced child in compound statement object must be of type statement"""
        if not isinstance(stmt, Statement):
            raise NotAStatementError(type(stmt))

    def _catchStatementNotFoundError(self, ref_stmt):
        """Tests this: A Referenced child in compound statement object must be in _children"""
        children = self.getChildren()
        try:
            ind = children.index(ref_stmt)
        except ValueError:
            raise StatementNotFoundError(str(ref_stmt))

    def _processDecl(self, stmt):
        """Helper to process declaration statements, called by addStatement, and its variants"""
        for k in stmt.getDeclaration().getDeclaredSymbols():
            self.symbolTable.addDeclaration(k.getSymbol(), \
stmt.getDeclaration())

    def addStatement(self, stmt):
        """Adds a statement to this compound statement object.
If the statement is of a type DeclarationStatement, 
its entries are put into the symbol table"""
        self._catchNotAStatementError(stmt)
        if isinstance(stmt, DeclarationStatement):
            self._processDecl(stmt)    
        self.setNumChildren(self.getNumChildren()+1)
        children = self.getChildren()
        children.append(stmt)
        stmt.setParent(self)
        
    def addStatementBefore(self, ref_stmt, stmt):
        """Adds a statement before a referenced statement in 
compound statement object. If the statement is of a type 
DeclarationStatement, its entries are put into the symbol table"""
        self._catchNotAStatementError(stmt)
        self._catchNotAStatementError(ref_stmt)
        self._catchStatementNotFoundError(ref_stmt)
        if isinstance(stmt, DeclarationStatement):
            self._processDecl(stmt)    
        self.setNumChildren(self.getNumChildren()+1)
        self.insertBefore(ref_stmt, stmt)

    def addStatementAfter(self, ref_stmt, stmt):
        """Adds a statement after a referenced statement in 
compound statement object. If the statement is of a type 
DeclarationStatement, its entries are put into the symbol table"""
        self._catchNotAStatementError(stmt)
        self._catchNotAStatementError(ref_stmt)
        self._catchStatementNotFoundError(ref_stmt)
        if isinstance(stmt, DeclarationStatement):
            self._processDecl(stmt)    
        self.setNumChildren(self.getNumChildren()+1)
        self.insertAfter(ref_stmt, stmt)

    def getSymbolTable(self):
        """Returns the SymbolTable object belonging to this compound statement object"""
        return self.symbolTable

    def getParentTables(self):
        """Returns a list of SymbolTable objects from hir.he parents of 
this compound statement object. Traverses the parent hierarchy 
of this compound statement and adds an SymbolTable object if it finds one"""
        retlist = []
        p = self.getParent()
        while p:
            if hasattr(p, 'symbolTable'):
                retlist.insert(0, p.getSymbolTable())
            p = p.getParent()    
        return retlist

    def findSymbol(self, identifier):
        """Looks up a symbol. If symbol is not 
in local SymbolTable, look up in 
parent hierarchy"""
        try:
            k = self.symbolTable.findSymbol(identifier)
            return k
        except KeyError:
            p = self.getParent()
            while p:
                if hasattr(p, 'symbolTable'):
                    k = p.getSymbolTable()
                    try:
                        s = k.findSymbol(identifier)
                        return k
                    except KeyError:
                        pass
                p = p.getParent()
        raise SymbolNotFoundError(str(identifier))

    def __repr__(self):
        """Returns a string representation of the contents of the compound statement object with enclosing {}. Currently the string is in AnsiC. Change this function to return different a representation."""
        retval = '{\n'
        for k in self.getChildren():
            retval += repr(k) + '\n'
        retval += '}'
        return retval
    __str__ = __repr__

    def items(self):
        """Returns items dict when called from hir.etstate. 
Adds __slots__ entry "symbolTable" to items dict.
Recurses into base classes and collects items from hir.here too."""
        items = {}
        items['symbolTable'] = self.symbolTable
        for k in CompoundStatement.__bases__:
            if hasattr(k, 'items'):
                supitems = k.items(self)
                for k,v in list(supitems.items()):
                    items[k] = v
        return dict(items)
    def __getstate__(self):
        """Returns a dict representing the contents of this Compound Statement object and its base classes instances' contents. Contents added by this class is "symbolTable"."""
        return self.items()

    def __setstate__(self, statedict):
        """Blindly calls setattr with entries from hir. __getstate__ like string->attr dict."""
        for k,v in list(statedict.items()):
            setattr(self, k, v)

from hir.BinaryExpression import BinaryExpression
from hir.Operator import binaryOperator
from hir.Identifier import Identifier
from hir.ExpressionStatement import ExpressionStatement
from hir.VariableDeclaration import VariableDeclaration
from hir.DeclarationStatement import DeclarationStatement
from hir.Keyword import specifiers
from hir.VariableDeclarator import VariableDeclarator

def CompoundStatementTest():
    id1 = Identifier('a')
    id2 = Identifier('b')
    binexp1 = BinaryExpression(id1, binaryOperator.ADD, id2)
    binexp2 = BinaryExpression(id1, binaryOperator.ADD, id2)
    binexp3 = BinaryExpression(id1, binaryOperator.ADD, id2)
    decl1 = DeclarationStatement(VariableDeclaration(specifiers.int8, VariableDeclarator(Identifier('y'))))
    Y = decl1
    expstmt1 = ExpressionStatement(binexp1)
    expstmt2 = ExpressionStatement(binexp2)
    expstmt3 = ExpressionStatement(binexp3)
    compstmt = CompoundStatement()
    compstmt.addStatement(decl1)
    compstmt.addStatementAfter(decl1, expstmt1)
    print (compstmt)
    k = CompoundStatement()
    decl1 = DeclarationStatement(VariableDeclaration(specifiers.int8, VariableDeclarator(Identifier('x'))))
    k.addStatement(decl1)
    k.addStatement(expstmt2)
    compstmt.addStatement(k)
    l = CompoundStatement()
    decl1 = DeclarationStatement(VariableDeclaration(specifiers.int8, VariableDeclarator(Identifier('z'))))
    l.addStatement(decl1)
    l.addStatement(expstmt2)
    k.addStatement(l)
    compstmt.addStatement(expstmt3)
    expstmt1.detach()
    print(('next compstmt:\n', compstmt))
    print ('symtabl:')
    print(('parent symtabl:', k.getParentTables()))
    print(('symbol look up:', k.findSymbol(Y.getDeclaration().getDeclaredSymbols()[0])))
    return compstmt

if __name__ == '__main__':
    compstmt = CompoundStatementTest()

