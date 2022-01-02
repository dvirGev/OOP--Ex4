class DiGraph():
    """This  class represents directed graph."""
    def __init__(self) -> None:
        super().__init__()
        self.nodes = {}
        self.edges = {}
        self.mc = 0
    def __repr__(self) -> str:
        return f'Node: {self.nodes}, Edges {self.edges}'

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        return len(self.nodes)

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        return len(self.edges)

    def get_all_v(self) -> dict:
        """
        return a dictionary of all the nodes in the Graph, each node is represented using a pair
        (node_id, node_data)
        """
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """
        return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
        """
        return self.nodes[id1].toMe

    def all_out_edges_of_node(self, id1: int) -> dict:
        """
        return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        return self.nodes[id1].fromMe

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self.mc

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        if (not id1 in self.nodes.keys()) or (not id2 in self.nodes.keys()):
            return False
        self.edges[(id1, id2)] = weight
        self.nodes[id1].fromMe[id2] = weight
        self.nodes[id2].toMe[id1] = weight
        self.mc += 1
        return True

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """
        if node_id in self.nodes.keys():
            return False
        self.nodes[node_id] = Node(node_id, (pos))
        self.mc += 1
        return True

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists the function will do nothing
        """
        if not node_id in self.nodes.keys():
            return False
        for src in self.nodes[node_id].toMe.keys():
            self.edges.pop((src, node_id))
            self.nodes[src].fromMe.pop(node_id)
        for dest in self.nodes[node_id].fromMe.keys():
            self.edges.pop((node_id, dest))
            self.nodes[dest].toMe.pop(node_id)
        self.nodes.pop(node_id)
        self.mc += 1
        return True

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """
        if (not node_id1 in self.nodes.keys()) or (not node_id2 in self.nodes.keys()) or (
        not (node_id1, node_id2) in self.edges.keys()):
            return False
        self.edges.pop((node_id1, node_id2))
        self.nodes[node_id1].fromMe.pop(node_id2)
        self.nodes[node_id2].toMe.pop(node_id1)
        self.mc += 1
        return True
class Node:
    def __init__(self, key: int, location = ()) -> None:
        self.key = key
        self.location = location
        self.tag = 0
        self.fromMe = {}
        self.toMe = {}
    def __repr__(self) -> str:
        return f'Key: {self.key}, Location {self.location}'