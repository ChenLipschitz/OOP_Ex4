import json
from src.graph import GraphAlgo, Node, Edge, DiGraph
from src.players import Pokémon, Agent
from src.client_python import client

class myGame:
    def __init__(self, graph: DiGraph):
        # a Pokémons list
        self.poks = {}
        self.agents = {}
        # default port
        PORT = 6666
        # host server (default localhost 127.0.0.1)
        HOST = '127.0.0.1'
        self.client = client()
        self.client.start_connection(HOST, PORT)
        self.client.add_agent("{\"id\":9}")
        self.client.add_agent("{\"id\":1}")
        self.client.add_agent("{\"id\":2}")
        self.client.add_agent("{\"id\":3}")

    def load_json(self):

    def addAgent(self):

    def