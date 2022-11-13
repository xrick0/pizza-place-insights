#! /usr/bin/env sh

# Exit in case of error
set -e
set -x

alembic upgrade head
