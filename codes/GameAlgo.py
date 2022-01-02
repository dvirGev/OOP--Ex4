import json
from DiGraph import *
from GraphAlgo import GraphAlgo
from codes.classes import pokemon
import math
class gameAlgo():
    def __init__(self) -> None:
        self.pokemons = []
        self.agents = []
        self.graph = DiGraph()
        self.graphAlgo = GraphAlgo()
        
    def update(self, pokemons = None, agents = None, graph = None) ->None:
        if pokemons != None:
            pokemons = pokemons
            pokemons_obj = json.loads(pokemons)
            pokemons = []
            for poke in pokemons_obj['Pokemons']:
                pokemons.append(pokemon(poke['Pokemon']))

    def pokemon_src_dest(self, pok: pokemon) -> list:
        for node1 in self.graph.nodes:

            for node2 in self.graph.nodes:
                if self.distanceNodes(self.graph.nodes[node1], self.graph.nodes[node2]) == (self.distancePokNode(self.graph.nodes[node1], pok) + self.distancePokNode(self.graph.nodes[node2], pok)):
                        return (node1, node2)
        return None

    def distanceNodes(self, node1: Node, node2: Node) -> float:
        dis = math.sqrt(pow(node1.location[0] - node2.location[0], 2) + pow(node1.location[1] - node2.location[1], 2))
        return dis

    def distancePokNode(self, node1: Node, pok: pokemon) -> float:
        dis = math.sqrt(pow(node1.location[0] - pok.pos[0], 2) + pow(node1.location[1] - pok.pos[1], 2))
        return dis
