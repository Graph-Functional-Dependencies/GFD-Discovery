import unittest
class test_node(unittest.TestCase):
    
    def setUp(self) -> None:
        self.node = Node(0,'people')
    
    def test_node_init(self):
        self.assertEqual(0,self.node.id)
        self.assertEqual('people',self.node.type)
        self.assertNotEqual(1,self.node.id)
        self.assertNotEqual('plane',self.node.type)

class test_edge(unittest.TestCase):
    
    def setUp(self) -> None:
        self.edge = Edge(0,from_node=Node(0,'people'),to_node=Node(1,'plane'),relation = 'have')

    def test_edge_init(self):
        self.assertEqual(0,self.edge.id)
        self.assertEqual(0,self.edge.from_node.id)
        self.assertEqual('people',self.edge.from_node.type)
        self.assertEqual(1,self.edge.to_node.id)
        self.assertEqual('plane',self.edge.to_node.type)

class test_graph(unittest.TestCase):

    def setUp(self) -> None:
        self.graph = Graph()

    def test_add_node(self):
        self.graph.add_node('monkey')   
        self.assertEqual(1,self.graph.node_number)
        self.graph.add_node('banana')
        self.assertEqual(2,self.graph.node_number)
        
    def test_add_edge(self):
        self.graph.add_node('monkey')
        self.graph.add_node('banana')
        id =self.graph.add_edge(1,2,'like')
        self.assertEqual(1,id)
        self.assertEqual(1,self.graph.edge_number)
        id_false =self.graph.add_edge(1,5,'like')
        self.assertEqual(-1,id_false)
        self.assertEqual(-1,self.graph.add_edge(1,2,'like'))


    def test_nodes(self):
        self.graph.add_node('monkey')
        self.graph.add_node('banana')        
        node_list = self.graph.nodes
        print(node_list)
        self.assertEqual(2,len(node_list))
        self.assertEqual(1,node_list[0].id)
        self.assertEqual('monkey',node_list[0].type)
        self.assertEqual(2,node_list[1].id)
        self.assertEqual('banana',node_list[1].type)

    def test_types(self):
        self.graph.add_node('monkey')
        self.graph.add_node('banana')
        self.graph.add_node('tree')
        self.graph.add_node('monkey')
        types = ['monkey','banana','tree']
        self.assertEqual(types,self.graph.types)

    def test_relations(self):
        self.graph.add_node('monkey')
        self.graph.add_node('banana')
        self.graph.add_node('tree')
        self.graph.add_edge(1,2,'like')
        self.graph.add_edge(1,3,'climb')
        self.graph.add_edge(3,2,'have')
        relations = ['like','climb','have']
        self.assertEqual(relations,self.graph.relations)

    def test_find_node(self):
        self.graph.add_node('monkey')
        self.graph.add_node('banana')
        self.graph.add_node('tree')
        self.graph.add_node('monkey')
        self.assertEqual('monkey',self.graph.find_node(4).type)
        self.assertEqual('banana',self.graph.find_node(2).type)
        self.assertEqual('monkey',self.graph.find_node(1).type)

    def test_find_edge(self):
        self.graph.add_node('monkey')
        self.graph.add_node('banana')
        self.graph.add_node('tree')
        self.graph.add_edge(1,2,'like')
        self.graph.add_edge(1,3,'climb')
        self.graph.add_edge(3,2,'have')
        self.assertEqual('like',self.graph.find_edge(1).relation)
        self.assertEqual('monkey',self.graph.find_edge(1).from_node.type)
        self.assertEqual('banana',self.graph.find_edge(1).to_node.type)
        self.assertEqual('climb',self.graph.find_edge(2).relation)
        self.assertEqual('monkey',self.graph.find_edge(2).from_node.type)
        self.assertEqual('tree',self.graph.find_edge(2).to_node.type)
    
    def test_find_edge_by_endpoints(self):
        self.graph.add_node('monkey')
        self.graph.add_node('banana')
        self.graph.add_node('tree')
        self.graph.add_edge(1,2,'like')
        self.graph.add_edge(1,3,'climb')
        self.graph.add_edge(3,2,'have')
        edges = self.graph.find_edge_by_endpoints(1,2)
        self.assertEqual(1,len(edges))
        self.assertEqual('like',edges[0].relation)
        self.assertEqual('monkey',edges[0].from_node.type)
        edges = self.graph.find_edge_by_endpoints(1,None)
        self.assertEqual(2,len(edges))
        self.assertEqual('climb',edges[1].relation)
        self.assertEqual('tree',edges[1].to_node.type)
       
    def test_find_relation(self):
        self.graph.add_node('monkey')
        self.graph.add_node('banana')
        self.graph.add_node('tree')
        self.graph.add_edge(1,2,'like')
        self.graph.add_edge(1,3,'climb')
        self.graph.add_edge(3,2,'have')
        self.assertEqual(([3],[2]),self.graph.find_relation('tree',3,'banana',2,'have'))
        self.assertNotEqual(([3],[2]),self.graph.find_relation('tree',1,'banana',2,'have'))
        self.assertEqual(([1],[2]),self.graph.find_relation('monkey',None,'banana',2,'like'))
        self.assertEqual(([],[]),self.graph.find_relation('monkey',None,'banana',None,'like'))

    def test_node_by_type(self):
        self.graph.add_node('monkey')
        self.graph.add_node('banana')
        self.graph.add_node('tree')
        self.graph.add_node('monkey')
        self.assertEqual(2,len(self.graph.find_node_by_type('monkey')))     
        self.assertEqual(1,self.graph.find_node_by_type('monkey')[0].id)
        self.assertEqual(4,self.graph.find_node_by_type('monkey')[1].id)


if __name__ =='__main__':
    unittest.main()
