from enum import Enum


class NodeType(Enum):
    INPUT = "INPUT"
    FILTER = "FILTER"
    SORT = "SORT"
    TEXT_TRANSFORMATION = "TEXT_TRANSFORMATION"
    OUTPUT = "OUTPUT"


valid_node_types = frozenset(NodeType.__members__.keys())
