import copy
from Graph import Graph, GFD

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
                        source_ids_origin, target_ids_origin = graph.find_relation(self.gfd, source_type, map[source_id_gfd], target_type, map[target_id_gfd], relation)
                        for source_id_origin, target_id_origin in zip(source_ids_origin, target_ids_origin):
                            if source_id_origin != None and target_id_origin != None:
                                l.append((source_id_origin, target_id_origin, i))
                    if len(l) >= sigma:
                        for source_id_origin, target_id_origin, index in l:
                            new_gfd, source_id_new_gfd, target_id_new_gfd = self.gfd.add_relation(source_type, source_id_gfd, target_type, target_id_gfd, relation)
                            new_map = copy.deepcopy(self.maps[index])
                            new_map[source_id_new_gfd] = source_id_origin
                            new_map[target_id_new_gfd] = target_id_origin
                            new_nodes.append(NodeData(new_gfd, new_map))
        return new_nodes

if __name__ == '__main__':
    k = 5
    G = Graph() # 读入一个图
    T = None # 用一个根节点root初始化T
    relations = G.relations
    types = G.types

    for type in types:
        nodes = G.find_node_by_type(type)
        gfd = GFD(type)
        node_id = gfd.nodes[0].id
        data = NodeData(gfd, [{node_id:node.id, None:None} for node in nodes])
        pass # 向T中新增一个节点, 父节点为root, 子节点数据为data
    
    for i in range (1, k * k):
        nodes = [] # 获取第i - 1层的所有节点
        if len(nodes) == 0:
            break
        for parent in nodes:
            parent_data = None # 获取parent节点的数据
            for relation in relations:
                for source in types:
                    for target in types:
                        children_data = parent_data.add_relation(G, source, target, relation)
                        for child_data in children_data:
                            pass # 向T中新增一个节点, 父节点为parent, 子节点数据为child_data
        nodes = [] # 获取第i层的所有节点
        for node1 in nodes:
            for node2 in nodes:
                if node1 == node2:
                    pass # 从T中删除node2, 如果不可行, 可以先记录节点id, 遍历结束后再删除
    results = [] # 获取T的所有不在第0层的叶节点