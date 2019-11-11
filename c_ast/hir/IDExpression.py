# This is to be treated like an abstract class, utility 
# struct, no direct application

from hir.Expression import Expression

class IDExpression(Expression):
    __slots__ = ['isTypename', 'isGlobal']

    def __init__(self, is_global=False, is_typename=False):
        Expression.__init__(self)
        self.isGlobal = is_global
        self.isTypename = is_typename

    def setGlobal(self, value):
        self.isGlobal = value

    def setTypename(self, value):
        self.isTypename = value

    def items(self):
        items = {}
        items['isTypename'] = getattr(self,'isTypename')
        items['isGlobal'] = getattr(self, 'isGlobal')
        for k in IDExpression.__bases__:
            if hasattr(k, 'items'):
                supitems = k.items(self)
                for k,v in list(supitems.items()):
                    items[k] = v
        return dict(items)

    def __getstate__(self):
        return dict(self.items())

    def __setstate__(self, statedict):
        for k,v in list(statedict.items()):
            setattr(self, k, v)

