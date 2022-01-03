from pygame import mixer

"""
@author AchiyaZigi
OOP - Ex4
Very simple GUI example for python client to communicates with the server and "play the game!"
"""
from types import SimpleNamespace
from client import Client
import json
from pygame import gfxdraw
import pygame
from pygame import *

import subprocess
import sys
from classes import *
from DiGraph import DiGraph
"""sys.argv[1]"""
subprocess.Popen(['powershell.exe', f'java -jar Ex4_Server_v0.0.jar {0}'])
# init pygame
WIDTH, HEIGHT = 1080, 720

# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
pygame.init()

screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
clock = pygame.time.Clock()
pygame.font.init()
FONT = pygame.font.SysFont('Arial', 20, bold=True)


client = Client()
client.start_connection(HOST, PORT)

def getPokemons()->list:
    pokemons = client.get_pokemons()
    pokemons_obj = json.loads(pokemons)
    pokemons = []
    for poke in pokemons_obj['Pokemons']:
        pokemons.append(pokemon(poke['Pokemon']))
    return pokemons

def loadGraph(jsonGraph: str)-> DiGraph:
    graph = DiGraph()
    di = json.loads(jsonGraph)
    for node in di["Nodes"]:
        id = int(node["id"])
        if "pos" in node:
            posData = node["pos"].split(',')
            graph.add_node(id, (float(posData[0]), float(posData[1]), float(posData[2])))
        else:
            graph.add_node(id)
    for edge in di["Edges"]:
        graph.add_edge(int(edge["src"]), int(edge["dest"]), float(edge["w"]))
    return graph
graph = loadGraph(client.get_graph())
# get data proportions
min_x = float('inf')
min_y = float('inf')
max_x = float('-inf')
max_y = float('-inf')

for n in graph.nodes.values():
        print(n.location)
        x = n.location[0]
        y = n.location[1]
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)

def scale(data, min_screen, max_screen, min_data, max_data):
    """
    get the scaled data with proportions min_data, max_data
    relative to min and max screen dimentions
    """
    return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) + min_screen


# decorate scale with the correct values

def my_scale(data, x=False, y=False):
    if x:
        return scale(data, 50, screen.get_width() - 50, min_x, max_x)
    if y:
        return scale(data, 50, screen.get_height()-50, min_y, max_y)


radius = 15

client.add_agent("{\"id\":0}")
# client.add_agent("{\"id\":1}")
# client.add_agent("{\"id\":2}")
# client.add_agent("{\"id\":3}")

# this commnad starts the server - the game is running now
client.start()

"""
The code below should be improved significantly:
The GUI and the "algo" are mixed - refactoring using MVC design pattern is required.
"""


while client.is_running() == 'true':
    pokemons = getPokemons()
    for p in pokemons:
        x = p.pos[0]
        y = p.pos[1]
        p.pos = [my_scale(float(x), x=True), my_scale(float(y), y=True), 0]
    agents = json.loads(client.get_agents(),
                        object_hook=lambda d: SimpleNamespace(**d)).Agents
    agents = [agent.Agent for agent in agents]
    for a in agents:
        x, y, _ = a.pos.split(',')
        a.pos = SimpleNamespace(x=my_scale(
            float(x), x=True), y=my_scale(float(y), y=True))
    # check events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    # refresh surface
    screen.fill(Color(0, 0, 0))

    # draw nodes
    for n in graph.nodes.values():
        x = my_scale(n.location[0], x=True)
        y = my_scale(n.location[1], y=True)

        # its just to get a nice antialiased circle
        gfxdraw.filled_circle(screen, int(x), int(y),
                              radius, Color(64, 80, 174))
        gfxdraw.aacircle(screen, int(x), int(y),
                         radius, Color(255, 255, 255))

        # draw the node id
        id_srf = FONT.render(str(n.key), True, Color(255, 255, 255))
        rect = id_srf.get_rect(center=(x, y))
        screen.blit(id_srf, rect)

    # draw edges
    for e in graph.edges.keys():
        # find the edge nodes
        src = graph.nodes[e[0]]
        dest = graph.nodes[e[1]]

        # scaled positions
        src_x = my_scale(src.location[0], x=True)
        src_y = my_scale(src.location[1], y=True)
        dest_x = my_scale(dest.location[0], x=True)
        dest_y = my_scale(dest.location[1], y=True)

        # draw the line
        pygame.draw.line(screen, Color(61, 72, 126),
                         (src_x, src_y), (dest_x, dest_y))

    # draw agents
    for agent in agents:
        pygame.draw.circle(screen, Color(122, 61, 23),
                           (int(agent.pos.x), int(agent.pos.y)), 10)
    # draw pokemons (note: should differ (GUI wise) between the up and the down pokemons (currently they are marked in the same way).
    for p in pokemons:
        pygame.draw.circle(screen, Color(0, 255, 255), (int(p.pos[0]), int(p.pos[1])), 10)

    # update screen changes
    display.update()

    # refresh rate
    clock.tick(60)

    # choose next edge
    for agent in agents:
        if agent.dest == -1:
            next_node = (agent.src - 1) % len(graph.nodes)
            client.choose_next_edge(
                '{"agent_id":'+str(agent.id)+', "next_node_id":'+str(next_node)+'}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())

    client.move()
# game over:
