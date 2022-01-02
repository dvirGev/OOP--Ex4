import json
from DiGraph import *
#from GraphAlgo import GraphAlgo
from classes import *

class gameAlgo():
    def __init__(self) -> None:
        self.pokemons = []
        self.agents = []
        self.graph = DiGraph()
        #self.graphAlgo = GraphAlgo()
        
    def update(self, pokemons = None, agents = None, graph = None) ->None:
        if pokemons != None:
            self.pokemons = []
            pokemons_obj = json.loads(pokemons)
            for poke in pokemons_obj['Pokemons']:
                self.pokemons.append(pokemon(poke['Pokemon']))
        
        if agents != None:
            self.agents = []
            agents_obj = json.loads(agents)
            for age in agents_obj['Agents']:
                self.agents.append(agent(age['Agent']))
        
        if graph != None:
            self.graph = DiGraph()
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