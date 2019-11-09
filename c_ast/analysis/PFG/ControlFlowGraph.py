from hir.Imports import *
from analysis.PFG.ProcBasicBlock import ProcBasicBlock
from hir.BreadthFirstIterator import BreadthFirstIterator
from hir.Statement import Statement
from analysis.PFG.BasicBlock import BasicBlock
from utils.Stack import Stack

class ControlFlowGraphException(Exception): pass
class InvalidHIRTypeError(ControlFlowGraphException): pass
class NotABasicBlockError(ControlFlowGraphException): pass
class StackNotFoundError(ControlFlowGraphException): pass
class DispatchFunctionNotFoundError(ControlFlowGraphException): pass

class ControlFlowGraph(object):
    __slots__ = ('_breakStack', '_continueStack', '_switchStack',\
    '_scopeEntryStack', '_scopeExitStack', '_bblist','_stateStack',\
    '_procName', '_uniq_id')
    def __init__(self, t):
        if not isinstance(t, Procedure):
            raise ControlFlowGraphException("Invalid type for ControlFlowGraph, init").with_traceback(type(t))
        self._procName = t.getIdentifier()
        self._uniq_id = 0
        self._initStateStacks()
        self._setBBFromProc(t)

    def _initStateStacks(self):
        self._breakStack = Stack("%s_breakStack" % repr(self._procName))
        self._continueStack = Stack("%s_continueStack" % repr(self._procName))
        self._switchStack = Stack("%s_switchStack" % repr(self._procName))
        self._scopeEntryStack = Stack("%s_scopeEntryStack" % repr(self._procName))
        self._scopeExitStack = Stack("%s_scopeExitStack" % repr(self._procName))
        self._bblist = []
        self._stateStack = [self._breakStack, \
                           self._continueStack, \
                           self._switchStack, \
                           self._scopeEntryStack, \
                           self._scopeExitStack]
        for k in self._stateStack:
            k.setTrackStackUpdate(True)

    def graphIt(self):
        dotfile = open("%s.%s" % (repr(self._procName), "dot"), "w")
        dotfile.write("digraph %s { \n" % self._procName) 
#node [shape=plaintext]\n" % self._procName)
        for k in self._bblist:
            dotfile.write(k.getName()+ " ")
            #           dotfile.write("[label=<\n\t<TABLE>\n")
            if k.getStatements():
                #dotfile.write("\t\t<TR><TD>%s</TD></TR>\n"%"Empty")
                dotfile.write("[label=<")
                for r in k.getStatements():
                    dotfile.write(self._fixForGraphIt(self._singleLineString(r)))
                    #\t\t<TR><TD>\"%s\"</TD></TR>\n" \
                    #% self._fixForGraphIt(self._singleLineString(r)))
                    #dotfile.write("\t</TABLE>>];\n")
                dotfile.write(">];\n")
            else:
                dotfile.write("[label=<EMPTY>];\n")
        for k in self._bblist:
            for r in k.getSuccs():
                dotfile.write("%s -> %s;\n" % (k.getName(), r.getName()))
        dotfile.write("}\n")
        dotfile.close()   
        
    def _setBBFromProc(self, t):
        p_BB = ProcBasicBlock(repr(self._procName))
        self._scopeEntryStack.push(p_BB.entryBB, "to add %s" % p_BB.entryBB.getName())
        self._scopeExitStack.push(p_BB.exitBB, "to add %s" % p_BB.exitBB.getName())
        # Nice if we can add Entry & RETURN Annontation here?
        self._extendBBWithList([p_BB.entryBB, p_BB.exitBB] )
        self._dispatcher(t.getBody())
        connect_last = self._pop("_scopeEntryStack", \
                "last_one connects to procedure exit BB")
        self._addSuccPred(connect_last, p_BB.exitBB)

    def _dispatcher(self, t):
        self._testAndApply(t)

    def _testAndApply(self, t):
        if hasattr(self, '_do_' + t.__class__.__name__):
            getattr(self, '_do_' + t.__class__.__name__)(t)
        else:
            raise DispatchFunctionNotFoundError('testAndApply fail: <%s> not found during CFG setup' % str(type(t)))

    def _catchNotABasicBlockError(self, u):
        if isinstance(u, list):
            for k in u:
                if not isinstance(k, BasicBlock):
                    raise NotABasicBlockError(type(k))
        elif not isinstance(u, BasicBlock):
            raise NotABasicBlockError(type(u))

    def _addSuccPred(self, u, v):
        self._catchNotABasicBlockError([u,v])
        u.addSuccessor(v)
        v.addPredecessor(u)

    def _addBasicBlock(self, tag=None):
        if tag:
            k = BasicBlock("%s_%s"%(repr(self._procName), tag))
        else:
            k = BasicBlock("%s_%s_%d"%(repr(self._procName), "L", self._getNextCount()))
        self._bblist.append(k)
        print("addBB:<%s>" % k)
        return k

    def _extendBBWithList(self, t):
        self._catchNotABasicBlockError(t)
        if isinstance(t, list):
            self._bblist.extend(t)
        else:
            self._bblist.append(t)

    def _push(self, aList, ntry, debugNfo=""):
        self._catchNotABasicBlockError(ntry)
        if hasattr(self, aList):
            aList = getattr(self, aList)
            aList.push(ntry, debugNfo)
        else:
            raise StackNotFoundError("Unknown Stack Variable requested: %s" % aList)
    def _pop(self, aList, debugNfo=""):
        if hasattr(self, aList):
            real_list = getattr(self, aList)
            k = real_list.pop(debugNfo)
            return k
        else:
            raise StackNotFoundError("Unknown Stack Variable requested: %s" % aList)
    def _peek(self, aList):
        if hasattr(self, aList):
            real_list = getattr(self, aList)
            return real_list.peek()
        else:
            raise StackNotFoundError("Unknown Stack Variable requested: %s" % aList)

    def _getNextCount(self):
        self._uniq_id += 1
        return self._uniq_id-1

    def _singleLineString(self, k):
        import re
        str_repr = k.__class__.__name__ + '_'
        b4 = re.sub('\n|;', ' ', repr(k))
        str_repr = b4
        return str_repr

    def _fixForGraphIt(self, b4):
        import re
        for k in "!~`@#$%^&*()_-+=|\[];'/.,><?\"\:(){}":
            r = '\\'+k
            b4 = re.sub('\\'+k, r, b4)
        return b4    

    def _createBasicBlock(self, aName):
        bb = BasicBlock("%s_%s_%d" \
                % (repr(self._procName), aName, self._uniq_id))
        return bb

    def _do_ForLoop(self,t):
        # do the initialization and test if init < limit
        uniq_num = self._getNextCount() 
        ie = t.getInit()
        eie, cie = list(map(ExpressionStatement, (t.getInit(), t.getCondition())))
        eie.setParent(t)
        cie.setParent(t)
        # lose the predecessor BB
        pred = self._pop("_scopeEntryStack", 
                "Predecessor BB: %s before processing for loop")
        # for_pre_header
        for_pre_header = self._createBasicBlock("FOR_PRE_HEADER")
        self._bblist.append(for_pre_header)
        self._addSuccPred(pred, for_pre_header)
        self._push("_scopeEntryStack", for_pre_header, \
                "_for_pre_header: %s before processing init expression" \
                % for_pre_header.getName())
        self._dispatcher(eie)
        for_pre_header = self._pop("_scopeEntryStack", \
                "_for_pre_header: %s after processing init expression" \
                % self._peek("_scopeEntryStack").getName())

        # for_header
        for_header = self._createBasicBlock("FOR_HEADER")
        self._bblist.append(for_header)
        self._addSuccPred(for_pre_header, for_header)
        self._push("_scopeEntryStack", for_header, \
                "_for_header: %s before processing conditional expression" \
                % for_header.getName())
        self._dispatcher(cie)
        for_header = self._pop("_scopeEntryStack", \
                "_for_header: %s after processing conditional expression" \
                % self._peek("_scopeEntryStack").getName())

        # for_exit
        for_exit = self._createBasicBlock("FOR_EXIT")
        self._bblist.append(for_exit)
        self._push("_breakStack", for_exit,
                "breaks must connect to _for_exit: %s" % for_exit.getName())

        # for_step
        for_step = self._createBasicBlock("FOR_STEP")
        self._bblist.append(for_step)
        self._push("_continueStack", for_step, \
                "continues must connect to _for_step: %s" % for_step.getName())

        # for_body
        for_body = self._createBasicBlock("FOR_BODY")
        self._bblist.append(for_body)
        self._addSuccPred(for_header, for_body)
        self._push("_scopeEntryStack", for_body, \
                "_for_body: %s before processing for body" \
                % for_body.getName())
        self._dispatcher(t.getBody())
        for_body = self._pop("_scopeEntryStack", \
                "_for_header: %s after processing for_body" \
                % self._peek("_scopeEntryStack").getName())
        self._addSuccPred(for_body, for_step)
        self._addSuccPred(for_step, for_header)
        self._addSuccPred(for_header, for_exit)
        self._push("_scopeEntryStack", for_exit, \
                "_for_exit: %s after processing for_loop" \
                % for_exit.getName())

    def _do_WhileLoop(self, t):
        print(self._singleLineString(t))
    def _do_DoLoop(self, t):
        print(self._singleLineString(t))
    def _do_SwitchStatement(self, t):
        print(self._singleLineString(t))
    def _do_ReturnStatement(self, t):
        print(self._singleLineString(t))

    def _process_IfThen(self, t, ifthen):
        # call _dispatcher with then block, but add then to scopeEntryStack first
        # add edge between ifentry and then
        self._push("_scopeEntryStack", ifthen, \
                "Pushing _if_then:%s into scopeEntryStack before then dispatch" \
                % ifthen.getName())
        thenStatement = t.getThenStatement()
        self._dispatcher(thenStatement)

    def _process_IfElse(self, t, ifelse):    
        self._push("_scopeEntryStack", ifelse, \
                "Pushing ElseStatement block:%s before processing ElseStatement" \
                % ifelse.getName())
        elseStatement = t.getElseStatement()
        self._dispatcher(elseStatement)

    def _handleIfStatement(self,t):
        uniq_num = self._getNextCount()
        pred = self._pop("_scopeEntryStack", \
                "predecessor: %s b4 processing new IfStatement" \
                % self._peek("_scopeEntryStack"))
        # process control expression
        # extract the control expression into an expression statement
        ce = t.getControlExpression()
        ece = ExpressionStatement(ce)
        ece.setParent(t)
        ifentry = self._createBasicBlock("IFENTRY")
        self._bblist.append(ifentry)
        self._push("_scopeEntryStack", ifentry, \
                "_if_entry:%s into _scopeEntryStack for processing control expression" \
                % ifentry.getName())
        self._dispatcher(ece)
        ifentry = self._pop("_scopeEntryStack",
                "_if_entry:%s from _scopeEntryStack after processing control expression" \
                % self._peek("_scopeEntryStack").getName())

        # set up a continuing set of edges
        # edge from pred and ifentry
        # taken edge from ifentry and ifthen
        self._addSuccPred(pred, ifentry)
        ifthen = self._createBasicBlock("IFTHEN")
        self._bblist.append(ifthen)
        self._addSuccPred(ifentry, ifthen) 
        self._process_IfThen(t, ifthen)
        # edge from ifthen to ifexit
        ifexit = self._createBasicBlock("IFEXIT")
        self._bblist.append(ifexit)
        self._addSuccPred(ifthen, ifexit)
        ifthen = self._pop("_scopeEntryStack",
                "_if_then:%s from _scopeEntryStack after processing then statement" \
                % self._peek("_scopeEntryStack").getName())
        # process else statement if any
        if t.getElseStatement():
            ifelse = self._createBasicBlock("IFELSE")
            self._bblist.append(ifelse)
            # not taken edge from ifentry to ifelse
            self._addSuccPred(ifentry, ifelse)
            self._process_IfElse(t, ifelse)
            # add edge between ifelse and ifexit after processing ElseStatement
            self._addSuccPred(ifelse, ifexit)
            ifelse = self._pop("_scopeEntryStack",
                "_if_else:%s from scopeEntryStack after else dispatch" \
                % ifelse.getName())
            self._addSuccPred(ifelse, ifexit)
        else:
            self._addSuccPred(ifentry, ifexit)
        self._push("_scopeEntryStack", ifexit, \
                "_if_exit:%s for use as pred" \
                % ifexit.getName())

    def _do_IfStatement(self, t):
        self._handleIfStatement(t)
        print(self._singleLineString(t))

    def _do_ExpressionStatement(self,t):
        pred_bb = self._peek("_scopeEntryStack")
        pred_bb.addStatement(t)
        print(self._singleLineString(t))

    def _do_DeclarationStatement(self,t):
        print(self._singleLineString(t))
    def _do_ContinueStatement(self, t):
        print(self._singleLineString(t))
    def _do_BreakStatement(self, t):
        print(self._singleLineString(t))
    def _do_CompoundStatement(self, t):
        for k in t.getChildren():
            self._testAndApply(k)
        print(self._singleLineString(t))

