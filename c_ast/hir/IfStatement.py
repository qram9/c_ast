from Statement import Statement
from CompoundStatement import CompoundStatement
from Expression import Expression
class NotAStatementError(Exception):
	def __init__(self, value=''):
		self.value = value
	def __repr__(self):
		return 'Invalid body type:(%s) for If statement' % self.value
class IfStatementException(Exception): pass
class InvalidExpressionForConditionError(IfStatementException): pass
class IfStatement(Statement):
    """Represents an Ansi C IfStatement, holds 3 children,
    ConditionExpression, 'if' part and the 'else' parts. 'If' parts and
    'else' parts are of type CompoundStatement or Statement. The true and false
    bodies represent a new scope for execution"""
    def __init__(self, condition, true_body, false_body=None):
        """Initialize takes 3 parameters, the 
        ConditionalExpression control statement, true_body, false_body 
        both either CompoundStatements or Statements."""
        if not isinstance(condition, Expression):
            raise InvalidExpressionForConditionError, type(condition)
        self.initialize()
        Statement.__init__(self)
        self.setNumChildren(3)
        self.setChild(0, condition)
        if isinstance(true_body, (CompoundStatement, Statement)):
            self.setChild(1, true_body)
        else:
            raise NotAStatementError(str(type(true_body)) + repr(true_body))
        if false_body:
            if isinstance(false_body, (CompoundStatement, Statement)):
                self.setChild(2, false_body)
            else:
                raise NotAStatementError(str(type(false_body)) + repr(false_body))
    def getControlExpression(self):
        """Returns the control statement that is used in the IF statement"""
        return self.getChild(0)
    def getThenStatement(self):
        """Returns the true CompoundStatement body"""
        return self.getChild(1)
    def getElseStatement(self):
        """Returns the false CompoundStatement body"""
        try:
            return self.getChild(2)
        except:
            return None
    def __repr__(self):
        """Returns the Ansi C representation of the
        HIR If Statement. For ex: if (...) {} else{}"""
        retval = 'if ('
        retval += repr(self.getChild(0)) + ') '
        retval += repr(self.getChild(1))
        try:
            if self.getChild(2):
                retval += 'else ' + repr(self.getChild(2))
        except:
            pass
        return retval
from Imports import *
def IfStatementTest():
    import copy
    control = ConditionalExpression(Identifier('a'), conditionalOperator.COMPARE_GT, IntegerLiteral(0))
    assignexp1 = AssignmentExpression(Identifier('a'), assignmentOperator.ADD, Identifier('b'))
    assignStmt1 = ExpressionStatement(assignexp1)
    decl1 = DeclarationStatement(VariableDeclaration(specifiers.inT, \
            VariableDeclarator(Identifier('y'))))
    body = CompoundStatement()
    body.addStatement(decl1)
    copy_ifbody = copy.deepcopy(body)
    body.addStatement(assignStmt1)
    assignStmt2 = copy.deepcopy(assignStmt1)
    copy_ifbody.addStatement(assignStmt2)
    ifconstruct = IfStatement(control, body)
    control = ConditionalExpression(Identifier('a'), conditionalOperator.COMPARE_LT, IntegerLiteral(0))
    ifconstruct = IfStatement(control, copy_ifbody, ifconstruct)
    return ifconstruct    
if __name__ == '__main__':
    print IfStatementTest()
    
