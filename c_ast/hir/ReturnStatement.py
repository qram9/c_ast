from hir.Expression import Expression
from hir.Statement import Statement

class InvalidReturnTypeError(Exception):
    def __init__(self, value):
        self.value = value
    def __repr__(self):
        return 'Invalid Return Type:(%s) for ReturnStatement, expecting Expression' % (value)

class ReturnStatement(Statement):
    def __init__(self, retvalue=None):
        self.initialize()
        if retvalue:
            if isinstance(retvalue, Expression):
                self.setNumChildren(1)
                self.setChild(0, retvalue)
            else:
                raise InvalidReturnTypeError(str(type(retvalue)))
    def __repr__(self):
        if len(self.getChildren()) == 0:
            return 'return;'
        else:
            retval = 'return '
            retval += repr(self.getChild(0))
            retval += ';'
            return retval

if __name__ == '__main__':
    from hir.Identifier import Identifier
    print(ReturnStatement())    
    print(ReturnStatement(Identifier('k')))
