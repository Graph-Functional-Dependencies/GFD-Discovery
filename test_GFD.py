import unittest
from Graph import GFD

class Test_GFD(unittest.TestCase):

    def setUp(self):
        self.gfd = GFD('person')

    def test_initial(self):
        self.assertEqual(1, len(self.gfd.nodes))
        self.assertEqual(0, len(self.gfd.edges))
        self.assertEqual('person', self.gfd.nodes[0].type)

    def test_add_relation(self):
        self.gfd, id1, id2 = self.gfd.add_relation('person', 1, 'product', None, 'create')
        
        self.assertEqual(2, len(self.gfd.nodes))
        self.assertEqual(1, len(self.gfd.edges))
        self.assertEqual('person', self.gfd.nodes[0].type)
        self.assertEqual('product', self.gfd.nodes[1].type)
        self.assertEqual('create', self.gfd.edges[0].relation)

        self.gfd = self.gfd.add_relation('person', None, 'person', 1, 'father')[0]

        self.assertEqual(3, len(self.gfd.nodes))
        self.assertEqual(2, len(self.gfd.edges))
        self.assertEqual('person', self.gfd.nodes[0].type)
        self.assertEqual('product', self.gfd.nodes[1].type)
        self.assertEqual('person', self.gfd.nodes[2].type)
        self.assertEqual('create', self.gfd.edges[0].relation)
        self.assertEqual('father', self.gfd.edges[1].relation)

        self.gfd = self.gfd.add_relation('person', 3, 'product', 2, 'create')[0]

        self.assertEqual(3, len(self.gfd.nodes))
        self.assertEqual(3, len(self.gfd.edges))
        self.assertEqual('person', self.gfd.nodes[0].type)
        self.assertEqual('product', self.gfd.nodes[1].type)
        self.assertEqual('person', self.gfd.nodes[2].type)
        self.assertEqual('create', self.gfd.edges[0].relation)
        self.assertEqual('father', self.gfd.edges[1].relation)
        self.assertEqual('create', self.gfd.edges[2].relation)

    def test_has_realtion(self):
        self.gfd = self.gfd.add_relation('person', 1, 'product', None, 'create')[0]
        self.gfd = self.gfd.add_relation('person', None, 'person', 1, 'father')[0]
        self.gfd = self.gfd.add_relation('person', 3, 'product', 2, 'create')[0]

        self.assertTrue(self.gfd.has_relation('create', 1, 2))
        self.assertTrue(self.gfd.has_relation('father', 3, 1))
        self.assertTrue(self.gfd.has_relation('create', 3, 2))
        self.assertFalse(self.gfd.has_relation('create', 2, 1))
        self.assertFalse(self.gfd.has_relation('father', 1, 2))
        self.assertFalse(self.gfd.has_relation('create', 2, 4))
        self.assertFalse(self.gfd.has_relation('create', 2, 2))

if __name__ == '__main__':
    unittest.main()