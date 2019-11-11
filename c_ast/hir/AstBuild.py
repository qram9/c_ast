from hir.CharLiteral import CharLiteral
from hir.IntegerLiteral import IntegerLiteral
from hir.FloatLiteral import FloatLiteral
from hir.Identifier import Identifier
from hir.IDExpression import IDExpression
from hir.Keyword import specifiers
from hir.SymbolTable import SymbolTable
from hir.VariableDeclarator import VariableDeclarator
from hir.VariableDeclaration import VariableDeclaration
from hir.Declaration import Declaration
from hir.Declarator import Declarator
from hir.Specifier import Specifier
from hir.ParameterDeclarator import ParameterDeclarator
from hir.BinaryExpression import BinaryExpression
from hir.AccessExpression import AccessExpression
from hir.ConditionalExpression import ConditionalExpression
from hir.UnaryExpression import UnaryExpression
from hir.Operator import binaryOperator, unaryOperator, assignmentOperator, conditionalOperator
from hir.AssignmentExpression import AssignmentExpression
from hir.ArraySpecifier import ArraySpecifier
from hir.Statement import Statement
from hir.ExpressionStatement import ExpressionStatement
from hir.DeclarationStatement import DeclarationStatement
from hir.CompoundStatement import CompoundStatement
from hir.IfStatement import IfStatement
from hir.FunctionCall import FunctionCall
from hir.ContinueStatement import ContinueStatement
from hir.DoLoop import DoLoop
from hir.WhileLoop import WhileLoop
from hir.ForLoop import ForLoop
from hir.Procedure import Procedure
from hir.Case import Case
from hir.Expression import Expression
from hir.BreakStatement import BreakStatement

SYMTAB = SymbolTable
STM = Statement
COMPSTM = CompoundStatement
IF = IfStatement
FOR = ForLoop
DO = DoLoop
WHILE = WhileLoop
FUNCTION = Procedure
VARDCL = VariableDeclaration
VARDTR = VariableDeclarator
DTR = Declarator
DCL = Declaration
SPEC = Specifier
spec = specifiers
ID = Identifier
EXP = Expression
EXPSTM = ExpressionStatement
BINEXP = BinaryExpression
ACCEXP = AccessExpression
DECLSTM = DeclarationStatement
ASNEXP = AssignmentExpression
ARRSPEC = ArraySpecifier
INTLIT = IntegerLiteral
CHARLIT = CharLiteral
FLOATLIT = FloatLiteral
UNAEXP = UnaryExpression
PARAMDTR = ParameterDeclarator
BINOP = binaryOperator
UNAOP = unaryOperator
ASNOP = assignmentOperator
CASE = Case
CONDOP = conditionalOperator
BREAK = BreakStatement
CALL = FunctionCall
CONTINUE = ContinueStatement
IDEXP = IDExpression
CONDEXP = ConditionalExpression
