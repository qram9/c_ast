"""This file holds all operator types
used in Ansi C expressions. There are 
four classes of operators. BinaryOperators,
UnaryOperators, AssignmentOperators and 
ConditionalOperators. 

TODO: Much the same problem with keywords here
especially with copies. Here I use an explicit 
cmp function and a list of objects 
so that different operator objects of same type 
when checked with == will compute true result.
The same change will be added here like the keywords
i.e. Instead of objects, I will use classes 
(which cannot be initialized) to represent 
Operators in the HIR"""

class Operator(object):
    __slots__ = ('to_str',)

    def __init__(self, to_str):
        self.to_str = to_str

    def __str__(self):
        return self.to_str
    __repr__ = __str__

    def __eq__(self, other):
        if isinstance(other, Operator): 
            return self.to_str == other.to_str
        else:
            return False

    def __getstate__(self):
        items = {}
        for name in Operator.__slots__:
            items[name] = getattr(self,name)
        return dict(items)
    def __setstate__(self, statedict):
        for k,v in list(statedict.items()):
            #print 'setting state:', k, v
            setattr(self, k, v)

class BinaryOperator(Operator): pass
class UnaryOperator(Operator): pass
class AssignmentOperator(Operator): pass
class ConditionalOperator(Operator): pass

class ConditionalOperators(object):
    __slots__ = ['conditional_op', 'operators', 
            'COMPARE_EQ', 'COMPARE_GT', 'COMPARE_GE', \
            'COMPARE_LT', 'COMPARE_LE', 'COMPARE_NE']
    def __init__(self):
        self.conditional_op = {
            'COMPARE_EQ' : '==',
            'COMPARE_GT' : '>',
            'COMPARE_GE': '>=',
            'COMPARE_LT' : '<', 
            'COMPARE_LE' : '<=', 
            'COMPARE_NE' : '!=', 
            }
        self.operators = {}
        for k,v in list(self.conditional_op.items()):
            self.operators[k] = BinaryOperator(v)
            setattr(self, k, self.operators[k])

    def getOperatorList(self):
        return [op for k,op in list(self.operators.items())]

class BinaryOperators(object):
    __slots__ = ['binary_op', 'operators', 'ADD', \
            'BITWISE_AND', 'BITWISE_XOR', 'BITWISE_OR',\
            'DIVIDE', 'LOGICAL_AND', 'LOGICAL_OR', \
            'MODULUS', 'MULTIPLY', 'SHIFT_LEFT', 'SHIFT_RIGHT', \
            'SUBTRACT', 'EQUAL']

    def __init__(self):
        self.binary_op = {
            'ADD' : '+', 
            'BITWISE_AND' : '&', 
            'BITWISE_XOR' : '^',
            'BITWISE_OR' : '|',
            'DIVIDE' : '/', 
            'LOGICAL_AND' : '&&', 
            'LOGICAL_OR' : '||', 
            'MODULUS' : '%', 
            'MULTIPLY' : '*', 
            'SHIFT_LEFT' : '<<', 
            'SHIFT_RIGHT' : '>>', 
            'SUBTRACT' : '-' } 
        self.operators = {}
        for k,v in list(self.binary_op.items()):
            self.operators[k] = BinaryOperator(v)
            setattr(self, k, self.operators[k])

    def getOperatorList(self):
        return [op for k,op in list(self.operators.items())]

    def __getstate__(self):
        items = {}
        for name in BinaryOperators.__slots__:
            items[name] = getattr(self,name)
        return dict(items)
    def __setstate__(self, statedict):
        for k,v in statedict.items:
            setattr(self, k, v)

class UnaryOperators(object):
    __slots__ = ['unary_op', 'operators', 'ADDRESS_OF', 'BITWISE_NOT', \
            'DEREFERENCE', 'LOGICAL_NEGATION', 'MINUS', 'PLUS', \
            'POST_DECREMENT', 'POST_INCREMENT', 'PRE_DECREMENT', \
            'PRE_INCREMENT']
    def __init__(self):
        self.unary_op = \
            {'ADDRESS_OF' : '&',
            'BITWISE_NOT' : '~',
            'DEREFERENCE' : '*',
            'LOGICAL_NEGATION' : '!',
            'MINUS' : '-',
            'PLUS' : '+',
            'POST_DECREMENT' : '--',
            'PRE_DECREMENT' : '--',
            'POST_INCREMENT' : '++',
            'PRE_INCREMENT' : '++'}
        self.operators = {}
        for k,v in list(self.unary_op.items()):
            self.operators[k] = UnaryOperator(v)
            setattr(self, k, self.operators[k])

    def getOperatorList(self):
        return [op for k,op in list(self.operators.items())]

    def __getstate__(self):
        items = {}
        for name in UnaryOperators.__slots__:
            items[name] = getattr(self,name)
        return dict(items)
    def __setstate__(self, statedict):
        for k,v in statedict.items:
            setattr(self, k, v)

class AssignmentOperators(object):
    __slots__ = ('assign_op', 'operators', 
            'ADD', 'BITWISE_AND', 'BITWISE_OR', 'BITWISE_EXCLUSIVE_OR',
            'DIVIDE', 'EQUAL', 'MODULUS', 'MULTIPLY', 'SHIFT_LEFT',
            'SHIFT_RIGHT', 'SUBTRACT')
    def __init__(self):
        self.assign_op = {'ADD' : '+=',
                'BITWISE_AND' : '&=',
                'BITWISE_OR' : '|=',
                'BITWISE_EXCLUSIVE_OR' : '^=',
                'DIVIDE' : '/=',
                'EQUAL' : '=', 
                'MODULUS' : '%=', 
                'MULTIPLY' : '*=', 
                'SHIFT_LEFT' : '<<=', 
                'SHIFT_RIGHT' : '>>=', 
                'SUBTRACT' : '-=' }
        self.operators = {}
        for k,v in list(self.assign_op.items()):
            self.operators[k] = AssignmentOperator(v)
            setattr(self, k, self.operators[k])

    def getOperatorList(self):
        return [op for k,op in list(self.operators.items())]

    def __getstate__(self):
        items = {}
        for name in AssignmentOperators.__slots__:
            items[name] = getattr(self,name)
        return dict(items)
    def __setstate__(self, statedict):
        for k,v in statedict.items:
            setattr(self, k, v)

binaryOperator = BinaryOperators()
unaryOperator = UnaryOperators()
assignmentOperator = AssignmentOperators()
conditionalOperator = ConditionalOperators()

def getBinaryOperatorList():
    bops = binaryOperator.getOperatorList()
    return bops
def getAssignmentOperatorList():
    aops = assignmentOperator.getOperatorList()
    return aops
def getUnaryOperatorList():
    uops = unaryOperator.getOperatorList()
    return uops
def getConditionalOperatorList():
    cops = conditionalOperator.getOperatorList()
    return cops

if __name__ == '__main__':
    print ('binary operators')
    for k in binaryOperator.binary_op:
        print((k, '->', type(getattr(binaryOperator, k))))
        print((k, '->', getattr(binaryOperator, k)))
    print ('unary operators')
    for k in unaryOperator.unary_op:
        print((k, '->', type(getattr(unaryOperator, k))))
        print((k, '->', getattr(unaryOperator, k)))
    print ('assignment operators')
    for k in assignmentOperator.assign_op:
        print((k, '->', type(getattr(assignmentOperator, k))))
        print((k, '->', getattr(assignmentOperator, k)))
