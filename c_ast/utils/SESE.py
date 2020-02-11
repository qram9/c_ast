from itertools import count
# import pudb

new_node_class = count().__next__
new_edge_class = count(-20).__next__


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
    __slots__ = ('edge_class', 'recent_size',
                 'recent_class', 'ord_pair',
                 'from_n', 'to_n')

    def __init__(self, from_n, to_n):
        self.edge_class, self.recent_size, self.recent_class = None, 0, 0
        self.ord_pair = (from_n, to_n)
        sort_from_n = from_n
        sort_to_n = to_n
        if sort_from_n > sort_to_n:
            tmp_n = sort_from_n
            sort_from_n = sort_to_n
            sort_to_n = tmp_n
        self.from_n = sort_from_n
        self.to_n = sort_to_n

    def __str__(self):
        return ("(" + str(self.from_n) + ", " + str(self.to_n) + ")" + ", "
                + "edge_class: " + str(self.edge_class))


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
        print("Need to concat:")
        print("  " + ", ".join([str(brack) for brack in self.bracket_list]))
        print("  " + ", ".join([str(brack) for brack in bl2.bracket_list]))
        self.bracket_list.extend(bl2.bracket_list)

    def __str__(self):
        ret = ''
        ret += ', '.join([str(a) for a in (self.bracket_list)])
        return ret


class Graph:
    ''' Using the Parent based DFS algo to do undirected graph DFS.'''
    __slots__ = ('start', 'nodes', 'node_dic', 'num_edges',
                 'parent', 'dfs_num', 'finish_num',
                 'start_time', 'dfs_time', 'pre_number',
                 'dir_adj_list', 'multi_graph_adj_list',
                 'post_order', 'tree_edges', 'back_edges',
                 'capping_back_edges', 'rev_dfs_num')

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

    def V(self):
        return len(self.nodes)

    def E(self):
        return len(self.num_edges)

    def add_node(self, anod):
        self.nodes.append(anod)
        self.dir_adj_list[anod.numeric_id] = []
        self.multi_graph_adj_list[anod.numeric_id] = []
        self.node_dic[anod.numeric_id] = anod

    def add_nodes_from(self, nodes):
        self.nodes = []
        self.node_dic = {}
        for k in nodes:
            anod = Node(k)
            anod.numeric_id = new_node_class()
            self.add_node(anod)
            self.back_edges[anod.numeric_id] = list()
            self.tree_edges[anod.numeric_id] = list()
            self.capping_back_edges[anod.numeric_id] = list()

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
        print("Visit", anod)
        for succ_nod in self.multi_graph_adj_list[anod]:
            if succ_nod not in self.parent:
                print("New treeedge", anod, succ_nod)
                edg = Edge(anod, succ_nod)
                self.tree_edges[anod].append(edg)
                self.tree_edges[succ_nod].append(edg)
                self.parent[succ_nod] = anod
                self.undirected_dfs_visit(succ_nod)
            else:
                dont_add = False
                for edg in self.tree_edges[succ_nod]:
                    if (edg.to_n == anod or edg.from_n == anod):
                        dont_add = True
                        break
                if dont_add is True:
                    print("Existing tree-edge ", anod, succ_nod)
                    continue

                for edg in self.back_edges[succ_nod]:
                    if (edg.to_n == anod or edg.from_n == anod):
                        dont_add = True
                        break
                if dont_add is True:
                    print("Existing back-edge", anod, succ_nod)
                    continue
                print("New backedge", anod, succ_nod)
                edg = Edge(anod, succ_nod)
                self.back_edges[succ_nod].append(edg)
                self.back_edges[anod].append(edg)
        self.post_order.append(self.node_dic[anod])
        self.dfs_time += 1
        print("Finish", anod)
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

    def cycle_equiv(self):
        for rev_df in range(self.pre_number - 1, 0, -1):
            anod = self.node_dic[self.rev_dfs_num[rev_df]]
            try:
                ''' Find the earliest headed among all backedges from current
node.'''
                hi0 = min([self.node_dic[edg.from_n
                                         if edg.to_n == anod.numeric_id
                                         else edg.to_n].dfs_num for edg in
                           self.back_edges[anod.numeric_id]])
            except ValueError:
                print("No backedge found for", anod.numeric_id)
                hi0 = len(self.nodes) + 1

            try:
                ''' Find a child's backedge and get one that is earliest
headed.'''
                hi1 = min([self.node_dic[nod].hi for nod in
                           self.multi_graph_adj_list[anod.numeric_id]
                           if (self.node_dic[nod].hi is not None
                               and self.parent[nod] == anod.numeric_id)])
            except ValueError:
                print("No child with backedge", anod.numeric_id)
                hi1 = len(self.nodes) + 1

            anod.hi = min([hi0, hi1])

            list_wo_hichild = [nod for nod in
                               self.multi_graph_adj_list[anod.numeric_id]
                               if (self.node_dic[nod].hi != hi1
                                   and self.parent[nod] == anod.numeric_id)]
            try:
                ''' Out of the remaining children, minus child satisfying hi1,
choose one with the earliest headed backedge. This is for the tree-backedges
scenario in Johnson et al.'''
                hi2 = min([self.node_dic[nod].hi for nod in
                           list_wo_hichild
                           if (self.node_dic[nod].hi is not None
                               and self.parent[nod] == anod.numeric_id)])
            except ValueError:
                print("No other child with a different backedge"
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
                    anod.blist.bracket_list = [edg_b for edg_b in
                                               anod.blist.bracket_list
                                               if cap_edg != edg_b]

            for back_edg in self.back_edges[anod.numeric_id]:
                nod = (back_edg.to_n if back_edg.from_n == anod.numeric_id
                       else back_edg.from_n)
                if self.descendant(anod.numeric_id, nod):
                    print("For ", anod.numeric_id)
                    print(" ", anod.blist)
                    anod.blist.bracket_list = [edg_b for edg_b in
                                               anod.blist.bracket_list
                                               if back_edg != edg_b]
                    print("After fixing ", anod.blist)
                    print(" ", anod.blist)
                    if back_edg.edge_class is None:
                        back_edg.edge_class = new_edge_class()
            print("Before", anod.blist)
            for back_edg in self.back_edges[anod.numeric_id]:
                nod = (back_edg.to_n if back_edg.from_n == anod.numeric_id
                       else back_edg.from_n)
                if self.ancestor(anod.numeric_id, nod):
                    print("Ancestor: anod.numeric_id",
                          anod.numeric_id, " to ", nod)
                    anod.blist.push(back_edg)
            print("After", anod.blist)

            if hi2 < hi0:
                print("Need to add a capping backedge")
                cap_edg = Edge(anod.numeric_id, self.rev_dfs_num[hi2])
                self.capping_back_edges[anod.numeric_id] = cap_edg
                self.capping_back_edges[self.rev_dfs_num[hi2]] = cap_edg
                anod.blist.push(cap_edg)

            if self.parent[anod.numeric_id] is not None:
                found_edg = None
                for edg in self.tree_edges[self.parent[anod.numeric_id]]:
                    if ((edg.from_n == self.parent[anod.numeric_id] and
                         edg.to_n == anod.numeric_id) or
                        (edg.to_n == self.parent[anod.numeric_id] and
                         edg.from_n == anod.numeric_id)):
                        found_edg = edg
                        break
                assert found_edg is not None
                b = anod.blist.top()
                assert b is not None
                if b.recent_size != anod.blist.size():
                    b.recent_size = anod.blist.size()
                    b.recent_class = new_edge_class()
                found_edg.edge_class = b.recent_class
                if b.recent_size == 1:
                    b.edge_class = found_edg.edge_class
        for anod in reversed(self.post_order):
            print("For " + str(anod) + "\n  Brackets: {" +
                  ", ".join(str(brac) for brac in
                            reversed(anod.blist.bracket_list))
                  + "}\n  back_edges: ["
                  + ", ".join([str(edg)
                               for edg in self.back_edges[anod.numeric_id]])
                  + "]\n  tree_edges: ["
                  + ", ".join([str(edg)
                               for edg in self.tree_edges[anod.numeric_id]])
                  + "]")

    def descendant(self, u, v):
        if (self.start_time[u] < self.start_time[v] and
           self.finish_num[u] > self.finish_num[v]):
            return True
        return False

    def ancestor(self, u, v):
        if (self.start_time[v] < self.start_time[u] and
           self.finish_num[v] > self.finish_num[u]):
            # pudb.set_trace()
            return True
        return False

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
        return dir_ret + mult_ret


if __name__ == '__main__':
    graph_obj = Graph()
    nodes = [1, 2, 3, 4, 5, 6, 7, 8]
    graph_obj.add_nodes_from(nodes)
    graph_obj.add_edge(graph_obj.nodes[0], graph_obj.nodes[1])
    graph_obj.add_edge(graph_obj.nodes[1], graph_obj.nodes[2])
    graph_obj.add_edge(graph_obj.nodes[2], graph_obj.nodes[3])
    graph_obj.add_edge(graph_obj.nodes[3], graph_obj.nodes[4])
    graph_obj.add_edge(graph_obj.nodes[4], graph_obj.nodes[5])
    graph_obj.add_edge(graph_obj.nodes[4], graph_obj.nodes[2])
    graph_obj.add_edge(graph_obj.nodes[5], graph_obj.nodes[6])
    graph_obj.add_edge(graph_obj.nodes[5], graph_obj.nodes[1])
    graph_obj.add_edge(graph_obj.nodes[6], graph_obj.nodes[7])
    graph_obj.add_edge(graph_obj.nodes[6], graph_obj.nodes[4])
    graph_obj.add_edge(graph_obj.nodes[7], graph_obj.nodes[0])

    print(graph_obj)
    print("Start node:", graph_obj.nodes[0].numeric_id)
    graph_obj.undirected_dfs_starting_at(graph_obj.nodes[0])
    graph_obj.fill_dfs_nums()
    graph_obj.cycle_equiv()
