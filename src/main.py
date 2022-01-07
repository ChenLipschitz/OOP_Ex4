import json

from src.client_python import client
from src.graph import DiGraph
from src.players.Agent import Agent
from src.players.Pokémon import Pokémon


class main():
    def __init__(self, g: DiGraph = DiGraph()) -> None:

        self.graph = g
        self.ListAgens = []
        self.pokemons = []

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

    def load_agents(self, file_name) -> bool:
        try:
            date = json.loads(file_name)
            AgentList = date['Agents']
            for ag in AgentList:
                agen = ag['Agent']
                temppos = agen['pos'].split(",")
                x = float(temppos[0])
                y = float(temppos[1])
                pos = (x, y, 0.0)
                is_alredy_exist = False
                # for loop hos run al the agents are all redy exzist
                for e in self.ListAgens:
                    # if the agent all redy exsit we need to replace is valuse
                    if e.id == agen['id']:
                        e.value = agen['value']
                        e.src = agen['src']
                        e.dest = agen['dest']
                        e.speed = agen['speed']
                        e.pos = pos
                        is_alredy_exist = True
                        break
                #if the agent not exzist on the kisr add
                if is_alredy_exist == False:
                    agent = Agent(agen['id'], agen['value'], agen['src'], agen['dest'], agen['speed'], pos)
                    self.ListAgens.append(agent)
            return True
        except:
            return False

    def load_pokemon(self, file_name):
        try:
            date = json.loads(file_name)
            PokemonsList = date['Pokemons']
            self.pokemons.clear()
            for p in PokemonsList:
                pok = p['Pokemon']
                tempos = pok['pos'].split(",")
                x = float(tempos[0])
                y = float(tempos[1])
                pos = (x, y, 0.0)
                pokemon = Pokémon(pok['value'], pok['type'], pos)
                self.pokemons.append(pokemon)
            return True
        except:
            return False


    ####### step 2
    # initial the date to the gui
    ######## step 3
    # runing the game
    ####### step 4
    # ruining on a loop of the condisons of the game
    ###### step 5
    # alocete to the agents by disatnce and chake if the pokemin was caputer and update the date
    ####### step 6
    # chake how much time the agent need to sleep befor his moving agin
    ## step 7
    #### moving the aigent by the permeters
