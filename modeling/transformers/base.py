from __future__ import annotations

from abc import abstractmethod
from typing import Protocol, Any, Iterable

from modeling.node import NodeType


class SupportsTransformation(Protocol):
    key: str
    type_: NodeType

    @abstractmethod
    def transform(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_params(self) -> dict[str, Any]:
        raise NotImplementedError

    @property
    def fields(self) -> Iterable[str]:
        ...
