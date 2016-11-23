import unittest

from flange.fairflow import *

def build_graph():
    util = Utils()
    g = nx.Graph()

    nodeA = g.add_node('A')
    nodeB = g.add_node('B')
    nodeC = g.add_node('C')
    nodeD = g.add_node('D')
    nodeE = g.add_node('E')
    nodeF = g.add_node('F')

    g.add_edge('A', 'B', weight=7)  
    g.add_edge('A', 'C', weight=9)
    g.add_edge('A', 'F', weight=14)  
    g.add_edge('B', 'C', weight=10)
    g.add_edge('B', 'D', weight=15)
    g.add_edge('C', 'D', weight=11)
    g.add_edge('C', 'F', weight=6)
    g.add_edge('D', 'E', weight=6)
    g.add_edge('E', 'F', weight=9)

    app1 = app("app1", 10, 'A', 'B')
    app2 = app("app2", 1, 'A', 'B')
    app3 = app("app3", 0.5, 'A', 'C')

    app1.set_demand(15)
    app2.set_demand(5)
    app3.set_demand(10)

    applist = [app1, app2, app3]

    util.assign_flowgroup(g, applist)
    fg_list = util.get_flowgroups()

    #print ("edge data is %s" %(g.selfloop_edges()))

    return g

class Test_fairflow(unittest.TestCase):

    graph = build_graph()

    def test_neighbourA(self):
        neighbors = self.graph.neighbors('A')
        neighbors.sort()
        self.assertEqual(neighbors, ['B', 'C', 'F'])

    def test_neighbourB(self):
        neighbors = self.graph.neighbors('B')
        neighbors.sort()
        self.assertEqual(neighbors, ['A', 'C', 'D'])

    def test_neighbourC(self):
        neighbors = self.graph.neighbors('C')
        neighbors.sort()
        self.assertEqual(neighbors, ['A', 'B', 'D', 'F'])

    def test_neighbourD(self):
        neighbors = self.graph.neighbors('D')
        neighbors.sort()
        self.assertEqual(neighbors, ['B', 'C', 'E'])

    def test_neighbourF(self):
        neighbors = self.graph.neighbors('F')
        neighbors.sort()
        self.assertEqual(neighbors, ['A', 'C', 'E'])

    def test_neighbourE(self):
        neighbors = self.graph.neighbors('E')
        neighbors.sort()
        self.assertEqual(neighbors, ['D', 'F'])

    def test_edges(self):
        edges = self.graph.edges()
        edge_set1 = set(map (lambda tup: tuple (sorted (tup)), edges))
        edge_set2 = set([('A', 'C'), ('A', 'F'), ('A', 'B'), ('C', 'F'), ('B', 'C'), ('C', 'D'), ('B', 'D'), ('D', 'E'), ('E', 'F')])
        self.assertEqual(edge_set1, edge_set2)

    def test_total_edges(self):
        self.assertEqual(self.graph.size(), 9)

    def test_has_edgeAC(self):
        self.assertTrue(self.graph.has_edge('A', 'C'))

    def test_has_edgeCF(self):
        self.assertTrue(self.graph.has_edge('C', 'F'))

    def test_has_edgeDE(self):
        self.assertTrue(self.graph.has_edge('D', 'E'))

    def test_nodeA(self):
        self.assertTrue(self.graph.has_node('A'))

    def test_nodeB(self):
        self.assertTrue(self.graph.has_node('B'))

    def test_nodeC(self):
        self.assertTrue(self.graph.has_node('C'))

    def test_nodeD(self):
        self.assertTrue(self.graph.has_node('D'))

    def test_nodeE(self):
        self.assertTrue(self.graph.has_node('E'))

    def test_nodeF(self):
        self.assertTrue(self.graph.has_node('F'))

    def test_nodeG(self):
        self.assertFalse(self.graph.has_node('G'))

    def test_total_nodes(self):
        self.assertEqual(self.graph.order(), 6)

    def test_degreeA(self):
        self.assertEqual(self.graph.degree('A'), 3)

    def test_degreeB(self):
        self.assertEqual(self.graph.degree('B'), 3)

    def test_degreeC(self):
        self.assertEqual(self.graph.degree('C'), 4)

    def test_degreeD(self):
        self.assertEqual(self.graph.degree('D'), 3)

    def test_degreeE(self):
        self.assertEqual(self.graph.degree('E'), 2)

    def test_degreeF(self):
        self.assertEqual(self.graph.degree('F'), 3)


if __name__ == '__main__':

    unittest.main()


