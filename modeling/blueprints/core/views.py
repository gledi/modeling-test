from flask import Blueprint, current_app, request, jsonify

from modeling.query import QueryBuilder
from modeling.db import get_db


core = Blueprint('core', __name__)


@core.get("/")
def index():
    return jsonify(message="modeling test")


@core.post("/queries")
def process_queries():
    req_data = request.get_json()

    query_builder = QueryBuilder(req_data)
    transformer = query_builder.build()
    sql_stmt = transformer.transform()
    params = transformer.get_params()

    current_app.logger.info(f"SQL Statement: %s", sql_stmt)

    db = get_db()

    rv = {}
    with db.cursor() as cur:
        cur.execute(sql_stmt, params)
        rv["items"] = cur.fetchall()

    return jsonify(rv)
