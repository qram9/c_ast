class DigrapherException(Exception): pass
class NotATraversableError(DigrapherException): pass
from Traversable import Traversable
from BreadthFirstIterator import BreadthFirstIterator

def Digrapher(t, pruneon=[]):
    """Function returns the string for a dot file that is to be 
    used used with graphviz to get pictures of HIR tree.  
    Add the 
    string "rankdir=LR;\n" for dot parameter to draw from 
    left to right. """
    retval = ""
    if not isinstance(t, Traversable):
        NotATraversableError, type(t)
    titr = BreadthFirstIterator(t)
    for k in pruneon:
        titr.PruneOn(k)
    graph_dict = {}
    retval += "digraph G {\n"
    #	retval += "\trankdir=LR;\n"
    #	retval += "\tsize=\"10,20\";\n"
    import re
    for k in titr.next():
        str_repr = re.sub('\n', ' ', repr(k))
        graph_dict[k] = str_repr
    titr = BreadthFirstIterator(t)
    child_num=0
    graph_node_dict = {}
    for k in titr.next():
        child_num+=1
        if graph_dict.has_key(k):
            retval += "\t%s%d [label = \"%s:%s\"];\n" \
% (k.__class__.__name__, child_num, k.__class__.__name__, graph_dict[k])
            graph_node_dict[k] = "%s%d" % (k.__class__.__name__, child_num)
        if k.getParent() \
and graph_node_dict.has_key(k.getParent()) \
and graph_node_dict.has_key(k):
			retval += "\t%s -> %s;\n" \
% (graph_node_dict[k.getParent()], graph_node_dict[k])
    retval += "}\n"
    return retval
