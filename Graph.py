import copy
from logging import setLoggerClass
from unittest.case import TestCase

class Node(object):
    def __init__(self, node_id:int, node_type:str):  # vert 表示添加的结点
        self.id = node_id
        self.type = node_type
        
    def __repr__(self):
        return "%s %s"%(self.id,self.type)

class Edge(object):
    def __init__(self, id:int, from_node:Node, to_node:Node, relation:str) -> None:
        self.from_node = from_node
        self.to_node = to_node
        self.relation = relation
        self.id = id

    '''
    def __repr__(self):
        return "%s %s"%(self.id,self.from_node,self.to_node,self.relation)
    '''

class Graph(object):
    def __init__(self):
        self.node_list = []  # 初始化点集
        self.node_number = 0  # 顶点个数初始化
        self.node_types = [] # 初始化类型
        self.edges = [] # 初始化边
        self.edge_number = 0



    @property
    def nodes(self) -> list:
        '''
        返回图中所有节点
        '''
        return self.node_list

    @property
    def types(self) -> list:
        '''
        返回图中所有的type
        '''
        return self.node_types

    @property
    def relations(self) -> list:
        '''
        返回图中所有的relation
        '''
        relations = []
        for edge in self.edges:
            if edge.relation not in relations:
                relations.append(edge.relation)
        return relations

    def find_node(self, id:int) -> Node:
        '''
        根据id查询节点
        '''
        return self.nodes[id - 1]

    def find_edge(self, id:int) -> Edge:
        '''
        根据id查询边
        '''
        return self.edges[id - 1]

    def find_edge_by_endpoints(self, source_id:int, target_id:int) -> list:
        '''
        根据起始点id查询边
        '''
        edges = []
        if source_id != None or target_id != None:
            for edge in self.edges:
                if (source_id == None or source_id == edge.from_node.id) and (target_id == None or target_id == edge.to_node.id):
                    edges.append(edge)
        return edges

    def add_node(self, node_type:str) -> int:
        '''
        新增一个节点
        
        参数
        ----
        node_type : str
            节点的type
        
        返回值
        ------
        id : int
            新增节点的id
        '''
        self.node_number = self.node_number + 1
        node_id = self.node_number
        node = Node(node_id, node_type)
        self.node_list.append(node)
        if node_type not in self.node_types:
            self.node_types.append(node_type)
        return node_id

    def add_edge(self, from_node_id:int, to_node_id:int, relation:str) -> int:
        '''
        新增一条边
        
        参数
        ----
        自定，但至少有relation
        
        返回值
        ------
        id : int
            新增边的id
        '''
        if from_node_id > len(self.node_list):
            return -1
        if to_node_id > len(self.node_list):
            return -1
        
        edges = self.find_edge_by_endpoints(from_node_id, to_node_id)
        for edge in edges:  
            if edge.relation == relation:
                return -1
        
        self.edge_number = self.edge_number + 1
        edge_id = self.edge_number
        from_node = self.find_node(from_node_id)
        to_node = self.find_node(to_node_id)
        edge = Edge(edge_id, from_node, to_node, relation)
        self.edges.append(edge)
        return edge_id

    def find_relation(self, source_type:str, source_id:int, target_type:str, target_id:int, relation:str) -> tuple:
        '''
        查询图中符合条件的关系
        
        参数
        ----       
        source_type : str
            源节点type
        source_id : int
            源节点id, 如果为None, 就要查询与目的节点相连的边是否有符合条件的关系
        target_type : str
            目的节点type
        target_id : int
            目的节点id, 如果为None, 就要查询与源节点相连的边是否有符合条件的关系
        relation : str
            要查询的关系
        
        返回值
        ------
        source_ids : list
            查询到的关系对应的源节点id
        target_ids : list
            查询到的关系对应的目的节点id
        '''
        source_list = []
        target_list = []

        edges = self.find_edge_by_endpoints(source_id, target_id)
        for edge in edges:
            if edge.from_node.type == source_type and edge.to_node.type == target_type and edge.relation == relation:
                source_list.append(edge.from_node.id)
                target_list.append(edge.to_node.id)
        
        return source_list, target_list

    def find_node_by_type(self, type: str) -> list:
        '''
        根据type查询节点
        
        参数
        ----
        type : str
            要查询的type
        
        返回值
        ------
        ids : list
            所有对应节点
        '''
        nodes = []
        for node in self.node_list:
            if node.type == type:
                nodes.append(node)
        return nodes

class GFD(Graph):
    def __init__(self, type:str) -> None:
        super().__init__()
        self.add_node(type)

    def add_relation(self, source_type:str, source_id:int, target_type:str, target_id:int, relation:str) -> tuple:
        '''
        添加一个关系
        
        参数
        ----
        source_type : str
            源节点的type
        source_id : int
            源节点的id
        target_type : str
            目的节点的type
        target_id : int
            目的节点的id
        relation : str
            要添加的关系类别

        返回值
        ------
        new_gfd : GFD
            添加关系后得到的新GFD
        source_id : int
            源节点id
        target_id : int
            目的节点id
        '''
        new_gfd = copy.deepcopy(self)
        if source_id is None:
            source_id = new_gfd.add_node(source_type)
        if target_id is None:
            target_id = new_gfd.add_node(target_type)
        # new_gfd = copy.deepcopy(self)
        new_gfd.add_edge(source_id, target_id, relation)
        return new_gfd, source_id, target_id

    def has_relation(self, relation:str, source_id:int, target_id:int) -> bool:
        '''
        查询指定的关系是否存在
        参数
        ----
        relation : str
            指定的关系类别
        source_id : int
            源节点id
        target_id : int
            目的节点id

        返回值
        ------
        has : bool
            true, 有这样一个关系存在
            false, 没有这样一个关系
        '''
        # 为什么都为空时返回true
        if source_id is None and target_id is None:
            return True
        if source_id is None or target_id is None:
            return False
        edges = self.find_edge_by_endpoints(source_id, target_id)
        for edge in edges:
            if edge.relation == relation:
                return True
        return False

    def newNodesAndEdges(self):
        """
        利用节点的type对节点进行重新排序，产生重排后的NodeList和EdgeList
        returns
        ------
        new_selfNodeList:重新排序后的节点列表
        new_selfEdgeList：重新排序后的边列表，第一排序依据为from_node，第二排序依据为to_node
        """
        # node 重新排序
        selfNodeList = self.nodes
        new_selfNodeList = sorted(selfNodeList, key=lambda x: x.type)
        selfNodeIDMap = {}
        # 构建映射ID map
        for index in range(len(new_selfNodeList)):
            selfNodeIDMap[new_selfNodeList[index].id] = index
        # 将edges中各条边的起始点id替换掉
        new_selfEdgeList = []
        for edge in self.edges:
            new_selfEdgeList.append(Edge(edge.id, Node(selfNodeIDMap[edge.from_node.id], edge.from_node.type),
                                          Node(selfNodeIDMap[edge.to_node.id], edge.to_node.type), edge.relation))
        new_selfEdgeList.sort(key = lambda x:(x.from_node.id, x.to_node.id))
        return new_selfNodeList, new_selfEdgeList

    def __eq__(self, o: object) -> bool:
        """
        利用前面的辅助函数newNodesAndEdges来判断连个GFD是否等价
        若两个GFD的newNodeList中每个点的type相同  AND  NewEdgeList中每条边的relation也相同，便认为等价
        returns
        ------
        True :表示2个GFD等价
        False:不等价
        """
        if isinstance(o, self.__class__):
            new_otherNodeList, new_otherEdgeList = o.newNodesAndEdges()
            new_myNodeList, new_myEdgeList = self.newNodesAndEdges()
            if (len(new_myNodeList) != len(new_otherNodeList)) or (len(new_myEdgeList) != len(new_otherEdgeList)):
                return False
            # 比较点的type
            for i in range(len(new_myNodeList)):
                if new_myNodeList[i].type != new_otherNodeList[i].type:
                    return False
            # 比较边的relation
            for i in range(len(new_myEdgeList)):
                if new_myEdgeList[i].relation != new_otherEdgeList[i].relation:
                    return False
            return True
        else:
            return False

    def __repr__(self):
        return "点的数目为 %s 边的数目为 %s 点的类型为%s 边的类型为%s"%(len(self.nodes),len(self.edges),self.types, self.relations)
