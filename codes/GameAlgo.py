import json
import math
from DiGraph import *
#from GraphAlgo import GraphAlgo
from classes import *
from client import Client
epsilon = 0.0000000001


class gameAlgo():
    def __init__(self) -> None:
        self.pokemons = []
        self.agents = {}
        self.graph = DiGraph()
        self.dijkstra = Dijkstra(self.graph)
        self.counter = 0

    def update(self, pokemons=None, agents=None, graph=None) -> None:
        if agents != None:
            agents_obj = json.loads(agents)
            for age in agents_obj['Agents']:
                id = int(age['Agent']['id'])
                if not id is self.agents:
                    self.agents[id] = agent(age['Agent'])
                else:
                    self.agents[id].update(age['Agent'])

        if graph != None:
            self.graph = DiGraph()
            graph_obj = json.loads(graph)
            for node in graph_obj["Nodes"]:
                id = int(node["id"])
                if "pos" in node:
                    posData = node["pos"].split(',')
                    self.graph.add_node(
                        id, (float(posData[0]), float(posData[1]), float(posData[2])))
                else:
                    self.graph.add_node(id)
            for edge in graph_obj["Edges"]:
                self.graph.add_edge(int(edge["src"]), int(
                    edge["dest"]), float(edge["w"]))

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
                dis1 = self.distanceNodes(
                    self.graph.nodes[node1], self.graph.nodes[node2])
                dis2 = (self.distancePokNode(
                    self.graph.nodes[node1], pok) + self.distancePokNode(self.graph.nodes[node2], pok))
                if abs(dis1 - dis2) <= epsilon:
                    if pok.type == -1:
                        pok.src = min(node1, node2)
                        pok.dest = max(node1, node2)
                    else:
                        pok.src = max(node1, node2)
                        pok.dest = min(node1, node2)
                    return

    def distanceNodes(self, node1: Node, node2: Node):
        dis = math.sqrt(pow(node1.location[0] - node2.location[0],
                        2) + pow(node1.location[1] - node2.location[1], 2))
        return dis

    def distancePokNode(self, node1: Node, pok: pokemon):
        dis = math.sqrt(
            pow(node1.location[0] - pok.pos[0], 2) + pow(node1.location[1] - pok.pos[1], 2))
        return dis

    def candidateAgent(self, p: pokemon) -> list:
        temp = []
        for a in self.agents.values():
            if len(a.stations) == 0:
                temp.append(a.id)
        if len(temp) == 0:
            temp.append(self.counter % len(self.agents))
            self.counter += 1
        return temp

    def calc(self, a: agent, p: pokemon):
        print(p.src, p.dest)
        if len(a.stations):
            distance = self.shortest_path(a.stations[-1], p.src)
        else:
            distance = self.shortest_path(a.src, p.src)
        time = (distance[0] / a.speed)
        return (time, distance)

    def allocateAgen(self, p: pokemon) -> None:
        candidAgents = self.candidateAgent(p)
        relevant = float('inf')
        candid = path = None
        for a in candidAgents:
            cal = self.calc(self.agents[a], p)
            if cal[0] < relevant:
                candid = self.agents[a].id
                path = cal[1][1]
        path.pop(0)
        self.agents[candid].stations += path
        self.agents[candid].stations.append(p.dest)
        p.agent = candid


    def allocateAllpokemon(self) -> None:
        for p in self.pokemons:
            if p.agent == None:
                self.allocateAgen(p)

    def CMD(self, client: Client) -> None:
        for a in self.agents.values():
            if a.dest == -1 and len(a.stations) !=  0:
                print(f"a = {a}\n src = {a.src}")
                client.choose_next_edge(
                    '{"agent_id":'+str(a.id)+', "next_node_id":'+str(a.stations[0])+'}')
                a.stations.pop(0)

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        """
        self.updateDijkstra(id1)
        self.dijkstra.buildPath(id2)
        w = self.dijkstra.dist[id2]
        l = self.dijkstra.path[id2]
        return (w, l)

    def updateDijkstra(self, src: int) -> None:
        if src != self.dijkstra.src or self.graph.mc != self.dijkstra.MC:
            self.dijkstra.src = src
            self.dijkstra.graph = self.graph
            self.dijkstra.MC = self.graph.mc
            self.dijkstra.alg()


class Dijkstra:
    def __init__(self, graph: DiGraph) -> None:
        """
        this class crate the Dijkstra algorithm.
        """
        self.src = -1
        self.MC = -1
        self.dist = {}
        self.path = {}
        self.dads = {}
        self.graph = graph

    def initMaps(self, dads: dict, Q: list) -> None:
        """
        initMaps of the algorithm if there are edge between two verticals put in the dist the wight between them else
        infinity.
        and initiate all the dads.
        """
        for node in self.graph.nodes.keys():
            if node != self.src:
                self.dist[node] = float('inf')
                dads[node] = float('inf')
                Q.append(node)
                self.path[node] = []
        dads[self.src] = self.src
        self.dist[self.src] = 0.0
        self.path[self.src] = []
        Q.append(self.src)

    def minInList(self, Q: list) -> int:
        """
        check what is the next vertical we check.
        return: node.
        """
        min2 = float('inf')
        ans = float('-inf')
        for node in Q:
            if min2 > self.dist[node]:
                ans = node
                min2 = self.dist[node]
        if ans != float('-inf'):
            Q.remove(ans)
        return ans

    def relax(self, src: int, dest: int) -> None:
        """
        the kernel of the algorithm check if we can relax the wight between the verticals
        return: None
        """
        newDist = self.dist[src] + self.graph.edges[(src, dest)]
        if newDist < self.dist[dest]:
            self.dist[dest] = newDist
            self.dads[dest] = src

    def alg(self):
        Q = []
        self.initMaps(self.dads, Q)
        while len(Q) != 0:
            u = self.minInList(Q)
            if u == float('-inf'):
                return
            for dest in self.graph.all_out_edges_of_node(u).keys():
                self.relax(u, dest)

    def buildPath(self, dest: int) -> None:
        """
        build the path between the verticals
        return: None
        """
        if len(self.path[dest]) != 0:
            return
        self.path[dest] = []
        if dest == self.src:
            self.path[dest].append(dest)
            return
        dad = self.dads[dest]
        if dad == float('inf'):
            return
        if dad in self.path:
            self.buildPath(dad)
        self.path[dest].extend(self.path[dad])
        self.path[dest].append(dest)
