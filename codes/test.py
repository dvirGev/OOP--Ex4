import unittest
import os
from GraphAlgo import GraphAlgo


class TestGraphAlgo(unittest.TestCase):
    """ this class is for checking are functions
    the name of the function we check is just the name of the function with 'test_' before
    """

    def test_load_from_json(self):
        graphAlgo = GraphAlgo()
        self.assertTrue(graphAlgo.load_from_json(r"C:\Users\dvir1\PycharmProjects\OOP--Ex4\data\testGraph.json"))  # graph without pos

    def test_save_from_json(self):
        graphAlgo = GraphAlgo()
        graphAlgo.load_from_json(r"C:\Users\dvir1\PycharmProjects\OOP--Ex4\data\testGraph.json")
        self.assertTrue(graphAlgo.save_to_json("temp.json"))
        os.remove("./temp.json")

    def test_shortest_path(self):
        graphAlgo = GraphAlgo()
        graphAlgo.graph.add_node(0)
        graphAlgo.graph.add_node(1)
        graphAlgo.graph.add_node(2)
        graphAlgo.graph.add_edge(0, 1, 1)
        graphAlgo.graph.add_edge(1, 2, 4)
        self.assertEqual(graphAlgo.shortest_path(0, 1), (1, [0, 1]))
        self.assertEqual(graphAlgo.shortest_path(0, 2), (5, [0, 1, 2]))
        graphAlgo.graph.remove_node(1)
        self.assertEqual(graphAlgo.shortest_path(0, 2), (float('inf'), []))

    def test_centerPoint(self):
        graphAlgo = GraphAlgo()
        graphAlgo.load_from_json(r"C:\Users\dvir1\PycharmProjects\OOP--Ex4\data\testGraph.json")
        print(graphAlgo.centerPoint())
        self.assertEqual((8, 9.925289024973141), graphAlgo.centerPoint())


class TestDiGraph(unittest.TestCase):
    def test_v_size(self):
        graphAlgo = GraphAlgo()
        graphAlgo.load_from_json(r"C:\Users\dvir1\PycharmProjects\OOP--Ex4\data\testGraph.json")
        self.assertEqual(graphAlgo.graph.v_size(), 17)

    def test_e_size(self):
        graphAlgo = GraphAlgo()
        graphAlgo.load_from_json(r"C:\Users\dvir1\PycharmProjects\OOP--Ex4\data\testGraph.json")
        self.assertEqual(graphAlgo.graph.e_size(), 36)

    def test_get_all_v(self):
        graphAlgo = GraphAlgo()
        graphAlgo.load_from_json(r"C:\Users\dvir1\PycharmProjects\OOP--Ex4\data\testGraph.json")
        self.assertEqual(len(graphAlgo.graph.get_all_v()), 17)

    def test_all_in_edges_of_node(self):
        graphAlgo = GraphAlgo()
        graphAlgo.load_from_json(r"C:\Users\dvir1\PycharmProjects\OOP--Ex4\data\testGraph.json")
        self.assertEqual(len(graphAlgo.graph.all_in_edges_of_node(0)), 2)

    def test_all_out_edges_of_node(self):
        graphAlgo = GraphAlgo()
        graphAlgo.load_from_json(r"C:\Users\dvir1\PycharmProjects\OOP--Ex4\data\testGraph.json")
        self.assertEqual(len(graphAlgo.graph.all_out_edges_of_node(0)), 2)

    def test_add_edge(self):
        graphAlgo = GraphAlgo()
        graphAlgo.load_from_json(r"C:\Users\dvir1\PycharmProjects\OOP--Ex4\data\testGraph.json")
        graphAlgo.graph.add_edge(0, 2, 3)
        self.assertEqual(graphAlgo.graph.edges[(0, 2)], 3)

    def test_get_mc(self):
        graphAlgo = GraphAlgo()
        graphAlgo.load_from_json(r"C:\Users\dvir1\PycharmProjects\OOP--Ex4\data\testGraph.json")
        self.assertEqual(graphAlgo.graph.get_mc(), 53)

    def test_add_node(self):
        graphAlgo = GraphAlgo()
        graphAlgo.load_from_json(r"C:\Users\dvir1\PycharmProjects\OOP--Ex4\data\testGraph.json")
        graphAlgo.graph.add_node(18, (35.21310882485876, 32.104636394957986, 0.0))
        self.assertEqual(graphAlgo.graph.v_size(), 18)

    def test_remove_node(self):
        graphAlgo = GraphAlgo()
        graphAlgo.load_from_json(r"C:\Users\dvir1\PycharmProjects\OOP--Ex4\data\testGraph.json")

        self.assertEqual(False, graphAlgo.graph.remove_node(18))
        self.assertEqual(True, graphAlgo.graph.remove_node(16))

    def test_remove_edge(self):
        graphAlgo = GraphAlgo()
        graphAlgo.load_from_json(r"C:\Users\dvir1\PycharmProjects\OOP--Ex4\data\testGraph.json")
        self.assertEqual(True, graphAlgo.graph.remove_edge(0, 1))
        self.assertEqual(False, graphAlgo.graph.remove_edge(0, 1))

    ###GameAlgo###

if __name__ == '__main__':
    unittest.main()