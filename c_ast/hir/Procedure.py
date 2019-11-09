from hir.Declaration import Declaration
from hir.Declarator import Declarator
from hir.SymbolTable import SymbolTable
from hir.Specifier import Specifier
from hir.CompoundStatement import CompoundStatement
from hir.Identifier import Identifier
from hir.ParameterDeclarator import ParameterDeclarator
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
class ProcedureException(Exception): pass
class LeadSpecNotASpecifierError(ProcedureException):  pass
class BodyNotCompoundStatementError(ProcedureException): pass
class NotAParameterDeclaratorError(ProcedureException): pass
class Procedure(Declaration):
    """Represents a Ansi C Procedure (also called Function) type.
    The Procedure is also a Declaration type and must be part of 
    the symbol table of a translation unit (or a file type). 
    Currently support for TranslationUnit is pending. """
    __slots__ = ['lead', 'symbolTable', 'proc_id', '_params']
    def _processDecl(self, params):
        if not isinstance(params, ParameterDeclarator):
            raise NotAParameterDeclaratorError(type(params))
        self._params = params
        for k in range(0,self._params.getNumChildren()):
            child = self._params.getChild(k)
            if not isinstance(child, Declaration):
                for l in child.getDeclaredSymbols():
                    self.symbolTable.addDeclaration(l, child)
    def __init__(self, iden, body, params, lead=[]):
        """Initializes procedure declarations with 
        lead parameters, Identifier for the 
        procedure name, a ParameterDeclarator and a 
        CompoundStatement Body type. Also initializes 
        a symbol table type."""
        self.lead = []
        self.initialize()
        Declaration.__init__(self)
        self.setNumChildren(1)
        self.symbolTable = SymbolTable()
        if not isinstance(body, CompoundStatement):
            raise BodyNotCompoundStatementError(type(body))
        self.setChild(0, body)
        if not isinstance(iden, Identifier):
            raise ProcedureIDNotIdentifierError(type(iden))
        self.proc_id = iden
        for k in lead:
            if not isinstance(k, Specifier):
                raise LeadSpecNotASpecifierError(type(k))
            self.lead.append(k)
        self._processDecl(params)
    def getBody(self):
        return self.getChild(0)
    def getIdentifier(self):
        return self.proc_id
    def getSymbolTable(self):
        return self.symbolTable
    def getParentTables(self):
        retlist = []
        p = self.getParent()
        while p:
            if hasattr(p, 'symbolTable'):
                retlist.insert(0, p.getSymbolTable())
            p = p.getParent()    
        return retlist
    def findSymbol(self, name):
        try:
            k = self.symbolTable.findSymbol(name)
            return k
        except KeyError:
            partab = self.getParentTables()
            for k in partab:
                try:
                    k = k.findSymbol(name)
                    return k
                except KeyError:
                    pass
        raise SymbolNotFoundError(str(name))
    def __repr__(self):
        """Returns Ansi C representation of a Procedure,
for example int proc_name (...) {...}. Change this 
function if you need to change the way the 
function is printed"""
        retval = ''
        for k in self.lead:
            retval += str(k) + ' '
        retval += repr(self.proc_id)
        retval += repr(self._params)
        retval += repr(self.getChild(0))
        return retval
    __str__ = __repr__

    def items(self):
        """Returns items dict to getstate, for pickle and copy,
with the values from hir.he __slots__, lead, symbolTable, 
proc_id, _params and then goes down on the class 
hierarchy and collects the rest of the __slots__"""
        items = {}
        items['lead'] = getattr(self, 'lead')
        items['symbolTable'] = getattr(self, 'symbolTable')
        items['proc_id'] = getattr(self, 'proc_id')
        items['_params'] = getattr(self, '_params')
        for k in Procedure.__bases__:
            if hasattr(k, 'items'):
                supitems = k.items(self)
                for k,v in list(supitems.items()):
                    items[k] = v
        return dict(items)

    def __getstate__(self):
        """Returns the results of the self.items function call
for pickle and copy"""
        return dict(self.items())

    def __setstate__(self, statedict):
        """Blindly sets the contents of statedict to __slots__"""
        for k,v in list(statedict.items()):
            setattr(self, k, v)
from hir.ForLoop import ForLoopTest
from hir.ParameterDeclarator import ParameterDeclaratorTest    
from hir.Identifier import Identifier
from hir.Keyword import specifiers
from hir.CompoundStatement import CompoundStatement
from hir.IfStatement import IfStatementTest

def procedureTest():
    forstmt = ForLoopTest()
    params = ParameterDeclaratorTest()#ParameterDeclarator() 
    proc_name = Identifier('my_proc')
    lead = [specifiers.int8]
    compstmt = CompoundStatement()
    compstmt.addStatement(forstmt)
    ifstmt = IfStatementTest()
    compstmt.addStatement(ifstmt)
    p = Procedure(proc_name, compstmt, params, lead)
    return p

if __name__ == '__main__':
    p = procedureTest()
    import copy
    print('Procedure test, ', p)
    print('Procedure test, copy', copy.deepcopy(p))
    print(p)
