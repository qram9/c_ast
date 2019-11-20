def children(node):
    """Returns a list containing all child nodes 
of a Traversable type node. Returns empty list
when the node has no children. Used by BF/DF/Flat
iterative tree visitor functions."""
    try:
        k = node.getChildren()
        return k
    except:
        return []


def bfsItr(root):
    """Yeilds the next object in a 
Breadth first Iterator. First object 
returned is the passed parameter. Following this
the children of the object are returned followed by
children's children... etc. all in breadth-first order.

Maintains a queue containing children nodes of 
a tree node. All children of the tree are visited 
in breadth first order. The queue is used as a 
FIFO implemention to acheive this breadth first
visiting."""
    queue = []
    queue.append(root)
    while len(queue):
        r = queue[0]
        yield r
        queue.remove(r)
        for k in children(r):
            queue.append(k)


if __name__ == '__main__':
    from hir.Procedure import procedureTest
    bfstest = procedureTest()
    for k in bfsItr(bfstest):
        print('next: ', id(k))
