from unittest import TestCase
from DiGraph import DiGraph
from GraphAlgo import GraphAlgo


# the class is for us, for internal tests
class DiGraphTest(TestCase):

    def test_v_size(self):
        g = DiGraph()
        ga = GraphAlgo()
        ga.graph = g
        ga.load_from_json('../data/A0.json')

        self.assertEqual(g.v_size(), 11)

    def test_e_size(self):
        g = DiGraph()
        ga = GraphAlgo()
        ga.graph = g
        ga.load_from_json('../data/A0.json')

        self.assertEqual(g.e_size(), 22)

    def test_get_mc(self):
        g = DiGraph()
        ga = GraphAlgo()
        ga.graph = g
        ga.load_from_json('../data/A0.json')

        self.assertEqual(g.get_mc(), 33)
        g.remove_edge(10, 9)
        self.assertEqual(g.get_mc(), 34)

    def test_add_edge(self):
        g = DiGraph()
        ga = GraphAlgo()
        ga.graph = g
        ga.load_from_json('../data/A0.json')

        self.assertEqual(g.e_size(), 22)
        g.add_edge(0, 5, 33)
        self.assertEqual(g.e_size(), 23)

    def test_add_node(self):
        g = DiGraph()
        ga = GraphAlgo()
        ga.graph = g
        ga.load_from_json('../data/A1.json')

        self.assertEqual(g.v_size(), 17)
        g.add_node(17, (1, 1, 0))
        self.assertEqual(g.v_size(), 18)

    def test_remove_node(self):
        g = DiGraph()
        ga = GraphAlgo()
        ga.graph = g
        ga.load_from_json('../data/A1.json')

        self.assertEqual(g.v_size(), 17)
        g.remove_node(1)
        self.assertEqual(g.v_size(), 16)

    def test_remove_edge(self):
        g = DiGraph()
        ga = GraphAlgo()
        ga.graph = g
        ga.load_from_json('../data/A0.json')

        self.assertEqual(g.e_size(), 22)
        g.remove_edge(0, 1)
        self.assertEqual(g.e_size(), 21)
