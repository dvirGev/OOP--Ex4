import subprocess
import sys

from GameAlgo import gameAlgo
from client import Client
from GUI import GUI
from classes import agent
###### python codes./Ex4.py
"""sys.argv[1]"""
subprocess.Popen(['powershell.exe', f'java -jar Ex4_Server_v0.0.jar {7}'])
# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
client = Client()
game = gameAlgo()


client.start_connection(HOST, PORT)

client.add_agent("{\"id\":0}")

game.update(client.get_pokemons(), client.get_agents(), client.get_graph())
gui = GUI(game)
client.start()
while client.is_running() == 'true':
    size = len(game.graph.nodes)
    for agent in game.agents:
        if agent.dest == -1:
            next_node = (agent.src - 1) % size
            client.choose_next_edge('{"agent_id":'+str(agent.id)+', "next_node_id":'+str(next_node)+'}')
            ttl = client.time_to_end()
            print(ttl, client.get_info())
    client.move()
    game.update(client.get_pokemons(), client.get_agents(), client.get_graph())
    gui.draw()

