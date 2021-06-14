from __future__ import annotations

from typing import Any, Iterable, TypedDict

from pydantic import BaseModel, Field

from modeling.transformers.base import SupportsTransformation
from modeling.node import NodeType


class TransformObject(TypedDict):
    tableName: str
    fields: Iterable[str]


class TransformObjectModel(BaseModel):
    table_name: str = Field(..., alias="tableName")
    fields: list[str] = Field(..., min_items=1)


class InputTransformer:
    def __init__(self,
                 key: str,
                 type_: NodeType,
                 transform_object: TransformObject,
                 input_: SupportsTransformation | None = None) -> None:
        self.key = key
        self.type_ = type_
        self.transform_object = TransformObjectModel(**transform_object)
        self.input_ = input_

    @property
    def fields(self) -> list[str]:
        return self.transform_object.fields

    def _gen_columns(self) -> str:
        return ", ".join(
            ["`{}`".format(field) for field in self.fields]
        )

    def _gen_table_name(self) -> str:
        return f"`{self.transform_object.table_name}`"

    def get_params(self) -> dict[str, Any]:
        return {}

    def transform(self) -> str:
        sql = "SELECT {cols} FROM {table_name}"

        return sql.format(
            cols=self._gen_columns(),
            table_name=self._gen_table_name()
        )
