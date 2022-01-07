import json
from src.graph import DiGraph
from src.players.Agent import Agent
from src.players.Pokémon import Pokémon


class main():
    def __init__(self, g: DiGraph = DiGraph()) -> None:
        self.graph = g
        self.ListAgens = []
        self.pokemons = []

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

    def load_agents(self, file_name) -> bool:
        try:
            sum_nodes = self.graph.v_size
            date = json.loads(file_name)
            AgentList = date['Agents']
            pos_ag = round(sum_nodes/len(AgentList))
            for ag in AgentList:
                place = pos_ag
                agen = ag['Agent']
                temppos = agen['pos'].split(",")
                x = float(temppos[0])
                y = float(temppos[1])
                z = 0.0
                pos = (x, y, z)
                is_alredy_exist = False
                # for loop hos run al the agents are all redy exzist
                for e in self.ListAgens:
                    # if the agent all redy exsit we need to replace is valuse
                    if e.id == agen['id']:
                        e.value = agen['value']
                        e.src = agen['src']
                        e.dest = agen['dest']
                        e.speed = agen['speed']
                        e.pos = self.graph.getnode(sum_nodes/2).getpos
                        is_alredy_exist = True
                        break
                # if the agent not exzist on the kisr add
                if is_alredy_exist == False:
                    agent = Agent(agen['id'], agen['value'], agen['src'], agen['dest'], agen['speed'], self.graph.getnode(place).getpos)
                    self.ListAgens.append(agent)
                place = place+pos_ag
            return True
        except:
            return False

    def load_pokemon(self, file_name):
        try:
            date = json.loads(file_name)
            PokemonsList = date['Pokemons']
            for p in PokemonsList:
                pok = p['Pokemon']
                tempos = pok['pos'].split(",")
                x = float(tempos[0])
                y = float(tempos[1])
                z=0.0
                pos = (x, y, z)
                node_pos = self.locaiton_pokemon(pos)
                pokemon = Pokémon(pok['value'], pok['type'], pos, node_pos)
                self.pokemons.append(pokemon)
            return True
        except:
            return False

    # we create a Straight equation to finde the src node of the pokemon
    def locaiton_pokemon(self, pos: tuple):
        # going throw all the nodes on the graph
        for n in self.graph.get_list_nodes:
            # going throw on al the nodes the node is pointed at to create a edge
            for e in self.graph.all_out_edges_of_node(n):
                temp_src = n.getpos
                temp_dest = e.getpos
                Incline = (temp_src[1] - temp_dest[1]) / (temp_src[0] - temp_dest[0])
                virebal = temp_src[1] - (temp_src[0] * Incline)
                if (pos[1] == Incline * pos[0] + virebal):
                    return n

