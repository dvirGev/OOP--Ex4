# from _typeshed import Self
# from os import stat_result
import copy

from GUI import GUI
from GraphAlgoInterface import GraphAlgoInterface
from GraphInterface import GraphInterface
import json

from DiGraph import DiGraph


class GraphAlgo(GraphAlgoInterface):
    """This class represents AlgoGraph."""

    def __init__(self, graph=DiGraph()) -> None:
        super().__init__()
        self.graph = graph
        self.dijkstra = Dijkstra(graph)

    def updateDijkstra(self, src: int) -> None:
        if src != self.dijkstra.src or self.graph.mc != self.dijkstra.MC:
            self.dijkstra.src = src
            self.dijkstra.MC = self.graph.mc
            self.dijkstra.alg()

    def get_graph(self) -> GraphInterface:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        try:
            self.graph = DiGraph()
            with open(file_name, "r") as fp:
                di = json.load(fp)
                for node in di["Nodes"]:
                    id = int(node["id"])
                    if "pos" in node:
                        posData = node["pos"].split(',')
                        self.graph.add_node(
                            id, (float(posData[0]), float(posData[1]), float(posData[2])))
                    else:
                        self.graph.add_node(id)
                for edge in di["Edges"]:
                    self.graph.add_edge(int(edge["src"]), int(edge["dest"]), float(edge["w"]))
        except:
            return False
        self.dijkstra.graph = self.graph
        return True

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        dict = {"Nodes": [], "Edges": []}
        for node in self.graph.nodes.values():
            id = node.key
            if (node.location != None):
                pos = f'{node.location[0]},{node.location[1]},{node.location[2]}'
                dict["Nodes"].append({"id": id, "pos": pos})
            else:
                dict["Nodes"].append({"id": id})

        for edge in self.graph.edges.keys():
            dict["Edges"].append(
                {"src": edge[0], "dest": edge[1], "w": self.graph.edges[edge]})

        try:
            with open(file_name, 'w') as f:
                json.dump(dict, indent=2, fp=f)
        except:
            return False
        return True

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

    def check_greedy(self, i: int, c: list, ins: list):
        first = i
        ins.append(i)
        c.remove(i)
        index = None
        sum = 0
        while len(c):
            low = float('inf')
            for j in c:
                if self.dijkstra.dist[j]< low:
                    low = self.dijkstra.dist[j]
                    index = j

            sum += low
            f = True
            path = self.shortest_path(i,index)[1]
            for j in path:
                if f:
                    f = False
                    continue
                else:
                    ins.append(j)
            i = index
            self.updateDijkstra(i)
            c.remove(index)
        return sum


    def TSP(self, node_lst: list[int]) -> (list[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """
        try:
            best = float('inf')
            permute = []
            for node in node_lst:
                self.updateDijkstra(node)
                cur = []
                value = self.check_greedy(node, copy.deepcopy(node_lst), cur)
                if value < best:
                    best = value
                    permute = cur
            return (permute,best)
        except:
            return ([], float('inf'))
                    

        

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """
        ans = (0, float('inf'))
        for src in self.graph.nodes.keys():
            self.updateDijkstra(src)
            maxDis = (src, max(self.dijkstra.dist.values()))
            if ans[1] > maxDis[1]:
                ans = maxDis
        return ans

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """
        GUI(self)


class Dijkstra:
    def __init__(self, graph: GraphInterface) -> None:
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
