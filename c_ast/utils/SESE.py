from itertools import count
import pudb

new_node_class = count().__next__
new_edge_class = count(-100).__next__
new_region_class = count(-1000).__next__


class Node:
    __slots__ = ('dfs_num', 'blist', 'hi', 'numeric_id', 'node_content')

    def __init__(self, node_c):
        self.dfs_num, self.blist, self.hi, self.numeric_id, \
            self.node_content = 0, Bracket_list(), None, 0, node_c

    def __str__(self):
        return ("<num = " + str(self.numeric_id)
                + ", dfs_num = " + str(self.dfs_num)
                + ", hi = " + str(self.hi) + ">")


class Edge:
    ''' To me, implementing edges this way makes sense
 for doing undirected DFS by Johnson et al (regarding
 self.from_n and self.to_n)'''
    __slots__ = ('edge_class', 'recent_size', 'recent_class', 'ord_pair',
                 'from_n', 'to_n', 'entry', 'exit')

    def __init__(self, from_n, to_n):
        self.edge_class, self.recent_size, self.recent_class = None, 0, 0
        self.ord_pair = (from_n, to_n)
        self.from_n = from_n
        self.to_n = to_n
        self.entry = None
        self.exit = None

    def __str__(self):
        return ("(" + str(self.from_n) + ", " + str(self.to_n) + ")" + ", "
                + "edge_class: " + str(self.edge_class) + " recent_class: " +
                str(self.recent_class))


class Bracket_list:
    __slots__ = ('bracket_list',)

    def __init__(self):
        self.bracket_list = list()

    def size(self):
        return len(self.bracket_list)

    def push(self, e):
        self.bracket_list.append(e)

    def top(self):
        return self.bracket_list[-1]

    def delete(self, e):
        self.bracket_list.remove(e)

    def concat(self, bl2):
        self.bracket_list.extend(bl2.bracket_list)

    def __str__(self):
        ret = ''
        ret += ', '.join([str(a) for a in (self.bracket_list)])
        return ret


class Region:
    __slots__ = ('num_id', 'entry', 'exit')

    def __init__(self):
        self.entry = None
        self.exit = None
        self.num_id = new_region_class()

    def __str__(self):
        ret = ('ID: ' + str(self.num_id) +\
               ' Entry:<' + str(self.entry) + '>'
               + ' Exit:<' + str(self.exit) + '>')
        return ret


class Graph:
    ''' Using the Parent based DFS algo to do undirected graph DFS.'''
    __slots__ = ('start', 'nodes', 'node_dic', 'num_edges',
                 'parent', 'dfs_num', 'finish_num',
                 'start_time', 'dfs_time', 'pre_number',
                 'dir_adj_list', 'multi_graph_adj_list',
                 'post_order', 'tree_edges', 'back_edges',
                 'capping_back_edges', 'rev_dfs_num', 'dfs_edges',
                 'brack_set', 'visited_node', 'edges', 'last_region',
                 'edges_by_class', 'first_of_class', 'last_of_class',
                 'regions', 'dir_edges')

    def __init__(self):
        self.start = 0
        self.dir_adj_list = dict()
        self.num_edges = 0
        self.multi_graph_adj_list = dict()
        self.nodes = list()
        self.parent = dict()
        self.dfs_num = dict()
        self.rev_dfs_num = dict()
        self.finish_num = dict()
        self.start_time = dict()
        self.dfs_time = 0
        self.post_order = list()
        self.node_dic = dict()
        self.tree_edges = dict()
        self.back_edges = dict()
        self.capping_back_edges = dict()
        self.pre_number = 0
        self.dfs_edges = list()
        self.brack_set = dict()
        self.visited_node = set()
        self.edges = list()
        self.last_region = dict()
        self.first_of_class = dict()
        self.last_of_class = dict()
        self.regions = list()
        self.dir_edges = list()

    def descendant(self, u, v):
        if (self.start_time[u] < self.start_time[v] and
           self.finish_num[u] > self.finish_num[v]):
            return True
        return False

    def ancestor(self, u, v):
        return self.descendant(v, u)

    def V(self):
        return len(self.nodes)

    def E(self):
        return len(self.num_edges)

    def add_node(self, anod):
        self.nodes.append(anod)
        self.dir_adj_list[anod.numeric_id] = []
        self.multi_graph_adj_list[anod.numeric_id] = []
        self.node_dic[anod.numeric_id] = anod
        self.back_edges[anod.numeric_id] = list()
        self.tree_edges[anod.numeric_id] = list()
        self.capping_back_edges[anod.numeric_id] = list()

    def add_nodes_from(self, nodes):
        self.nodes = []
        self.node_dic = {}
        for k in nodes:
            anod = Node(k)
            anod.numeric_id = new_node_class()
            self.add_node(anod)

    @staticmethod
    def add_to_adj_list(adj_list, from_a, to_a):
        if from_a not in adj_list:
            adj_list[from_a] = list()
        adj_list[from_a].append(to_a)

    def add_edge(self, from_nod, to_nod):
        '''Edges are stored in an list without checking for membership.'''
        from_a = from_nod.numeric_id  # get int id of node
        to_a = to_nod.numeric_id
        self.num_edges += 1
        self.add_to_adj_list(self.dir_adj_list, from_a, to_a)
        self.add_to_adj_list(self.multi_graph_adj_list, from_a, to_a)
        self.add_to_adj_list(self.multi_graph_adj_list, to_a, from_a)

    def dfs_visit(self, anod):
        for succ_nod in self.dir_adj_list[anod]:
            if succ_nod not in self.parent:
                self.dir_edges.append((anod, succ_nod))
                self.parent[succ_nod] = anod
                self.dfs_visit(succ_nod)

    def dfs(self):
        self.parent = dict()
        for anod_i in self.nodes:
            anod = anod_i.numeric_id
            if anod not in self.parent:
                self.parent[anod] = None
                self.dfs_visit(anod)

    def dfs_starting_at(self, start_node):
        self.parent = dict()
        self.parent[start_node.numeric_id] = None
        self.dfs_visit(start_node.numeric_id)

    def undirected_dfs_visit(self, anod):
        self.dfs_num[anod] = self.pre_number
        self.rev_dfs_num[self.pre_number] = anod
        self.dfs_time += 1
        self.pre_number += 1
        self.start_time[anod] = self.dfs_time
        for succ_nod in self.multi_graph_adj_list[anod]:
            if succ_nod not in self.parent:
                print("New treeedge", anod, succ_nod)
                edg = Edge(anod, succ_nod)
                self.dfs_edges.append(edg)
                self.tree_edges[anod].append(edg)
                self.tree_edges[succ_nod].append(edg)
                self.parent[succ_nod] = anod
                self.edges.append(edg)
                self.undirected_dfs_visit(succ_nod)
            else:
                ''' This stuff of treating a directed graph
as an undirected version tends to be very rarely seen or
spoken about. I googled for my part - but was not much lucky...
Has ended up confusing me quite a lot.

In the adj-list representation for undirected, we have
edges going from src to dest and from dest to src (with
dest and src relationship from the directed version).
Edge counts are double that of the incoming directed version.
Now, that means that the duplicated tree edges would become back-edges
during undirected DFS. However, we need to think of edges
as an 'unordered-set of two nodes' rather than an 'ordered-pair'.
That would then imply setting the edge on first-visit
as a tree-edge. It is confusing as to what happens if the order
of visitation does not start at the root of the incoming CFG.
So basically all this needs to be unit-tested rigourously.

What I did is prioritize a tree-edge. Basically, not mark an edge as a
back-edge if it is already a tree-edge.

Generally directed or undirected graphs can have multiple
incoming back-edges or what gets called parallel-edges or self-loops.
Even a loop with just two nodes seems to get lost.
Imagine a->b and b->a. These are going to look perfect in
a CFG, no questions asked. Now, how to we differentiate
this tree-edge a->b and back-edge b->a, as these two edges
are the same set {a,b}. It would then be argued that a->b and b->a are both
the same in undirected and trivially cycle-equivalent, just as
they are in directed... maybe all that is part of the story.
These edges seem to fall out of consideration
but manage to stand not. Maybe Johnson et al has
many surprises in store.'''
                dont_add = False
                for edg in self.tree_edges[succ_nod]:
                    if (edg.to_n == anod or edg.from_n == anod):
                        dont_add = True
                        break
                if dont_add is True:
                    continue

                for edg in self.back_edges[succ_nod]:
                    if (edg.to_n == anod or edg.from_n == anod):
                        dont_add = True
                        break
                if dont_add is True:
                    continue
                edg = Edge(anod, succ_nod)
                print("backedge", edg)
                # pudb.set_trace()
                self.edges.append(edg)
                self.back_edges[succ_nod].append(edg)
                self.back_edges[anod].append(edg)
        self.post_order.append(self.node_dic[anod])
        self.dfs_time += 1
        self.finish_num[anod] = self.dfs_time

    def undirected_dfs_starting_at(self, start_node):
        self.parent = dict()
        self.parent[start_node.numeric_id] = None
        self.undirected_dfs_visit(start_node.numeric_id)

    def undirected_dfs(self):
        self.parent = dict()
        self.back_edges = dict()
        self.tree_edges = dict()
        for anod_i in self.nodes:
            anod = anod_i.numeric_id
            if anod not in self.parent:
                self.parent[anod] = None
                self.undirected_dfs_visit(anod)

    def fill_dfs_nums(self):
        for nod in self.nodes:
            num_id = nod.numeric_id
            nod.dfs_num = self.dfs_num[num_id]

    def undirected_edge_dfs(self, curnod):
        ''' DFS visitor containing the implementation
of slow cycle equivalence algorithm given in Johnson et al'''
        self.visited_node.add(curnod)
        for edg in self.tree_edges[curnod]:
            succ = edg.to_n if edg.from_n == curnod else edg.from_n
            if succ not in self.visited_node:
                self.undirected_edge_dfs(succ)
        # point of retreat

        self.brack_set[curnod] = set()

        for edg in self.tree_edges[curnod]:
            if edg.from_n != curnod:
                continue
            succ = edg.to_n
            self.brack_set[curnod] = self.brack_set[curnod].union(
                                                self.brack_set[succ])

        for back_edg in self.back_edges[curnod]:
            if back_edg.from_n == curnod:
                succnod = back_edg.to_n
            elif back_edg.to_n == curnod:
                succnod = back_edg.from_n
            else:
                succnod = None
            if self.descendant(succnod, curnod):
                self.brack_set[curnod].add(back_edg)
            elif self.ancestor(succnod, curnod):
                self.brack_set[curnod].remove(back_edg)

    def slow_cycle_equiv(self):
        ''' The slow cycle equivalence algorithm discussed in Johnson et al'''
        self.visited_node.clear()
        self.undirected_edge_dfs(0)
        for nod in self.nodes:
            if nod.numeric_id not in self.visited_node:
                self.undirected_edge_dfs(nod.numeric_id)
        for nod_num, brack_set in self.brack_set.items():
            print("Brackets for:", nod_num,
                  ', '.join([str(edg) for edg in brack_set]))

    def cycle_equiv(self):
        ''' Faithful (?) implementation of Johnson et al
CycleEquiv algo PLDI1994'''
        # The algorithm says "reverse depth-first order"
        # I never heard or that phrase or order being used anywhere
        # - here goes nothing
        # dfs num is pretty much same as 'preorder' numbering
        for rev_df in range(self.pre_number - 1, 0, -1):
            anod = self.node_dic[self.rev_dfs_num[rev_df]]
            print("Visit ", anod.numeric_id, rev_df)
            try:
                ''' Find the earliest headed (backedge succ with the lowest
dfs-num or preorder number among all back-edges heading back
from current node.'''
                hi0 = min([self.node_dic[edg.from_n
                                         if edg.to_n == anod.numeric_id
                                         else edg.to_n].dfs_num for edg in
                           self.back_edges[anod.numeric_id]])
            except ValueError:
                print("No back-edge found for", anod.numeric_id)
                hi0 = len(self.nodes) + 1

            try:
                ''' Look at all children's back-edges
and get one that goes to the smallest dfs-num.'''
                hi1 = min([self.node_dic[nod].hi for nod in
                           self.multi_graph_adj_list[anod.numeric_id]
                           if (self.node_dic[nod].hi is not None
                               and self.parent[nod] == anod.numeric_id)])
            except ValueError:
                print("No child with back-edge", anod.numeric_id)
                hi1 = len(self.nodes) + 1
            ''' Set hi to the highest point reached either by
children's backedges or the current node's backedges'''
            anod.hi = min([hi0, hi1])

            list_wo_hichild = [nod for nod in
                               self.multi_graph_adj_list[anod.numeric_id]
                               if (self.node_dic[nod].hi != hi1
                                   and self.parent[nod] == anod.numeric_id)]
            try:
                ''' Out of the remaining children, minus child satisfying hi1,
choose one with the earliest headed back-edge. This is for the tree-back-edges
scenario in Johnson et al. This back-edge is going to be headed a little lower
than the first and the area between the first and this new one is the edges
that participate in all cycles from one side of the tree and not
from the next. The capping backedge is set to
the second highest point and is indicative of
the commanality of cycles between the several arms
coming out of the current node.'''
                hi2 = min([self.node_dic[nod].hi for nod in
                           list_wo_hichild
                           if (self.node_dic[nod].hi is not None
                               and self.parent[nod] == anod.numeric_id)])
            except ValueError:
                print("No other child with a different back-edge"
                      " ending earliest", anod.numeric_id)
                hi2 = len(self.nodes) + 1

            anod.blist = Bracket_list()
            for nod in self.multi_graph_adj_list[anod.numeric_id]:
                if self.parent[nod] != anod.numeric_id:
                    continue
                anod.blist.concat(self.node_dic[nod].blist)

            for cap_edg in self.capping_back_edges[anod.numeric_id]:
                nod = (cap_edg.to_n if cap_edg.from_n == anod.numeric_id
                       else cap_edg.from_n)
                if self.descendant(anod.numeric_id, nod):
                    print("Nod:", nod, "is descendant of", anod.numeric_id)
                    print("Delete capping_back_edge:", cap_edg, "from",
                          str(anod.blist))
                    anod.blist.bracket_list = [edg_b for edg_b in
                                               anod.blist.bracket_list
                                               if cap_edg != edg_b]

            for back_edg in self.back_edges[anod.numeric_id]:
                nod = (back_edg.to_n if back_edg.from_n == anod.numeric_id
                       else back_edg.from_n)
                if self.descendant(anod.numeric_id, nod):
                    print("Nod:", nod, "is descendant of", anod.numeric_id)
                    print("Delete back_edge:", back_edg, "from",
                          str(anod.blist))
                    anod.blist.bracket_list = [edg_b for edg_b in
                                               anod.blist.bracket_list
                                               if back_edg != edg_b]
                    print("After removing edge:", back_edg,
                          "from", str(anod.blist))
                    if back_edg.edge_class is None:
                        back_edg.edge_class = new_edge_class()
                        print("Back-edge gets a new class:", back_edg)

            for back_edg in self.back_edges[anod.numeric_id]:
                nod = (back_edg.to_n if back_edg.from_n == anod.numeric_id
                       else back_edg.from_n)
                if self.ancestor(anod.numeric_id, nod):
                    print("Adding new bracket, back_edge:", back_edg)
                    anod.blist.push(back_edg)
                    print("All brackets:", anod.blist)

            if hi2 < hi0:
                ''' Backedges going up from current node are given less
priority if hi2 reaches higher than hi0, or the capping back-edge is the
most indicative bracket in the scenario with hi2 < hi0.
This way we now point to the common backward-point in the
graph shared by this node and all of its children.'''
                cap_edg = Edge(anod.numeric_id, self.rev_dfs_num[hi2])
                print("Capping Edge", str(cap_edg))
                self.capping_back_edges[anod.numeric_id].append(cap_edg)
                self.capping_back_edges[self.rev_dfs_num[hi2]].append(cap_edg)
                anod.blist.push(cap_edg)

            if self.parent[anod.numeric_id] is not None:
                ''' A tree-edge is same as the most-recent-equivalence-class
given to a bracket. This concept is somewhat vagueish to explain. If there is
only one bracket for a tree-edge, the tree-edge and the bracket
are cycle-equivalent and thus are in the same equivalence class.
If there is more than one, then the tree-edge's equivalence
class is the most-recent-equivalence class assigned to the top-most
bracket in the tree-edge's bracket-list. The tree-edge does not get
the same-equivalence class as the top-most-bracket but
rather this 'recent-class'. Here comes the reasoning.
There is more than one bracket in the tree-edge's bracket-list. If we
set the eq-class to the top, then we would be saying that the top-most
back-edge or bracket is cyc-equiv to the tree-edge.
But we know there is more than one bracket
and thus there is a cycle without this top-most bracket. So none of these
brackets are in the same equiv-class as the tree-edge. What remains to be
said is that tree-edges that share the same bracket-lists get the
same eq-class while each bracket in their bracket lists
get their own eq-classes.'''
                found_edg = None
                for edg in self.tree_edges[anod.numeric_id]:
                    if edg.from_n == self.parent[anod.numeric_id]:
                        found_edg = edg
                assert found_edg is not None
                print("Parent edge for", anod.numeric_id,
                      found_edg, self.parent[anod.numeric_id])
                b = anod.blist.top()
                assert b is not None
                if b.recent_size != anod.blist.size():
                    print("Need to create a new class for:", b,
                          " size", anod.blist.size())
                    b.recent_size = anod.blist.size()
                    b.recent_class = new_edge_class()
                print("Setting tree edge to bracket's top",
                      found_edg.from_n, found_edg.to_n, b, b.recent_class)
                found_edg.edge_class = b.recent_class
                if b.recent_size == 1:
                    b.edge_class = found_edg.edge_class
                    print("Passing:", b)

        for anod in reversed(self.post_order):
            try:
                top = anod.blist.top()
            except IndexError:
                top = ''
            print("For " + str(anod) + "\n  Top Bracket: {"
                  + str(top)
                  + "}\n  All Brackets: {"
                  + ", ".join([str(brack)
                               for brack in anod.blist.bracket_list])
                  + "}\n  back_edges: ["
                  + ", ".join([str(edg)
                               for edg in self.back_edges[anod.numeric_id]])
                  + "]\n  tree_edges: ["
                  + ", ".join([str(edg)
                               for edg in self.tree_edges[anod.numeric_id]])
                  + "]")

    def find_regions(self):
        '''Find regions - walk over edges in dfs order and fill
in regions for each edge.'''
        class_for_each_edges = dict()

        for edg in self.edges:
            edge_class = edg.edge_class
            class_for_each_edges[(edg.from_n, edg.to_n)] = edge_class
            class_for_each_edges[(edg.to_n, edg.from_n)] = edge_class
        self.dfs_starting_at(self.nodes[0])

        for edg in self.dir_edges:
            print("Edge visitor", edg)
            edg_from, edg_to = edg
            if (edg_from, edg_to) not in class_for_each_edges:
                edg_class = class_for_each_edges[(edg_to, edg_from)]
            else:
                edg_class = class_for_each_edges[(edg_to, edg_from)]

            if edg_class not in self.first_of_class:
                self.first_of_class[edg_class] = edg
            self.last_of_class[edg_class] = edg

        for edg in self.dir_edges:
            edg_from, edg_to = edg
            if (edg_from, edg_to) not in class_for_each_edges:
                edge_class = class_for_each_edges[(edg_to, edg_from)]
            else:
                edge_class = class_for_each_edges[(edg_to, edg_from)]

            print("Visiting edge for regions:", edg)
            if edge_class in self.last_region:
                r = self.last_region[edge_class]
                r.exit = edg
                # edg.exit = r
                print("Exit for:", r.num_id, edg)
            if (edg != self.last_of_class[edge_class]):
                r = Region()
                self.regions.append(r)
                r.entry = edg
                # edg.entry = r
                self.last_region[edge_class] = r
                print("New region for:", edge_class, edg)
            elif (self.last_of_class[edge_class]
                  == self.first_of_class[edge_class]):
                r = Region()
                self.regions.append(r)
                r.entry = r.exit = edg
                # edg.entry = edg.exit = edg
                print("New region with last == first:", edge_class, edg)

    def __str__(self):
        def to_str_adj_list(an_adj_list):
            aret = ''
            for nod in self.nodes:
                aret += str(nod.numeric_id)
                aret += ' - ['
                if nod.numeric_id in an_adj_list:
                    aret += ', '.join([str(ijk)
                                      for ijk in an_adj_list[nod.numeric_id]])
                aret += ']\n'
            return aret
        dir_ret = '\nVertices, Directed edges\n'
        dir_ret += to_str_adj_list(self.dir_adj_list)
        mult_ret = '\nVertices, Undirected edges\n'
        mult_ret += to_str_adj_list(self.multi_graph_adj_list)
        region_str = '\nRegions:\n'
        for region in self.regions:
            region_str += str(region) + '\n'

        tree_str = '\n---- TREE EDGES ----\n'
        for nod, edges in self.tree_edges.items():
            if len(edges) > 0:
                tree_str += ('Adj[' + str(nod) + ']')
                tree_str += ('\n  {' + '; '.join([str(edg) for edg in edges])
                             + '}\n')

        back_str = '\n---- BACK EDGES ----\n'
        for nod, edges in self.back_edges.items():
            if len(edges) > 0:
                back_str += ('Adj[' + str(nod) + ']')
                back_str += ('\n  {' + '; '.join([str(edg) for edg in edges])
                             + '}\n')

        return dir_ret + mult_ret + region_str + tree_str + back_str

    def dot_it(self, prefix):
        with open(prefix + '.dot', 'w') as fof:
            fof.write('Digraph G {\n')
            for nod in self.nodes:
                if nod.numeric_id in self.dir_adj_list:
                    for succ in self.dir_adj_list[nod.numeric_id]:
                        fof.write(str(nod.numeric_id) + ' -> '
                                  + str(succ) + ';\n')
            fof.write('}\n')


def run_three_nodes():
    graph_obj = Graph()
    nodes = [1, 2, 3]
    graph_obj.add_nodes_from(nodes)
    graph_obj.add_edge(graph_obj.nodes[0], graph_obj.nodes[1])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[2])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[0])
    print("three_nodes: start node:", graph_obj.nodes[0].numeric_id)
    graph_obj.undirected_dfs_starting_at(graph_obj.nodes[0])
    graph_obj.fill_dfs_nums()
    graph_obj.cycle_equiv()
    graph_obj.find_regions()
    graph_obj.dot_it('three_nodes')
    print(graph_obj)


def run_tree_loops():
    graph_obj = Graph()
    nodes = [1, 2, 3, 4, 5, 6, 7]
    graph_obj.add_nodes_from(nodes)
    graph_obj.add_edge(graph_obj.nodes[0], graph_obj.nodes[1])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[2])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[5])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[3])
    graph_obj.add_edge(graph_obj.nodes[3], graph_obj.nodes[4])
    graph_obj.add_edge(graph_obj.nodes[4], graph_obj.nodes[1])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[5])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[6])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[4])
    graph_obj.add_edge(graph_obj.nodes[5], graph_obj.nodes[6])
    graph_obj.add_edge(graph_obj.nodes[6], graph_obj.nodes[1])
    graph_obj.add_edge(graph_obj.nodes[5], graph_obj.nodes[0])
    print("tree_loops: start node:", graph_obj.nodes[0].numeric_id)
    graph_obj.undirected_dfs_starting_at(graph_obj.nodes[0])
    graph_obj.fill_dfs_nums()
    graph_obj.cycle_equiv()
    graph_obj.find_regions()
    graph_obj.dot_it('tree_loops')
    print(graph_obj)


def run_dense_dag():
    graph_obj = Graph()
    nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    graph_obj.add_nodes_from(nodes)
    graph_obj.add_edge(graph_obj.nodes[0], graph_obj.nodes[1])

    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[2])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[3])
    graph_obj.add_edge(graph_obj.nodes[3], graph_obj.nodes[4])
    graph_obj.add_edge(graph_obj.nodes[4], graph_obj.nodes[5])
    graph_obj.add_edge(graph_obj.nodes[5], graph_obj.nodes[6])
    graph_obj.add_edge(graph_obj.nodes[6], graph_obj.nodes[7])
    graph_obj.add_edge(graph_obj.nodes[7], graph_obj.nodes[8])
    graph_obj.add_edge(graph_obj.nodes[8], graph_obj.nodes[0])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[3])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[4])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[5])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[6])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[7])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[4])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[5])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[6])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[7])
    graph_obj.add_edge(graph_obj.nodes[3], graph_obj.nodes[5])
    graph_obj.add_edge(graph_obj.nodes[3], graph_obj.nodes[6])
    graph_obj.add_edge(graph_obj.nodes[3], graph_obj.nodes[7])
    graph_obj.add_edge(graph_obj.nodes[4], graph_obj.nodes[6])
    graph_obj.add_edge(graph_obj.nodes[4], graph_obj.nodes[7])
    graph_obj.add_edge(graph_obj.nodes[5], graph_obj.nodes[7])
    print("dense_dag: start node:", graph_obj.nodes[0].numeric_id)
    graph_obj.undirected_dfs_starting_at(graph_obj.nodes[0])
    graph_obj.fill_dfs_nums()
    graph_obj.cycle_equiv()
    graph_obj.find_regions()
    graph_obj.dot_it('dense_dag')
    print(graph_obj)


def run_sparse_dag():
    graph_obj = Graph()
    nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    graph_obj.add_nodes_from(nodes)
    graph_obj.add_edge(graph_obj.nodes[0], graph_obj.nodes[1])

    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[2])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[3])
    graph_obj.add_edge(graph_obj.nodes[3], graph_obj.nodes[4])
    graph_obj.add_edge(graph_obj.nodes[4], graph_obj.nodes[5])
    graph_obj.add_edge(graph_obj.nodes[5], graph_obj.nodes[6])
    graph_obj.add_edge(graph_obj.nodes[6], graph_obj.nodes[7])
    graph_obj.add_edge(graph_obj.nodes[7], graph_obj.nodes[8])
    graph_obj.add_edge(graph_obj.nodes[8], graph_obj.nodes[9])
    graph_obj.add_edge(graph_obj.nodes[9], graph_obj.nodes[10])

    graph_obj.add_edge(graph_obj.nodes[10], graph_obj.nodes[0])

    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[3])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[4])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[5])

    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[4])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[5])

    graph_obj.add_edge(graph_obj.nodes[6], graph_obj.nodes[8])
    graph_obj.add_edge(graph_obj.nodes[6], graph_obj.nodes[9])
    graph_obj.add_edge(graph_obj.nodes[7], graph_obj.nodes[9])

    graph_obj.add_edge(graph_obj.nodes[3], graph_obj.nodes[5])

    print("sparse_dag: start node:", graph_obj.nodes[0].numeric_id)
    graph_obj.undirected_dfs_starting_at(graph_obj.nodes[0])
    graph_obj.fill_dfs_nums()
    graph_obj.cycle_equiv()
    graph_obj.find_regions()
    graph_obj.dot_it('sparse_dag')
    print(graph_obj)


def run_simple():
    graph_obj = Graph()
    nodes = [1, 2, 3, 4]
    graph_obj.add_nodes_from(nodes)
    graph_obj.add_edge(graph_obj.nodes[0], graph_obj.nodes[1])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[2])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[3])
    graph_obj.add_edge(graph_obj.nodes[3], graph_obj.nodes[0])

    print("simple: start node:", graph_obj.nodes[0].numeric_id)
    graph_obj.undirected_dfs_starting_at(graph_obj.nodes[0])
    graph_obj.fill_dfs_nums()
    graph_obj.cycle_equiv()
    graph_obj.find_regions()
    graph_obj.dot_it('simple')
    print(graph_obj)


def run_case1():
    graph_obj = Graph()
    nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    graph_obj.add_nodes_from(nodes)
    graph_obj.add_edge(graph_obj.nodes[0], graph_obj.nodes[1])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[2])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[3])
    graph_obj.add_edge(graph_obj.nodes[3], graph_obj.nodes[4])
    graph_obj.add_edge(graph_obj.nodes[4], graph_obj.nodes[5])
    graph_obj.add_edge(graph_obj.nodes[5], graph_obj.nodes[6])
    graph_obj.add_edge(graph_obj.nodes[6], graph_obj.nodes[7])
    graph_obj.add_edge(graph_obj.nodes[7], graph_obj.nodes[8])
    graph_obj.add_edge(graph_obj.nodes[8], graph_obj.nodes[9])
    graph_obj.add_edge(graph_obj.nodes[9], graph_obj.nodes[0])
    graph_obj.add_edge(graph_obj.nodes[8], graph_obj.nodes[6])
    graph_obj.add_edge(graph_obj.nodes[5], graph_obj.nodes[1])
    graph_obj.add_edge(graph_obj.nodes[4], graph_obj.nodes[2])

    print("case 1: start node:", graph_obj.nodes[0].numeric_id)
    graph_obj.undirected_dfs_starting_at(graph_obj.nodes[0])
    graph_obj.fill_dfs_nums()
    graph_obj.cycle_equiv()
    graph_obj.dot_it('case1')
    graph_obj.find_regions()
    graph_obj.slow_cycle_equiv()
    print(graph_obj)


def run_case2():
    graph_obj = Graph()
    nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    graph_obj.add_nodes_from(nodes)
    graph_obj.add_edge(graph_obj.nodes[0], graph_obj.nodes[1])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[2])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[3])
    graph_obj.add_edge(graph_obj.nodes[3], graph_obj.nodes[4])
    graph_obj.add_edge(graph_obj.nodes[4], graph_obj.nodes[5])
    graph_obj.add_edge(graph_obj.nodes[5], graph_obj.nodes[6])
    graph_obj.add_edge(graph_obj.nodes[6], graph_obj.nodes[7])
    graph_obj.add_edge(graph_obj.nodes[7], graph_obj.nodes[8])
    graph_obj.add_edge(graph_obj.nodes[8], graph_obj.nodes[0])
    graph_obj.add_edge(graph_obj.nodes[7], graph_obj.nodes[2])
    graph_obj.add_edge(graph_obj.nodes[6], graph_obj.nodes[1])
    graph_obj.add_edge(graph_obj.nodes[5], graph_obj.nodes[3])

    print("case 2: start node:", graph_obj.nodes[0].numeric_id)
    graph_obj.undirected_dfs_starting_at(graph_obj.nodes[0])
    graph_obj.fill_dfs_nums()
    graph_obj.cycle_equiv()
    graph_obj.find_regions()
    graph_obj.dot_it('case2')
    graph_obj.slow_cycle_equiv()
    print(graph_obj)


def run_case3():
    graph_obj = Graph()
    nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    graph_obj.add_nodes_from(nodes)
    graph_obj.add_edge(graph_obj.nodes[0], graph_obj.nodes[1])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[2])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[3])
    graph_obj.add_edge(graph_obj.nodes[3], graph_obj.nodes[4])
    graph_obj.add_edge(graph_obj.nodes[4], graph_obj.nodes[5])
    graph_obj.add_edge(graph_obj.nodes[5], graph_obj.nodes[6])
    graph_obj.add_edge(graph_obj.nodes[5], graph_obj.nodes[7])
    graph_obj.add_edge(graph_obj.nodes[6], graph_obj.nodes[8])
    graph_obj.add_edge(graph_obj.nodes[7], graph_obj.nodes[9])
    graph_obj.add_edge(graph_obj.nodes[9], graph_obj.nodes[0])
    graph_obj.add_edge(graph_obj.nodes[8], graph_obj.nodes[1])
    graph_obj.add_edge(graph_obj.nodes[6], graph_obj.nodes[3])
    graph_obj.add_edge(graph_obj.nodes[7], graph_obj.nodes[2])

    print("case 3: Start node:", graph_obj.nodes[0].numeric_id)
    graph_obj.undirected_dfs_starting_at(graph_obj.nodes[0])
    graph_obj.fill_dfs_nums()
    graph_obj.cycle_equiv()
    graph_obj.find_regions()
    graph_obj.dot_it('case3')
    graph_obj.slow_cycle_equiv()
    print(graph_obj)


def run_dag1():
    graph_obj = Graph()
    nodes = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    graph_obj.add_nodes_from(nodes)
    graph_obj.add_edge(graph_obj.nodes[0], graph_obj.nodes[1])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[2])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[3])
    graph_obj.add_edge(graph_obj.nodes[3], graph_obj.nodes[4])
    graph_obj.add_edge(graph_obj.nodes[4], graph_obj.nodes[5])
    graph_obj.add_edge(graph_obj.nodes[5], graph_obj.nodes[6])
    graph_obj.add_edge(graph_obj.nodes[6], graph_obj.nodes[7])
    graph_obj.add_edge(graph_obj.nodes[7], graph_obj.nodes[8])
    graph_obj.add_edge(graph_obj.nodes[8], graph_obj.nodes[9])
    graph_obj.add_edge(graph_obj.nodes[9], graph_obj.nodes[0])
    graph_obj.add_edge(graph_obj.nodes[6], graph_obj.nodes[8])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[5])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[4])

    print("dag 1: start node:", graph_obj.nodes[0].numeric_id)
    graph_obj.undirected_dfs_starting_at(graph_obj.nodes[0])
    graph_obj.fill_dfs_nums()
    graph_obj.cycle_equiv()
    graph_obj.dot_it('dag1')
    graph_obj.find_regions()
    graph_obj.slow_cycle_equiv()
    print(graph_obj)


if __name__ == '__main__':
    new_node_class = count().__next__
    run_simple()
    new_node_class = count().__next__
    run_case1()
    new_node_class = count().__next__
    run_case2()
    new_node_class = count().__next__
    run_case3()
    new_node_class = count().__next__
    run_sparse_dag()
    new_node_class = count().__next__
    run_dag1()
