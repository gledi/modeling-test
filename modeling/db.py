import pymysql
import click
from flask import Flask, current_app, g
from flask.cli import with_appcontext
from faker import Faker


def get_db(with_database: bool = True) -> pymysql.Connection:
    if "db" not in g:
        config = current_app.config.get_namespace("DATABASE_")
        if not with_database:
            config.pop("database", None)

        g.db = pymysql.connect(
            **config,
            cursorclass=pymysql.cursors.DictCursor,
        )
    return g.db


def close_db(exc: Exception = None) -> None:
    db: pymysql.Connection = g.pop("db", None)
    if db is not None:
        db.close()


def init_db() -> None:
    faker = Faker()

    rows = []
    for i in range(100):
        name = faker.name()
        age = faker.random_int(min=1, max=90)
        rows.append((name, age,))
    sql_ins = "INSERT INTO users (name, age) VALUES (%s, %s)"

    db = get_db()

    with db.cursor() as cur:
        cur.execute("DROP TABLE IF EXISTS users")

        with current_app.open_resource("data/users.sql", "r") as f:
            sql_stmt = f.read()
            cur.execute(sql_stmt)

        cur.executemany(sql_ins, rows)
        db.commit()


@click.command("init-db")
@with_appcontext
def init_db_cmd() -> None:
    """Initialize DB from scratch."""
    init_db()
    click.echo("Recreated the database ...")


def init_app(app: Flask) -> None:
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_cmd)
