import json
from src.graph import DiGraph
from src.graph.Node import Node
from src.players.Agent import Agent
from src.players.Pokémon import Pokémon


class main():
    def __init__(self, g: DiGraph = DiGraph()) -> None:
        self.graph = g
        self.Agens = []
        self.pokemons = []

    # returns the pokemons list
    def ListPokemons(self):
        return self.pokemons

    # return the agents list
    def ListAgens(self):
        return self.Agens

    # loads graph from the json file
    def load_graph(self, file_name: str) -> bool:
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

    # load agents to the game from the json file
    def load_agents(self, file_name) -> bool:
        try:
            sum_nodes = self.graph.v_size
            date = json.loads(file_name)
            AgentList = date['Agents']
            pos_ag = round(sum_nodes / len(AgentList))
            for ag in AgentList:
                place = pos_ag
                # agen represents agent
                agen = ag['Agent']
                temp_pos = agen['pos'].split(",")
                x = float(temp_pos[0])
                y = float(temp_pos[1])
                z = 0.0
                pos = (x, y, z)
                is_already_exist = False
                # loop all the agents who are already exist
                for e in self.Agens:
                    # if the agent is already exist we need to replace it's value
                    if e.id == agen['id']:
                        e.value = agen['value']
                        e.src = agen['src']
                        e.dest = agen['dest']
                        e.speed = agen['speed']
                        e.pos = self.graph.getnode(sum_nodes / 2).getpos
                        is_already_exist = True
                        break
                # if the agent doesn't exist on the coordinate, add
                if not is_already_exist:
                    agent = Agent(agen['id'], agen['value'], agen['src'], agen['dest'], agen['speed'],
                                  self.graph.getnode(place).getpos)
                    self.Agens.append(agent)
                place = place + pos_ag
            return True
        except:
            return False

    # load pokemons for the game from the json file
    def load_pokemon(self, file_name):
        try:
            date = json.loads(file_name)
            PokemonsList = date['Pokemons']
            for p in PokemonsList:
                pok = p['Pokemon']
                tempos = pok['pos'].split(",")
                x = float(tempos[0])
                y = float(tempos[1])
                z = 0.0
                pos = (x, y, z)
                node_pos = self.location_pokemon(pos)
                pokemon = Pokémon(pok['value'], pok['type'], pos, node_pos)
                self.pokemons.append(pokemon)
            return True
        except:
            return False

    # by using the linear equation we fined the pokemon's src node
    def location_pokemon(self, pos: tuple) -> (Node, Node):
        # loop all nodes on the graph
        for n in self.graph.get_list_nodes:
            # going through all the nodes the node is pointed at to create a edge
            for e in self.graph.all_out_edges_of_node(n):
                temp_src = n.getpos
                temp_dest = e.getpos
                Incline = (temp_src[1] - temp_dest[1]) / (temp_src[0] - temp_dest[0])
                variable = temp_src[1] - (temp_src[0] * Incline)
                if pos[1] == Incline * pos[0] + variable:
                    # n -> src , e -> dest
                    return n, e

    # finds the shortest path from one node to another
    def shortest_path(self, id1: int, id2: int) -> (float, list):
        ans = []
        ans_dist = self.shortest_path_dist(id1, id2)
        if ans_dist == -1:
            return None
        if id1 == id2:
            return 0, []
        self.reset()
        self.Dijkstra(self.graph.getnode(id1), self.graph.getnode(id2))
        node_src = self.graph.getnode(id1)
        node_dest = self.graph.getnode(id2)
        back = []
        temp = node_dest
        while temp.gettag() != -1:
            back.append(temp)
            temp = self.graph.getnode(temp.gettag())

        ans.append(node_src.key)

        for i in range(len(back) - 1, -1, -1):
            ans.append(back[i].key)
        self.reset()
        return ans_dist, ans

    # auxiliary method, calculates distance for the shortest_path method
    def shortest_path_dist(self, src: int, dest: int) -> float:
        self.reset()
        ans = self.Dijkstra(self.graph.get_all_v().get(src), self.graph.get_all_v().get(dest))
        self.reset()
        if ans == 1000000:
            return -1
        return ans

    # resets nodes
    def reset(self):
        for n in self.graph.nodes.values():
            n.setinfo("White")
            n.settag(-1)
            n.setweight(float('inf'))

    # represents the Dijkstra algorithm for finding the shortest paths between nodes in a graph
    def Dijkstra(self, src: Node, dest: Node):
        most_short = float('inf')
        queue = []
        src.setWeight(0.0)
        queue.append(src)
        while len(queue) != 0:
            queue.sort()
            temp = queue.pop(0)
            if temp.getinfo() == "White":
                temp.setinfo("Black")
                if temp.getkey() == dest.getKey():
                    return temp.getweight()
                for edg in self.graph.all_out_edges_of_node(temp.getkey()):
                    temped = self.graph.edges[temp.getkey()][edg]
                    tempno = self.graph.getnode(edg)
                    if tempno.info == "White":
                        if temp.getweight() + temped.getweight() < tempno.getweight():
                            tempno.setweight(temp.getweight() + temped.getweight())
                            tempno.settag(temp.getkey())
                        queue.append(tempno)
        return most_short

    def threeShortestPath(self, id1: Node, id2: Node, id3: Node) -> (float, list):
        """
        calculate shortest path between 3 nodes
        @return: weight, path
        """
        if id1.getKey() in self.graph.nodes.keys() and id2.getKey() \
                in self.graph.nodes.keys() and id3.getKey() in self.graph.nodes.keys():
            w, ans = self.shortest_path(id1.getKey(), id2.getKey())
            w1, ans1 = self.shortest_path(id2.getKey(), id3.getKey())
            ans1.pop(0)
            w += w1
            ans.extend(ans1)
            return w, ans
        else:
            return "the node does not exist"
