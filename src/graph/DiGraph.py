from src.graph.Edge import Edge
from src.graph.GraphInterface import GraphInterface
from src.graph.Node import Node



class DiGraph(GraphInterface):
    # init graph
    def __init__(self) -> None:
        super().__init__()
        self.nodes = {}
        self.edges = {}
        self.SizeOfEdge = 0
        self.list_nodes = []
        self.list_edges = []
        self.mc = 0

    # returns the size of the nodes
    def v_size(self) -> int:
        return len(self.nodes)

    # returns the size of the edges
    def e_size(self) -> int:
        return self.SizeOfEdge

    # returns the nodes as a dictionary
    def get_all_v(self) -> dict:
        return self.nodes

    # returns all the nodes in a list
    def get_list_nodes(self) -> list:
        return self.list_nodes

    # returns all the edges in a list
    def get_list_edges(self) -> list:
        return self.list_edges

    # returns all the nodes that point to the given node
    def all_in_edges_of_node(self, id1: int) -> dict:
        ans = {}
        # loop all the nodes (the key value in edge represents the src node)
        for s in self.edges.keys():
            # loop all the dest nodes
            for d in self.edges[s].keys():
                if d == id1:
                    if s not in ans.keys():
                        ans[s] = self.edges[s][id1]

        return ans

    # return all the nodes which the given node is pointing at
    def all_out_edges_of_node(self, id1: int) -> dict:
        return self.edges[id1]

    # return the number of the actions that were made on the graph
    def get_mc(self) -> int:
        return self.mc

    # add edge to graph
    # id1 - src , id2 - dst
    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        # if id1 or id2 do not exist as nodes in the graph
        if id1 not in self.nodes.keys() or id2 not in self.nodes.keys():
            return False
        edge = Edge(id1, id2, weight)
        if id1 in self.edges.keys():
            # if the edge already exist in the graph
            if id2 in self.edges[id1].keys():
                return False
            else:
                self.edges[id1][id2] = edge
                self.SizeOfEdge += 1
        else:
            edge = Edge(id1, id2, weight)
            # we have created two dictionaries, the key valur of the first dict is the src node, the value us the second dict
            # in the second dict the key is the dest node and the value is all the edge perimeters
            self.edges[id1] = {id2: edge}
            self.SizeOfEdge += 1
        # save into a list all the perimeters we need to the save file
        self.list_edges.append({'src': id1, 'dest': id2, 'w': weight})
        self.mc = self.mc + 1
        return True

    # add node to the graph
    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        # if the node is already exist
        if node_id in self.nodes.keys():
            return False
        else:
            self.nodes[node_id] = Node(node_id, pos)

        self.list_nodes.append({'id': node_id, 'pos': pos})
        self.mc = self.mc + 1
        return True

    # return node by his id
    def getnode(self, id: int) -> Node:
        return self.nodes[id]

    # remove node from graph
    def remove_node(self, node_id: int) -> bool:
        if node_id not in self.nodes.keys():
            return False
        else:
            # remove from nodes
            self.nodes.pop(node_id)
        # remove all the edges that node is their src
        if node_id in self.edges.keys():
            self.edges.pop(node_id)
        for i in self.list_edges:
            if i['src'] == node_id or i['dest'] == node_id:
                self.list_edges.remove(i)
                self.SizeOfEdge -= 1

        self.mc = self.mc + 1
        return True

    # remove edge from graph
    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        # if the node id does not exist
        if node_id1 not in self.edges.keys():
            return False
        # if id1 exist in src but id2 does not exist in dest
        if node_id1 in self.edges.keys() and node_id2 not in self.edges[node_id1].keys():
            return False
        else:
            self.edges[node_id1].pop(node_id2)
            # if node id1 = src and node id2 = dest, delete it
            for i in self.list_edges:
                # delete in case one of the nodes was deleted
                if i['src'] == node_id1 and i['dest'] == node_id2:
                    self.list_edges.remove(i)
                    break
            # self.list_edges[node_id1].pop(node_id2)
            self.SizeOfEdge -= 1
        self.mc = self.mc + 1
        return True

    # return edge by src and dest
    def get_edge(self, src: int, dest: int):
        return self.edges[src][dest]