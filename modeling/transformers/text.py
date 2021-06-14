from __future__ import annotations

from typing import Any, Iterable, TypedDict

from pydantic import BaseModel, Field

from modeling.node import NodeType
from modeling.errors import InvalidFieldName
from modeling.transformers.base import SupportsTransformation


class TextTransformObject(TypedDict):
    column: str
    transformation: str


class TransformObjectModel(BaseModel):
    column: str = Field(...)
    transformation: str = Field(...)


class TextTransformationTransformer:
    def __init__(self,
                 key: str,
                 type_: NodeType,
                 transform_object: Iterable[TextTransformObject],
                 input_: SupportsTransformation) -> None:
        self.key = key
        self.type_ = type_
        self.transform_object = [
            TransformObjectModel(**obj) for obj in transform_object
        ]
        self.input_ = input_

    @property
    def _text_transform_fields(self) -> str:
        return ", ".join(tr.column for tr in self.transform_object)

    @property
    def fields(self) -> Iterable[str]:
        return self.input_.fields

    def _has_valid_field_names(self) -> bool:
        text_tr_fields = {tr_obj.column for tr_obj in self.transform_object}
        valid_fields = set(self.input_.fields)
        return not text_tr_fields - valid_fields

    def _gen_columns(self) -> str:
        transformations_lookup = {tr.column: tr.transformation
                                  for tr in self.transform_object}

        cols = []
        for field in self.fields:
            transformation = transformations_lookup.get(field)
            if transformation is None:
                cols.append(f"`{field}`")
                continue
            col = f'{transformation}(`{field}`) AS `{field}`'
            cols.append(col)

        return ', '.join(cols)

    def get_params(self) -> dict[str, Any]:
        return self.input_.get_params()

    def transform(self) -> str:
        if not self._has_valid_field_names():
            raise InvalidFieldName(f"One of {self._text_transform_fields!r} "
                                   "is not a valid column name.")

        sql = "SELECT {cols} {clauses}"

        original_sql = self.input_.transform()
        clauses = original_sql[original_sql.index("FROM "):]

        return sql.format(
            cols=self._gen_columns(),
            clauses=clauses,
        )
