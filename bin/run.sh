#!/usr/bin/env bash

set -euo pipefail

/bin/bash /app/bin/wait-for-it.sh -t 30 db:3306 -- echo "Database is up and running ..."

flask init-db

gunicorn --bind=0.0.0.0:5000 --name=modeling-test "modeling.app:create_app()"
