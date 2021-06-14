from __future__ import annotations

import math
from typing import Any
from operator import itemgetter
from itertools import chain

from pydantic import BaseModel, Field

from modeling.errors import InvalidQueryError
from modeling.node import NodeType
from modeling.loader import load_transformer
from modeling.transformers.base import SupportsTransformation


class NodeModel(BaseModel):
    key: str = Field(...)
    type_: NodeType = Field(..., alias="type")
    transform_object: Any = Field(..., alias="transformObject")


class QueryBuilder:
    def __init__(self, request_data: dict[str, list[Any]]) -> None:
        try:
            nodes, edges = itemgetter("nodes", "edges")(request_data)
        except KeyError:
            raise InvalidQueryError("Should contain both 'nodes' & 'edges'")

        self._edge_ordering = {
            k: i
            for i, k
            in enumerate(chain(*(itemgetter('from', 'to')(edge) for edge in edges)))
        }
        self.edges = edges
        self.nodes = [
            NodeModel(**node) for node in sorted(nodes, key=self._key_func)
        ]

    def _key_func(self, node: dict[str, Any]) -> float:
        return self._edge_ordering.get(node.get("key"), math.inf)

    def build(self) -> SupportsTransformation:
        input_: SupportsTransformation = None
        for node in self.nodes:
            Transformer = load_transformer(node.type_)
            input_ = Transformer(**node.dict(), input_=input_)
        return input_
