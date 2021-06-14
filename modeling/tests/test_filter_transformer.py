from modeling.node import NodeType
from modeling.transformers.input import InputTransformer
from modeling.transformers.filter import FilterTransformer


def create_transformers():
    inp_tr = InputTransformer("A", NodeType.INPUT, {
        "tableName": "users",
        "fields": ["id", "username", "age"]
    })

    filter_tr = FilterTransformer("B", NodeType.FILTER, {
        "variable_field_name": "age",
        "joinOperator": "AND",
        "operations": [
            {"operator": ">", "value": "18"},
        ]
    }, input_=inp_tr)

    return inp_tr, filter_tr


def test_filter_transformer_shows_fields():
    _, filter_tr = create_transformers()

    assert filter_tr.fields == ["id", "username", "age"]


def test_filter_transformer_accepts_valid_columns():
    _, filter_tr = create_transformers()

    assert filter_tr._is_valid_field_name() is True


def test_filter_transformer_generates_where_clause():
    _, filter_tr = create_transformers()

    where_clause = filter_tr._gen_where_clause()

    assert where_clause == "age > %(b_age_0)s"


def test_filter_transformer_generates_param_entries():
    _, filter_tr = create_transformers()

    entry = next(filter_tr._gen_param_entries())

    assert entry == ('b_age_0', '>', '18')


def test_filter_transformer_generates_params_dict():
    _, filter_tr = create_transformers()

    params = filter_tr.get_params()

    assert params == {'b_age_0': '18'}


def test_filter_transformer_generates_sql_query():
    _, filter_tr = create_transformers()

    sql = filter_tr.transform()

    assert sql == "SELECT `id`, `username`, `age` FROM `users` WHERE age > %(b_age_0)s"
