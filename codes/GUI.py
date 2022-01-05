import json
from os import system
import pygame
from pygame import *
from pygame.time import Clock

from GameAlgo import gameAlgo
from client import Client

WIDTH, HEIGHT = 1080, 720
radius = 25
background = 'GUIData/background.png'
song = 'GUIData/song.wav'
node = 'GUIData/node.png'
agent = 'GUIData/agent.gif'
pikachu = 'GUIData/pikachu.png'
charmander = 'GUIData/charmander.png'
squirtle = 'GUIData/squirtle.png'
bulbasaur = 'GUIData/bulbasaur.png'
pygame.init()
mixer.init()
font.init()

class GUI():
    def __init__(self, gameAlgo: gameAlgo, client: Client) -> None:
        self.client = client
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
        squirtle_image = image.load(squirtle)
        squirtle_image = pygame.transform.scale(squirtle_image, (35, 35))
        bulbasaur_image = image.load(bulbasaur)
        bulbasaur_image = pygame.transform.scale(bulbasaur_image, (35, 35))
        self.pokemos_image = [pikachu_image, charmander_image, squirtle_image, bulbasaur_image]
        mixer.music.load(song)
        #mixer.music.play(-1) # If the loops is -1 then the music will repeat indefinitely.
        
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
        buttonColor = (28, 172, 74)
        buttonWidth = 70
        self.exit_button = Button(buttonColor, 2, 2, buttonWidth, 20, 'EXIT')
        self.music_button = Button(buttonColor, 2+buttonWidth, 2, buttonWidth, 20, 'MUSIC')
        self.move_button = Button(buttonColor, 2+2*buttonWidth, 2, buttonWidth, 20, 'MOVES')
        self.time_button = Button(buttonColor, 2+3*buttonWidth, 2, buttonWidth, 20, 'TIME')
        self.grade_button = Button(buttonColor, 2+4*buttonWidth, 2, buttonWidth, 20, 'GRADE')
        self.isPLay = 0
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.music_button.isOver(pygame.mouse.get_pos()):
                        if self.isPLay % 2:
                            mixer.music.stop()
                        else:
                            mixer.music.play(-1)
                        self.isPLay+=1
                    if self.exit_button.isOver(mouse.get_pos()):
                        pygame.quit()
                        exit(0)
                        return False
        self.drawButtons()
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
        index = 0
        pokemons = self.gameAlgo.pokemons
        for p in pokemons:
            # print(p.__dict__)
            x = self.my_scale(p.pos[0], x=True)
            y = self.my_scale(p.pos[1], y=True)
            
            self.screen.blit(self.pokemos_image[index%len(self.pokemos_image)], (x, y))
            index += 1
    def drawAgents(self):
        agents = self.gameAlgo.agents.values()
        for agent in agents:
            x = self.my_scale(agent.pos[0], x=True) - radius/2
            y = self.my_scale(agent.pos[1], y=True) - radius/2  
            
            self.screen.blit(self.agent_image, (x, y)) 
    def drawButtons(self)->None:
        self.music_button.draw(self.screen, (0,0,0))
        self.exit_button.draw(self.screen, (0,0,0)) 
        data = json.loads(self.client.get_info())["GameServer"]
        self.move_button.text = 'MOVES: ' + str(data['moves'])
        self.move_button.draw(self.screen, (0,0,0))
        self.time_button.text = 'TIME: ' + str(int(float(self.client.time_to_end()) / 1000))
        self.time_button.draw(self.screen, (0,0,0))
        self.grade_button.text = 'GRADE: ' + str(data["grade"])
        self.grade_button.draw(self.screen, (0,0,0))
            
class Button():
    def __init__(self, color, x,y,width,height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self,win,outline=None):
        #Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x-2,self.y-2,self.width+4,self.height+4),0)
            
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.height),0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 10)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        #Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False
    
    