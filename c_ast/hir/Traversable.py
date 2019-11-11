class TraversableException(Exception): pass
class NumChildrenNotSetError(TraversableException):
    """Raise exception if not 
'number of children of a traversable node 
must be set prior to inserting children'"""
    def __init__(self, func='', iden=0):
        self.value1 = value1
        self.value2 = value2
    def __str__(self):
        raise NumChildrenNotSetError('Set number of children for traversable class on calling: (%s) for Traversable: (%s)' % (self.func, str(self.iden)))

class ChildIndexOutOfRangeError(TraversableException):
    """An index for a child must be smaller than _num_children"""
    def __init__(self, value1=0, value2=0):
        self.value1 = value1
        self.value2 = value2
    def __str__(self):
        return 'Invalid Index for children((referedIndex(%d), lastIndex(%d))'%(self.value1, self.value2)

class ParentNotTraversableError(TraversableException):
    """Parent must be a Traversable type"""
    def __init__(self, value=''):
        self.value = value
    def __str__(self):
        return 'Invalid type: (%s) for parent, must subclass Traversable' % (self.value)

class ChildNotTraversableError(TraversableException):
    """Exception for Specified Child, must be a Traversable type"""
    def __init__(self, value=''):
        self.value = value
    def __str__(self):
        return 'Invalid type: (%s) for parent, must subclass Traversable' % (self.value)

class ChildNotFoundError(TraversableException):
    """The refered Traversable type child must be present"""
    def __init__(self, value=''):
        self.value = value
    def __str__(self):
        return 'Specified child: (%s) not found' % (self.value)

class ParentNotSetError(TraversableException):
    """Parent must be set for trees"""
    pass

class ChildNotSetError(TraversableException):
    """Exception for Specified Child, must be set in traversable"""
    pass

class IndexTypeMustBeIntError(TraversableException):
    """Exception for argument for getChild, setChild, setNumChildren, argument must be Integer"""
    pass

#class ParentChildNotOKError(TraversableException):
#    pass

class Traversable(object):
    __slots__ = ['_parent', '_children', '_num_children']

    def initialize(self):
        """Derived classes have use for this function 
to set up a place holder in base class Traversable 
for initializing children to empty list"""
        self._children = []
        self._parent = None

    def __init__(self, num_children=0):
        """Call initialize function to Set up 
_children as a list to hold children"""
        self.initialize()
        self._num_children = num_children

# List of exception testing functions
    def _catchInvalidIndexTypeError(self, num):
        """Catch IndexTypeMustBeIntError"""
        if not isinstance(num, int):
            raise IndexTypeMustBeIntError(str(type(num)))
    def _catchNumChildrenNotSetError(self, func):
        """Catch NumChildrenNotSetError"""
        if not hasattr(self, '_num_children'):
            raise NumChildrenNotSetError(func, id(self))
    def _catchNumChildError(self, which):
        """Catch ChildIndexOutOfRangeError"""
        if which >= self._num_children:
            raise ChildIndexOutOfRangeError(which, self._num_children)
    def _catchChildNotTraversableError(self, t):
        """Catch ChildNotTraversableError"""
        if not isinstance(t, Traversable):
            raise ChildNotTraversableError(str(type(t)))
    def _catchChildNotFoundError(self, n, t):
        """Catch ChildNotFoundError"""
        try:
            k = self._children.index(t)
        except ValueError:
            raise ChildNotFoundError(n+'('+str(t)+')')

    def setNumChildren(self, num):
        """Set the Number of children for this 
Traversable object"""
        self._catchInvalidIndexTypeError(num)
        self._num_children = num
        return self

    def getNumChildren(self):
        """Returns the number of children for 
this Traversable object"""
        return self._num_children

    def setParent(self, t):
        """Set Parent, either to None or 
another Traversable object"""
        if not t:
            self._parent = None
        elif isinstance(t, Traversable):
            self._parent = t
        else:
            raise ParentNotTraversableError(str(type(t)))
        return self

    def removeChild(self, t):
        """Look for a given traversable object, 
remove it from hir.children, set its _parent to None"""
        self._catchChildNotFoundError('removeChild', t)
        t.setParent(None)
        self._children.remove(t)
        return self

    def insertBefore(self, ref, t):
        """Inserts a Traversable object, t, before a 
reference Traversable object ref belonging to 
_children. Tests if the insertion will not affect, 
conditions, ChildIndexOutOfRangeError"""
        self._catchNumChildrenNotSetError('setChild')
        if self.getNumChildren() == len(self._children):
            raise ChildIndexOutOfRangeError (self._num_children+1, self._num_children)
        self._catchChildNotTraversableError(t)
        self._catchChildNotTraversableError(ref)
        self._catchChildNotFoundError('insertBefore', ref)
        t.setParent(self)
        self._children.insert(self._children.index(ref), t)
        return self

    def insertAfter(self, ref, t):
        """Inserts a Traversable object, t, 
after a reference Traversable object ref belonging 
to _children. Tests if the insertion will not affect, 
conditions, ChildIndexOutOfRangeError"""
        self._catchNumChildrenNotSetError('setChild')
        if self.getNumChildren() == len(self._children):
            raise ChildIndexOutOfRangeError (self._num_children+1, self._num_children)
        self._catchChildNotTraversableError(t)
        self._catchChildNotTraversableError(ref)
        self._catchChildNotFoundError('insertAfter', ref)
        t.setParent(self)
        self._children.insert(self._children.index(ref)+1, t)
        return self

    def setChild(self, which, t):
        """Given an index to this Traversable object, 
look if there is a child at the index already, if so 
removeChild and insert t in its place"""
        self._catchInvalidIndexTypeError(which)
        self._catchChildNotTraversableError(t)
        self._catchNumChildrenNotSetError('setChild')
        self._catchNumChildError(which)
        try:
            indx = self._children[which]
            self.removeChild(self._children[which])
            self._children.insert(which, t)
        except IndexError:
            self._children.append(t)
        t.setParent(self)
        return self

    def detach(self):
        """Detach this Traversable object "tree" from hir.ts parent"""
        if hasattr(self, '_parent'):
            self._parent.removeChild(self)
            self._parent = None
        return self

    def getParent(self):
        """Get the parent node, (parent can be None)"""
        return self._parent    

    def getChildren(self):
        """Get the children list, dangerous method"""
        return self._children

    def getChild(self, which):
        """Look up a child node by an index value"""
        self._catchInvalidIndexTypeError(which)
        try:
            l = self._children[which]
            return self._children[which]
        except IndexError:
            raise ChildIndexOutOfRangeError(self._num_children, which)

    def items(self):
        """Returns a state dict with the __slots__ entries, 
_num_children, _children, _parent"""
        items = {}
        k = self.getNumChildren()
        items['_num_children'] = k
        k = self.getChildren()
        items['_children'] = list(k)
        k = self.getParent()
        items['_parent'] = k
        return dict(items)

    def __getstate__(self):
        """Returns a dict when called from hir.ickle or copy. 
Returned dict contains __slots__ entries: _num_children, 
_children, _parent"""
        return dict(self.items())
    def __setstate__(self, statedict):
        """Blindly sets state with a given getState type dict"""
        for k,v in list(statedict.items()):
            setattr(self, k, v)

