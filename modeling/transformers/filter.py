from __future__ import annotations

from typing import Any, Iterable, Iterator, TypedDict

from pydantic import BaseModel, Field

from modeling.errors import InvalidFieldName
from modeling.node import NodeType
from modeling.transformers.base import SupportsTransformation


class FilterOperation(TypedDict):
    operator: str
    value: str


class TransformObject(TypedDict):
    variable_field_name: str
    joinOperator: str
    operations: Iterable[FilterOperation]


class FilterOperationModel(BaseModel):
    operator: str = Field(...)
    value: str = Field(...)


class TransformObjectModel(BaseModel):
    field_name: str = Field(..., alias="variable_field_name")
    join_operator: str = Field(..., alias="joinOperator")
    operations: list[FilterOperationModel] = Field(..., min_items=1)


class FilterTransformer:
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

    def _is_valid_field_name(self) -> bool:
        return self.transform_object.field_name in set(self.input_.fields)

    def _gen_where_clause(self) -> str:
        field = self.transform_object.field_name
        join_op = self.transform_object.join_operator

        return f" {join_op} ".join(
            f"{field} {op} %({key})s"
            for key, op, _
            in self._gen_param_entries()
        )

    def _gen_param_entries(self) -> Iterator[tuple[str, str, Any]]:
        field = self.transform_object.field_name
        for ix, operation in enumerate(self.transform_object.operations):
            param_key = f"{self.key.lower()}_{field}_{ix}"
            yield (param_key, operation.operator, operation.value)

    def get_params(self) -> dict[str, Any]:
        params = self.input_.get_params()

        for key, _, val in self._gen_param_entries():
            params[key] = val

        return params

    def transform(self) -> str:
        if not self._is_valid_field_name():
            raise InvalidFieldName(f"{self.transform_object.field_name!r} "
                                   "is not a valid column name.")

        sql = "{input_sql} WHERE {ops}"

        return sql.format(
            input_sql=self.input_.transform(),
            ops=self._gen_where_clause(),
        )
