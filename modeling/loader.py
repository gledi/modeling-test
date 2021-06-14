from __future__ import annotations

import modeling.transformers
from modeling.node import NodeType
from modeling.transformers.base import SupportsTransformation


def load_transformer(node_type: NodeType) -> type[SupportsTransformation]:
    transformer_name = "".join(part.title() for part in node_type.value.split("_"))
    class_name = f"{transformer_name}Transformer"
    transformer_class: type[SupportsTransformation] = getattr(
        modeling.transformers,
        class_name,
    )
    return transformer_class
