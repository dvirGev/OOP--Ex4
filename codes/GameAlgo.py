import json
from DiGraph import *
from GraphAlgo import GraphAlgo
from codes.classes import pokemon
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