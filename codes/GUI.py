from os import system
import pygame
from pygame import *
from pygame.time import Clock

from GameAlgo import gameAlgo

WIDTH, HEIGHT = 1080, 720
radius = 25
background = 'GUIData/background.png'
song = 'GUIData/song.wav'
node = 'GUIData/node.png'
agent = 'GUIData/agent.gif'
pikachu = 'GUIData/pikachu.png'
charmander = 'GUIData/charmander.png'
pygame.init()
mixer.init()
font.init()

class GUI():
    def __init__(self, gameAlgo: gameAlgo) -> None:
        self.gameAlgo = gameAlgo
        self.screen = display.set_mode((WIDTH, HEIGHT), depth=32, flags=RESIZABLE)
        self.background_image = image.load(background)
        self.node_image = image.load(node)
        self.node_image = pygame.transform.scale(self.node_image, (radius, radius))
        self.agent_image = image.load(agent)
        self.agent_image = pygame.transform.scale(self.agent_image, (40, 40))
        pikachu_image = image.load(pikachu)
        pikachu_image = pygame.transform.scale(pikachu_image, (35, 35))
        charmander_image = image.load(charmander)
        charmander_image = pygame.transform.scale(charmander_image, (35, 35))
        self.pokemos_image = [pikachu_image, charmander_image]
        mixer.music.load(song)
        mixer.music.play(-1) # If the loops is -1 then the music will repeat indefinitely.
        mixer.music.play()
        
        self.min_x = float('inf')
        self.min_y = float('inf')
        self.max_x = float('-inf')
        self.max_y = float('-inf')
        #find min and max
        for n in self.gameAlgo.graph.nodes.values():
            x = n.location[0]
            y = n.location[1]
            self.min_x = min(self.min_x, x)
            self.min_y = min(self.min_y, y)
            self.max_x = max(self.max_x, x)
            self.max_y = max(self.max_y, y)
    def scale(self, data, min_screen, max_screen, min_data, max_data):
        """
        get the scaled data with proportions min_data, max_data
        relative to min and max screen dimentions
        """
        return ((data - min_data) / (max_data-min_data)) * (max_screen - min_screen) +min_screen 
    # decorate scale with the correct values
    def my_scale(self, data, x=False, y=False):
        if x:
            return self.scale(data, 50, self.screen.get_width() - 50, self.min_x, self.max_x)
        if y:
            return self.scale(data, 50, self.screen.get_height()-50, self.min_y, self.max_y)
        
    def draw(self) -> bool:
        background_image = transform.scale(self.background_image, (self.screen.get_width(), self.screen.get_height()))
        self.screen.blit(background_image, [0,0])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
                return False
        self.drawEdges()
        self.drawNode()
        self.drawPokemons()
        self.drawAgents()
        # refresh rate
        #Clock.tick(60)
        display.update()
        return True
    
    def drawNode(self):
        graph = self.gameAlgo.graph
        for n in graph.nodes.values():
            x = self.my_scale(n.location[0], x=True)
            y = self.my_scale(n.location[1], y=True)
            # its just to get a nice antialiased circle
            self.screen.blit(self.node_image, (x, y))
            
        # # draw the node id
        # id_srf = FONT.render(str(n.key), True, Color(255, 255, 255))
        # rect = id_srf.get_rect(center=(x, y))
        # screen.blit(id_srf, rect)
    def drawEdges(self):
        graph = self.gameAlgo.graph
        for e in graph.edges.keys():
            # find the edge nodes
            src = graph.nodes[e[0]]
            dest = graph.nodes[e[1]]

            # scaled positions
            src_x = self.my_scale(src.location[0], x=True) + radius/2
            src_y = self.my_scale(src.location[1], y=True) + radius/2
            dest_x = self.my_scale(dest.location[0], x=True) + radius/2
            dest_y = self.my_scale(dest.location[1], y=True) + radius/2

            # draw the line
            pygame.draw.line(self.screen, Color(61, 72, 126), (src_x, src_y), (dest_x, dest_y), 5)
    def drawPokemons(self):
        pokemons = self.gameAlgo.pokemons
        for p in pokemons:
            # print(p.__dict__)
            x = self.my_scale(p.pos[0], x=True)
            y = self.my_scale(p.pos[1], y=True)
            
            self.screen.blit(self.pokemos_image[1], (x, y))
    def drawAgents(self):
        agents = self.gameAlgo.agents
        for agent in agents:
            x = self.my_scale(agent.pos[0], x=True) - radius/2
            y = self.my_scale(agent.pos[1], y=True) - radius/2  
            
            self.screen.blit(self.agent_image, (x, y))      
    
    