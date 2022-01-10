"""
part of the code was taken from AchiyaZigi, who wrote the task
OOP - Ex4
GUI for python client to communicate with the server and "play the game!"
"""
from math import inf
from types import SimpleNamespace
from client import Client
import json
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
WIDTH, HEIGHT = 1080, 720

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

clock = pygame.time.Clock()
timer = time.time()
client = Client()
client.start_connection(HOST, PORT)
play = main(client.get_info())

# graph = play.graph

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
for i in range(play.numOfAgent):
    st = "{id:"
    st += str(i)
    st += "}"
    client.add_agent(st)

# this command starts the server - the game is running now
client.start()


# allocates for each pokemon the closest agent
def AllocateAgent():
    for agent in play.ListAgens():
        if agent.src == agent.lestdest or len(agent.whereTo) == 0:
            v = float("-inf")
            bestPok = Pokémon( 0, 0,(0.0, 0.0, 0.0), 0)
            pokemons_list = play.ListPokemons()
            for pok in pokemons_list:
                if not pok.wasTaken:
                    srcPok, destPok = play.location_pokemon(pok.pos)
                    agent.lestdest = destPok.getKey()
                    if agent.src == srcPok.getKey():
                        w, lst = play.shortest_path(srcPok, destPok)
                    elif agent.src == destPok.getKey():
                        lst = [srcPok.getKey(), destPok.getKey()]
                        bestPok = pok
                        agent.whereTo = lst
                        break
                    else:
                        temp_node = play.graph.getnode(agent.src)
                        w, lst = play.threeShortestPath(temp_node, srcPok, destPok)

                    lst.pop(0)
                    if (pok.value - w) > v:
                        v = pok.value - w
                        bestPok = pok
                        agent.whereTo = lst

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
    for agent in play.Agens:
        image = agent_image
        rect = image.get_rect()
        rect.center = (agent.pos[0], agent.pos[1])
        # agentId = font.render(str(agent.id), True, black)
        screen.blit(image, rect)
        # screen.blit(agentId, rect)


# draw pokemons according to their type-> up or down
def draw_pokemons():
    for p in play.pokemons:
        if p.type > 0:
            image = pok_up_image
        else:
            image = pok_down_image
        rect = image.get_rect()
        rect.center = (p.posScale[0], p.posScale[1])
        screen.blit(image, rect)
        # update screen changes

    display.update()


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


def load_pokemons():
    play.load_pokemon(client.get_pokemons())
    for p in play.pokemons:
        x, y, _ = p.pos
        x = my_scale(float(x), x=True)
        y = my_scale(float(y), y=True)
        p.posScale = (x, y, 0.0)


def load_agent():
    play.load_agents(client.get_agents())
    for a in play.Agens:
        x, y, _ = a.pos
        x = my_scale(float(x), x=True)
        y = my_scale(float(y), y=True)
        a.pos = (x, y, 0.0)


def move_the_agent():
    inf = json.loads(client.get_info(), object_hook=lambda d: SimpleNamespace(**d)).GameServer
    flag = True
    for agent in play.ListAgens():
        if agent.dest == -1:
            flag = False
            nextNode = agent.whereTo.pop(0)
            print("next: ", nextNode)
            print("agent: ", agent.ID)
            client.choose_next_edge('{"agent_id":' + str(agent.ID) + ', "next_node_id":' + str(nextNode) + '}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    if inf.moves / (time.time() - timer) < 10 and flag:
        client.move()


while client.is_running() == 'true':
    # counts the agent moves
    # split the getInfo (string) and take the third element (moves)
    agent_mc = client.get_info().split(',')
    number_of_moves = agent_mc[2].split(':')[1]
    agent_mc_button = Button(x=35, y=20 + 30, height=20, width=80, text=f"Moves: {number_of_moves}")
    timer = time.time()
    timer_button = Button(x=35, y=20 + 30 + 30, height=20, width=80,
                          text="Time To End: " + str(int(float(client.time_to_end()) / 1000)))
    # load agents and pokemons
    load_pokemons()
    load_agent()
    check_events()
    top_left_screen = (0, 0)
    # refresh surface
    temp_screen.fill((0, 0, 0))
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
    move_the_agent()

client.stop_connection()
# done-> Game Over!
