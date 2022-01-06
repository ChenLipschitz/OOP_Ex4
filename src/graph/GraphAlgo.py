import json
from GraphInterface import GraphInterface
from GraphAlgoInterface import GraphAlgoInterface
from DiGraph import DiGraph
from Node import Node
from typing import List
import pygame


class GraphAlgo(GraphAlgoInterface):

    def __init__(self, g: DiGraph = DiGraph()) -> None:
        self.graph = g

    def get_graph(self) -> GraphInterface:
        return self.graph

    # load json file
    def load_from_json(self, file_name: str) -> bool:
        with open(file_name, 'r') as f:
            data = json.load(f)
        l_nodes = data["Nodes"]
        l_edges = data["Edges"]
        for dic_nodes in l_nodes:
            pos = dic_nodes["pos"].split(',')
            # at first save id, second save the position
            self.graph.add_node(dic_nodes['id'], (float(pos[0]), float(pos[1]), float(pos[2])))
        for dic_edges in l_edges:
            self.graph.add_edge(dic_edges['src'], dic_edges['dest'], dic_edges['w'])
        return True

    # save to json file
    def save_to_json(self, file_name: str) -> bool:
        graph_dic = {'Nodes': self.graph.get_list_nodes(), 'Edges': self.graph.get_list_edges()}
        with open(file_name, 'w') as json_file:
            json.dump(graph_dic, json_file)
        return True

    def Dijkstra(self, src: Node, dest: Node):
        mostshort = float('inf')
        queue = []
        src.setweight(0.0)
        queue.append(src)
        while len(queue) != 0:
            queue.sort()
            temp = queue.pop(0)
            # white == was not visited
            if temp.getinfo() == "White":
                # Black == was visited
                temp.setinfo("Black")
                # if all the nodes were visited
                if temp.getkey() == dest.getkey():
                    return temp.getweight()
                for edg in self.graph.all_out_edges_of_node(temp.getkey()):
                    temped = self.graph.edges[temp.getkey()][edg]
                    tempno = self.graph.getnode(edg)
                    if tempno.info == "White":
                        if temp.getweight() + temped.getweight() < tempno.getweight():
                            tempno.setweight(temp.getweight() + temped.getweight())
                            tempno.settag(temp.getkey())
                        queue.append(tempno)
        return mostshort

    # reset after executing one of the algorithms
    def reset(self):
        for n in self.graph.nodes.values():
            n.setinfo("White")
            n.settag(-1)
            n.setweight(float('inf'))

    # returns a list of all the node which were visited and the distance of all nodes list
    def shortest_path(self, id1: int, id2: int) -> (float, list):
        ans = []
        ansdist = self.shortest_path_dist(id1, id2)
        # -1 -> there is no path between id1 and id2
        if ansdist == -1:
            return None
        if id1 == id2:
            return (0, [])
        self.reset()
        # search for the shortest path by changing the tags
        self.Dijkstra(self.graph.getnode(id1), self.graph.getnode(id2))
        nodesrc = self.graph.getnode(id1)
        nodedest = self.graph.getnode(id2)
        back = []
        temp = nodedest
        # loop as long as the algo didnt get to the start node
        while temp.gettag() != -1:
            back.append(temp)
            temp = self.graph.getnode(temp.gettag())

        ans.append(nodesrc.key)

        # enters all the path answers to a list
        for i in range(len(back)-1, -1, -1):
            ans.append(back[i].key)
        self.reset()
        return (ansdist, ans)

    def shortest_path_dist(self, src: int, dest: int) -> float:
        self.reset()
        ans = self.Dijkstra(self.graph.get_all_v().get(src), self.graph.get_all_v().get(dest))
        self.reset()
        if ans == float('inf'):
            return -1
        return ans

    # returns a list of the nodes id's in the path, and the overall distance
    def TSP(self, node_lst: List[int]) -> (List[int], float):
        list_ans = []
        p = []
        sec = []
        ans = 0
        for n in node_lst:
            sec.append(n)
        firstvalue = sec.pop(0)
        while len(sec) != 0:
            best = float('inf')
            for nod in sec:
                temp = self.shortest_path_dist(firstvalue, nod)
                if temp < best:
                    best = temp
                    Ntemp = nod
            p = self.shortest_path(firstvalue, Ntemp)
            p = p[1]
            for i in range(1, len(p), 1):
                list_ans.append(p[i])
            sec.remove(Ntemp)
            firstvalue = Ntemp
            # computes the distance between all vertices
        for a in range(0, len(list_ans)-1, 1):
            temp = self.graph.get_edge(list_ans[a],list_ans[a+1]).getweight()
            ans = ans+temp
        return list_ans,ans

    # Finds the node that has the shortest distance to it's farthest node.
    # returns the nodes id, min-maximum distance
    def centerPoint(self) -> (int, float):
        c = 0
        for_d = Node(-1, (0, 0, 0))
        ans_dist = float('inf')
        for nod in self.graph.nodes.values():
            self.reset()
            # creates path between each node in the graph
            self.Dijkstra(nod, for_d)
            temp = float('-inf')
            for tempn in self.graph.nodes.values():
                # finds the node with the highest weight
                if tempn.getweight() > temp:
                    temp = tempn.getweight()
            if temp < ans_dist:
                ans_dist = temp
                c = nod.key
        return c, ans_dist

    # shows the graph as GUI, (x,y) coordinates, z->height =0
    # def plot_graph(self) -> None:
