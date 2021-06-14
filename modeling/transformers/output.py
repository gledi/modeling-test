from __future__ import annotations

from typing import Any, Iterable, TypedDict

from pydantic import BaseModel, Field, PositiveInt

from modeling.transformers.base import SupportsTransformation
from modeling.node import NodeType


class TransformObject(TypedDict):
    limit: int
    offset: int


class TransformObjectModel(BaseModel):
    limit: PositiveInt = Field(...)
    offset: int = Field(0)


class OutputTransformer:
    def __init__(self,
                 key: str,
                 type_: NodeType,
                 transform_object: TransformObject,
                 input_: SupportsTransformation) -> None:
        self.key = key
        self.type_ = type_
        self.transform_object = TransformObjectModel(**transform_object)
        self.input_ = input_

    @property
    def fields(self) -> Iterable[str]:
        return self.input_.fields

    def _gen_limit_clause(self) -> str:
        tr = self.transform_object
        return f"LIMIT {tr.offset}, {tr.limit}"

    def get_params(self) -> dict[str, Any]:
        return self.input_.get_params()

    def transform(self) -> str:
        sql = "{query} {limit_clause}"

        return sql.format(
            query=self.input_.transform(),
            limit_clause=self._gen_limit_clause(),
        )
