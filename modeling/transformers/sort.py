from __future__ import annotations

from typing import Any, Iterable, Literal, TypedDict

from pydantic import BaseModel, Field

from modeling.errors import InvalidFieldName
from modeling.node import NodeType
from modeling.transformers.base import SupportsTransformation


class TransformObject(TypedDict):
    target: str
    order: Literal["ASC", "DESC"] | None


class TransformObjectModel(BaseModel):
    target: str = Field(...)
    order: Literal["ASC", "DESC"] = Field("ASC")


class SortTransformer:
    def __init__(self,
                 key: str,
                 type_: NodeType,
                 transform_object: Iterable[TransformObject],
                 input_: SupportsTransformation) -> None:
        self.key = key
        self.type_ = type_
        self.transform_object = [
            TransformObjectModel(**obj) for obj in transform_object
        ]
        self.input_ = input_

    @property
    def fields(self) -> Iterable[str]:
        return self.input_.fields

    @property
    def _sort_fields(self) -> str:
        return ', '.join(col.target for col in self.transform_object)

    def _has_valid_fieldnames(self) -> bool:
        sort_fields = {tr_obj.target for tr_obj in self.transform_object}
        valid_fields = set(self.fields)
        return not sort_fields - valid_fields

    def _gen_orderby_clause(self) -> str:
        return ", ".join(
            f"{col.target} {col.order}"
            for col in self.transform_object
        )

    def get_params(self) -> dict[str, Any]:
        return self.input_.get_params()

    def transform(self) -> str:
        if not self._has_valid_fieldnames():
            raise InvalidFieldName(f"One of {self._sort_fields!r} "
                                   "is not a valid column name.")
        sql = "{input_sql} ORDER BY {orderby_clause}"

        return sql.format(
            input_sql=self.input_.transform(),
            orderby_clause=self._gen_orderby_clause(),
        )
