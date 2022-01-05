import json
import subprocess
import sys
import time
from GameAlgo import gameAlgo
from client import Client
from GUI import GUI
from classes import agent
###### python codes./Ex4.py
"""sys.argv[1]"""
subprocess.Popen(['powershell.exe', f'java -jar Ex4_Server_v0.0.jar {sys.argv[1]}'])
# default port
PORT = 6666
# server host (default localhost 127.0.0.1)
HOST = '127.0.0.1'
client = Client()
client.start_connection(HOST, PORT)

game = gameAlgo()




def addAgents():
    size = int(json.loads(client.get_info())["GameServer"]["agents"])
    for i in range(size):
        client.add_agent("{\"id\":" + str(i) + "}")
addAgents()

game.update(client.get_pokemons(), client.get_agents(), client.get_graph())
gui = GUI(game, client)
client.start()
while client.is_running() == 'true':
    game.update(client.get_pokemons(), client.get_agents())
    game.allocateAllagent()
    game.CMD(client)
    gui.draw()
    game.sleep(client)
    client.move()

