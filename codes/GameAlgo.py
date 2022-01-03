import json
import math
from DiGraph import *
#from GraphAlgo import GraphAlgo
from classes import *
epsilon = 0.0000001

class gameAlgo():
    def __init__(self) -> None:
        self.pokemons = []
        self.agents = []
        self.graph = DiGraph()
        #self.graphAlgo = GraphAlgo()
        
    def update(self, pokemons = None, agents = None, graph = None) ->None:
        if agents != None:
            self.agents = []
            agents_obj = json.loads(agents)
            for age in agents_obj['Agents']:
                self.agents.append(agent(age['Agent']))
        
        if graph != None:
            self.graph = DiGraph()
            print(graph)
            graph_obj = json.loads(graph)
            for node in graph_obj["Nodes"]:
                id = int(node["id"])
                if "pos" in node:
                    posData = node["pos"].split(',')
                    self.graph.add_node(id, (float(posData[0]), float(posData[1]), float(posData[2])))
                else:
                    self.graph.add_node(id)
            for edge in graph_obj["Edges"]:
                self.graph.add_edge(int(edge["src"]), int(edge["dest"]), float(edge["w"]))
        
        if pokemons != None:
            self.pokemons = []
            pokemons_obj = json.loads(pokemons)
            for poke in pokemons_obj['Pokemons']:
                p = pokemon(poke['Pokemon'])
                self.pokemon_src_dest(p)
                self.pokemons.append(p)
    
    def pokemon_src_dest(self, pok: pokemon) -> None:
        for node1 in self.graph.nodes:
            for node2 in self.graph.nodes:
                dis1 = self.distanceNodes(self.graph.nodes[node1], self.graph.nodes[node2])
                dis2 = (self.distancePokNode(self.graph.nodes[node1], pok) + self.distancePokNode(self.graph.nodes[node2], pok))
                 # print(f"node 1 pos = {self.graph.nodes[node1]}\n node2 pos = {node2.location[0]}")
                if abs(dis1 - dis2) <= epsilon:
                    if pok.type == -1:
                        pok.src = min(node1, node2)
                        pok.dest = max(node1,node2)
                    else:
                        pok.src = max(node1, node2)
                        pok.dest = min(node1, node2)
                    return

    def distanceNodes(self, node1: Node, node2: Node):
        dis = math.sqrt(pow(node1.location[0] - node2.location[0], 2) + pow(node1.location[1] - node2.location[1], 2))
        return dis
 
    def distancePokNode(self, node1: Node, pok: pokemon):
        dis = math.sqrt(pow(node1.location[0] - pok.pos[0], 2) + pow(node1.location[1] - pok.pos[1], 2))
        return dis