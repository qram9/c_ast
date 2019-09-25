import sys
class Stack(object):
    __slots__ = ("_stack", "_trackStackUpdate", "_lastState", \
    "_presentState", "_lastAction", "_stackString", "_stackName", \
    "_stackDotFile", "_state_count")
    
    def __init__(self, name):
        self._stack = []
        self._trackStackUpdate = False
        self._stackString = []
        self._lastState = self._stackString
        self._presentState = self._lastState
        self._stackName = "%s" % (name)

    def __del__(self):
        if self._trackStackUpdate:
            self._stackDotFile.write("}\n")
            self._stackDotFile.close()

    def push(self, ntry, debugNfo=""):
        self._stack.insert(0,ntry)
        self._updateStackStatus("push_ "+debugNfo)

    def pop(self, debugNfo=""):
        k = self._stack.pop(0)
        self._updateStackStatus("pop_ "+debugNfo)        
        return k

    def peek(self):
        k = self._stack[0]    
        return k

    def setTrackStackUpdate(self, todo):
        self._trackStackUpdate = todo
        if self._trackStackUpdate:
            self._stackDotFile = open("%s.%s" % (self._stackName, "dot"), "w")
            self._stackDotFile.write("digraph %s {node [shape=plaintext]\n" \
            % self._stackName)
            #self._stackDotFile.write("rankdir=\"LR\"\n"
            self._state_count = 0

    def _updateStackStatus(self, action):
        if self._trackStackUpdate:
            import copy        
            self._lastState = copy.copy(self._presentState)
            self._updateStackString(action)            
            self._presentState = self._stackString
            self._lastAction = action
            self._graphIt()

    def _nextStateCount(self):
        self._state_count +=1
        return self._state_count

    def _graphIt(self):
        self._stackDotFile.write("stack_%d " % self._nextStateCount())
        self._stackDotFile.write("[label=<\n\t<TABLE>\n")
        if not self._presentState:
            self._stackDotFile.write("\t\t<TR><TD>%s</TD></TR>\n"%"Empty")      
        for k in self._presentState:
            self._stackDotFile.write("\t\t<TR><TD>%s</TD></TR>\n"%k)      
        self._stackDotFile.write("\t</TABLE>>];\n")
        self._stackDotFile.write("stack_%d -> stack_%d [label=\"%s\"];\n" % \
        (self._state_count-1, self._state_count, self._lastAction))

    def _updateStackString(self,action):
        if action.startswith("push"):
            self._stackString.insert(0,self._singleLineString(self.peek()))
        elif action.startswith("pop"):
            self._stackString.pop(0)
        return self._stackString

    def _singleLineString(self, k):
        import re
        str_repr = ""
        #str_repr = k.__class__.__name__ + ':'
        str_repr += re.sub('\n', ' ', repr(k))
        return str_repr

    def __repr__(self):
        ret = ""
        for k in self._presentState:
            ret += self._singleLineString(k)
        return ret
