class Node(object):
    pass
class Edge(object):
    pass
class Graph(object):
    @property
    def nodes(self) -> list:
        '''
        返回图中所有节点
        '''
        pass
    @property
    def types(self) -> list:
        '''
        返回图中所有的type
        '''
        pass
    @property
    def relations(self) -> list:
        '''
        返回图中所有的relation
        '''
        pass
    def get_node(self, id:int) -> Node:
        '''
        根据id查询节点
        '''
        pass
    def get_edge(self, id:int)-> Edge:
        '''
        根据id查询边
        '''
    def get_edge(self, source_id:int, target_id:int) -> Edge:
        '''
        根据起始点id查询边
        '''
    def add_node(self) -> int:
        '''
        新增一个节点

        参数
        ----
        自定，但至少有type

        返回值
        ------
        id : int
            新增节点的id
        '''
        pass
    def add_edge(self) -> int:
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
        pass
    def find_relation(self, gfd:'GFD', source_type:str, source_id:int, target_type:str, target_id:int, relation:str) -> tuple:
        '''
        查询图中符合条件的关系

        参数
        ----
        gfd : GFD
            对应的GFD
        source_type : str
            源节点type
        source_id : int
            源节点id, 如果为None, 则说明要向gfd中新增一个源节点
        target_type : str
            目的节点type
        target_id : int
            目的节点id, 如果为None, 则说明要向gfd中新增一个目的节点
        relation : str
            要查询的关系

        返回值
        ------
        source_ids : list
            查询到的关系对应的源节点id
        target_ids : list
            查询到的关系对应的目的节点id
        '''
        pass
    def find_node_by_type(self, type:str) -> list:
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
        pass

class GFD(Graph):
    def __init__(self, type:str) -> None:
        super().__init__()
        # TODO 根据type初始化一个single-node GFD
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
        pass
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
        pass
    def __eq__(self, o: object) -> bool:
        # TODO 重写
        return super().__eq__(o)