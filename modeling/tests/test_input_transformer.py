from modeling.node import NodeType
from modeling.transformers.input import InputTransformer


def create_transformer():
    inp_tr = InputTransformer("A", NodeType.INPUT, {
        "tableName": "users",
        "fields": ["id", "username", "age"]
    })
    return inp_tr


def test_input_transformer_shows_fields():
    inp_tr = create_transformer()

    assert inp_tr.fields == ["id", "username", "age"]


def test_input_transformer_generates_quoted_column_names():
    inp_tr = create_transformer()

    cols = inp_tr._gen_columns()

    assert cols == "`id`, `username`, `age`"


def test_input_transformer_quotes_table_name():
    inp_tr = create_transformer()

    table_name = inp_tr._gen_table_name()

    assert table_name == "`users`"


def test_input_tranformer_generates_sql_query():
    inp_tr = create_transformer()

    sql_stmt = inp_tr.transform()

    assert sql_stmt == "SELECT `id`, `username`, `age` FROM `users`"


def test_input_transformer_generates_empty_params():
    inp_tr = create_transformer()
    params = inp_tr.get_params()
    assert params == {}
