# Tracker Bot

## Description

Telegram Bot fot tracking your daily work activity.

It can help you understand what you spend time on during the day and generates
excel tables for the selected period.

<a href="https://github.com/Ileriayo/markdown-badges">
  <p align="center">
    <img alt="Python" src="https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54"/>
    <img alt="Docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white"/>
    <img alt="Postgres" src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white" />
    <img alt="Redis" src="https://img.shields.io/badge/redis-%23DD0031.svg?style=for-the-badge&logo=redis&logoColor=white" />
    <img alt="GitHub" src="https://img.shields.io/badge/github-%23121011.svg?style=for-the-badge&logo=github&logoColor=white"/>
    <img alt="GitHub Actions" src="https://img.shields.io/badge/githubactions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white"/>
  </p>
</a>

Main technologies:

- [python 3.11](https://www.python.org/downloads/release/python-3110/)
- [poetry](https://python-poetry.org/)
- [aiogram 3.0](https://docs.aiogram.dev/en/v3.0.0/)
- [aiogram_dialog 2.0](https://aiogram-dialog.readthedocs.io/en/2.0.0/)
- [sqlalchemy 2.0](https://docs.sqlalchemy.org/en/20/)
- [alembic](https://alembic.sqlalchemy.org/en/latest/)
- [asyncpg](https://github.com/MagicStack/asyncpg)
- [docker](https://www.docker.com/)

## Demo

...coming soon...

## Installation

For running and building app you need to get source code of this repo:

```bash
git clone https://github.com/andy-takker/organization_parser
```

or you can get public docker image from Docker hub for AMD64/ARM64 ([here](https://hub.docker.com/r/andytakker/tracker_bot)).

## Configuration

An example of the settings is in the file `.env.dev`.

```bash
cp .env.dev .env
```

```bash
TELEGRAM_BOT_TOKEN    # your telegram bot token

POSTGRES_HOST         # host of your database server
POSTGRES_PORT         # port of your database server
POSTGRES_USER         # user for connection to your database
POSTGRES_PASSWORD     # password for user for connection to your database
POSTGRES_DB           # database name 


REDIS_HOST            # host of your redis server
REDIS_PORT            # port of your redis server
REDIS_PASSWORD        # password for connection to your redis server
REDIS_DB              # redis database number
```

## Running

You can run bot in two ways: with docker or natively as is

### Docker

```bash
docker compose up -d --build
docker compose exec tracker_bot alembic -c ./src/alembic.ini upgrade head
```

### Local

For local running I recommend use [venv](https://docs.python.org/3/library/venv.html) and you need to install poetry.

```bash
python -m venv .venv
source .venv/bin/activate  # for unix systems
pip install -U pip poetry 
poetry install --no-root
set -a
source .env
set +a
alembic -c ./src/alembic.ini upgrade head # create db and all tables
python ./src/cli.py
```

### Database

Project database is PostgreSQL with async driver - `asyncpg`.

`alembic` is used to manage the database version.
To automatically create a new migration, run

```bash
alembic -c ./src/alembic.ini revision --autogenerate -m "New migration"
```

To update database to last actual version use

```bash
alembic -c ./src/alembic.ini upgrade head
```
