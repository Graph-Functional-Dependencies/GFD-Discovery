import copy
from Graph import Graph, GFD
from treelib import Tree
import pandas as pd

sigma = 5
class NodeData(object):
    
    def __init__(self, gfd:GFD, maps:list) -> None:
        self.gfd = gfd
        self.maps = maps

    def add_relation(self, graph:Graph, source_type:str, target_type:str, relation:str) -> list:
        '''
        在原有的GFD上添加一个指定的关系，返回所有可行的子节点数据

        参数
        ----
        graph : 原图
        source_type : 源节点的type
        target_type : 目的节点的type
        relation : 关系类别
        
        返回值
        ------
        new_nodes : list
            一个包含所有可行子节点数据的列表
        '''
        new_nodes = []
        source_ids_gfd = self.gfd.find_node_by_type(source_type)
        source_ids_gfd.append(None)
        target_ids_gfd = self.gfd.find_node_by_type(target_type)
        target_ids_gfd.append(None)
        for source_id_gfd in source_ids_gfd:
            for target_id_gfd in target_ids_gfd:
                if not self.gfd.has_relation(relation, source_id_gfd, target_id_gfd):
                    l = []
                    for i in range(len(self.maps)):
                        map = self.maps[i]
                        source_ids_origin, target_ids_origin = graph.find_relation(source_type, map[source_id_gfd], target_type, map[target_id_gfd], relation)
                        for source_id_origin, target_id_origin in zip(source_ids_origin, target_ids_origin):
                            l.append((source_id_origin, target_id_origin, i))
                    if len(l) >= sigma:
                        new_gfd, source_id_new_gfd, target_id_new_gfd = self.gfd.add_relation(source_type, source_id_gfd, target_type, target_id_gfd, relation)
                        new_maps = []
                        for source_id_origin, target_id_origin, index in l:
                            new_map = copy.deepcopy(self.maps[index])
                            new_map[source_id_new_gfd] = source_id_origin
                            new_map[target_id_new_gfd] = target_id_origin
                            new_maps.append(new_map)
                        new_nodes.append(NodeData(new_gfd, new_maps))
        return new_nodes

if __name__ == '__main__':
    k = 5
    G = Graph()
    nodeData = pd.read_csv('dataset/diy/node.csv')
    edgeData = pd.read_csv('dataset/diy/edge.csv')
    # 加点
    for i in range(nodeData.shape[0]):
        row = nodeData.loc[i]
        G.add_node(row['nodeType'])
    # 加边
    for i in range(edgeData.shape[0]):
        row = edgeData.loc[i]
        G.add_edge(row['sourceID'],row['targetID'],row['edgeType'])
    T = Tree()
    T.create_node(identifier='root')
    relations = G.relations
    types = G.types

    for type in types:
        nodes = G.find_node_by_type(type)
        gfd = GFD(type)
        node_id = gfd.nodes[0].id
        data = NodeData(gfd, [{node_id:node.id, None:None} for node in nodes])
        T.create_node(parent='root', data=data)
    
    for i in range (2, k * k + 2):
        nodes = [] 
        for node in T.filter_nodes(lambda x:T.depth(x)==i-1):
            nodes.append(node)
        if len(nodes) == 0:
            break
        for parent in nodes:
            parent_data = parent.data
            for relation in relations:
                for source in types:
                    for target in types:
                        children_data = parent_data.add_relation(G, source, target, relation)
                        for child_data in children_data:
                            T.create_node(parent=parent.identifier, data=child_data)
        nodes = []
        for node in T.filter_nodes(lambda x:T.depth(x)==i):
            nodes.append(node)
        for node1 in nodes:
            for node2 in nodes:
                if node1.data.gfd == node2.data.gfd:
                    T.remove_node(node2.identifier)
                    
    results = [] 
    for node in T.filter_nodes(lambda x:T.depth(x)!=1 and x.is_leaf()):
        results.append(node)