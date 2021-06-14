import sys
import time
import json

from modeling.query import QueryBuilder


def main(argv=None):
    if argv is None:
        argv = sys.argv[1:]

    with open("request-data.json", "r", encoding="utf-8") as f:
        req_data = json.load(f)

    start = time.perf_counter_ns()

    qb = QueryBuilder(req_data)
    transformer = qb.build()
    sql = transformer.transform()
    params = transformer.get_params()

    end = time.perf_counter_ns()

    print(sql)
    print(params)
    print(end - start)


if __name__ == "__main__":
    sys.exit(main())
