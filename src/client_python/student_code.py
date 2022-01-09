"""
part of the code was taken from AchiyaZigi, who wrote the task
OOP - Ex4
GUI for python client to communicate with the server and "play the game!"
"""
from math import inf
from types import SimpleNamespace
from client import Client
import json
import sys
from pygame import gfxdraw
import pygame
from pygame import *
import time
from src.GUI.Button import Button
from src.main import main
from src.players.Agent import Agent
from src.players.Pokémon import Pokémon
from src.graph.DiGraph import DiGraph

# init pygame
WIDTH, HEIGHT = 800, 600

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'

pygame.init()

# inits the display window details
pygame.display.set_caption("Pokémon Game")
icon = pygame.image.load('pokeball.png')
background_image = pygame.image.load('pixelgame-background11.jpg')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))
pygame.display.set_icon(icon)
screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
temp_screen = screen.copy()
window = pygame.Surface((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
# agent image
agent_image = pygame.image.load('ashKetchum.png')
# pokemon image
pok_up_image = pygame.image.load('pokeball.png')
pok_down_image = pygame.image.load('pokeball2.png')
exit_button = Button(x=35, y=20, height=20, width=40, text='Exit')
black = (0, 0, 0)

clock = pygame.time.Clock()
timer = time.time()
client = Client()
client.start_connection(HOST, PORT)
play = main(Client.get_info())
#graph = play.graph

# fonts init
pygame.font.init()
timer_font = pygame.font.SysFont('Ariel', 30, bold=True)
player_score_font = pygame.font.SysFont('Ariel', 30, bold=True)
node_id_font = pygame.font.SysFont('Ariel', 15, bold=False)

pokemons = client.get_pokemons()
pokemons_obj = json.loads(pokemons, object_hook=lambda d: SimpleNamespace(**d))

graph_json = client.get_graph()
FONT = pygame.font.SysFont('Arial', 20, bold=True)

# load the json string into SimpleNamespace Object
graph = json.loads(
    graph_json, object_hook=lambda json_dict: SimpleNamespace(**json_dict))

for n in graph.Nodes:
    x, y, _ = n.pos.split(',')
    n.pos = SimpleNamespace(x=float(x), y=float(y))

# get data proportions
min_x = min(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
min_y = min(list(graph.Nodes), key=lambda n: n.pos.y).pos.y
max_x = max(list(graph.Nodes), key=lambda n: n.pos.x).pos.x
max_y = max(list(graph.Nodes), key=lambda n: n.pos.y).pos.y


def scale(data, min_screen, max_screen, min_data, max_data):
    """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
    return ((data - min_data) / (max_data - min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values
def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height() - 50, min_y, max_y)


radius = 15

# add agents
client.add_agent("{\"id\":0}")
client.add_agent("{\"id\":1}")
client.add_agent("{\"id\":2}")
client.add_agent("{\"id\":3}")

# this command starts the server - the game is running now
client.start()


# allocates for each pokemon the closest agent
def AllocateAgent():
    for agent in play.ListAgens():
        if agent.src == agent.lastDest or len(agent.orderList) == 0:
            v = ("-inf")
            bestPok = Pokémon(0, (0.0, 0.0, 0.0), 0, 0, False,0)
            pokemons_list = play.ListPokemons()
            for pok in pokemons_list:
                if not pok.wasTaken:
                    srcPok, destPok = play.location_pokemon(pok.pos)

                    agent.lastDest = destPok.id
                    if agent.src == srcPok.id:
                        w, lst = play.shortest_path(srcPok, destPok)
                    elif agent.src == destPok.id:
                        lst = [srcPok.id, destPok.id]
                        bestPok = pok
                        agent.orderList = lst
                        break
                    else:
                        temp_node =play.graph.getnode(agent.src)
                        w, lst = play.threeShortestPath(temp_node, srcPok, destPok)

                    lst.pop(0)
                    if (pok.value - w) > v:
                        v = pok.value - w
                        bestPok = pok
                        agent.orderList = lst

            bestPok.wasTaken = True


# draw nodes
def draw_vertices():
    for n in graph.Nodes:
        x = my_scale(n.pos.x, x=True)
        y = my_scale(n.pos.y, y=True)
        # its just to get a nice initialized circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.id), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)


# draw edges
def draw_edges():
    for e in graph.Edges:
        # find the edge nodes
        src = next(n for n in graph.Nodes if n.id == e.src)
        dest = next(n for n in graph.Nodes if n.id == e.dest)

        # scaled positions
        src_x = my_scale(src.pos.x, x=True)
        src_y = my_scale(src.pos.y, y=True)
        dest_x = my_scale(dest.pos.x, x=True)
        dest_y = my_scale(dest.pos.y, y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))


# draw agents
def draw_agents():
    for agent in agents:
        screen.blit(agent_image, (int(agent.pos.x - 5),
                                  int(agent.pos.y - 30)))


# draw pokemons according to their type-> up or down
def draw_pokemons():
    for p in pokemons:
        x = p.pos.x
        y = p.pos.y - 15
        if p.type == -1:
            screen.blit(pok_down_image, (int(x), int(y)))
        else:
            screen.blit(pok_up_image, (int(x), int(y)))


# check events, i.e: if a button is pressed
def check_events():
    for event in pygame.event.get():
        # if the player wants to exit the game and pressed the default exit button
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # if the player wants to exit the game and pressed the exit button
            if exit_button.onTop(mouse.get_pos()):
                pygame.quit()
                exit(0)


while client.is_running() == 'true':
    # counts the agent moves
    # split the getInfo (string) and take the third element (moves)
    agent_mc = client.get_info().split(',')
    number_of_moves = agent_mc[2].split(':')[1]
    agent_mc_button = Button(x=35, y=20 + 30, height=20, width=80, text=f"Moves: {number_of_moves}")
    timer = time.time()
    timer_button = Button(x=35, y=20 + 30 + 30, height=20, width=80,
                          text="Time To End: " + str(int(float(client.time_to_end()) / 1000)))
    pokemons = json.loads(client.get_pokemons(),
                          object_hook=lambda d: SimpleNamespace(**d)).Pokemons
    pokemons = [p.Pokemon for p in pokemons]
    for p in pokemons:
        x, y, _ = p.pos.split(',')
        p.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))

    check_events()
    top_left_screen = (0, 0)
    # refresh surface
    temp_screen.fill(black)
    temp_screen.blit(background_image, (0, 0))
    screen.blit(pygame.transform.scale(temp_screen, screen.get_rect().size), top_left_screen)
    exit_button.draw(screen)
    agent_mc_button.draw(screen)
    timer_button.draw(screen)

    # draw game
    draw_edges()
    draw_vertices()
    draw_agents()
    draw_pokemons()

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    AllocateAgent()
    flag = True

    for agent in play.ListAgens():
        if agent.dest == -1:
            flag = False
            nextNode = agent.orderList.pop(0)
            print("next: ", nextNode)
            print("agent: ", agent.id)
            client.choose_next_edge('{"agent_id":' + str(agent.id) + ', "next_node_id":' + str(nextNode) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    if number_of_moves / (time.time() - timer) < 10 and flag:
        client.move()

# done-> Game Over!
